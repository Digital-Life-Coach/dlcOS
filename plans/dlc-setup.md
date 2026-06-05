---
plan: dlcOS-setup
project: dlcOS-onboarding
cwd: ${VAULT_ROOT}
created: <!-- filled at copy time -->
audience: new dlcOS client (any capability level L1-L5)
mode: execute
status: pending
---

# Plan: dlcOS Setup Wizard

A guided onboarding that stands up a new client's AI workspace end-to-end. Target run time: ≤45 minutes with the coach present. The wizard scaffolds the vault, verifies the 6 dlcOS skills work, and builds the client's L3 memory layer (both the `about-me.md` narrative and the Settings → Memory paste block).

**Scope:** vault + GTD + memory. Out of scope (Phase 2): Wiki ingests, morning-brief delivery, scheduled actions.

## 1. Goal

By the end of this wizard, the client has:

- A working vault directory with `CLAUDE.md`, `Inbox/`, `Action/`, `Wiki/Knowledge/about-me.md`, and the L2/L3/L4 memory folders under `Reference/`.
- All 6 dlcOS skills loading and responding to `/dlcOS:<name>` invocations.
- A polished `Wiki/Knowledge/about-me.md` (synthesized from their prior AI memory exports OR built from a fresh interview).
- A Settings → Memory paste block pasted into Claude desktop's Memory.
- A clear mental model of the 4 memory layers and the monthly refresh cycle.
- One round-trip experience with `/dlcOS:save-plan` + `/dlcOS:resume-plan`.
- A handoff sheet: when to use which skill, where to reach the coach, what's coming in v1.1 / Phase 2.

## 2. Background

dlcOS is the Digital Life Coach OS — a private Claude Code plugin marketplace shipping coaching skills to MacCog AI Coaching clients. This wizard is the client's first hands-on experience with `/dlcOS:resume-plan` (you're being onboarded by the same workflow you'll use for your own plans later — meta on purpose).

