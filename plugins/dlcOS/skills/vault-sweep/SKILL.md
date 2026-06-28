---
name: vault-sweep
description: Run an unattended vault health sweep — spawn the dlcOS:vault-hygiene agent in report-only mode to detect broken WikiLinks, aging Inbox items, and empty sections, and write a dated log to Reference/Dailies/. Detects but does NOT fix. Use when the user says /dlcOS:vault-sweep, "sweep my vault", or as a scheduled/cron health check. For interactive repair use /dlcOS:vault-lint instead.
---

# /dlcOS:vault-sweep — Unattended Vault Health Sweep

Thin wrapper that spawns the `dlcOS:vault-hygiene` subagent in **report-only mode**. Detect-and-log only — no repairs, no edits to vault content. Safe to run on a schedule.

## Steps

1. **Spawn the agent.** Use the `Agent` tool with `subagent_type: dlcOS:vault-hygiene`. Tell it explicitly: *"Run in REPORT-ONLY mode. Resolve the vault root from the `dlcOS:vault-root` marker. Detect only; write the report to `Reference/Dailies/vault-lint-YYYY-MM-DD.md`; make no other file writes."*
2. **Surface the summary.** Report the headline counts (broken links, aging Inbox items, empty sections) and the path to the log it wrote.
3. **If issues were found, suggest the fix path:** *"Run `/dlcOS:vault-lint` to repair the broken links interactively."*

## Notes

- Report-only mode writes exactly one file: the dated lint log. It never repairs links or edits content.
- Good fit for a scheduled run (e.g. a weekly cron/launchd job). Pair with `/dlcOS:vault-lint` when you actually want to apply fixes.
- Same detection engine as `/dlcOS:vault-lint` — the only difference is fix vs. report-only.
