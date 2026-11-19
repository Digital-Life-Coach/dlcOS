#!/usr/bin/env python3
"""claude_md_lint.py: deterministic size + rules-not-stories lint for a vault's instruction files.

Read-only, stdlib only. Ported from a personal vault's /claude-md-audit engine with every
vault-specific path, name and rule removed. Checks:

  size       per-file bytes, lines, sections, ranked (no hard limit; ranking, not judgment)
  load       bytes a session loads when launched in each folder (CLAUDE.md walk-up chain
             plus the optional global file)
  stories    sections that read as dated incident write-ups (2+ dated incident stamps), and
             each file's write-up share. A heuristic that points where to look.
  pointers   markdown links, wikilinks and vault-relative backtick paths that resolve to nothing
  inferred   "INFERRED YYYY-MM-DD" markers older than --inferred-days
  sessions   "Session Context" blocks holding more than --session-max dated entries
  dupes      the same long line in 2+ instruction files

Vault root: --vault, else $VAULT_ROOT, else the `<!-- dlcOS:vault-root --> /path` marker in
./CLAUDE.md or ./AGENTS.md. Exit 0 = ran, 2 = a check crashed (never a clean pass).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

EXCLUDE_DIRS = {"node_modules", ".git", ".venv", "venv", "dist", "build", ".next", "vendor",
                "__pycache__", "worktrees", ".obsidian", "archive", "Archive", "completed"}
INSTRUCTION_NAMES = ("CLAUDE.md", "AGENTS.md")
PATTERN_MARKERS = ("YYYY", "*", "<", ">", "…", "...", "{", "$", "XX", "M-DD", "[")
RUNTIME_SUFFIXES = (".flag", ".lock", ".env", ".log", ".sqlite", ".db")

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(((?:[^()\s]|\([^()\s]*\))+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
BACKTICK_RE = re.compile(r"`([^`\s][^`]*?)`")
INFERRED_RE = re.compile(r"INFERRED(?:\s+[A-Z]{2,20})?\s+(\d{4}-\d{2}-\d{2})")
MARKER_RE = re.compile(r"<!--\s*dlcOS:vault-root\s*-->\s*(\S.*)")
NON_WORD_RE = re.compile(r"\W+")
INCIDENT_RE = re.compile(
    r"\b(Burned|Found|Fixed|Hit|Confirmed|Shipped|Caught|Verified live)\b[^.\n]{0,40}?20\d\d-\d\d-\d\d"
    r"|\*\*20\d\d-\d\d-\d\d\.?\*\*|\(20\d\d-\d\d-\d\d\)", re.I)


class Ctx:
    def __init__(self, root: Path, global_md: Path | None):
        self.root, self.global_md = root, global_md

    def rel(self, p: Path) -> str:
        try:
            return str(p.relative_to(self.root))
        except ValueError:
            return str(p).replace(str(Path.home()), "~")


def resolve_root(arg: str | None, cwd: Path) -> Path:
    cand = arg or os.getenv("VAULT_ROOT")
    if not cand:
        for name in INSTRUCTION_NAMES:
            f = cwd / name
            if f.is_file():
                m = MARKER_RE.search(f.read_text(encoding="utf-8", errors="replace"))
                if m:
                    cand = m.group(1).strip().strip("`")
                    break
    if not cand:
        raise SystemExit("vault root not found: pass --vault, set VAULT_ROOT, or add the "
                         "`<!-- dlcOS:vault-root --> /path` marker to CLAUDE.md")
    root = Path(cand).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"vault root is not a directory: {root}")
    return root


def finding(fid, check, severity, evidence, path=""):
    return {"id": fid, "check": check, "severity": severity, "evidence": evidence, "path": path}


# ------------------------------------------------------------- inventory ----

def list_files(root: Path) -> list[str]:
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in EXCLUDE_DIRS and "rchived" not in d]
        for fn in fns:
            out.append(os.path.relpath(os.path.join(dp, fn), root))
    return out


def find_instruction_files(root: Path, files: list[str]) -> list[Path]:
    return sorted(root / f for f in files if Path(f).name in INSTRUCTION_NAMES)


def split_sections(text: str) -> list[tuple[str, str]]:
    secs: list[tuple[str, list[str]]] = [("(top)", [])]
    fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            secs.append((line[3:].strip(), []))
        secs[-1][1].append(line)
    return [(h, "\n".join(b)) for h, b in secs if "\n".join(b).strip()]


def profile_file(ctx: Ctx, path: Path, top: int = 3) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows, story_bytes = [], 0
    for heading, body in split_sections(text):
        n = len(body.encode())
        hits = len(INCIDENT_RE.findall(body)) + len(INCIDENT_RE.findall(heading))
        story = hits >= 2
        story_bytes += n if story else 0
        rows.append({"heading": heading, "bytes": n, "incident_stamps": hits, "story": story})
    size = len(text.encode())
    return {"path": ctx.rel(path), "bytes": size, "lines": text.count("\n") + 1, "sections": len(rows),
            "story_share": round(story_bytes / size, 2) if size else 0.0,
            "story_sections": [r["heading"] for r in rows if r["story"]],
            "top_sections": sorted(rows, key=lambda r: -r["bytes"])[:top]}


def startup_loads(ctx: Ctx, mds: list[Path]) -> list[dict]:
    sizes = {p.parent: p.stat().st_size for p in mds if p.name == "CLAUDE.md"}
    gbytes = ctx.global_md.stat().st_size if ctx.global_md and ctx.global_md.exists() else 0
    rows = []
    for folder in sizes:
        chain, total, d = [], gbytes, folder
        while True:
            if d in sizes:
                chain.append(ctx.rel(d / "CLAUDE.md"))
                total += sizes[d]
            if d == ctx.root or ctx.root not in d.parents:
                break
            d = d.parent
        rows.append({"folder": ctx.rel(folder) if folder != ctx.root else ".", "bytes": total,
                     "approx_tokens": total // 4, "chain": list(reversed(chain))})
    return sorted(rows, key=lambda r: -r["bytes"])


# -------------------------------------------------------------- pointers ----

def build_resolver(ctx: Ctx, files: list[str]):
    stems, names, fileset = defaultdict(int), set(), set(files)
    for f in files:
        p = Path(f)
        stems[p.stem] += 1
        names.add(p.name)

    def exists(target: str, source: Path) -> bool:
        t = unquote(target).split("#")[0].split("?")[0].strip().rstrip(".,;:)")
        if not t:
            return True
        if t.startswith("~/"):
            return Path(t).expanduser().exists()
        if t.startswith("/"):
            return Path(t).exists()
        for cand in (source.parent / t, ctx.root / t.removeprefix("./")):
            try:
                if cand.exists():
                    return True
            except OSError:
                pass
        if t.removeprefix("./") in fileset:
            return True
        name = Path(t).name
        return name in names or Path(t).stem in stems or (name + ".md") in names

    return exists


def top_dirs(root: Path) -> tuple[str, ...]:
    """Backtick paths count as pointers only when they start with a real top-level folder here."""
    return tuple(d.name + "/" for d in root.iterdir() if d.is_dir() and d.name not in (".git", ".obsidian"))


def check_pointers(ctx: Ctx, files: list[Path], exists) -> list[dict]:
    out, tops = [], top_dirs(ctx.root)
    for path in files:
        fence = False
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            cands = [("link", m.group(1)) for m in MD_LINK_RE.finditer(line)]
            cands += [("wikilink", m.group(1)) for m in WIKILINK_RE.finditer(line)]
            cands += [("backtick", m.group(1)) for m in BACKTICK_RE.finditer(line)
                      if m.group(1).startswith(tops) and "/" in m.group(1).rstrip("/")]
            for kind, target in cands:
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#") \
                        or (kind != "wikilink" and "." not in target and "/" not in target):
                    continue
                if target.rstrip("/").endswith(RUNTIME_SUFFIXES) or ":" in target or " → " in target:
                    continue
                if any(mk in target for mk in PATTERN_MARKERS):
                    continue
                if kind == "backtick" and re.search(r"\s(-|--)\w", target):
                    continue
                if not exists(target, path):
                    out.append(finding(f"pointer:{ctx.rel(path)}:{target}", "pointers",
                                       "low" if kind == "backtick" else "medium",
                                       f"{kind} `{target}` (line {lineno}) resolves to nothing", ctx.rel(path)))
    return out


# ------------------------------------------------------------ rule lints ----

def check_inferred(ctx: Ctx, files: list[Path], today: dt.date, max_days: int) -> list[dict]:
    out = []
    for path in files:
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for m in INFERRED_RE.finditer(line):
                try:
                    age = (today - dt.date.fromisoformat(m.group(1))).days
                except ValueError:
                    continue
                if age > max_days:
                    out.append(finding(f"inferred:{ctx.rel(path)}:{m.group(1)}:{lineno}", "inferred", "medium",
                                       f"INFERRED marker {age}d old (line {lineno}): confirm or cut: "
                                       f"{line.strip()[:140]}", ctx.rel(path)))
    return out


def check_session_context(ctx: Ctx, files: list[Path], max_entries: int) -> list[dict]:
    out = []
    for path in files:
        for heading, body in split_sections(path.read_text(encoding="utf-8", errors="replace")):
            if "session context" not in heading.lower():
                continue
            entries, started = [], False
            for l in body.splitlines():
                if re.match(r"\s*[-*] \[?20\d\d-", l):
                    entries.append(l)
                    started = True
                elif started and not l.strip().startswith(("-", "*")):
                    break
            if len(entries) > max_entries:
                out.append(finding(f"sessions:{ctx.rel(path)}", "sessions", "low",
                                   f"Session Context holds {len(entries)} entries (max {max_entries})",
                                   ctx.rel(path)))
    return out


def normalize(line: str) -> str:
    s = re.sub(r"^\s*([-*]|\d+\.)\s+", "", line)
    s = re.sub(r"[*_`⭐🚫⚠️]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def check_dupes(ctx: Ctx, files: list[Path], min_chars: int = 80) -> list[dict]:
    seen, sample = defaultdict(set), {}
    for path in files:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            n = normalize(line)
            if len(n) >= min_chars and not n.startswith(("|", "#", ">")):
                seen[n].add(ctx.rel(path))
                sample.setdefault(n, line.strip())
    out = []
    for n, where in seen.items():
        if len(where) > 1:
            key = NON_WORD_RE.sub("", n)[:60]
            out.append(finding(f"dupe:{key}", "dupes", "low",
                               f"same line in {len(where)} files: {', '.join(sorted(where))}: "
                               f"\"{sample[n][:120]}\"", sorted(where)[0]))
    return out


# ------------------------------------------------------------------ main ----

def run(root: Path, global_md: Path | None = None, memory_index: Path | None = None,
        today: dt.date | None = None, inferred_days: int = 30, session_max: int = 3) -> dict:
    today = today or dt.date.today()
    ctx = Ctx(root, global_md)
    errors, findings, profiles, loads = [], [], [], []
    files = list_files(root)
    mds = find_instruction_files(root, files)
    instr = list(mds)
    for extra in (memory_index, global_md):
        if extra and extra.is_file() and extra not in instr:
            instr.append(extra)
    try:
        profiles = sorted((profile_file(ctx, p) for p in mds), key=lambda r: -r["bytes"])
        loads = startup_loads(ctx, mds)
    except Exception as exc:
        errors.append({"check": "size/load", "evidence": f"crashed: {exc}"})
    exists = build_resolver(ctx, files)
    for name, fn in (("pointers", lambda: check_pointers(ctx, instr, exists)),
                     ("inferred", lambda: check_inferred(ctx, instr, today, inferred_days)),
                     ("sessions", lambda: check_session_context(ctx, mds, session_max)),
                     ("dupes", lambda: check_dupes(ctx, instr))):
        try:
            findings += fn()
        except Exception as exc:
            errors.append({"check": name, "evidence": f"crashed: {exc}"})
    return {"generated": dt.datetime.now().isoformat(timespec="seconds"), "root": str(root),
            "file_count": len(mds), "total_bytes": sum(p["bytes"] for p in profiles),
            "profiles": profiles, "loads": loads, "findings": findings, "scan_errors": errors}


def report(result: dict) -> str:
    L = [f"# Instruction-file lint: {result['generated'][:10]}", "",
         f"{result['file_count']} CLAUDE.md/AGENTS.md files, {result['total_bytes'] / 1000:.1f}KB total "
         f"(about {result['total_bytes'] / 4000:.1f}K tokens). Sizes are ranked, not judged against a limit.", ""]
    if result["scan_errors"]:
        L += [f"**{len(result['scan_errors'])} check(s) could not run. This is not a clean pass:**"]
        L += [f"- {e['check']}: {e['evidence']}" for e in result["scan_errors"]] + [""]
    L += ["## Startup load by launch folder (top 15)", "", "| Folder | Loaded | Tokens | Chain |", "|---|---|---|---|"]
    for r in result["loads"][:15]:
        L.append(f"| `{r['folder']}` | {r['bytes'] / 1000:.1f}KB | {r['approx_tokens'] / 1000:.1f}K | "
                 f"{' > '.join(Path(c).parent.name or '.' for c in r['chain'])} |")
    L += ["", "## Largest files (top 20)", "",
          "| File | Size | Sections | Story share | Biggest section |", "|---|---|---|---|---|"]
    for p in result["profiles"][:20]:
        big = p["top_sections"][0] if p["top_sections"] else {"heading": "", "bytes": 0}
        L.append(f"| `{p['path']}` | {p['bytes'] / 1000:.1f}KB | {p['sections']} | {int(p['story_share'] * 100)}% | "
                 f"{big['heading'][:50]} ({big['bytes'] / 1000:.1f}KB) |")
    L += ["", "*Story share = bytes in sections with 2+ dated incident stamps (Burned/Found/Fixed 20XX-...). "
          "It runs low. Use it to pick files to review, never to size a move.*", ""]
    stories = [(p["path"], h) for p in result["profiles"] for h in p["story_sections"]]
    if stories:
        L += ["## Sections that read as write-ups (keep the rule + a pointer; move the story to a history file)", ""]
        L += [f"- `{p}`: {h}" for p, h in stories] + [""]
    by = defaultdict(list)
    for f in result["findings"]:
        by[f["check"]].append(f)
    L += ["## Findings", ""]
    if not result["findings"]:
        L += ["No findings across pointers, inferred, sessions, dupes.", ""]
    for check in sorted(by):
        L.append(f"### {check}: {len(by[check])}")
        L += [f"- [{f['severity']}] `{f['path']}`: {f['evidence']}" for f in sorted(by[check], key=lambda f: f["path"])]
        L.append("")
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", help="vault root (else $VAULT_ROOT, else the dlcOS:vault-root marker)")
    ap.add_argument("--global-md", help="a global instruction file that loads on top (e.g. ~/.claude/CLAUDE.md)")
    ap.add_argument("--memory-index", help="a memory index file to include in link/INFERRED/dupe checks")
    ap.add_argument("--inferred-days", type=int, default=30)
    ap.add_argument("--session-max", type=int, default=3)
    ap.add_argument("--json", metavar="PATH", help="also write the full result as JSON")
    a = ap.parse_args(argv)
    root = resolve_root(a.vault, Path.cwd())
    g = Path(a.global_md).expanduser() if a.global_md else None
    m = Path(a.memory_index).expanduser() if a.memory_index else None
    res = run(root, g, m, inferred_days=a.inferred_days, session_max=a.session_max)
    print(report(res))
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=2))
    return 2 if res["scan_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
