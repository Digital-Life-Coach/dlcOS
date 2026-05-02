---
name: dlc-save-plan
description: Save the current plan to disk in a self-contained format so a future Claude session (possibly a different model) can critique and execute it without access to this conversation. Writes to ${VAULT_ROOT}/Reference/Plans/YYYY-MM-DD-slug.md, drops a pointer in the project CLAUDE.md under "## Pending Plans", and explains design decisions so the next agent can audit them. Use when the user says /dlc-save-plan, "save this plan", "hand this off", "park this for a new session", or wants a fresh model to critique before implementation. Pairs with /dlc-resume-plan.
---

# /dlc-save-plan — Hand off a plan to a future session

Use when the user wants to stop here, start a fresh session (often a different model — Sonnet → Opus, etc.) and have that agent **critique and then implement** the plan. This is NOT `/dlc-end`. `/dlc-end` summarizes a finished session; `/dlc-save-plan` packages an unfinished plan with enough context that a cold-start agent can act on it.

If you're tempted to use both in the same session, run `/dlc-save-plan` FIRST (so the plan file is captured), THEN `/dlc-end` (which summarizes the session including the fact that a plan was parked).

---

## Step 0 — Resolve VAULT_ROOT

Walk up from the current working directory to find the nearest `CLAUDE.md`. Grep it for the line:

```
<!-- dlcos:vault-root --> /absolute/path/to/vault
```

That path is `${VAULT_ROOT}` for the rest of this skill. If the line is missing, stop and tell the user:

> "I can't find the dlcOS vault-root marker. Add this line to your project CLAUDE.md (replace the path with your vault's absolute path):
> `<!-- dlcos:vault-root --> /absolute/path/to/your/vault`
> Then re-run /dlc-save-plan."

---

## Step 1 — Confirm scope with the user

Before writing anything, ask:

1. What's the **slug** for this plan? (3-6 words, kebab-case, e.g. `wp-fleet-rollout`)
2. Is the audience (a) a fresh Opus session (b) a fresh Sonnet session (c) doesn't matter — assume zero context
3. Should the future agent **critique-then-execute** or **just execute**? (default: critique-then-execute)

Default to (c) and critique-then-execute if the user says "just save it."

---

## Step 2 — Build the plan file

Write to: `${VAULT_ROOT}/Reference/Plans/YYYY-MM-DD-<slug>.md`

Use today's date from the system context. If a file with that path already exists, append `-2`, `-3`, etc.

The file MUST follow this schema. Sections §1, §3, §4, §5, §7, and §10 are **mandatory** — write them even if sparse. Sections §6, §8, and §9 are optional: omit the heading entirely if there is genuinely nothing to say. The future agent relies on the mandatory sections being present.

```markdown
---
plan: <slug>
created: YYYY-MM-DD HH:MM
author_model: <model id from environment, e.g. claude-opus-4-7>
audience: <fresh-opus | fresh-sonnet | any>
mode: <critique-then-execute | execute>
status: pending
---

# Plan: <human title>

## 1. Goal
One paragraph. What outcome defines done? Why does this matter *now*?

## 2. Background & Why This Approach
What is the surrounding context? What problem does this solve? What alternative
approaches were considered and rejected, and *why*? This is where you defend
your design choices — the future agent will critique these, so be honest about
tradeoffs. If you bluff here, the critique pass becomes useless.

## 3. Current State Snapshot
- **Working directory:** <absolute path>
- **Git branch:** <branch>, <clean | dirty — list dirty files>
- **Relevant files (with line numbers where useful):**
  - `path/to/file.ts:42` — <what's there, why it matters>
- **What's already been done this session:**
  - <bullet list — commands run, files edited, things tried that didn't work>
- **What's NOT yet done:**
  - <bullet list — the actual work remaining>

## 4. The Plan (Numbered Steps)
Each step must be concrete enough to execute without re-deriving context.
Include exact commands, file paths, and expected outcomes.

1. **<Step name>** — <what to do, where, expected result>
   - Files: `<paths>`
   - Command(s): `<exact shell or tool calls>`
   - Verify: <how the agent confirms this step worked>
2. ...

## 5. Decisions & Rationale (for critique)
List each non-obvious choice as: **Decision** → **Why** → **What would change my mind**.
The future agent uses this section to push back. If a decision has no
"what would change my mind" it's probably dogma — flag it as such.

## 6. Risks & Open Questions
- Things that could go wrong and how to detect them
- Questions the user needs to answer before/during execution (numbered, with multiple-choice options where possible)

## 7. Success Criteria
A checklist the future agent uses to know it's done.
- [ ] <criterion 1>
- [ ] <criterion 2>

## 8. Rollback / Safety
What's reversible? What isn't? If step N fails, how do we get back to a clean state?

## 9. References
- Related plans, wiki pages, dailies, prior sessions
- External docs / URLs

## 10. Notes for the Critic
A direct message from author-Claude to critic-Claude. What are you LEAST sure
about? Where do you most want a second opinion? Be specific — "review step 4"
is useless; "in step 4 I assumed the WP REST cache invalidates on save_post,
but I haven't verified — please check before relying on it" is useful.
```

