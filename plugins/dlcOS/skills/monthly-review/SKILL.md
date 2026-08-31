---
name: monthly-review
description: Monthly memory + horizon check. Synthesizes the month's daily notes into an L2 themes-rolling entry, audits L3 memory (about-me.md, Settings → Memory backup, themes hygiene, duplicate facts) and surfaces fixes as approval drafts, then asks one 90-day horizon question and one cutting-time check-in. Cut from the same cloth as /dlcOS:weekly-review — same Step 0, same pre-flight briefing, same collect-then-apply pattern, same wrap. Use when the user says /dlcOS:monthly-review, "monthly review", "memory health check", "refresh my memory", or at the start of a new month.
---

# monthly-review — Monthly Memory + Horizon Check

*Invoke as `/dlcOS:monthly-review`*

Built to feel like `/dlcOS:weekly-review` — same Step 0, same pre-flight briefing shape, same collect-then-apply pattern, same wrap. Where weekly is tactical (tasks, projects, this week), monthly is reflective (themes, memory, the next 90 days).

Three jobs:
1. **Look back (L2)** — synthesize the past month's daily notes into a new `themes-rolling.md` entry; roll the oldest entry to archive when there are more than three.
2. **Audit (L3)** — check `about-me.md`, your Settings → Memory backup, and `themes-rolling.md` for staleness, contradictions, and drift. Every fix is surfaced as a **draft for your approval** — this skill never rewrites your memory on its own.
3. **Look forward** — one 90-day horizon question and one cutting-time check-in. Verbatim answers feed the daily note; they're seed material for next month's review.

**Arguments:**
- `--audit-only` — Skip Phase 1 (themes) and Phase 3 (look forward); run only the L3 audit.

---

## Step 0 — Resolve VAULT_ROOT

Walk up from the current working directory to find the nearest **`CLAUDE.md` or `AGENTS.md`** (both carry the same dlcOS markers; a Codex-driven vault may only auto-load `AGENTS.md`, so check both and use whichever has the marker). Grep it for the line:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

That path is `${VAULT_ROOT}` for the rest of this skill. If the line is missing, stop and tell the user:

> "I can't find the dlcOS vault-root marker. Add this line to your project CLAUDE.md:
> `<!-- dlcOS:vault-root --> /absolute/path/to/your/vault`
> Then re-run /dlcOS:monthly-review."

---

## Phase 0: Pre-flight (Claude solo)

Gather everything before presenting anything. Run reads in parallel where possible.

### 0a. Locate the window

Read `${VAULT_ROOT}/Reference/Themes/themes-rolling.md`. The newest entry's month tells you where the last review left off. The window for this run is **everything since that entry** — usually the past calendar month. If the file is empty (first run), the window is every daily note that exists. Note the date range — if you're running before month-end, the entry header will say so (e.g. `May 2026 (2026-05-01 – 2026-05-22, early review)`).

### 0b. Read the month's dailies

List `${VAULT_ROOT}/Reference/Dailies/`. Read every daily note inside the window from 0a. These are the raw material for the L2 theme synthesis and the contradiction check.

### 0c. Read current L3

Read:
- `${VAULT_ROOT}/Wiki/Knowledge/about-me.md` — the long-form L3 narrative.
- `${VAULT_ROOT}/Wiki/Knowledge/settings-memory-block.md` — the saved backup of what *should* be in Claude Settings → Memory.

### 0d. Read forward-look anchors

