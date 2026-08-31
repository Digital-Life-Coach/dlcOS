---
name: weekly-review
description: Guided GTD weekly review — pre-flight data gathering, inbox processing, task/project/someday sweep with collect-and-apply decisions, optional Google Calendar integration, and weekly wrap. Use when the user says /dlcOS:weekly-review, "weekly review", "do my GTD review", or "it's Friday let's review". Use --quick for a 30-min tactical-only version. Pairs with /dlcOS:end (session close) and /dlcOS:morning-brief (daily brief setup).
---

# weekly-review — GTD Weekly Review

*Invoke as `/dlcOS:weekly-review`*

Interactive weekly review. Claude gathers all data, then walks the user through Get Clear → Get Current → Get Creative → Wrap. All decisions are collected and applied in a single batch at the end of Phase 2.

Target: Friday, flexible to Saturday.

**Arguments:**
- `--quick` — Skip Phase 3 (Get Creative). ~30 min tactical-only review.
- `--phase N` — Resume from a specific phase (1–4) if a prior review was interrupted.

---

## Step 0 — Resolve VAULT_ROOT

Walk up from the current working directory to find the nearest **`CLAUDE.md` or `AGENTS.md`** (both carry the same dlcOS markers; a Codex-driven vault may only auto-load `AGENTS.md`, so check both and use whichever has the marker). Grep it for the line:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

That path is `${VAULT_ROOT}` for the rest of this skill. If the line is missing, stop and tell the user:

> "I can't find the dlcOS vault-root marker. Add this line to your project CLAUDE.md:
> `<!-- dlcOS:vault-root --> /absolute/path/to/your/vault`
> Then re-run /dlcOS:weekly-review."

Also check for the optional Google Calendar flag:
```
<!-- dlcOS:gcal-enabled -->
```
If present, run the GCal steps (0c, 0d, 2d) marked **[GCal]** below. If absent, skip those steps silently. To enable: add `<!-- dlcOS:gcal-enabled -->` to your CLAUDE.md and ensure the Google Calendar MCP is active.

---

## Phase 0: Pre-flight (Claude solo)

Gather all data before presenting anything. Run in parallel where possible.

### 0a. Inbox scan

```bash
ls "${VAULT_ROOT}/Inbox/"
```

Read each file found. Categorize: task / project idea / reference / wiki-worthy / junk.

### 0b. Completion sweep

Read `${VAULT_ROOT}/Action/TASKS.md`. Find all lines matching `- [x]`. These need archiving to `Action/COMPLETED.md`.

### 0c. [GCal] Calendar pull — past 7 days

*Only run if `<!-- dlcOS:gcal-enabled -->` is present.*

Use Google Calendar MCP (`gcal_list_events`) for the past 7 days across all calendars.

Group events by category or contact. For each group, compute event count and total duration. Note anything that looks like a commitment or follow-up.

### 0d. [GCal] Calendar pull — next 14 days

*Only run if `<!-- dlcOS:gcal-enabled -->` is present.*

Use Google Calendar MCP (`gcal_list_events`) for the next 14 days. Flag events that need prep, have conflicts, or are new since last review.

### 0f. Stale task scan

Parse `${VAULT_ROOT}/Action/TASKS.md`. Flag any unchecked item that has been in the file 14+ days without being touched. Use git blame or the "Last updated" timestamp as a proxy.

### 0g. Project health check

Parse `${VAULT_ROOT}/Action/PROJECTS.md`. Flag:
- Projects with no next action
- Projects where the next action is already checked off (stale)
- Projects with no activity in COMPLETED.md for 14+ days

### 0h. SOMEDAY flags

Parse `${VAULT_ROOT}/Action/SOMEDAY.md`. Flag items that are:
- 60+ days old (estimate from "Last refreshed" date vs. item position)
- Newly relevant based on recent activity

### 0j. Week's completions

Read `${VAULT_ROOT}/Action/COMPLETED.md`. Extract entries from the past 7 days. This feeds Phase 3 ("What got done this week").

---

### Pre-flight Output: Review Briefing

Present as a structured summary:

