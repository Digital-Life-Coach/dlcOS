---
name: vault-lint
description: Run a vault health check interactively — spawn the dlcOS:vault-hygiene agent in fix mode to find broken WikiLinks (and aging Inbox items / empty sections), repair the safe ones, and report. Use when the user says /dlcOS:vault-lint, "check my vault", "find broken links", "clean up my vault", or after a big reorganization that may have left dangling links. For unattended/scheduled report-only runs use /dlcOS:vault-sweep instead.
---

# /dlcOS:vault-lint — Interactive Vault Health Check

Thin wrapper that spawns the `dlcOS:vault-hygiene` subagent in **fix mode** and surfaces its report.

## Steps

1. **Spawn the agent.** Use the `Agent` tool with `subagent_type: dlcOS:vault-hygiene`. Tell it explicitly: *"Run in FIX mode. Resolve the vault root from the `dlcOS:vault-root` marker."*
2. **Present the report verbatim.** The agent returns a structured markdown report (broken links found/fixed, aging Inbox items, empty sections). Show it.
3. **Walk through anything it flagged for manual review.** For ambiguous broken links (multiple candidate targets) or aging Inbox items, ask the user how to resolve each — the agent deliberately doesn't auto-fix these. Use `AskUserQuestion` (multiSelect where it's a batch).
4. **Confirm.** Report how many links were auto-fixed and how many items still need the user's judgment.

## Notes

- The agent only auto-fixes *safe* repairs (unambiguous moved/deleted wikilinks). It never edits planning docs or `Inbox/` drafts.
- If the vault isn't a git repo, the agent still finds broken links but can't diagnose *why* they broke (no move/delete history) — that's expected.
- This is the interactive entry point. The scheduled, write-nothing-but-a-log version is `/dlcOS:vault-sweep`.
