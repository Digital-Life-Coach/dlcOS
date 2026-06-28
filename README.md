# dlcOS — The Digital Life Coach OS

Private Claude Code plugin marketplace for [MacCog](https://maccog.com) AI Coaching clients.

This repository ships an opinionated set of Claude Code skills **and subagents** that give clients a working AI-augmented workflow on day one — file-based GTD, plan handoff between sessions, weekly review, a setup wizard that walks through onboarding, and a small fleet of agents for drafting, vault search, web research, and vault health.

## Who this is for

This marketplace is **invite-only** for active MacCog AI Coaching clients. If you're a client who's been added to this org, see `docs/client-quickstart.md` to get started.

If you're not a client and you've stumbled across this repo, that's fine — there's nothing sensitive here, but the skills are tailored to a specific coaching relationship and workflow. They won't be useful in isolation.

## What's inside

All skills are namespaced under `/dlcOS:` — type `/dlcOS:` and tab-complete to see them all grouped together.

| Skill | What it does |
|---|---|
| `/dlcOS:setup` | One-time setup wizard. Run this first. |
| `/dlcOS:save-plan` | Park an in-progress plan for a future session to critique and execute. |
| `/dlcOS:resume-plan` | Pick up a plan saved by `/dlcOS:save-plan`. Critiques first, then executes. |
| `/dlcOS:end` | End-of-session ritual. Summarizes, routes durable knowledge, surfaces Office Hours. |
| `/dlcOS:weekly-review` | Friday GTD review. Tasks, projects, someday, optional Google Calendar. |
| `/dlcOS:monthly-review` | Monthly memory maintenance. Synthesizes themes, audits memory for staleness and drift. |
| `/dlcOS:morning-brief` | Interactive setup for a per-client daily brief. |
| `/dlcOS:draft` | Draft an email, post, or proposal in your voice (spawns the `drafter` agent), then pick where it goes. |
| `/dlcOS:vault-lint` | Interactively check your vault for broken links and fix the safe ones (spawns `vault-hygiene`). |
| `/dlcOS:vault-sweep` | Unattended vault health sweep — detects and logs, fixes nothing. Good for a schedule. |
| `/dlcOS:promote-lessons` | Approve lessons your learning agents propose, so they get smarter over time. |
| `/dlcOS:setup-librarian-index` | *(add-on)* Provision a local semantic-search index so `librarian` finds by meaning, not just keywords. |

Coming later: `/dlcOS:inbox-triage` for inbox-zero workflow.

## Agents

Subagents are specialists Claude can hand a focused task to. They're auto-discovered under scoped names (`dlcOS:<name>`) and each resolves your vault path automatically. Invoke one with `@dlcOS:<name>`, ask Claude in plain language ("use webscout to research X"), or let a skill spawn it.

| Agent | What it does |
|---|---|
| `dlcOS:librarian` | Curated search over your vault — returns a synthesized answer with citations, not raw file dumps. Keyword-based out of the box; upgrades to semantic search with the `setup-librarian-index` add-on. |
| `dlcOS:drafter` | Writes prose in *your* voice (emails, posts, proposals), driven by `Wiki/Knowledge/voice.md`. Returns a draft; never sends. Usually reached via `/dlcOS:draft`. |
| `dlcOS:webscout` | Open-web research — pulls primary sources first, returns a cited brief with a confidence rating. |
| `dlcOS:vault-hygiene` | Vault health — finds broken WikiLinks and repairs the safe ones. Reached via `/dlcOS:vault-lint` (fix) or `/dlcOS:vault-sweep` (report). |

`librarian` and `drafter` **learn across sessions**: they propose small lessons at the end of a run that you approve with `/dlcOS:promote-lessons`, stored in a private `~/.claude/agents/<name>-learned.md` companion file they read on every future run.

## Install

```
/plugin marketplace add Digital-Life-Coach/dlcOS
/plugin install dlcOS@dlcOS
/reload-plugins
```

Then run `/dlcOS:setup` to scaffold your AI workspace.

## Updates

`/dlcOS:end` checks for plugin updates at session close and prints a one-line nudge if a newer version is available.

Run `/plugin update` to pull the latest.

## Support

- Docs: `docs/client-quickstart.md`, `docs/skills-reference.md`, `docs/troubleshooting.md`
- Office Hours: see your Office Hours calendar (publicly readable iCal feed configured during setup)
- Direct: text Justin at the number from your onboarding session

## License

MacCog client use only. See `LICENSE`.
