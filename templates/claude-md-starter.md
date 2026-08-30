# CLAUDE.md

*This file orchestrates Claude's behavior in your dlcOS-managed vault. The markers below are read by dlcOS skills at runtime — leave them in place even if you're not using a feature yet.*

<!-- dlcOS:vault-root --> /absolute/path/to/your/vault
<!-- dlcOS:office-hours-ical --> https://example.com/office-hours.ics  (replace with your coach's calendar URL, or delete this line to disable Office Hours nudges)
<!-- dlcOS:gcal-enabled -->  (delete this line to disable Google Calendar integration in /dlcOS:weekly-review)
<!-- dlcOS:coach-contact --> text 805-720-9276 or book at [BLAB link]  (how you actually reach your coach — set during setup; edit freely, or delete this line if you reach them some other way)

---

## Who I Am

See [`Wiki/Knowledge/about-me.md`](Wiki/Knowledge/about-me.md) — populated by `/dlcOS:setup` Stage 4a, kept current by `/dlcOS:monthly-review`.

## Pending Plans

*Used by `/dlcOS:save-plan` and `/dlcOS:resume-plan`. Each entry: one line, link to the plan file in `Reference/Plans/`. Optional dlcOS add-ons appear here as pending plans you can pick up anytime — run `/dlcOS:resume-plan <name>` to start the guided setup.*

<!-- dlcOS:addons-start -->
- `setup-email` *(v2.1 add-on)* — Let Claude read your inbox, and (on Fastmail, or Gmail with extra setup) save drafts straight into your Drafts folder. Drafts only — nothing is ever sent without you. Run `/dlcOS:setup-email` when ready.
- `dashboard-setup` *(v2.0 add-on)* — Your daily command center as a phone-installable web app, running on your own machine. Technical setup; coach-run. Run `/dlcOS:dashboard-setup` when ready.
- `setup-librarian-index` *(v2.0 add-on)* — Give the `librarian` agent a local semantic-search index so it finds things by meaning, not just keywords. Everything stays on your machine. Technical setup (needs Python + `uv`). Run `/dlcOS:setup-librarian-index` when ready.
<!-- dlcOS:addons-end -->


## Session Context

*Rolling 3 most recent daily notes, appended by `/dlcOS:end`.*

## Memory Layers

- **L1** — this conversation (handled natively by Claude)
- **L2** — `Reference/Themes/themes-rolling.md` (rolling 90-day synthesis; kept current by `/dlcOS:monthly-review`)
- **L3** — Claude Settings → Memory + [`Wiki/Knowledge/about-me.md`](Wiki/Knowledge/about-me.md)
- **L4** — `Reference/Dailies/`, `Reference/Themes/` archive, `Reference/Patterns/`

## When You Learn Something Durable About Me

*(Instruction to Claude.)* If something comes up that will still be true next week — a fact about me, how I work, a decision I've made — it belongs in my memory, not just this chat. Route it:

- **A lasting fact about who I am or how I work** → tell me to add it to **Claude Settings → Memory** (the short version I carry into every conversation), and offer to update [`Wiki/Knowledge/about-me.md`](Wiki/Knowledge/about-me.md) (the longer version) if my vault is open.
- **Something true for just one project** → put it in that project's notes, not my global memory.
- **When in doubt** → ask me where it goes. One home per fact — don't scatter the same fact across several places.

Don't write to `Reference/Themes/` yourself — `/dlcOS:monthly-review` keeps that current and audits the rest of my memory monthly.

See your coach if anything in this file looks unfamiliar. Reach them the way the `dlcOS:coach-contact` marker at the top of this file says.
