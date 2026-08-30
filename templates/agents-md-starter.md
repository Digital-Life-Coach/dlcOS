# AGENTS.md

*The tool-neutral twin of `CLAUDE.md`. Codex, Cursor, Aider, and most other coding agents read `AGENTS.md`; Claude reads `CLAUDE.md`. Same vault, same preferences, two front doors — so whichever tool you open, it knows who you are and where things live.*

*Kept in sync with `CLAUDE.md` by `/dlcOS:end` and audited monthly by `/dlcOS:monthly-review`. If you edit one by hand, edit the other — or say "sync my AGENTS.md" and Claude will do it.*

---

## Vault root

<!-- dlcOS:vault-root --> /absolute/path/to/your/vault

*(The dlcOS plugin's own runtime markers — office hours, calendar, coach contact — live in `CLAUDE.md` only; they configure Claude-specific skills that other tools don't run. Everything below applies to every tool.)*

## Who I Am

See [`Wiki/Knowledge/about-me.md`](Wiki/Knowledge/about-me.md) — the long narrative version of me: how I work, what I'm building, what I care about. Read it before doing anything substantial on my behalf.

My writing voice, if you're drafting anything in my name: [`Wiki/Knowledge/voice.md`](Wiki/Knowledge/voice.md).

## Where things live

| What | Where |
|------|-------|
| Things I've captured but not sorted | `Inbox/` |
| My tasks | `Action/TASKS.md` |
| My projects | `Action/PROJECTS.md` |
| Maybe-someday | `Action/SOMEDAY.md` |
| Finished work | `Action/COMPLETED.md` |
| Reference material, notes, people, topics | `Wiki/` |
| Saved plans (handoffs between sessions) | `Reference/Plans/` |
| Daily session notes | `Reference/Dailies/` |
| Rolling 90-day themes | `Reference/Themes/themes-rolling.md` |

*If you renamed any of these during setup, fix this table to match reality. The names don't matter; this table being true does.*

## How to work with me

<!-- Filled during /dlcOS:setup Stage 1 from my answers. Terse vs. detailed? Markdown vs. prose? Ask before acting, or act and report? Anything you should never do? -->

## Memory — when you learn something durable about me

If something comes up that will still be true next week — a fact about me, how I work, a decision I've made — it belongs in my memory, not just this chat. Route it:

- **A lasting fact about who I am or how I work** → offer to update [`Wiki/Knowledge/about-me.md`](Wiki/Knowledge/about-me.md), and tell me to also add the short version to my Claude Settings → Memory (which lives on Claude's side and is the one thing you can't write for me).
- **Something true for just one project** → put it in that project's notes, not my global memory.
- **When in doubt** → ask me where it goes. One home per fact — don't scatter the same fact across several places.

Don't write to `Reference/Themes/` yourself — that's maintained monthly by a review process.

## Ground rules

- **Never send anything on my behalf** — email, messages, posts. Draft it and show me.
- **Never delete files without asking.**
- **My health information and anything a third party told me in confidence stay in this vault** — never in cloud-stored assistant memory, never in a summary that leaves my machine.

---

*Something in this file look unfamiliar? Ask your coach — contact details are in `CLAUDE.md`.*
