# AGENTS.md

*The tool-neutral twin of `CLAUDE.md`. Codex, Cursor, Aider, and most other coding agents read `AGENTS.md`; Claude reads `CLAUDE.md`. Same vault, same preferences, two front doors — so whichever tool you open, it knows who you are and where things live.*

*Kept in sync with `CLAUDE.md` by `/dlcOS:end` and audited monthly by `/dlcOS:monthly-review`. If you edit one by hand, edit the other — or say "sync my AGENTS.md" and Claude will do it.*

---

## Vault root

<!-- dlcOS:vault-root --> /absolute/path/to/your/vault

*This marker must match the one in `CLAUDE.md` exactly. Every dlcOS skill resolves your vault from it, and it has to be in **both** files — Claude auto-loads `CLAUDE.md`, Codex auto-loads this one. A marker in one and not the other is why a skill stops before it starts.*

*Other dlcOS runtime markers (office hours, calendar, coach contact, review dates) live in `CLAUDE.md` and are mirrored here when set. Everything below applies to every tool.*

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

If something comes up that will still be true next week — a fact about me, how I work, a decision I've made — it belongs in my memory, not just this chat.

**Write it in the same turn I say it. Do not wait for the end of the session.**

There may not be an end. Threads run for days and auto-compact as they grow, so by the time any end-of-session wrap-up runs, the part of the conversation holding the fact may already have been summarized away. A sweep at the end can only save what's still in context; writing as you go saves everything. Don't wait for me to ask, and don't batch it up for later.

You always know when you're about to reply. That's the checkpoint — not some natural stopping point that may never arrive. Before you send, ask whether I stated something durable in this turn. If I did, route and write it. If you judge it not durable enough to keep, that's a fine answer — but make the judgment now rather than deferring it.

**Check before you overwrite.** Editing a fact in place is the right default — the vault should stay small. But verify two things first. *Is the existing value actually wrong?* "Today" is when someone typed, not when the thing happened; resolve relative dates with `date`/`stat` rather than from the sentence. *And is it an identifier?* Headings, filenames, folders and slugs are addresses other files resolve against; grep for inbound references before changing one, and fix them all in the same edit. A broken WikiLink renders as ordinary text — nothing fails, nothing logs.

Route it:

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
