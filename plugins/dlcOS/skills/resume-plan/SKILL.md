---
name: resume-plan
description: Resume a plan saved by /dlcOS:save-plan in a previous session. Reads the plan file, runs a critique pass (challenges decisions, surfaces risks the prior agent missed), gets the user's go-ahead, then executes step-by-step updating status in the plan file. Use when the user says /dlcOS:resume-plan, "resume the plan", "pick up where we left off", "implement the saved plan", or starts a fresh session referencing a parked plan. Pairs with /dlcOS:save-plan.
---

# resume-plan — Critique then execute a saved plan

*Invoke as `/dlcOS:resume-plan`*

You are (probably) a fresh session — possibly a different model than the one that wrote the plan. That's the point: you bring independent judgment.

---

## Step 0 — Resolve VAULT_ROOT

Walk up from the current working directory to find the nearest `CLAUDE.md`. Grep it for the line:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

That path is `${VAULT_ROOT}` for the rest of this skill. If the line is missing, stop and tell the user:

> "I can't find the dlcOS vault-root marker. Add this line to your project CLAUDE.md (replace the path with your vault's absolute path):
> `<!-- dlcOS:vault-root --> /absolute/path/to/your/vault`
> Then re-run /dlcOS:resume-plan."

---

## Step 1 — Find the plan

If the user passed a slug (e.g. `/dlcOS:resume-plan wp-fleet-rollout`), look for `${VAULT_ROOT}/Reference/Plans/*<slug>*.md`.

Otherwise:

1. Read the nearest CLAUDE.md (walk up from cwd; default `${VAULT_ROOT}/CLAUDE.md`).
2. Find the `## Pending Plans` section.
3. If exactly one entry → use it. If multiple → list them numbered, ask the user which to resume (multiple-choice `(a)/(b)/(c)`).
4. If none → tell the user no pending plans found, suggest `/dlcOS:save-plan` if they meant to save one.

Read the plan file in full before doing anything else. Do not skim.

---

## Step 2 — Critique pass (REQUIRED unless mode: execute)

Check the plan's `mode:` frontmatter. If `execute`, skip to Step 3.

Otherwise, before touching any file, produce a critique. Read the plan as an adversary, not a collaborator:

- **Sanity-check the current state snapshot.** Spot-check 2-3 claims (file paths, line numbers, branch state, "this was already done"). The previous session's snapshot may already be stale. Use Read/Bash to verify.
- **Challenge each decision in section 5.** For each one, ask: is the "why" actually load-bearing? Does the "what would change my mind" condition already hold? Is there a simpler approach the author dismissed too quickly?
- **Stress-test the plan steps.** For each step: what assumption is it making? What happens if that assumption is wrong? Is the verify step actually sufficient?
- **Pay attention to section 10** ("Notes for the Critic") — author-Claude flagged what they were least sure about. Start there.
- **Look for what's missing.** Authentication? Rate limits? Concurrent sessions? Rollback? The author may have had a blind spot.

Output the critique as:

```markdown
## Critique of <slug>

### What holds up
- <point — why it's solid>

### What I'd push back on
1. <issue> — <why> — <recommended change>
2. ...

### What's stale
- <claim in the plan that no longer matches current state>

### Recommended changes before executing
(numbered, multiple-choice where the user needs to decide)
1. <change> — proceed (a) yes (b) no (c) modify: ...
```

Then **stop and wait for the user's response.** Do not start executing.

---

## Step 3 — Reconcile and execute

Once the user has responded to the critique:

1. Update the plan file in place to reflect any agreed changes (edit sections 4/5/6 as needed; do not rewrite history — append a `## Critique Resolution` section at the bottom noting what changed and why).
2. Flip the frontmatter `status:` from `pending` → `in-progress`.
3. Execute the steps **in order**, one at a time. After each step:
   - Run the step's "Verify" check.
   - Update the step in the file: prepend `[x]` if it's a checklist item, or add a `> Done YYYY-MM-DD HH:MM — <note>` line under the step.
   - If a step fails, STOP. Do not silently improvise — report what failed, what you tried, and ask the user how to proceed (multiple-choice).
4. Honor the user's standing rules from the project CLAUDE.md: surgical changes, ask before destructive ops, no `--no-verify`, no force-push to main, etc.

---

## Step 4 — Close out the plan

When all steps are done and success criteria pass:

1. Update frontmatter: `status: complete`, add `completed: YYYY-MM-DD HH:MM`.
2. Append a `## Outcome` section: what shipped, what changed vs. the plan, any follow-up tasks (route those to `${VAULT_ROOT}/GTD/TASKS.md` per project conventions, NOT into the plan file).
3. Remove the plan's pointer line from `## Pending Plans` in CLAUDE.md.
4. Move the file to `${VAULT_ROOT}/Reference/Plans/archive/<original-filename>` (create the dir if needed).
5. Tell the user where the archived plan lives and summarize the outcome in 2-3 sentences. Suggest `/dlcOS:end` if the session is wrapping.

If success criteria don't all pass, leave `status: in-progress`, leave the CLAUDE.md pointer, and tell the user exactly which criteria failed.

---

## If the plan is partially done and the user wants to abandon it

Update frontmatter `status: abandoned`, append `## Abandoned` section explaining why, move to `${VAULT_ROOT}/Reference/Plans/archive/`, remove pointer from CLAUDE.md. Don't silently delete.

---

## Anti-patterns

- ❌ Skipping the critique pass to "save time" — the entire reason this skill exists is the independent review
- ❌ Trusting the plan's "current state" snapshot without spot-checking — sessions in between may have changed things
- ❌ Editing the plan file's history (sections 1-10) instead of appending — preserves the audit trail
- ❌ Forgetting to clean up the CLAUDE.md pointer when done — leaves stale entries that bloat future sessions
- ❌ Bundling multiple steps' execution before reporting — go step by step so the user can interrupt
