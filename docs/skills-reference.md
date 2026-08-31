# Skills Reference

Every dlcOS skill, what it does, when to use it, what it produces. Skim once; come back when you forget which skill fits what you're trying to do.

**Two ways to invoke any skill:** type `/dlcOS:` to see them all in the slash menu, or just talk naturally — most skills auto-trigger when you say things like "save this plan" or "wrap up the session."

---

## `/dlcOS:setup`

**What it does.** Onboards you end-to-end. Builds your vault, verifies the other skills work, synthesizes your memory layers, and hands off with a checklist. Run once, with your coach.

**When to use it.** Your first session after `/plugin install dlcOS@dlcOS`. Or if you nuke your vault and need to rebuild from scratch — the wizard is idempotent.

**What it produces.** A working vault directory with `CLAUDE.md`, `Inbox/`, `Action/`, `Wiki/Knowledge/me.md`, and L2/L3/L4 memory folders; up to three optional Wiki starter areas chosen from a curated list; and a Settings → Memory paste block for Claude desktop. If a selected data source is available, setup can build a small initial index. Recurring sync and large migrations come later.

**Time.** ~45 minutes with coach present.

---

## `/dlcOS:save-plan`

**What it does.** Captures the current plan into a self-contained file that a future session — possibly a different model — can critique and execute without seeing your current conversation.

**When to use it.** When you've thought through how to approach something but you're not ready to execute. Or when you want a fresh model to challenge your thinking before you commit.

**What it produces.** A markdown file at `Reference/Plans/YYYY-MM-DD-slug.md` with goal, current state, numbered steps, decisions, risks, success criteria. Adds a pointer line to your `CLAUDE.md` under `## Pending Plans`.

**Pairs with.** `/dlcOS:resume-plan`.

---

## `/dlcOS:resume-plan`

**What it does.** Reads a plan you saved earlier, runs a critique pass (challenges decisions, surfaces risks, spot-checks the "current state" snapshot), waits for your go-ahead, then executes step by step — updating the plan file as it goes.

**When to use it.** When you're ready to actually do the work you parked. Run in a fresh session — that's the point. The new session brings independent judgment.

**What it produces.** The work itself, plus an updated plan file (status flipped to `in-progress`, then `complete`, then archived).

**Pairs with.** `/dlcOS:save-plan`.

---

## `/dlcOS:end`

**What it does.** Wraps up the current session cleanly. Summarizes what happened, writes a daily note, optionally commits to git, prints a one-line nudge for next Office Hours, checks for plugin updates.

**When to use it.** Every time you stop working. Make this a habit — it's how the daily/weekly/monthly memory layers get fed.

**What it produces.** A daily note at `Reference/Dailies/YYYY-MM-DD.md`. Optionally a git commit if your vault is a repo. A "see you next Office Hours" line if your coach has a calendar configured.

**Note.** If you have unfinished work to hand off to a future session, run `/dlcOS:save-plan` FIRST, then `/dlcOS:end`.

---

## `/dlcOS:weekly-review`

**What it does.** Guided GTD weekly review. Pre-flight data gather, inbox processing, project sweep, task sweep, someday review, weekly wrap. Optional Google Calendar pull if you've opted in.

**When to use it.** Fridays are the canonical day, but any once-a-week cadence works. Use `--quick` for a 30-minute tactical version when you're crunched.

**What it produces.** Updated `Action/PROJECTS.md`, `Action/TASKS.md`, `Action/SOMEDAY.md`. A weekly wrap note. A stronger "next 2-3 Office Hours" surfacing than `/dlcOS:end`.

---

## `/dlcOS:monthly-review`

**What it does.** Monthly memory + horizon check — the loop that keeps your memory from going stale and surfaces what's next. Three things, in order: synthesizes the month's daily notes into a new themes entry (L2); audits your L3 memory (`me.md` vs. recent reality, Settings → Memory drift, themes hygiene, duplicate facts) and surfaces every fix as an approval draft; then asks one 90-day horizon question and one cutting-time check-in. Cut from the same cloth as `/dlcOS:weekly-review` — same shape, just monthly and reflective.

**When to use it.** Once a month — the start of a new month is the natural trigger. Running it before month-end is fine; the entry header notes the partial window. Use `--audit-only` to skip the themes write and the horizon questions, and just run the L3 audit.

**What it produces.** A new entry in `Reference/Themes/themes-rolling.md` (oldest entry rolls to a dated archive when there are more than three). Approved edits to `Wiki/Knowledge/me.md` and `settings-memory-block.md`, plus a fresh Settings → Memory paste block when yours has drifted. A Monthly Review block in today's daily note with your verbatim horizon + cutting-time answers — seed material for next month.

**Pairs with.** `/dlcOS:weekly-review` (tactical GTD) and `/dlcOS:end` (session close).

---

## `/dlcOS:morning-brief`

**What it does.** Two modes.

