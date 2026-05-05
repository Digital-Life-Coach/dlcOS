---
name: end
description: End-of-session wrap-up for dlcOS clients — summarize the session, route durable context to the right home (Tier 1/2/3), check off completed tasks, write daily note, compact conversation, optional git commit. Closes with an Office Hours nudge and plugin update check. Use when the user says "we're done", "wrap up the session", "end", or invokes /dlcOS:end. Run /dlcOS:save-plan FIRST if there's unfinished work to hand off to a future session. Pairs with /dlcOS:save-plan and /dlcOS:resume-plan.
---

# end — Session Close Ritual

*Invoke as `/dlcOS:end`*

Run this at the end of every Claude Code session. It captures what happened, updates the right files, and hands off cleanly to the next session. Designed to be fast (~30 seconds) and safe to run from any dlcOS vault.

---

## Step 0 — Resolve VAULT_ROOT

Walk up from the current working directory to find the nearest `CLAUDE.md`. Grep it for the line:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

That path is `${VAULT_ROOT}` for the rest of this skill. If the line is missing, stop and tell the user:

> "I can't find the dlcOS vault-root marker. Add this line to your project CLAUDE.md (replace the path with your vault's absolute path):
> `<!-- dlcOS:vault-root --> /absolute/path/to/your/vault`
> Then re-run /dlcOS:end."

---

## Step 1: Generate Session Summary

Ask yourself:

> "Summarize this session. What decisions did we make? What's still unresolved? What context would a fresh conversation need to continue where we left off?"

Structure the answer as:

```markdown
## Session Context
*Updated: YYYY-MM-DD HH:MM*

**What changed:**
- [bullet list of actions taken]

**Decisions made:**
- [bullet list of decisions and their rationale]

**Still open:**
- [bullet list of unresolved items]

**Handoff context:**
[1-2 sentences a fresh session would need to pick up where this left off]
```

---

## Step 2: Route Session Context (do NOT dump into CLAUDE.md)

CLAUDE.md is auto-loaded into every future session's opening context. Session summaries dumped here are the #1 source of context bloat. Route by tier:

### Tier 1 — Durable context → promote into the right home (REQUIRED)

Scan the summary from Step 1. For each item that is a **permanent rule, architecture decision, resolved gotcha, or confirmed convention**, you MUST promote it now — this step is not optional:

- Cross-project knowledge (API quirks, tool behavior, workflow rules) → `${VAULT_ROOT}/Wiki/Knowledge/<topic>.md` (update existing page or create one)
- Project-specific architecture / rules → the relevant section of that project's CLAUDE.md **body** (not Session Context)
- New preferences about how Claude should work → save as a memory (feedback type) if the system supports it

"Durable" means: a future session would need this and it won't be obvious from reading the files.

Before moving to Step 3, explicitly answer: "Did this session produce any durable knowledge? If yes, where did I write it?" If the answer is "no durable knowledge this session," state that — don't skip the question.

### Tier 2 — Episodic detail → Dailies only

Everything else from the summary (what-changed bullets, exploratory decisions, handoff prose) belongs in `${VAULT_ROOT}/Reference/Dailies/YYYY-MM-DD.md` — written in Step 5. Dailies are NOT auto-loaded, so they can be as detailed as needed.

### Tier 3 — Still-open items → route out of CLAUDE.md

- Actionable → `${VAULT_ROOT}/GTD/TASKS.md` (with priority tag)
- Blocked on external reply → `${VAULT_ROOT}/Projects/Awaiting Responses/<topic>.md`
- Idea, not yet actionable → `${VAULT_ROOT}/GTD/IDEAS.md` or `${VAULT_ROOT}/Inbox/ideas.md`

Never leave a growing "Still open" bullet list inside CLAUDE.md.

### The Session Context block in CLAUDE.md

After routing above, the CLAUDE.md `## Session Context` section is **only a rolling pointer list**, max 3 entries, newest first:

```markdown
## Session Context

Recent sessions (see daily for full detail):
- [2026-04-17](Reference/Dailies/2026-04-17.md) — one-line hook
- [2026-04-16](Reference/Dailies/2026-04-16.md) — one-line hook
- [2026-04-15](Reference/Dailies/2026-04-15.md) — one-line hook
```

**Hard rules:**
- Max 3 links. When adding today's, drop the oldest.
- Each line ≤120 chars. The hook is a tight phrase, not a summary.
- No "What changed / Decisions / Still open" subsections here — those live in the daily.
- If multiple projects were touched, write the pointer into EACH project's CLAUDE.md, each pointing to the same daily.

---

## Step 3: Check Off Completed Tasks

Review what was accomplished this session. If any tasks in `${VAULT_ROOT}/GTD/TASKS.md` were completed during this session, mark them `[x]`.

**Important:** Only check off tasks that THIS session actually completed. Do not scan for previously-checked tasks or archive anything — archiving is handled by the daily brief.

### Pending Plans check