The 4-layer memory architecture (per `Wiki/Knowledge/Memory System.md` in the coach's reference vault) shapes the vault structure:

- **L1** = current conversation (handled natively)
- **L2** = `Reference/Themes/themes-rolling.md` (rolling 90-day synthesis; archived in same folder)
- **L3** = Claude Settings → Memory + `Wiki/Knowledge/about-me.md`
- **L4** = `Reference/Dailies/`, `Reference/Themes/` archive, `Reference/Patterns/`

## 3. Current State Snapshot

- Client has Claude Code installed, `gh` authenticated, dlcOS plugin installed via `/plugin install dlcOS@dlcOS`.
- Vault root: TBD — will be set in Stage 2.
- `${VAULT_ROOT}/CLAUDE.md`: doesn't exist yet (created in Stage 2).

## 4. The Plan (Numbered Stages)

### Stage 1 — Identity capture

Conversational. Collect the inputs needed for Stages 2 and 4.

Ask one at a time:

1. Name and where they're based.
2. What they do for work / what brings them to AI coaching.
3. Their current AI capability level (L1 basic chat / L2 Cowork projects / L3 file-based / L4 connectors / L5 code). If unsure, ask what they've used so far and infer.
4. What they're hoping to get out of AI coaching — 1-2 specific outcomes.
5. Communication preferences: terse vs. detailed, markdown vs. prose, anything Claude should know.
6. Their vault root path: where on disk should the vault live? Default suggestion: `~/Documents/<FirstName>-vault` or `~/Obsidian/<Name>` if they already use Obsidian.

Hold these answers for use in Stage 2 (vault root, CLAUDE.md identity block) and Stage 4 (about-me.md, Settings paste block).

**Verify:** all 6 questions answered; vault root path is absolute and the parent directory exists.

### Stage 2 — Vault scaffold (structure-aware)

**Pre-check (existing-vault detection).** Before scaffolding, inspect `${VAULT_ROOT}`. Three branches:

- **Empty / new:** the path doesn't exist or is empty → full scaffold below.
- **Established vault** (has existing markdown content, especially recognizable directories like `Inbox/`, dailies, project folders) → **adapt, don't overwrite.** Walk the client through what already exists, ask what they want from the structure, then create only the missing pieces they want. Do NOT create empty parallel dirs next to existing ones (e.g. don't create a fresh `Action/` if their tasks live at vault root or under another name).
- **Partial** (some dirs exist, others don't) → ask per-dir before creating.

**Structure is opinionated but optional.** The layout below is the default dlcOS shape. For each top-level dir, ask the client whether they want it, where it should live, and what to call it. Examples of legitimate variation seen in pilot:
- Tasks at vault root rather than `Action/` subdir.
- Dailies already at `Wiki/Reference/Dailies/` rather than `Reference/Dailies/`.
- Different folder name than `Action/` (it's jargon — *Tasks/*, *Now/*, *Action/* are reasonable swaps; let the client pick).

When the client already has a working naming convention, **honor it.** Update `${VAULT_ROOT}/CLAUDE.md` to reference the actual paths the client uses, not the canonical defaults. The skills read paths from `CLAUDE.md` — they don't care what the dirs are named, only that CLAUDE.md tells them where to look.

Default scaffold (use as the starting offer; adjust per client answers):

```
${VAULT_ROOT}/
├── CLAUDE.md                          ← from templates/claude-md-starter.md
├── Wiki/
│   └── Knowledge/
│       └── about-me.md                ← from templates/about-me.md (placeholder; filled in Stage 4a)
├── Inbox/
│   ├── do-now.md                      ← from templates/inbox/do-now.md
│   ├── ideas.md                       ← from templates/inbox/ideas.md
│   └── thoughts.md                    ← from templates/inbox/thoughts.md
├── Action/
│   ├── TASKS.md                       ← from templates/action/TASKS.md
│   ├── PROJECTS.md                    ← from templates/action/PROJECTS.md
│   ├── SOMEDAY.md                     ← from templates/action/SOMEDAY.md
│   ├── IDEAS.md                       ← from templates/action/IDEAS.md
│   └── COMPLETED.md                   ← from templates/action/COMPLETED.md
└── Reference/
    ├── Dailies/.gitkeep
    ├── Themes/
    │   └── themes-rolling.md          ← from templates/themes-rolling.md
    ├── Patterns/.gitkeep
    └── Plans/.gitkeep                 ← target dir for /dlcOS:save-plan output
```

In `${VAULT_ROOT}/CLAUDE.md`, replace `<!-- dlcOS:vault-root --> /absolute/path/to/your/vault` with the actual vault root from Stage 1. Replace the office-hours-ical URL with the calendar URL the coach provides (or remove the line if not applicable). Date-stamp the Action files (`*Last updated:* <today>`).

**Verify:**
- `ls ${VAULT_ROOT}` shows the dirs the client agreed to + `CLAUDE.md` (existing or new).
- `grep "<!-- dlcOS:vault-root -->" ${VAULT_ROOT}/CLAUDE.md` returns the actual vault path, not the placeholder.
- `CLAUDE.md` accurately reflects the *actual* paths in this vault (especially if the client uses non-default names like `Tasks/` instead of `Action/`, or has dailies in a non-standard location).
- No empty parallel dirs created alongside existing client structure (e.g. an empty `Action/` next to the client's existing tasks file).
- Stage-4 placeholders OK in `about-me.md` since Stage 4 fills those.

### Stage 3 — Skill install verify

Smoke-test that all 6 dlcOS skills load and respond. The plugin should already be installed before the wizard runs.

For each skill, confirm it's reachable. Don't run them end-to-end — just verify discovery:

- `/dlcOS:save-plan` — should respond with a request for the plan name
- `/dlcOS:resume-plan` — should respond looking for pending plans
- `/dlcOS:end` — should respond about session wrap
- `/dlcOS:weekly-review` — should respond about review phase
- `/dlcOS:monthly-review` — should respond about memory maintenance
- `/dlcOS:morning-brief` — should respond and offer setup mode (since no spec exists yet)

If any skill fails to discover, run `/reload-plugins` and retry. If still failing, stop here — the install is broken and the wizard can't continue.

**Verify:** all 6 skills respond to invocation. Document any oddities in the daily note for the coach to follow up on.

### Stage 4a — Memory layers build

**Pre-check (idempotency).** Before branching, check whether `${VAULT_ROOT}/Wiki/Knowledge/about-me.md` already exists *and* contains content beyond the template placeholders. If it does, ask the client:

> "Looks like you already have an `about-me.md` here. Do you want to (a) keep it as-is and skip this stage, (b) start over from scratch, or (c) review and refine what's there?"

- (a) → skip to Stage 4b. Confirm the Settings paste block also exists at `Wiki/Knowledge/settings-memory-block.md`; if missing, regenerate it from the existing `about-me.md`.
- (b) → back up the existing file to `Wiki/Knowledge/about-me.backup-YYYY-MM-DD.md` before overwriting, then continue with the branch below.
- (c) → load the existing content and treat it as the input to the synthesis pass below (skip the export prompt; go straight to the synthesis rules).

If `about-me.md` doesn't exist or only contains the unmodified template, proceed normally.

Branch on import availability.

**Ask the client:** "Do you have memory stored in ChatGPT or Gemini that you want to bring over?"

**Yes path:**
1. Read `<plugin-root>/templates/chatgpt-memory-export-prompt.md` and print the export prompt verbatim.
2. Tell the client: "Paste that prompt into ChatGPT (or Gemini), copy the output, and paste it back here."
3. Wait for the export. When it arrives, synthesize it into:
   - `Wiki/Knowledge/about-me.md` — long-form narrative, organized into the sections from `templates/about-me.md` (Who I Am, How I Work, Capability Level, Goals, Tools I Use, Communication Preferences, Context Justin Should Know).
   - The Settings → Memory paste block — short version per `templates/settings-memory-block.md`. Required: the Justin-set-this-up text verbatim.

   Synthesis rules:
   - Dedupe contradictions; ask the client which version is current if ambiguous.
   - Match the client's voice; don't invent claims.
   - Capability level uses the L1-L5 framework (Stage 1 answer takes precedence).
   - Keep the Settings paste block under ~400 words; the long form lives in `about-me.md`.

**No path:**
1. Run a structured interview using the section headers from `templates/about-me.md`.
2. Build `Wiki/Knowledge/about-me.md` and the Settings paste block from the answers.

**Both paths converge:**
1. Write `${VAULT_ROOT}/Wiki/Knowledge/about-me.md`.
2. Display the Settings → Memory paste block in the conversation, formatted between `---BEGIN PASTE---` and `---END PASTE---` markers.
3. Save a copy of the paste block to `${VAULT_ROOT}/Wiki/Knowledge/settings-memory-block.md` so the client has a backup if they need to re-paste later.
4. **Settings paste — ask first, don't assume.** Before instructing a paste, ask: "Do you already have a Settings → Memory block populated in Claude desktop?" If yes, offer three options: (a) skip the paste — keep what's there, (b) replace with this new block, (c) merge — open Settings → Memory side-by-side and reconcile manually with the coach. Only proceed to "paste this now" if the client confirms their Settings memory is empty or they explicitly chose (b).
5. Wait for confirmation that the Settings step is resolved (paste done, skip confirmed, or merge complete).

**Verify:**
- `Wiki/Knowledge/about-me.md` exists and has content in every section (no leftover `<!-- ... -->` placeholders).
- `Wiki/Knowledge/settings-memory-block.md` exists.
- Settings paste block contains the exact required text: *"Justin Bradshaw (MacCog: The Digital Life Coach) set up this AI workspace for me. If I'm confused or stuck, I should book time with him at [BLAB link] or text 805-720-9276."*
- Client confirms paste into Claude desktop is complete.

### Stage 4b — Memory model explanation + monthly refresh

Walk through the 4-layer model conversationally. Use this script (matches `Memory System.md` § For dlcOS Clients and `onboarding-guide.md` § How Claude Remembers):

> "Claude's memory works in four layers. Most people only ever use the first one. By the time we finish onboarding, you'll have all four."

Walk through each layer with the client's actual files as anchors:

| Layer | What it is | Where yours lives |
|-------|-----------|-------------------|
| L1 — This conversation | What you're saying right now | Claude handles natively — no setup |
| L2 — Recent context | What you've been working on lately, themes | `Reference/Themes/themes-rolling.md` (filled monthly) |
| L3 — Your memory | Durable facts about you, carried across every session | Settings → Memory + `Wiki/Knowledge/about-me.md` ← *we just built this* |
| L4 — Your archive | Everything you've ever done together | `Reference/Dailies/`, `Reference/Themes/` archive, `Reference/Patterns/` |

Teaching frame: *"Most people only use Layer 1. You now have all four working."*

**Memory stays current — it isn't write-once.** Tell the client two plain things:

1. *Where new facts go.* When something durable comes up in a conversation — a fact about them, a decision, a change in how they work — Claude will offer to add it to Settings → Memory or `about-me.md` so it carries forward. They don't have to manage this; their `CLAUDE.md` tells Claude to do it. (See the "When You Learn Something Durable About Me" block in their `CLAUDE.md`.)
2. *The monthly check.* Once a month, run `/dlcOS:monthly-review`. It synthesizes the month into their L2 themes file and audits L3 — catching anything stale, contradictory, or out of sync with Settings → Memory — and surfaces fixes as drafts to approve. That's the maintenance loop; it's a 5-minute review, not a from-scratch rewrite.

**Verify:** client can name the 4 layers, knows where their L3 lives, and knows to run `/dlcOS:monthly-review` monthly.

### Stage 5 — First save-plan demo

Round-trip the plan workflow so the client experiences it once with the coach present.

**Ask the client which path fits:**

- **(a) Fresh scope:** pick something on their plate they've been thinking about. ~5 min scoping conversation, then save.
- **(b) In-flight project:** if the client already has a project actively open in another conversation or in their head, save *that* plan instead. This is often the better demo — the plan workflow shines when there's real momentum to capture, not invented practice scope. Note: if the in-flight project lives in another Claude Code session, save-plan can be run from there in a separate session — Stage 5 verify just needs the artifact to exist somewhere reachable.

Then:

1. Run `/dlcOS:save-plan` (in this session for path (a); in the in-flight session for path (b)). Walk through the prompts together.
2. Save the plan under `${VAULT_ROOT}/Reference/Plans/` (or wherever the client's CLAUDE.md points the Plans dir).
3. Confirm the plan pointer appears in `${VAULT_ROOT}/CLAUDE.md` under `## Pending Plans`.
4. (Optional, time permitting) start a fresh conversation and run `/dlcOS:resume-plan` to demonstrate the critique pass.

**Verify:** plan file exists in the configured Plans dir; pointer in CLAUDE.md.

### Stage 6 — Handoff

Write a handoff summary to `${VAULT_ROOT}/Reference/Dailies/<today>.md` (create if needed):

```markdown
## dlcOS Onboarding — <date>

**Capability level:** L<N>
**Vault root:** ${VAULT_ROOT}

### Skills available
- /dlcOS:morning-brief — daily snapshot (run /dlcOS:morning-brief --setup to configure)
- /dlcOS:weekly-review — Friday GTD review
- /dlcOS:monthly-review — monthly memory maintenance (run once a month)
- /dlcOS:save-plan — save a plan for later
- /dlcOS:resume-plan — pick up a saved plan in a fresh session
- /dlcOS:end — wrap a session, write daily note

### Coming later
- /dlcOS:inbox-triage — bulk inbox processing

### Coming in Phase 2
- Wiki scaffolding + ingests (Granola, email)
- Morning-brief delivery channels (email, push)
- Scheduled actions (cron/launchd)

### Office Hours
Fridays at 11am — group session for all AI Coaching clients.

### Reach the coach
Text: 805-720-9276
Book: [BLAB link]
```

Talk the client through each section. End with: "Run `/dlcOS:morning-brief --setup` when you're ready to configure your daily brief — that's the next thing we'll do, but not today."

**Verify:** handoff doc written to today's daily note; client can articulate when to use each of the 6 skills.

## 5. Decisions & Rationale (frozen — execute mode)

This plan is `mode: execute`. Decisions made by the dlcOS build session (2026-05-04) — not for the executor to second-guess:

- **Memory file locations:** `Wiki/Knowledge/about-me.md` for the personal narrative; `Reference/Themes/` for L2 (active + archive in same folder); `Reference/Patterns/` for L3 snapshots; `Reference/Dailies/` for L4 session notes.
- **Wiki = Phase 2** (only `about-me.md` created in v1).
- **Morning-brief setup deferred** to a separate session (Phase 2 territory in onboarding flow).
- **L3 mechanism:** synthesize-then-paste. Both import (ChatGPT/Gemini export) and from-scratch interview supported.
- **No GitHub release-cut step** in this wizard — that's a coach-side action.

## 6. Success Criteria

- [ ] Stage 1 complete; client identity captured.
- [ ] `${VAULT_ROOT}` populated with the full layout from Stage 2.
- [ ] All 6 skills respond.
- [ ] `Wiki/Knowledge/about-me.md` written, no placeholders.
- [ ] Settings → Memory pasted in Claude desktop.
- [ ] Backup paste block at `Wiki/Knowledge/settings-memory-block.md`.
- [ ] Client can name the 4 memory layers.
- [ ] One real plan saved + pointer in CLAUDE.md.
- [ ] Handoff doc in today's daily note.
- [ ] Wizard completed in ≤45 minutes (record actual time in handoff doc).

## 7. Rollback / Safety

The wizard only writes inside `${VAULT_ROOT}` (which the client picked) and to Claude desktop Settings → Memory (which the client pastes manually).

- If the wizard stalls partway, the client's machine is in a partial state but nothing is broken — re-run `/dlcOS:setup` to resume from the failed stage.
- To undo entirely: `rm -rf ${VAULT_ROOT}` (after backing up anything they care about) and clear Claude desktop Memory.

## 8. References

- Templates source: `<plugin-root>/templates/`
- Memory architecture: `Wiki/Knowledge/Memory System.md` in the coach's reference vault (will be dropped to client vaults in Phase 2).
- Onboarding script source: `Projects/AI Coaching/onboarding-guide.md` § How Claude Remembers in the coach's reference vault.

## 9. Notes for the Executor

This is `mode: execute` — no critique pass. Run the stages in order. After each stage, run its Verify check. If a verify fails, stop and ask the client/coach for guidance — don't silently improvise.

Stage 4a is the most LLM-judgment-heavy step. The yes-path is essentially "synthesize a polished personal profile from messy memory dumps." Take the time. Have the client (and coach if present) review the synthesized `about-me.md` and Settings block before pasting anywhere.