For Phase 3, silently pull context so you can listen with grounding (don't lecture the client back with these):
- `${VAULT_ROOT}/Wiki/Knowledge/about-me.md` § Goals — the 1–2 year horizon the client wrote during onboarding.
- `${VAULT_ROOT}/Action/PROJECTS.md` — what's P1 right now.
- The two prior `themes-rolling.md` entries — recurring themes vs. one-shots.

### 0e. Stalled-from-last-month scan

Read the prior `themes-rolling.md` entry. Note any **theme or goal that appeared there but is absent from this month's dailies**. Those go into the wrap as "stalled" flags — material the client may want to let go or recommit to.

### 0f. Pre-flight briefing

Present as a structured summary, then ask to proceed:

```
=== MONTHLY REVIEW — [Month YYYY] ===

📓 DAILIES IN WINDOW: [N] notes ([date range])
📊 THEMES-ROLLING: [N] entries (newest: [Month YYYY])
🧠 ABOUT-ME: last refreshed [date from file footer]
🎯 GOALS (about-me): [N] populated / [N] empty
📁 P1 PROJECTS: [N] active
⏸️ STALLED FROM LAST MONTH: [N] flagged
```

Then: `Ready to start? Phase 1: Look Back — synthesize this month's themes.`

---

## Phase 1: Look Back — L2 themes-rolling entry

*Skip this phase if `--audit-only` was passed.*

### 1a. Synthesize the month

From the dailies in the window, write one new entry. It is a **synthesis, not a log** — themes, not a list of what happened each day.

A good entry has:
- **3–5 themes** — recurring topics, what the client kept coming back to, what they were building toward.
- **1–2 blocks** — friction patterns that showed up more than once.
- **1 highlight** — an insight, decision, or win worth carrying forward.

Draft it in **numbered** shape (numbers read cleaner than bullets in long entries):

```markdown
## [Month YYYY]

**Themes:**
1. **[Short label]** — [one or two sentences].
2. ...

**Blocks:**
1. **[Short label]** — [one or two sentences].

**Highlight:** *"[insight or decision, in the client's own words if possible]"*
```

**Partial-month / early run:** if the dailies window doesn't cover a full month (running before month-end, or covering a custom range), put the range in the header: `## May 2026 (2026-05-01 – 2026-05-22, early review)`.

### 1b. Show the draft, get approval

Present the drafted entry. Ask: *"Add this as the [Month YYYY] entry? (yes / edit)"* Apply only on confirmation.

### 1c. Prepend and roll

On approval, prepend the entry to `${VAULT_ROOT}/Reference/Themes/themes-rolling.md` (newest first). Then count the entries: if there are now **more than three**, move the oldest entry into `${VAULT_ROOT}/Reference/Themes/YYYY-MM.md` (a dated archive file for that entry's month). Never delete an entry — it always rolls to the archive.

---

## Phase 2: Audit — L3 memory drift (collect, then apply)

Same pattern as `/dlcOS:weekly-review` Phase 2: collect every finding silently across the sub-phases below, then present the full list at the end and apply only what the client approves.

Initialize an empty drafts collector.

### 2a. about-me.md vs. recent reality

Compare `about-me.md` against the month's dailies. Flag:
- **Contradictions** — `about-me.md` says something the dailies show is no longer true (e.g. "focused on launching X" when the dailies show X shipped weeks ago).
- **Staleness** — a section that hasn't kept up: a capability level that has clearly grown, goals that have been met or abandoned, tools no longer used.
- **Gaps** — something the dailies show is now central to the client's work or life that `about-me.md` never mentions.

For each, add a draft to the collector: specific old → new edit.

### 2b. Settings → Memory drift

Claude cannot read the Settings → Memory GUI directly — so this check works against the `settings-memory-block.md` backup file.

Regenerate the short Settings block from the *current* `about-me.md` (same shape as `templates/settings-memory-block.md` — under ~400 words; keep the required coach-attribution sentence verbatim, and carry the client's own contact line through unchanged — it's theirs, not boilerplate to regenerate). Diff it against the saved `settings-memory-block.md`.

If they differ, the client's actual Settings → Memory is probably stale too. Add to the collector: an updated `settings-memory-block.md` **and** a clean paste block for the client to copy into Claude desktop → Settings → Memory.

### 2c. themes-rolling hygiene

Check `themes-rolling.md`:
- More than three entries that were never rolled to an archive → draft the roll.
- An entry that reads like a day-by-day log rather than a synthesis → draft a tightened version.
- Broken internal links or references to files that no longer exist → draft the fix.

### 2d. One home per fact

Scan for the same durable fact living in two places (`about-me.md` *and* the Settings block *and* a project file). Memory should have one home per fact. Add a draft: pick the right home, remove the duplicates.

### 2e. Surface drafts for approval

Present every collected draft as a numbered list. Keep it short — if the audit found nothing, say so plainly and proceed to Phase 3.

```
=== MEMORY AUDIT — [N] drafts ===

1. about-me.md — [what's stale/wrong]
   [old] → [new]

2. Settings → Memory — out of sync with about-me.md
   → updated paste block ready below

3. themes-rolling.md — [N] un-rolled entries
   → roll [Month YYYY] to archive

Apply which? (all / numbers / none)
```

### 2f. Apply approved drafts

Apply only what the client approved:
- **about-me.md edits** — edit the file, update its `*Last refreshed:*` footer to today.
- **Settings → Memory** — overwrite `settings-memory-block.md`, then display the new paste block between `---BEGIN PASTE---` / `---END PASTE---` markers and tell the client to paste it into Claude desktop → Settings → Memory. Wait for them to confirm the paste is done.
- **themes-rolling rolls / fixes** — apply the file moves and edits.

Never apply a memory change the client did not explicitly approve.

---

## Phase 3: Look Forward — 90-day horizon + cutting-time check-in

*Skip if `--audit-only` was passed.*

Two questions, asked one at a time. Wait for each answer before asking the next. **Capture verbatim** — these feed the daily note and become seed material for next month. Don't editorialize the answers; just record.

You silently have the forward-look anchors from Phase 0d (Goals, P1 projects, recent themes) — let them inform how you listen and follow up, but do **not** read them back to the client up front.

### 3a. The 90-day horizon question

> "Look at the next 90 days. What do you most want to have moved or shipped by then? And what are you doing today that doesn't serve that?"

Wait for the answer. Capture verbatim.

If the answer names a specific outcome that has no home in `Action/PROJECTS.md` or `about-me.md` § Goals, offer to capture it — but as an *idea* in `Inbox/ideas.md`, not as a P1 task. Don't push the GTD machinery on a horizon answer.

### 3b. Cutting-time check-in

> "What do you want to cut this month to operate more cleanly? Could be a habit, a commitment, a file, a tab you keep open — anything costing energy without earning it."

Wait for the answer. Capture verbatim.

If the answer names something concrete and actionable (a habit to drop, a commitment to renegotiate, a subscription to cancel), offer to add it as a P1 task in `Action/TASKS.md`. Don't push — only add if the client wants it as a task.

---

## Phase 4: Wrap

### 4a. Daily note

Append to `${VAULT_ROOT}/Reference/Dailies/YYYY-MM-DD.md` (create if needed). Mirror the shape of `/dlcOS:weekly-review`'s wrap note — same headings rhythm, more reflective content:

```markdown
## Monthly Review — [Month YYYY][, date range if early run]

**Themes in one paragraph:** [one-paragraph prose distillation of this month's themes — what the month was actually about, in the client's voice as much as possible.]

**90-Day Horizon (verbatim):**
> [the answer to Phase 3a]

**Cutting this month (verbatim):**
> [the answer to Phase 3b]

**L3 audit:** [N] drafts surfaced, [N] applied
**Settings → Memory:** [re-pasted / no change needed / skipped]

**Stalled from last month:**
- [theme/goal from prior themes-rolling entry that's absent this month, with a one-line note — or "none" if nothing stalled]

**Skipped phases:**
- [e.g. "Phase 1 + 3 (--audit-only)" / "Phase 1 (themes-rolling already current)" / "none"]

**Open follow-ups:**
- [audit items the client wants to act on but not now; horizon items that didn't land yet]
```

### 4b. Update timestamps

If `about-me.md` was edited, confirm its `*Last refreshed:*` footer shows today's date.

### 4c. Git commit (conditional)

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$REPO_ROOT" ] && [ "$(pwd)" = "$REPO_ROOT" ]; then
  git add -A && git commit -m "monthly review: [Month YYYY] — themes entry + memory audit + horizon"
fi
```

### 4d. Write the last-run marker

Update (or add, if missing) this line in the nearest `CLAUDE.md`, near the other `dlcOS:` markers — and mirror it into `AGENTS.md` if that file exists, so both stay in sync:

```
<!-- dlcOS:monthly-review-last --> YYYY-MM-DD
```

Use today's date. `/dlcOS:end` reads this marker to nudge the client when a review is overdue — without it, every session looks overdue.

### 4e. Closing summary

Tell the client:
- Files changed and what moved (mirror the way `/dlcOS:weekly-review` reports its wrap).
- What was skipped and why.
- Anything **stalled from last month** that's gone a second month without movement — flag it as a candidate to let go or recommit to (named, not lectured).
- Suggest `/dlcOS:end` to close the session.

---

## What This Skill Does NOT Do

- **Auto-write memory** — every memory change is a draft the client approves. No silent edits.
- **Read Settings → Memory directly** — Claude can't see the GUI; the audit works from the `settings-memory-block.md` backup, and the client does the final paste.
- **Tactical GTD review** — tasks, projects, inbox processing, calendar sweep belong to `/dlcOS:weekly-review`. This is the reflective cousin, cut from the same cloth.
- **Session logging** — daily-note session detail is `/dlcOS:end`'s job; this writes a Monthly Review *block* alongside whatever else lands in today's daily.
