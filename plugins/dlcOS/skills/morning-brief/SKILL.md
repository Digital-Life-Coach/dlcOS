---
name: morning-brief
description: Morning brief for dlcOS clients — two modes. First run: interactive setup wizard that builds a personalized brief spec and writes it to ${VAULT_ROOT}/Reference/dlcOS-morning-brief.md. Subsequent runs: delivers a static GTD summary (P1 tasks, projects needing attention, inbox count, yesterday's completions) pulled live from vault files, written to Reference/Dailies/. Use when the user says /dlcOS:morning-brief, "morning brief", "what's my day look like", or "set up my daily brief". Use --setup to re-run the setup wizard even if a spec already exists. Use --dry-run to preview without writing the daily file.
---

# morning-brief — Daily Brief

*Invoke as `/dlcOS:morning-brief`*

Two modes, selected automatically:

- **Setup mode** (first run, or `--setup`): Collaboratively builds a brief spec and writes it to `${VAULT_ROOT}/Reference/dlcOS-morning-brief.md`. Takes ~10 minutes.
- **Brief mode** (spec exists): Pulls live data from your vault files and delivers today's brief. Takes ~30 seconds.

**Arguments:**
- `--setup` — Force re-run the setup wizard even if a spec already exists.
- `--dry-run` — Print the brief to the conversation instead of writing to the daily file.

---

## Step 0 — Resolve VAULT_ROOT

Walk up from the current working directory to find the nearest `CLAUDE.md`. Grep it for the line:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

That path is `${VAULT_ROOT}` for the rest of this skill. If the line is missing, stop and tell the user:

> "I can't find the dlcOS vault-root marker. Add this line to your project CLAUDE.md:
> `<!-- dlcOS:vault-root --> /absolute/path/to/your/vault`
> Then re-run /dlcOS:morning-brief."

---

## Step 1 — Route to Setup or Brief

Check whether `${VAULT_ROOT}/Reference/dlcOS-morning-brief.md` exists.

- **File absent** OR `--setup` flag → go to **Setup Mode** (Steps 2–4)
- **File present** AND no `--setup` flag → go to **Brief Mode** (Steps 5–7)

---

## Setup Mode

### Step 2 — Pitch and Section Selection

Tell the user:

> "Let's set up your morning brief. Each morning (or whenever you run `/dlcOS:morning-brief`) I'll pull live data from your vault and give you a focused daily snapshot. This is a v1 brief — it reads directly from your GTD files. In a future version it can also pull from your calendar, email, and other sources.
>
> Which sections would you like in your brief?"

Present as a menu — user picks any combination. Group by category so it doesn't feel overwhelming:

```
=== BRIEF SECTIONS — pick any ===

── TASKS & PROJECTS ──────────────────────────────────
a) ✅ P1 tasks            Your top-priority open tasks (recommended)
b) 📋 All open tasks      Full task list, grouped by priority
c) 📁 Projects needing    Projects with no next action or stalled 14+ days
   attention             (recommended)
d) ⭐ This week's top 3   Tasks you marked as THIS WEEK in your last weekly review

── COMPLETIONS & MOMENTUM ────────────────────────────
e) ✅ Yesterday's          Tasks checked off in the past 24 hours (recommended)
   completions
f) 📈 Weekly wins         Everything completed in the past 7 days — good for Monday
g) 🔥 Streak check        Days in a row you've completed at least 1 task

── CAPTURE & INBOX ───────────────────────────────────
h) 📥 Inbox count         How many files are waiting in Inbox/ (recommended)
i) 💡 SOMEDAY surface     One aged SOMEDAY item (60+ days) surfaced daily, in rotation
j) 💭 Idea of the day     One item from IDEAS.md, rotated daily

── REFLECTION ────────────────────────────────────────
k) ❓ Daily question      One reflection question generated fresh each morning
   (AI-generated)        (e.g. "What's one thing you've been avoiding?")
l) 🎯 Intention setter    Claude asks: "What would make today a success?" — you answer,
                          it writes your answer to the daily note
m) 📖 Journal prompt      A writing prompt based on what's in your GTD system right now

── CONTEXT & AWARENESS ───────────────────────────────
n) 📆 Today's date/day    Day of week, date, week number — useful anchor
o) 🌤  Weather             Current conditions for your location (requires location config)
p) ⏰ Time-sensitive       Tasks or projects with upcoming deadlines (reads due dates
   items                 from task frontmatter or inline dates)
q) 🔁 Recurring check-in  A rotating reminder from a custom list you define (e.g. weekly
                          calls, habits, routines)

── CUSTOM ────────────────────────────────────────────
z) ✏️  Custom section      Describe anything else you want — Claude will figure out
                          how to pull it from your vault

Starter pack (recommended for most people): a + c + e + h
Power pack: a + c + d + e + f + h + i + k
Reflective pack: a + e + h + k + l + m
```

Wait for the user's choices. Default if they say "starter" or "recommend": a + c + e + h.

### Step 3 — Delivery and Config

Ask the following, one at a time (don't dump all at once):

1. **Brief title:** "What do you want to call your daily brief? This becomes the heading each morning." (e.g. 'The Morning Brief', 'Daily Snapshot', 'Good Morning', 'What's Up')

2. **If section o (weather) was selected:** "What city/location should I use for weather? (e.g. 'San Luis Obispo, CA')"

3. **If section q (recurring check-in) was selected:** "Give me a list of recurring reminders to rotate through — one will surface each morning. These can be habits, relationship nudges, routine checks, anything. List them one per line."

4. **Delivery:** "Your brief will write to `Reference/Dailies/YYYY-MM-DD.md` in your vault — you'll see it each time you open a session. In phase 2 we can add email or push notification delivery. Sound good for now?"

5. **Custom sections:** "Anything else you'd want surfaced each morning that wasn't on the list? Describe it in plain English and I'll figure out how to pull it from your vault."

Collect all answers before writing the spec.

### Step 4 — Write Brief Spec and First Preview

Write `${VAULT_ROOT}/Reference/dlcOS-morning-brief.md`:

```markdown
# dlcOS Morning Brief Spec

*Generated by /dlcOS:morning-brief setup on YYYY-MM-DD. Edit this file to change your brief.*

## Title
[chosen title]

## Sections
[list only the enabled sections, one per line, e.g.:]
- a: P1 tasks
- c: projects needing attention
- e: yesterday's completions
- h: inbox count
- k: daily question

## Config
location: [city, state — for weather; leave blank if section o not enabled]
someday_index: 0
ideas_index: 0

## Recurring check-ins
[one per line — rotated daily in section q; leave blank if not enabled]
- [reminder 1]
- [reminder 2]

## Custom sections
[free-form description of any custom sections the user requested]

## Delivery
- v1: file-only → writes to ${VAULT_ROOT}/Reference/Dailies/YYYY-MM-DD.md
- Phase 2: email / notification (configure when ready)
```

Then immediately run **Brief Mode** (Steps 5–7) as a first preview, so the user sees their brief live before ending the session.

---

## Brief Mode

### Step 5 — Read Brief Spec

Read `${VAULT_ROOT}/Reference/dlcOS-morning-brief.md`. Parse:
- Title
- Which sections are enabled
- Any custom sections

### Step 6 — Gather Data

Pull only the data needed for the enabled sections. Run reads in parallel where possible.

**Section a — P1 tasks:**
Read `${VAULT_ROOT}/Action/TASKS.md`. Extract all unchecked `- [ ]` items tagged P1. If no P1 section exists, take the first 5 unchecked items. Cap display at 7 — if more, show 7 and note "…and N more."

**Section b — All open tasks:**
Read `${VAULT_ROOT}/Action/TASKS.md`. Show all unchecked items grouped by P1/P2/P3. Collapse P3 to a count unless there are fewer than 5 total.

**Section c — Projects needing attention:**
Read `${VAULT_ROOT}/Action/PROJECTS.md`. Flag projects that:
- Have no next action line, OR
- Have a next action that's already checked off, OR
- Have no entry in COMPLETED.md in the past 14 days

**Section d — This week's top 3:**
Read `${VAULT_ROOT}/Action/TASKS.md`. Find items marked `⭐ THIS WEEK`. List them. If none found, note "No THIS WEEK items — run `/dlcOS:weekly-review` to set them."

**Section e — Yesterday's completions:**
Read `${VAULT_ROOT}/Action/COMPLETED.md`. Extract items dated yesterday (or the most recent date in the file if nothing from yesterday).

**Section f — Weekly wins:**
Read `${VAULT_ROOT}/Action/COMPLETED.md`. Extract all items from the past 7 days. Group by day. Good opener for Monday runs.

**Section g — Streak check:**
Read `${VAULT_ROOT}/Action/COMPLETED.md`. Count consecutive days (going backwards from yesterday) that have at least one completion entry. Print: "🔥 N-day streak" or "No streak yet this week."

**Section h — Inbox count:**
```bash
ls "${VAULT_ROOT}/Inbox/" | wc -l
```
Note the count. If > 5, add a nudge: "run `/dlcOS:weekly-review` to process."

**Section i — SOMEDAY surface:**
Read `${VAULT_ROOT}/Action/SOMEDAY.md`. Track the last surfaced item index in the spec file (`someday_index` field). Advance by 1 each run (wrap around at end of list). Surface one item with its category.

**Section j — Idea of the day:**
Read `${VAULT_ROOT}/Action/IDEAS.md`. Rotate through items the same way as section i, using an `ideas_index` field in the spec.

**Section k — Daily question:**
Generate one fresh reflection question informed by what's in the GTD system right now. Ground it in something real — e.g. if there's a stalled project, ask about that; if completions were heavy, ask about momentum. Examples:
- "You've had [project] stalled for 14 days. What's actually blocking it?"
- "You completed [N] things this week. What made those easier than usual?"
- "What's one thing on your P2 list you've been quietly avoiding?"

**Section l — Intention setter:**
Ask: "What would make today a success?" — wait for the user's answer, then write it as a `## Today's Intention` heading at the top of `${VAULT_ROOT}/Reference/Dailies/YYYY-MM-DD.md`.

**Section m — Journal prompt:**
Generate a writing prompt based on what surfaced during the brief. Write it to the daily note as `## Journal Prompt` so the user can return to it later.

**Section n — Date/day anchor:**
Print: `📅 [Full day of week], [Month D, YYYY] — Week [N] of [Year]`

**Section o — Weather:**
Read the location from the spec file (`location` field, set during setup). Fetch current conditions via wttr.in:
```bash
curl -sf "https://wttr.in/${LOCATION}?format=3" 2>/dev/null
```
Skip silently if location not configured or fetch fails.

**Section p — Time-sensitive items:**
Read `${VAULT_ROOT}/Action/TASKS.md` and `${VAULT_ROOT}/Action/PROJECTS.md`. Look for inline dates (formats: `due: YYYY-MM-DD`, `by YYYY-MM-DD`, `📅 YYYY-MM-DD`). Flag anything due within 7 days.

**Section q — Recurring check-in:**
Read the `recurring` list from the spec file. Rotate through items daily (one per day) so they surface on a cadence without piling up. Examples a user might add: "Call mom this week?", "Check in with [client]", "Log workout."

**Custom sections (z):** Execute per the spec's free-form description as best you can from vault files. If the user described something that requires a specific file path or format, note that in the spec during setup so it's reliably found on future runs.

### Step 7 — Compose and Deliver

Assemble the brief in this format:

```markdown
# [Title] — [Day, Month Date]

[for each enabled section, in order:]

## ✅ P1 Tasks
- [ ] [task 1]
- [ ] [task 2]
...

## 📁 Projects Needing Attention
- **[Project Name]** — [reason: no next action / stalled N days]
...

## 📥 Inbox
[N] files waiting. [nudge if > 5]

## ✅ Yesterday's Completions
- [x] [task completed]
...

## 💡 SOMEDAY Surface
**[Idea title]** *(category)*
[1-line description if available]
Consider: promote to project / kill / leave for now

## ⭐ This Week's Top 3
1. [task]
2. [task]
3. [task]
```

**Deliver:**
- Unless `--dry-run`: append to `${VAULT_ROOT}/Reference/Dailies/YYYY-MM-DD.md` under a `## Morning Brief` heading (create the file if it doesn't exist today)
- Always: print the brief to the conversation so the user sees it immediately

---

## What This Skill Does NOT Do (v1)

- **Email or notification delivery** — v1 writes file-only. Phase 2 adds delivery channels.
- **Calendar pull** — no GCal integration in the brief for v1 (use `/dlcOS:weekly-review` for calendar review)
- **Automatic scheduling** — v1 is on-demand only. Phase 2 adds cron/launchd setup.
- **Granola or email ingestion** — those are phase 2 features
- **Replace the weekly review** — the brief is a daily snapshot, not a GTD sweep