- **First run (or `--setup`):** interactive wizard that asks what you want in your daily brief — sources, sections, delivery preference — and writes the spec to `Reference/dlcOS-morning-brief.md`.
- **Subsequent runs:** delivers a static GTD summary (P1 tasks, projects needing attention, inbox file counts, yesterday's completions) pulled live from your vault, written to `Reference/Dailies/`.

**When to use it.** First thing in the morning, ideally on a schedule. The setup wizard runs once; daily delivery is fast.

**What it produces.** First run: a brief spec file. Subsequent runs: today's brief in `Reference/Dailies/YYYY-MM-DD-brief.md`.

**Note.** The full brief engine (multi-source ingest, scheduled delivery, email/SMS) ships in Phase 2. v1 brief is GTD-only and file-only.

---

## `/dlcOS:draft`

**What it does.** Spawns the `dlcOS:drafter` agent to write a piece of prose — email, reply, post, proposal — in your voice, then asks where it should go (save as markdown, hand it to you, or save to your email Drafts if email is set up). Never sends anything without you saying so explicitly.

**When to use it.** Any time you'd write something that goes out in your name and want it to sound like you.

**What it produces.** A draft, delivered the way you pick. Drafter reads `Wiki/Knowledge/voice.md` every run — fill that in (Stage 4c of setup, or it'll prompt you) so drafts sound like you instead of generic AI.

---

## `/dlcOS:vault-lint`

**What it does.** Runs the `dlcOS:vault-hygiene` agent interactively to find broken `[[WikiLinks]]` (and aging Inbox items), repairs the safe/unambiguous ones, and walks you through anything that needs a judgment call.

**When to use it.** After a big reorganization, or anytime links feel broken.

**What it produces.** A health report; safe link fixes applied in place.

---

## `/dlcOS:vault-sweep`

**What it does.** Same detection as `/dlcOS:vault-lint`, but **report-only** — it writes a dated log to `Reference/Dailies/` and fixes nothing. Safe to run on a schedule.

**When to use it.** As an unattended/scheduled health check. Follow up with `/dlcOS:vault-lint` when you want to apply fixes.

---

## `/dlcOS:promote-lessons`

**What it does.** When a learning agent (`librarian` or `drafter`) ends a run by proposing small lessons, this surfaces them for your approval and writes the approved ones into that agent's private companion file — so it gets sharper over time.

**When to use it.** Right after an agent run that ends with a "Proposed lessons" block.

**What it produces.** Approved lessons appended to `~/.claude/agents/<name>-learned.md`; rejected ones are dropped.

---

## `/dlcOS:setup-librarian-index` *(add-on)*

**What it does.** Provisions a local semantic-search index over your vault (installs the agent-library tool, builds the index, wires a daily refresh, writes the `dlcOS:librarian-index` marker). Upgrades `librarian` from keyword matching to ranked semantic search. Everything stays on your machine.

**When to use it.** Optional, when you want `librarian` to find things by meaning. Technical setup — needs Python + `uv`; do it with your coach if that's unfamiliar.

---

## `/dlcOS:memory-harden` *(add-on)*

**What it does.** Sets up the six canonical memory files in `Wiki/Knowledge/` — `me`, `voice`, `preferences`, `assistant`, `decisions`, `environment` — each owning exactly one subject, so the same fact stops getting written into three different places. Writes the routing hub at `Wiki/Knowledge/Memory/MEMORY.md`, moves Claude Code's hidden memory folder into the vault beside it (visible in Obsidian, editable or deletable any time), and wires `AGENTS.md` so Codex and ChatGPT follow the same rules rather than just Claude.

**When to use it.** Any time you want to see exactly what Claude has been keeping as memory outside a conversation, or stop it from scattering extra memory files you never asked for. Safe to run once, safe to re-run.

**What it produces.** Six canonical files in `Wiki/Knowledge/`, plus `Wiki/Knowledge/Memory/MEMORY.md` (the routing hub and shard index) and `Wiki/Knowledge/Memory/README.md`. Earlier versions used `Reference/Memory/` and locked it read-only; re-running migrates that layout and removes the lock.

---

## Agents (subagents)

Skills are things *you* run; agents are specialists *Claude* hands a focused task to. Invoke with `@dlcOS:<name>`, ask in plain language, or let a skill spawn one.

- **`dlcOS:librarian`** — curated vault search (synthesis + citations, not raw dumps). Keyword mode by default; semantic with the index add-on.
- **`dlcOS:drafter`** — prose in your voice. Usually via `/dlcOS:draft`.
- **`dlcOS:webscout`** — open-web research with primary sources + a cited brief.
- **`dlcOS:vault-hygiene`** — broken-link detection + safe repair. Via `/dlcOS:vault-lint` / `/dlcOS:vault-sweep`.

---

## When to use which — quick decision tree

- **Start of day** → `/dlcOS:morning-brief`
- **Need to write something in your voice** → `/dlcOS:draft`
- **Mid-session, hit a fork** → `/dlcOS:save-plan`, then close out and resume in a fresh session
- **End of work session** → `/dlcOS:end`
- **Friday afternoon** → `/dlcOS:weekly-review`
- **Links feel broken** → `/dlcOS:vault-lint`
- **Start of the month** → `/dlcOS:monthly-review`
- **Brand new client** → `/dlcOS:setup` (with your coach)

---

## What's not here yet

These are deferred to a later release / Phase 2:

- `/dlcOS:inbox-triage` — inbox-zero workflow (after the upstream skill is battle-tested)
- Recurring Granola/email/other Wiki ingests and large historical imports (Phase 2)
- Scheduled delivery (cron/launchd) for morning-brief (Phase 2)
