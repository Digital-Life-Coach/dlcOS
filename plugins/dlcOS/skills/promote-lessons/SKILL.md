---
name: promote-lessons
description: Review proposed lessons from a subagent's most recent run and promote the approved ones into that agent's companion learned-lessons file, so the agent gets smarter across sessions. Use when a learning subagent (librarian or drafter) ends its output with a "**Proposed lessons:**" block, or when the user says /dlcOS:promote-lessons. Approved entries get written with a date; rejected ones evaporate.
---

# /dlcOS:promote-lessons — Subagent Lesson Approval

The dlcOS learning agents (`librarian`, `drafter`) run fresh every time. To compound across runs, they propose up to 3 lessons at the end of an invocation. This skill surfaces those proposals for your approval and writes the approved ones into the agent's companion file — which the agent reads at the start of every future run.

## Companion file locations (user-scope)

| Agent | Companion file |
|---|---|
| librarian | `~/.claude/agents/librarian-learned.md` |
| drafter | `~/.claude/agents/drafter-learned.md` |

Companion files live at **user scope** (`~/.claude/agents/`), not inside the vault — they're agent-tuning, not vault content, and this keeps them out of the user's notes and backups. They're created on first approval, not at install. (webscout and vault-hygiene don't learn — they have no companion file.)

## Steps

### 1. Find the proposals

The proposals are in the most recent subagent output in the current conversation, shaped like:

```
**Proposed lessons:**
- <rule>. Triggered by: <context>.
- <rule>. Triggered by: <context>.
```

If there's no recent block, tell the user: *"No proposed lessons in the recent conversation. A learning subagent has to end its run with a `**Proposed lessons:**` block for this skill to fire."* Stop.

### 2. Surface them for approval

Use `AskUserQuestion` with `multiSelect: true` — one option per proposal, label = the rule (trimmed to fit), description = the trigger context. Agents are capped at 3 proposals; if you somehow see more, surface the first 3 and flag it.

### 3. Write approved entries

For each approved entry, append to the matching companion file:

```markdown
## YYYY-MM-DD

- <rule>. *(Triggered by: <context>. Approved: YYYY-MM-DD.)*
```

Group same-day approvals under one date header. If the file doesn't exist yet, create it with this header first:

```markdown
---
agent: <name>
purpose: Durable learned lessons. Curated by /dlcOS:promote-lessons; read at the start of every <name> invocation.
---

# <Name> — Learned Lessons

Lead with the rule. Provenance in italics after.

```

### 4. Confirm

Report: *"Promoted N lessons to `<path>`. Dropped M."* Done.

## Design notes

- **No rejected-patterns file.** Keeping the companion file lean preserves the agent's context sharpness when it reads the file at invocation start. If an agent keeps re-proposing the same rejected lesson, that's a signal to edit its main `.md`, not to track negatives.
- **Hard cap at 3 per run.** Agents self-enforce; this skill is the approval gate.
- **Approval-required, not silent-write.** You're not in the room when the subagent runs, so approval IS the audit. Date + provenance per entry lets you prune stale lessons later (e.g. during `/dlcOS:monthly-review`).
- **Adding a new learning agent later?** Add a row to the table above, and add the read-companion + propose-block sections to that agent's `.md` (copy the pattern from `librarian.md`).
