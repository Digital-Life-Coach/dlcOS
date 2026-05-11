# Skills Reference

Every dlcOS skill, what it does, when to use it, what it produces. Skim once; come back when you forget which skill fits what you're trying to do.

**Two ways to invoke any skill:** type `/dlcOS:` to see them all in the slash menu, or just talk naturally — most skills auto-trigger when you say things like "save this plan" or "wrap up the session."

---

## `/dlcOS:setup`

**What it does.** Onboards you end-to-end. Builds your vault, verifies the other skills work, synthesizes your memory layers, and hands off with a checklist. Run once, with your coach.

**When to use it.** Your first session after `/plugin install dlcOS@dlcOS`. Or if you nuke your vault and need to rebuild from scratch — the wizard is idempotent.

**What it produces.** A working vault directory with `CLAUDE.md`, `Inbox/`, `Action/`, `Wiki/Knowledge/about-me.md`, and L2/L3/L4 memory folders. A Settings → Memory paste block for Claude desktop.

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

**When to use it.** Every time you stop working. Make this a habit — it's how the daily/weekly/quarterly memory layers get fed.

**What it produces.** A daily note at `Reference/Dailies/YYYY-MM-DD.md`. Optionally a git commit if your vault is a repo. A "see you next Office Hours" line if your coach has a calendar configured.

**Note.** If you have unfinished work to hand off to a future session, run `/dlcOS:save-plan` FIRST, then `/dlcOS:end`.

---

## `/dlcOS:weekly-review`

**What it does.** Guided GTD weekly review. Pre-flight data gather, inbox processing, project sweep, task sweep, someday review, weekly wrap. Optional Google Calendar pull if you've opted in.

**When to use it.** Fridays are the canonical day, but any once-a-week cadence works. Use `--quick` for a 30-minute tactical version when you're crunched.

**What it produces.** Updated `Action/PROJECTS.md`, `Action/TASKS.md`, `Action/SOMEDAY.md`. A weekly wrap note. A stronger "next 2-3 Office Hours" surfacing than `/dlcOS:end`.

---

## `/dlcOS:morning-brief`

**What it does.** Two modes.

- **First run (or `--setup`):** interactive wizard that asks what you want in your daily brief — sources, sections, delivery preference — and writes the spec to `Reference/dlcOS-morning-brief.md`.
- **Subsequent runs:** delivers a static GTD summary (P1 tasks, projects needing attention, inbox file counts, yesterday's completions) pulled live from your vault, written to `Reference/Dailies/`.

**When to use it.** First thing in the morning, ideally on a schedule. The setup wizard runs once; daily delivery is fast.

**What it produces.** First run: a brief spec file. Subsequent runs: today's brief in `Reference/Dailies/YYYY-MM-DD-brief.md`.

**Note.** The full brief engine (multi-source ingest, scheduled delivery, email/SMS) ships in Phase 2. v1 brief is GTD-only and file-only.

---

## When to use which — quick decision tree

- **Start of day** → `/dlcOS:morning-brief`
- **Mid-session, hit a fork** → `/dlcOS:save-plan`, then close out and resume in a fresh session
- **End of work session** → `/dlcOS:end`
- **Friday afternoon** → `/dlcOS:weekly-review`
- **Brand new client** → `/dlcOS:setup` (with your coach)

---

## What's NOT here in v1

These are deferred to v1.1 / Phase 2:

- `/dlcOS:inbox-triage` — inbox-zero workflow (v1.1, after the upstream skill is battle-tested)
- `/dlcOS:monthly-review` — quarterly memory refresh + themes synthesis (v1.1)
- Granola meeting ingest, email ingest, full Wiki scaffolding (Phase 2)
- Scheduled delivery (cron/launchd) for morning-brief (Phase 2)
