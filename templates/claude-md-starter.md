# CLAUDE.md

*This file orchestrates Claude's behavior in your dlcOS-managed vault. The markers below are read by dlcOS skills at runtime — leave them in place even if you're not using a feature yet.*

<!-- dlcOS:vault-root --> /absolute/path/to/your/vault
<!-- dlcOS:office-hours-ical --> https://example.com/office-hours.ics  (replace with your coach's calendar URL, or delete this line to disable Office Hours nudges)
<!-- dlcOS:gcal-enabled -->  (delete this line to disable Google Calendar integration in /dlcOS:weekly-review)

---

## Who I Am

See [`Wiki/Knowledge/about-me.md`](Wiki/Knowledge/about-me.md) — populated by `/dlcOS:setup` Stage 4a. Refreshed quarterly.

## Pending Plans

*Used by `/dlcOS:save-plan` and `/dlcOS:resume-plan`. Each entry: one line, link to the plan file in `Reference/Plans/`.*

## Session Context

*Rolling 3 most recent daily notes, appended by `/dlcOS:end`.*

## Memory Layers

- **L1** — this conversation (handled natively by Claude)
- **L2** — `Reference/Themes/themes-rolling.md` (rolling 90-day synthesis; populated by `/dlcOS:monthly-review` in v1.1)
- **L3** — Claude Settings → Memory + [`Wiki/Knowledge/about-me.md`](Wiki/Knowledge/about-me.md)
- **L4** — `Reference/Dailies/`, `Reference/Themes/` archive, `Reference/Patterns/`

See your coach if anything in this file looks unfamiliar — text **805-720-9276** or book at the BLAB link they shared.
