# CLAUDE.md

*Claude Code reads this file, not `AGENTS.md`. The shared instructions are canonical in `AGENTS.md` and imported below, so every tool — Claude, Codex, ChatGPT — behaves the same way.*

*Edit `AGENTS.md` for anything that isn't Claude- or dlcOS-specific. Only the sections below the import belong here.*

<!-- dlcOS:vault-root --> /absolute/path/to/your/vault
<!-- dlcOS:office-hours-ical --> https://example.com/office-hours.ics  (replace with your coach's calendar URL, or delete this line to disable Office Hours nudges)
<!-- dlcOS:gcal-enabled -->  (delete this line to disable Google Calendar integration in /dlcOS:weekly-review)

@AGENTS.md

---

# Claude- and dlcOS-specific

*Everything above comes from the canonical file. The rest of this page is only used by Claude Code and the `/dlcOS:` skills.*

## Pending Plans

*Used by `/dlcOS:save-plan` and `/dlcOS:resume-plan`. Each entry: one line, link to the plan file in `Reference/Plans/`. Optional dlcOS add-ons appear here as pending plans you can pick up anytime — run `/dlcOS:resume-plan <name>` to start the guided setup.*

<!-- dlcOS:addons-start -->
- `setup-email` *(v1.1 add-on)* — Connect Gmail or Fastmail for inbox triage + auto-archive of sent emails to your wiki. Drafts mode by default; review and send manually. Run `/dlcOS:setup-email` when ready.
- `setup-dashboard` *(v1.1 add-on)* — Your daily command center as a phone-installable web app (HQ dashboard PWA over Tailscale). Run `/dlcOS:setup-dashboard` when ready.
- `setup-librarian-index` *(v2.0 add-on)* — Give the `librarian` agent a local semantic-search index so it finds things by meaning, not just keywords. Everything stays on your machine. Technical setup (needs Python + `uv`). Run `/dlcOS:setup-librarian-index` when ready.
<!-- dlcOS:addons-end -->

## Session Context

*Rolling 3 most recent daily notes, appended by `/dlcOS:end`.*

## dlcOS notes

- L2 (`Reference/Themes/themes-rolling.md`) is maintained by `/dlcOS:monthly-review`. Don't write it by hand.
- Memory routing lives in `AGENTS.md` and `Wiki/Knowledge/Memory/MEMORY.md`, not here — so that Codex and every other tool get the same rules. Don't restate them in this file.

See your coach if anything here looks unfamiliar — text **805-720-9276** or book at the BLAB link they shared.
