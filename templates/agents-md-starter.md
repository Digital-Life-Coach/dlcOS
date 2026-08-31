# AGENTS.md

*Instructions for any AI assistant working in this vault — Codex, ChatGPT, Claude, or whatever comes next.*

**This file is canonical.** It is the single source of truth for how any AI behaves in this vault. Most tools read `AGENTS.md` directly. Claude Code reads `CLAUDE.md`, which imports this file, so both end up with the same instructions.

*Edit this file. Do not edit the shared sections of `CLAUDE.md` — it holds only Claude-specific extras below its import.*

---

## Who this vault belongs to

<!-- Name, location, the one-paragraph version. -->

The longer version is in [`Wiki/Knowledge/me.md`](Wiki/Knowledge/me.md). Read it before doing anything that depends on knowing them.

## How to talk to them

See [`Wiki/Knowledge/assistant.md`](Wiki/Knowledge/assistant.md). That file is the single home for tone and conduct.

**Do not restate those rules here.** A summary in this file and the real rules in `assistant.md` will drift apart, and then nobody knows which one is current. Link, don't copy.

## How work should be delivered

See [`Wiki/Knowledge/preferences.md`](Wiki/Knowledge/preferences.md) — formats, cadence, and what to decide without asking.

## Before you recommend anything

Check [`Wiki/Knowledge/decisions.md`](Wiki/Knowledge/decisions.md). If it's already settled, respect the reasoning or argue with the actual reason — don't reopen it as though it were new.

## Before you touch anything technical

Check [`Wiki/Knowledge/environment.md`](Wiki/Knowledge/environment.md) — machines, what runs where, how access flows, and gotchas that already cost someone an afternoon.

---

## Memory — required read

**[`Wiki/Knowledge/Memory/MEMORY.md`](Wiki/Knowledge/Memory/MEMORY.md) is a required read before you write anything durable.** It holds the routing rule and the table of canonical files.

Claude Code loads it automatically, because that folder is its memory directory. **If you are any other tool, you must open it yourself** — nothing will inject it for you.

The short version, so there is no excuse for getting it wrong:

1. If a canonical file in `Wiki/Knowledge/` covers the subject, write it there and add a one-line pointer to `MEMORY.md`.
2. If nothing fits, create a shard in `Wiki/Knowledge/Memory/` and index it.
3. If the fact already exists somewhere, update that copy — never write a second one.

**One home per fact.** When in doubt, ask.

## Where things live

| Folder | What's in it |
|---|---|
| `Inbox/` | Quick capture. `do-now.md` urgent, `ideas.md` maybe-someday, `thoughts.md` everything else. |
| `Action/` | Tasks and projects. |
| `Wiki/Knowledge/` | The canonical memory files, plus `Memory/` for shards. General reference. |
| `Wiki/` (other) | Domain folders. Mark any that are sensitive — see the rule below. |
| `Reference/` | `Dailies/`, `Themes/`, `Patterns/`, `Plans/`. |

## Rules that matter

**Sensitive material stays out of persistent cloud storage.**
<!-- Name the folders. Sending material the owner deliberately opens to the active AI service for processing is normally fine; durable storage in cloud chat history, saved memory, or a vendor profile is not. Say which folders should only be read when explicitly opened, never as ambient context. -->

**Say when something leaves the machine.** If a tool uploads, syncs, or sends the contents of this vault anywhere, say so *before* doing it, not after.

**One home per fact.** Don't scatter the same fact across several files. If you're unsure where something belongs, ask.

---

## How memory works here

Durable memory lives in **files the vault's owner controls**, not a vendor's stored profile.

- **L1 — this conversation.** Handled natively by whatever tool is in use. Disappears when it ends.
- **L2 — recent context.** `Reference/Themes/themes-rolling.md`, a rolling 90-day synthesis. Maintained by `/dlcOS:monthly-review` — don't write it by hand.
- **L3 — canonical memory.** The six files in `Wiki/Knowledge/`, indexed by `Wiki/Knowledge/Memory/MEMORY.md`, plus shards in `Wiki/Knowledge/Memory/` for anything that doesn't fit a canonical subject.
- **L4 — the archive.** `Reference/Dailies/`, the `Reference/Themes/` archive, `Reference/Patterns/`.

**This is the mechanism the whole vault depends on.** If durable facts stop landing in files, the vault goes stale and the design has failed.

---

*If anything in this file looks unfamiliar or wrong, ask your coach.*