Read the `## Pending Plans` section in CLAUDE.md. If any entry is older than 14 days (compare the saved date in the entry's note against today), flag it to the user:

> "Heads up: `<slug>` was saved on `<date>` and hasn't been resumed. Run `/dlcOS:resume-plan` or let me know if it should be abandoned."

Do NOT remove entries here — only `/dlcOS:resume-plan` removes them on successful completion. This is a visibility check only.

### Unsaved / partial plan check

Two cases trigger `/dlcOS:save-plan` before continuing:

1. **Unsaved plan** — this session produced a multi-step approach that was proposed but never executed, and it is NOT already in `## Pending Plans`.
2. **Partially enacted plan** — execution started but didn't finish. Reconstruct the plan from Step 1's "Still open" bullets + what was actually completed, mark done-vs-remaining explicitly, and hand to `/dlcOS:save-plan` so the next session can resume with full context.

Skip only if the session was pure execution that fully completed, or pure exploration with no plan-shaped artifact left behind.

---

## Step 3b: Sweep Read Articles (vault only)

Only run if the current working directory is inside `${VAULT_ROOT}`.

Scan `${VAULT_ROOT}/Inbox/Reading List/*.md` for any file whose frontmatter has `Status: Read` (case-insensitive). For each match:

1. Move it to `${VAULT_ROOT}/Wiki/Articles/`
2. If a file with the same name already exists, append `-<YYYYMMDD>` to the incoming filename
3. Log the moves in a single bullet under the daily note's session block (e.g. `**Read sweep:** 3 articles → Wiki/Articles/`)

```bash
VAULT_ROOT="<resolved above>"
for f in "${VAULT_ROOT}/Inbox/Reading List"/*.md; do
  [ -f "$f" ] || continue
  awk '/^---$/{n++; next} n==1 && tolower($0) ~ /^status:[[:space:]]*read[[:space:]]*$/ {found=1} END{exit !found}' "$f" && \
    mv "$f" "${VAULT_ROOT}/Wiki/Articles/$(basename "$f")"
done
```

If no files match, say nothing — silent success.

---

## Step 4: Append to Daily Note

Append a session block to `${VAULT_ROOT}/Reference/Dailies/YYYY-MM-DD.md` (create the file if it doesn't exist for today).

Use this format:

```markdown
---

## Session: [project or topic name]

**What changed:**
- [same bullets from Step 1]

**Decisions made:**
- [same bullets from Step 1]

**Files modified:**
- [list key files changed]
```

**Append, don't overwrite.** Multiple sessions will each add their own block to the same daily note. Use `---` as a separator between session blocks.

---

## Step 5: Compact Conversation

After completing all file writes, tell the user:

> "All session data saved. Run `/compact` now if you're continuing this session."

Do NOT attempt to run `/compact` yourself — it's a CLI command that only the user can invoke. This step is a **reminder**, not an action.

---

## Step 6: Git Commit (conditional)

Only run this step if the current working directory is inside the vault root AND the vault is a git repository.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$REPO_ROOT" ] && [ "$(pwd)" = "$REPO_ROOT" ]; then
  git add -A && git commit -m "end: [brief description of session work]"
fi
```

If the working directory is a subdirectory or a non-git directory, skip entirely.

---

## Step 7: Office Hours Nudge

Check whether the client has configured an Office Hours iCal feed. Look for this line in the nearest `CLAUDE.md`:

```
<!-- dlcOS:office-hours-ical --> https://calendar.google.com/calendar/ical/.../basic.ics
```

If the line is present, fetch the feed and find the next upcoming event:

```bash
ICAL_URL="<extracted from CLAUDE.md>"
ICAL=$(curl -sf "$ICAL_URL" 2>/dev/null) || exit 0   # skip silently on failure
TODAY=$(date +%Y%m%d)

echo "$ICAL" | awk -v today="$TODAY" '
  /BEGIN:VEVENT/        { in_event=1; dtstart=""; summary="" }
  in_event && /^DTSTART/ {
    val=$0; sub(/^DTSTART[^:]*:/, "", val)
    dtstart=substr(val, 1, 8)          # YYYYMMDD
  }
  in_event && /^SUMMARY:/ { summary=substr($0, 9) }
  /END:VEVENT/ && in_event {
    in_event=0
    if (dtstart >= today && dtstart != "") {
      # Format: YYYYMMDD → Month D
      y=substr(dtstart,1,4); m=substr(dtstart,5,2)+0; d=substr(dtstart,7,2)+0
      months="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec"
      split(months, mo, " ")
      printf "📅 Next Office Hours: %s %d\n", mo[m], d
      exit
    }
  }
'
```

If the config line is absent or the fetch fails or no upcoming events are found, skip this step silently — no message, no error.

---

## Step 8: Plugin Update Check

Check whether a newer version of the dlcOS plugin is available:

```bash
LATEST=$(gh api repos/Digital-Life-Coach/dlcOS/releases/latest --jq '.tag_name' 2>/dev/null)
```

- If `gh` is not installed, or the command fails (including 404 if no releases have been cut yet), skip silently.
- If `$LATEST` is returned, compare it against the installed plugin version (visible in `/plugin list`). If a newer version is available, print:

> "🔄 dlcOS update available: `<version>`. Run `/plugin update dlcOS@dlcOS` to upgrade."

---

## What /dlcOS:end Does NOT Do

These are handled by `/dlcOS:morning-brief`, not `/dlcOS:end`:

- Archive checked tasks to `GTD/COMPLETED.md`
- Process `Inbox/` folder
- Reprioritize PROJECTS.md or create next actions
- Promote SOMEDAY items

`/dlcOS:end` is a **save and summarize** ritual, not a **review and plan** ritual. Keep it fast.
