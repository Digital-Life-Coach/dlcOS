---
name: vault-lint
description: Run a vault health check interactively (broken links, aging Inbox, plus an instruction-file size and rules-not-stories lint of your CLAUDE.md files) — spawn the dlcOS:vault-hygiene agent in fix mode to find broken WikiLinks (and aging Inbox items / empty sections), repair the safe ones, and report. Use when the user says /dlcOS:vault-lint, "check my vault", "find broken links", "clean up my vault", or after a big reorganization that may have left dangling links. For unattended/scheduled report-only runs use /dlcOS:vault-sweep instead.
---

# /dlcOS:vault-lint — Interactive Vault Health Check

Thin wrapper that spawns the `dlcOS:vault-hygiene` subagent in **fix mode** and surfaces its report.


> **Harness note — how to reach the agent.**
> - **Claude Code:** `Agent` tool with `subagent_type: dlcOS:vault-hygiene` (auto-discovered from the plugin).
> - **Codex:** no named-agent registry, but `spawn_agent` exists. **Check the file is actually there first** (`ls agents/vault-hygiene.md` relative to the plugin dir) — it ships today because Codex copies the whole plugin directory into its cache, not because `.codex-plugin/plugin.json` declares an `agents` key (it has none). That's an undeclared side effect, not a contract; if a future Codex version narrows to manifest-declared copying, the file silently stops shipping. If present, spawn and pass its contents as instructions. If missing, drop straight to the inline rung below rather than erroring.
> - **Neither (or the Codex file check above came up empty):** do the work inline in this session, following `agents/vault-hygiene.md` if you can find a copy of it, or its intent (FIX-mode link repair) if you can't. The agent exists to keep the main context clean, not because the work needs a separate process. Slower and noisier, never wrong.

## Steps

1. **Spawn the agent** *(where subagents exist and, on Codex, the agent file actually exists — see harness note above)*. Use the `Agent` tool with `subagent_type: dlcOS:vault-hygiene`. Tell it explicitly: *"Run in FIX mode. Resolve the vault root from the `dlcOS:vault-root` marker."* In Codex, `spawn_agent` with that file's contents as the task. Without either, run its FIX-mode instructions inline.
2. **Present the report verbatim.** The agent returns a structured markdown report (broken links found/fixed, aging Inbox items, empty sections). Show it.
3. **Walk through anything it flagged for manual review.** For ambiguous broken links (multiple candidate targets) or aging Inbox items, ask the user how to resolve each — the agent deliberately doesn't auto-fix these. Use `AskUserQuestion` (multiSelect where it's a batch) if the harness has it; otherwise a numbered list.
4. **Confirm.** Report how many links were auto-fixed and how many items still need the user's judgment.

## Instruction-file lint (CLAUDE.md size + rules-not-stories)

Run this alongside step 1 (or alone when the user says "why is my CLAUDE.md so big", "audit my CLAUDE.md"). It is deterministic, read-only and needs only Python 3:

```bash
python3 "<plugin dir>/skills/vault-lint/scripts/claude_md_lint.py" --vault "${VAULT_ROOT}" [--global-md ~/.claude/CLAUDE.md] [--memory-index <path>]
```

`VAULT_ROOT` comes from the `dlcOS:vault-root` marker, as in step 1. It ranks CLAUDE.md/AGENTS.md files by size, estimates startup load per launch folder, flags sections that read as dated incident write-ups, dead links and paths, `INFERRED` markers older than 30 days, Session Context blocks over 3 entries, and duplicate lines. Exit 2 means a check crashed: say so, never call it clean.

Present the report. For each flagged write-up section, propose a one- or two-sentence rule to keep in place and a destination file for the story. Edit only what the user approves, and migrate the text before cutting it. The story-share number runs low: use it to pick files to read, not to size a move.

## Notes

- The agent only auto-fixes *safe* repairs (unambiguous moved/deleted wikilinks). It never edits planning docs or `Inbox/` drafts.
- If the vault isn't a git repo, the agent still finds broken links but can't diagnose *why* they broke (no move/delete history) — that's expected.
- This is the interactive entry point. The scheduled, write-nothing-but-a-log version is `/dlcOS:vault-sweep`.