```
=== WEEKLY REVIEW BRIEFING ===
📅 Week of [date range]

📥 INBOX: [N] items waiting
✅ COMPLETED THIS WEEK: [N] tasks archived
📋 TASKS: [N] open ([N] stale 14+ days)
📁 PROJECTS: [N] active ([N] need attention)
💡 SOMEDAY: [N] flagged for review
📆 CALENDAR: [N] events past week, [N] upcoming   ← only if GCal enabled
```

Then: `Ready to start? Phase 1: Get Clear`

---

## Phase 1: Get Clear (~10 min)

### 1a. Physical sweep prompt

> "Go sweep your desk and physical space. Anything to capture? Drop it in Inbox/ or tell me here. I'll wait."

Wait for response. If items are dropped into Inbox/, re-scan.

### 1b. Process Inbox/

For each file in `${VAULT_ROOT}/Inbox/`:
1. Read the file
2. Propose a destination:
   - **TASKS** — actionable next step → propose priority level and project tag
   - **PROJECTS** — multi-step outcome → create project entry + next action
   - **SOMEDAY** — idea, not committed → propose category
   - **Wiki** — reference/knowledge → propose wiki page name
   - **Delete** — noise
3. User confirms or redirects
4. Execute the move (hold file deletions until batch apply at 2i)

### 1c. Uncaptured items scan

Read the 3 most recent files in `${VAULT_ROOT}/Reference/Dailies/`. Look for open loops, action items, or ideas not already in TASKS.md or PROJECTS.md. Present findings — user decides: capture or ignore.

---

## Phase 2: Get Current (~25 min)

**All decisions are COLLECTED, not applied. Everything applies in one batch at step 2i.**

Initialize a decisions collector.

### 2a. Task sweep

Walk through `${VAULT_ROOT}/Action/TASKS.md` section by section: P1 → P2 → P3.

Skip checked items (handled in pre-flight).

For each unchecked task, present:

```
📋 [Task description]
   Priority: P[N] | Project: [name]
   Age: [N] days

   1. Keep at P[N]
   2. Promote to P[N-1]
   3. Demote to P[N+1]
   4. Kill (remove entirely)
   5. Reword → [ask for new wording]
   6. Move to SOMEDAY
```

Collect decision. Move to next item.

### 2b. Project review

Walk through `${VAULT_ROOT}/Action/PROJECTS.md` one project at a time:

```
📁 [Project Name]
   Status: [status] | Priority: P[N]
   Next action: [current next action text]
   Last completion: [date and task from COMPLETED.md, or "none"]
   Days since activity: [N]

   1. Keep as-is
   2. Change priority → [ask new priority]
   3. New next action → [ask for new action text]
   4. Mark project complete
   5. Kill project
   6. Move to SOMEDAY
```

Collect decision. Move to next project.

### 2d. [GCal] Calendar review — next 2 weeks

*Only run if `<!-- dlcOS:gcal-enabled -->` is present.*

Present upcoming events as a timeline:

```
📆 NEXT 2 WEEKS:

[Day, Date]:
  [time] — [event title] ([duration])

[Day, Date]:
  [time] — [event title] ([duration])
```

Ask:
- Any prep needed before specific events?
- Any conflicts to resolve?

Capture prep tasks → add to decisions collector.

### 2f. SOMEDAY flagged items

Present only items flagged in pre-flight (aged 60+ days or newly relevant):

```
💡 [Idea title]
   Category: [section in SOMEDAY.md] | Age: ~[N] days
   Why flagged: [aged out / connects to active project X]

   1. Promote to project
   2. Kill
   3. Leave for now
```

Collect decisions.

### 2i. Decision summary & apply

Present the FULL list of collected decisions:

```
=== DECISION SUMMARY ===

TASKS ([N] decisions):
  ✅ Keep P1: [task]
  ⬆️ Promote to P1: [task]
  ⬇️ Demote to P3: [task]
  ❌ Kill: [task]
  ✏️ Reword: [old] → [new]
  📦 → SOMEDAY: [task]

PROJECTS ([N] decisions):
  ✅ Keep: [project] (P[N])
  📝 New next action: [project] → "[new action]"
  🏁 Complete: [project]
  ❌ Kill: [project]

SOMEDAY ([N] flagged):
  ⬆️ Promote: [idea]
  ❌ Kill: [idea]

UPCOMING PREP ([N] items):      ← only if GCal enabled
  📋 [new task for upcoming event]

Apply all? (yes / edit by number)
```