### Filling it in well

- **Be ruthlessly concrete.** "Update the dashboard" is useless. "Edit `Work/Dashboards/hub/server.ts:128` to change the polling interval from 60s to 30s" is useful.
- **Quote the actual code/commands** rather than describing them. The next agent shouldn't have to re-read the same files you did.
- **Include negative results.** If you tried `X` and it didn't work, say so — otherwise the next agent will retry it.
- **Honor the user's preferences** as documented in the project CLAUDE.md (numbering, multiple-choice formatting, etc.).
- **No emojis** unless the user asked for them.

---

## Step 3 — Drop a pointer in the right CLAUDE.md

Find the nearest CLAUDE.md walking up from the current working directory. If the working dir is inside `${VAULT_ROOT}`, default to `${VAULT_ROOT}/CLAUDE.md` unless a more-specific project CLAUDE.md exists in the path.

In that CLAUDE.md, find or create a top-level `## Pending Plans` section (place it directly under the H1 / front matter, before any other H2 — high visibility). Append:

```markdown
- [`<slug>`](Reference/Plans/YYYY-MM-DD-<slug>.md) — <one-line goal> *(saved YYYY-MM-DD by <model>, audience: <audience>, mode: <mode>)*
```

Use a path relative to the CLAUDE.md's directory. Keep each entry to one line. If the section grows past ~5 entries, ask the user which to retire (move to `Reference/Plans/archive/`).

If a `## Pending Plans` section already exists, append to it. Do NOT remove existing entries.

---

## Step 4 — Verify the handoff

Before reporting done:

1. Re-read the plan file you just wrote. Ask: *"If I had no memory of this conversation, could I execute this?"* If no, fix it.
2. Confirm the CLAUDE.md pointer renders as valid markdown (relative link resolves).
3. Output to the user: the plan file path, the CLAUDE.md you updated, and the exact phrase to start the next session: **"Run /dlc-resume-plan"** (or `/dlc-resume-plan <slug>` if there are multiple pending plans).

---

## Step 5 — Do NOT also run /dlc-end

`/dlc-save-plan` deliberately does not write a daily note, post to dashboards, or commit. If the user also wants to close out the session, they'll run `/dlc-end` separately.

After reporting the plan as saved, remind the user: **"Run `/dlc-end` when you're ready to close this session."**

---

## Anti-patterns (don't do these)

- ❌ Writing the plan into CLAUDE.md directly (bloats every future session)
- ❌ Vague steps ("then update the config")
- ❌ Skipping section 5 because "the steps are obvious" — the critique pass needs decisions to chew on
- ❌ Filing the plan under the project directory instead of `${VAULT_ROOT}/Reference/Plans/` — splits the index
- ❌ Running `/dlc-save-plan` for a finished session — that's `/dlc-end`'s job
