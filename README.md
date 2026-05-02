# dlcOS — The Digital Life Coach OS

Private Claude Code plugin marketplace for [MacCog](https://maccog.com) AI Coaching clients.

This repository ships an opinionated set of Claude Code skills that give clients a working AI-augmented workflow on day one — file-based GTD, plan handoff between sessions, weekly review, and a setup wizard that walks through onboarding.

## Who this is for

This marketplace is **invite-only** for active MacCog AI Coaching clients. If you're a client who's been added to this org, see `docs/client-quickstart.md` to get started.

If you're not a client and you've stumbled across this repo, that's fine — there's nothing sensitive here, but the skills are tailored to a specific coaching relationship and workflow. They won't be useful in isolation.

## What's inside

| Skill | What it does |
|---|---|
| `dlc-setup` | One-time setup wizard. Run this first. |
| `dlc-save-plan` | Park an in-progress plan for a future session to critique and execute. |
| `dlc-resume-plan` | Pick up a plan saved by `/dlc-save-plan`. Critiques first, then executes. |
| `dlc-end` | End-of-session ritual. Summarizes, routes durable knowledge, surfaces Office Hours. |
| `dlc-weekly-review` | Friday GTD review. Tasks, projects, someday, optional Google Calendar. |
| `dlc-morning-brief` | Interactive setup for a per-client daily brief. |

Coming in v1.1: `dlc-inbox-triage` for inbox-zero workflow.

## Install

```
/plugin marketplace add Digital-Life-Coach/dlcOS
/plugin install dlc@Digital-Life-Coach
```

Then run `/dlc-setup` to scaffold your AI workspace.

## Updates

Each skill carries its own SemVer. `/dlc-end` checks for plugin updates at session close and prints a one-line nudge if newer versions are available.

Run `/plugin update` to pull the latest.

## Support

- Docs: `docs/client-quickstart.md`, `docs/skills-reference.md`, `docs/troubleshooting.md`
- Office Hours: see your Office Hours calendar (publicly readable iCal feed configured during setup)
- Direct: text Justin at the number from your onboarding session

## License

MacCog client use only. See `LICENSE`.