Wait for confirmation. If "edit #N", adjust and re-present.

Once confirmed, apply ALL changes in one batch:
1. Archive checked items to `${VAULT_ROOT}/Action/COMPLETED.md`
2. Update `${VAULT_ROOT}/Action/TASKS.md`
3. Update `${VAULT_ROOT}/Action/PROJECTS.md`
4. Update `${VAULT_ROOT}/Action/SOMEDAY.md`
5. Delete processed Inbox/ files

---

## Phase 3: Get Creative (~10 min)

**Skip if `--quick` flag was used.**

### 3a. Horizons check

Pick the most relevant horizon based on what came up in Phase 2. Rotate — don't do all horizons every week.

**H2 — Areas of Focus:**
Ask: "Any area of your life or work getting neglected? Think across your main domains: work/business, key relationships, health, finances, creative pursuits."

**H3 — Goals (1–2 year):**
Ask: "Any goal that needs a new project or a next action that doesn't exist yet?"

**H4 — Vision:**
Ask: "Still on the right track? Career, lifestyle — anything shifting?"

### 3b. Next week's top 3

Ask the user to pick their top 3 priorities for the coming week. Add a `⭐ THIS WEEK` marker to those items in TASKS.md.

### 3c. Idea spark

Based on what came up during the review, surface 1–2 connections:
- A SOMEDAY idea that connects to something discussed in Phase 2
- A pattern in the week's completions that suggests a new direction
- A relationship or commitment that could use more attention

---

## Phase 4: Wrap (~10 min)

### 4a. Office Hours nudge

Check for `<!-- dlcOS:office-hours-ical --> <URL>` in the nearest CLAUDE.md. If present, fetch the iCal feed and surface the next 2–3 upcoming Office Hours sessions:

```
📅 Upcoming Office Hours:
  [Day, Date] at [time]
  [Day, Date] at [time]
```

Skip silently if the config line is absent or the fetch fails.

### 4b. Write daily note

Append weekly review summary to `${VAULT_ROOT}/Reference/Dailies/YYYY-MM-DD.md`:

```markdown
## Weekly Review — [date]

**Scope:** [N] tasks reviewed, [N] projects reviewed, [N] SOMEDAY items flagged
**Decisions:** [N] tasks kept, [N] promoted, [N] demoted, [N] killed
**Projects:** [N] kept, [N] new next actions, [N] completed, [N] killed
**Next week's top 3:**
1. [priority 1]
2. [priority 2]
3. [priority 3]
```

### 4c. Update timestamps

Update the "Last updated" line in:
- `${VAULT_ROOT}/Action/TASKS.md` → `*Last updated: YYYY-MM-DD*`
- `${VAULT_ROOT}/Action/PROJECTS.md` → `*Last updated: YYYY-MM-DD*`
- `${VAULT_ROOT}/Action/SOMEDAY.md` → `*Last refreshed: YYYY-MM-DD*`

### 4d. Git commit (conditional)

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$REPO_ROOT" ] && [ "$(pwd)" = "$REPO_ROOT" ]; then
  git add -A && git commit -m "weekly review: YYYY-MM-DD — [brief summary]"
fi
```

### 4e. Write the last-run marker

Update (or add, if missing) this line in the nearest `CLAUDE.md`, near the other `dlcOS:` markers — and mirror it into `AGENTS.md` if that file exists, so both stay in sync:

```
<!-- dlcOS:weekly-review-last --> YYYY-MM-DD
```

Use today's date. `/dlcOS:end` reads this marker to nudge the client when a review is overdue — without it, every session looks overdue.

---

## What This Skill Does NOT Do

- **Billing review** — no FreshBooks or CRM invoice drafting; handle billing separately
- **Email open loops** — no email API scan; check email in a dedicated session
- **Full SOMEDAY scan** — only flagged items (aged 60+, newly relevant); full scan is a separate exercise
- **CRM sync** — no Daylite/HubSpot pull; those require MacCog-specific integrations
- **Dashboard posting** — `/dlcOS:end` handles session close and any webhook hooks
- **Journaling** — reflection questions are separate; keep this review tactical
