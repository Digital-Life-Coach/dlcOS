---
name: vault-deep-clean
description: >-
  Twice-a-year vault deep clean for dlcOS clients. Scans six areas (config
  permissions and secrets, CLAUDE.md/AGENTS.md drift, memory checks, generated
  output, stale files, vault-local skills), then moves dead files out of the vault
  into the client's archive folder under a link-gated rule. Three phases, scan →
  approve → apply; report-only by default. Coach-run. Use when the user or coach says
  /dlcOS:vault-deep-clean, "deep clean the vault", "run the six-month clean", or when
  /dlcOS:monthly-review flags the last audit doc as more than 180 days old.
  Run one module with --module=<name>.
---

# /dlcOS:vault-deep-clean — twice-a-year vault maintenance

Runs about twice a year. It does the work a weekly or monthly review can't: work that is slow, touches many files, or pointless to repeat monthly. **This is the highest-risk skill in the plugin**, so it is report-only by default, and nothing changes without an explicit approval per batch. The coach runs it with the client present; an L1–L2 client should not be asked to judge a permissions list.

Nothing is ever deleted. Eviction is a move plus a manifest line.

---

## Step 0 — Resolve VAULT_ROOT and ARCHIVE_ROOT

Walk up from the working directory to the nearest **`CLAUDE.md` or `AGENTS.md`** and read:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
<!-- dlcOS:archive-root --> /absolute/path/to/vault-archive
```

- **No `vault-root` marker:** stop. Tell the user to run `/dlcOS:setup`.
- **No `archive-root` marker** (vault set up before this skill shipped): run **Stage 2 § Archive folder and backup** of the setup wizard (`${MARKETPLACE_ROOT}/plans/dlc-setup.md`, resolved as `/dlcOS:setup` Step 2 describes) before going further. Report-only scans may proceed without it; an apply may not.

Read the vault's "Where things live" section in `CLAUDE.md`/`AGENTS.md` for real folder names. This skill says `Action/`, `Inbox/`, `Reference/` for the defaults; use whatever the client actually has.

> **Harness note.** Nothing here needs a named subagent. On a large vault, hand one module's scan to a subagent to keep the main context clean (Claude Code `Agent` tool / Codex `spawn_agent` with this file's module section as the task), or run it inline if neither exists. Where the text says "approval panel", use `AskUserQuestion` (multiSelect) if the harness has it, otherwise a numbered list the user answers by number.

## Vocabulary

- **`completed/`** — finished but still referenced. Stays in the vault.
- **`archive/`** — dead. Can be evicted to `${ARCHIVE_ROOT}`.
- **`baseline/`** — frozen on purpose for comparison. Never rewritten, never evicted.

If the client has folders called "archive" that are still referenced, the eviction rule below catches them. Don't rename client folders to match this vocabulary without asking.

## Phases — always in this order

1. **SCAN** — every module reports findings. The only write is the audit doc.
2. **APPROVE** — findings that would change files go to the user as approval panels (≤4 questions × 4 options per round, chained). No approval, no apply.
3. **APPLY** — do only what was approved, module by module, and update the audit doc as you go.

Default is **report-only** (scan only). `--apply` enables phases 2–3. `--module=<name>` scopes any run to one module.

## Preconditions (check before ANY apply)

- **A restore point exists.**
  - Vault is a git repo → working tree committed, or make a `deep-clean-checkpoint` commit first.
  - No git → the backup recorded by setup (`<!-- dlcOS:backup -->` marker) must have run within the last 24 hours. Check it (macOS Time Machine: `tmutil latestbackup`; otherwise ask the user to confirm the date). If you can't confirm it, **apply only moves** (reversible from the manifest). No content edits.
- `${ARCHIVE_ROOT}` exists, is writable, and is **not inside `${VAULT_ROOT}`**.
- **The archive is not indexed.** If the vault has the `<!-- dlcOS:librarian-index -->` marker, read `~/.librarian/sources.json` and confirm no registered source path contains `${ARCHIVE_ROOT}`. The librarian index has no working exclusion: the `exclude` key in `sources.json` is ignored on rebuild, and dot-folders are not skipped. The only thing that keeps a folder out of the index is sitting outside every registered path. A client who registered `~/Documents` instead of the vault would index the archive. If so, stop and tell the coach.
- Hard cap: no module touches more than 200 files in one apply without a fresh approval round.

## The eviction rule (three tiers, link-gated)

For each candidate, find inbound references: wikilinks, markdown relative links, and plain mentions of the path.

| Inbound from | Action |
|---|---|
| Nothing | Evict |
| Ordinary notes, dailies, Wiki pages | Evict, and rewrite those links to the `ARCHIVED:` marker |
| **Live authority**: `CLAUDE.md`, `AGENTS.md`, any `SKILL.md` in the vault, the client's projects and tasks files (`Action/PROJECTS.md`, `Action/TASKS.md` by default) | **Do not evict.** Report as "archived in name only" |
| **Historical record**: the completed-tasks file (`Action/COMPLETED.md` by default) | Not evidence the file is alive, and **never rewritten**. It records where a file was at the time |

A link from live authority means the file is not dead. That is a finding, not a link to fix.

**How to evict:** move (never copy, never delete) to `${ARCHIVE_ROOT}/<same relative path>`. Append one row to `${VAULT_ROOT}/Reference/Archive Manifest.md` (create it on first eviction): original path, date, reason, inbound-link count. Rewrite remaining tier-2 links to the plain text `ARCHIVED: <original/relative/path.md>`. The marker is deliberately not a link: Obsidian shows nothing broken, and the `dlcOS:vault-hygiene` agent knows to skip it. The manifest stays in the vault so a search still finds that the file exists.

**Never evict:** anything under a `baseline/` folder; `Reference/Dailies/YYYY-MM-DD.md` session notes (they stay in the vault for good, and `/dlcOS:monthly-review` reads them); `Wiki/Knowledge/about-me.md` and `settings-memory-block.md`; anything you cannot positively identify.

**Lock the archive.** Keep archive files read-only (files only; folders stay writable). Wrap every archive write so a failed run can't leave it unlocked:

```bash
archive_write() {  # usage: archive_write <cmd...>
  trap 'find "$ARCHIVE_ROOT" -type f -exec chmod a-w {} +' EXIT
  find "$ARCHIVE_ROOT" -type f -exec chmod u+w {} +
  "$@"
}
```

On Windows or a synced folder where `chmod` has no effect, skip the lock and say so in the audit doc.

## Modules (six)

### `config`
`${VAULT_ROOT}/.claude/settings.json`, `settings.local.json` files anywhere in the vault, and `~/.claude/settings.json`. (Codex: `~/.codex/config.toml`.) Sort every permission entry into *safe-universal / scoped / dead / dangerous*; propose cutting only the last two. **Never propose removing basic read-only grants** (bare `Read`, `Grep`, `Glob`, `ls`). Cutting those makes every session ask for approval more often, and it happened on the first real run of this skill's parent. Scan for plaintext secrets (`Authorization: Bearer`, `Api-Key`, `X-Api-Key`, `sk-`, `ghp_`, `xox`). **Show secret findings and the rotation checklist in the session only. Never write them to any file, including the audit doc** (the audit doc records "N secrets found, checklist given in session"). Removing a key from a file does not make it dead; the checklist says what to rotate.

### `orchestration`
`CLAUDE.md` and `AGENTS.md`, root and any nested copies. Find: instructions for projects that no longer exist, pointers that no longer resolve, "Where things live" paths that don't match the real folders, and **drift between the two files**. Every `dlcOS:` marker in one must be in the other with the same value, because a marker in only one file is the usual reason a skill stops at Step 0 on a working vault. Propose fixes per file; **never auto-edit**.

### `memory`
Checking, not synthesis (`/dlcOS:monthly-review` does synthesis). Does every file, folder, and path named in `about-me.md`, `settings-memory-block.md`, and `Reference/Themes/themes-rolling.md` still exist? Do two memory files state the same fact differently? **Never name a memory file in a deletion or merge prompt without reading its full text first in this session.** Write the new content before removing anything old.

### `generated`
Move machine-written output older than 90 days to the archive. In a default dlcOS vault that means `Reference/Dailies/vault-lint-YYYY-MM-DD.md` sweep logs, plus any log the coach has added. Identify files by filename pattern; **refuse to archive anything that doesn't match a known generated pattern. When in doubt, keep.** Dated session notes (`Reference/Dailies/YYYY-MM-DD.md`) are never generated output, even if a skill wrote part of them. **The first run of this module on a vault is report-only, regardless of `--apply`.**

### `stale`
Superseded versions (`*-v2`, `*-old`, `*-backup`, `* copy`, `*.bak*`, sync conflict copies, dated snapshots next to a live file), temp files never moved, stray `.DS_Store`, and orphans with zero inbound links and no change in 6+ months. Route everything through the eviction rule; never delete. Show candidates as approval panels. `.DS_Store` files may be deleted as a batch after one approval; they are OS debris, not content.

### `skills`
Only vault-local skills (`${VAULT_ROOT}/.claude/skills/`, `${VAULT_ROOT}/.agents/skills/`), not the dlcOS plugin's own. Mechanical checks: paths that no longer exist, near-duplicate skills. If the vault has none, report "no vault-local skills" and move on.

## Audit doc (every run, including report-only)

Write `${VAULT_ROOT}/Reference/Deep Clean - YYYY-MM-DD.md` with per-module findings; what was approved, applied, and declined; and a **diff against the previous audit doc**. "We flagged this last time and it came back" is the signal this schedule exists to produce.

## Trigger

By staleness, not a schedule. `/dlcOS:monthly-review` nudges when the newest `Reference/Deep Clean - *.md` is more than 180 days old, or when none exists and the vault is more than 180 days old. Don't add a cron or launchd job.

## What this skill does NOT do

- Delete content. Moves and manifest rows only (the one exception is `.DS_Store`, after approval).
- Edit `CLAUDE.md`, `AGENTS.md`, or memory files without a per-file yes.
- Write new tasks into the client's tasks file. Anything that needs doing goes in the audit doc's follow-ups and is raised with the user.
- Check scheduled jobs or automation health. Client vaults don't have the coach's automation stack; that module stays coach-side.
- Change backup configuration. Setup owns that; this skill only checks the restore point exists.
