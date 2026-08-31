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

A guided onboarding that stands up a new client's AI workspace end-to-end. Target run time: ≤45 minutes with the coach present. The wizard scaffolds the vault, verifies the core dlcOS skills work, and builds the client's L3 memory layer (both the `about-me.md` narrative and the Settings → Memory paste block).

**Scope:** vault + GTD + memory, including a small client-selected Wiki starter set. Out of scope (Phase 2): unattended/recurring Wiki ingests, morning-brief delivery, scheduled actions.

## 1. Goal

By the end of this wizard, the client has:

- A working vault directory with `CLAUDE.md`, `Inbox/`, `Action/`, `Wiki/Knowledge/about-me.md`, and the L2/L3/L4 memory folders under `Reference/`.
- The core dlcOS skills loading and responding to `/dlcOS:<name>` invocations.
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

**Structure is opinionated but optional — and how much you ask depends on capability level.** The layout below is the default dlcOS shape. Take the client's Stage 1 capability answer and branch:

**L1–L2 — decide for them, offer to change it later.** Do not ask an L1 client to choose between `Action/`, `Tasks/`, and `Now/`. They have no basis to evaluate that choice; it's jargon dressed up as a preference, and it makes the first ten minutes of their vault feel like a configuration screen. Build the default scaffold, then tell them in one sentence:

> "I've set up a standard layout — an Inbox for anything you haven't sorted yet, an Action folder for tasks and projects, a Wiki for reference, and a Reference folder for the automatic notes. If any of those names bug you later, say so and we'll rename them; nothing breaks."

Then move on. The one thing to confirm out loud is the **vault root path**, because that's about where their files live, which they do have an opinion about.

**L3+ — run the full interview.** For each top-level dir, ask whether they want it, where it should live, and what to call it. Examples of legitimate variation seen in pilot:
- Tasks at vault root rather than `Action/` subdir.
- Dailies already at `Wiki/Reference/Dailies/` rather than `Reference/Dailies/`.
- Different folder name than `Action/` (it's jargon — *Tasks/*, *Now/*, *Action/* are reasonable swaps; let the client pick).

**Both branches:** when the client already has a working naming convention, **honor it.** Update `${VAULT_ROOT}/CLAUDE.md` *and* `${VAULT_ROOT}/AGENTS.md` to reference the actual paths the client uses, not the canonical defaults. The skills read paths from `CLAUDE.md` — they don't care what the dirs are named, only that it tells them where to look.

Note the existing-vault pre-check above still runs for every capability level. "Decide for them" applies to *naming a new scaffold*, never to touching structure the client already has.

Default scaffold (use as the starting offer; adjust per client answers):

```
${VAULT_ROOT}/
├── CLAUDE.md                          ← from templates/claude-md-starter.md
├── AGENTS.md                          ← from templates/agents-md-starter.md (tool-neutral twin — see below)
├── START-HERE.md                      ← from templates/START-HERE.md (client-facing orientation; finished in Stage 6)
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

#### Wiki starter packs — let the client choose

After agreeing on the base structure, tell the client:

> "Your Wiki is where Claude keeps useful reference material that isn't a task. I can set up a few starter areas now and, where you already have source material available, pull in an initial index. Pick only what would be useful today; you can add the rest later."

Show this curated list. Use plain-language labels first; mention example sources only to help the client recognize what they already have.

| Starter area | Useful for | Possible starting sources | Default destination |
|---|---|---|---|
| People & relationships | Important context, preferences, last touch, follow-ups | Contacts, CRM, existing notes | `Wiki/People/` |
| Clients & work | Client briefs, active engagements, key decisions | CRM, project folders, email, meeting notes | `Wiki/Clients/` |
| Meetings | Searchable meeting summaries and decisions | Granola, Zoom transcripts, calendar notes, markdown exports | `Wiki/Meetings/` |
| Companies & organizations | Vendors, partners, memberships, institutions | Contacts, email, existing documents | `Wiki/Organizations/` |
| Personal knowledge | Topics, procedures, lessons, reference notes | Apple Notes, Notion, Obsidian, Google Drive, markdown files | `Wiki/Knowledge/` |
| Reading & research | Articles, books, highlights, saved links | Browser bookmarks, Readwise, Kindle highlights, reading lists | `Wiki/Library/` |
| Health & wellness | Providers, routines, goals, non-sensitive reference material | Health notes, PDFs, exported reports | `Wiki/Health/` |
| Home, vehicles & possessions | Maintenance history, manuals, warranties, service providers | Drive folders, email receipts, PDFs, existing notes | `Wiki/Home/` |
| Travel & places | Trips, itineraries, favorite places, loyalty details | Calendar, email confirmations, travel notes | `Wiki/Travel/` |
| Recipes & food | Recipes, meal ideas, restaurant notes | Notes, bookmarks, recipe exports | `Wiki/Food/` |

Ask them to choose **up to 3 starter areas** for onboarding. "None for now" is a valid choice. Also accept a client-suggested area that is not on the list.

For each selection:

1. Ask which source, if any, they want to start from. Never imply a connector or account is available until you verify it.
2. If the source is accessible in the current session, preview what will be imported and ask for confirmation before reading or copying in bulk. Create the destination and a concise `README.md` index describing its purpose, source, organization, and last import date; then import a small representative batch or index that can be completed during onboarding.
3. If the source is not accessible, still create the destination and `README.md`, add a `## Source to connect` note with the source and intended import, and tell the client exactly what access/export is needed later. Do not stall the rest of onboarding.
4. Prefer links or summaries over duplicating entire source archives. Preserve source attribution and dates. Do not import secrets, credentials, financial account numbers, medical identifiers, or other highly sensitive data without an explicit item-level review.
5. If the client already has a matching folder or convention, use it. Never create a parallel folder merely to match the defaults above.

Keep this stage to **10 minutes maximum**. This is a useful starting surface, not a full migration. Recurring synchronization and large historical imports remain Phase 2 work.

#### Write BOTH orchestration files

`CLAUDE.md` is Claude-only. Any client who uses Codex, Cursor, Aider, or anything else reads `AGENTS.md` instead — and gets nothing: no vault map, no communication preferences, no memory routing rule. Assume the client will use more than one tool, because most of them do.

1. Copy `${TEMPLATES}/claude-md-starter.md` → `${VAULT_ROOT}/CLAUDE.md`.
2. Copy `${TEMPLATES}/agents-md-starter.md` → `${VAULT_ROOT}/AGENTS.md`.
3. In **both**: replace `<!-- dlcOS:vault-root --> /absolute/path/to/your/vault` with the actual vault root from Stage 1, and correct the "Where things live" paths to whatever this vault actually uses. **The vault-root marker must be in both files, not just `CLAUDE.md`** — every dlcOS skill resolves the vault from it, and a Codex-driven vault auto-loads only `AGENTS.md`. A marker in one file and not the other is the single most likely reason a skill stops at Step 0 on a working vault.
4. In `CLAUDE.md` only: replace the office-hours-ical URL with the calendar URL the coach provides (or remove the line if not applicable).
5. In `AGENTS.md`: fill the "How to work with me" section from the Stage 1 communication-preferences answer.
6. Copy `${TEMPLATES}/START-HERE.md` → `${VAULT_ROOT}/START-HERE.md` and date it. Its "What's here" and "What's still unfinished" sections get filled in Stage 6, once you know what actually happened.
7. Date-stamp the Action files (`*Last updated:* <today>`).

**Set the coach-contact marker.** `CLAUDE.md` ships a `<!-- dlcOS:coach-contact -->` line with Justin's phone and booking link as the default. Ask, don't assume:

> "How do you actually reach me when you're stuck?"

Write their real answer. For most clients that's the text/booking default. For a client who's married to their coach, or sees them weekly, or works in the same building, a booking CTA reads as absurd — and boilerplate that obviously wasn't written for this person quietly undermines everything around it, especially for an anxious client. If they reach the coach some other way entirely, delete the marker line.

**Verify:**
- `ls ${VAULT_ROOT}` shows the dirs the client agreed to + `CLAUDE.md` (existing or new).
- `grep "<!-- dlcOS:vault-root -->" ${VAULT_ROOT}/CLAUDE.md` returns the actual vault path, not the placeholder.
- `${VAULT_ROOT}/AGENTS.md` exists, carries the same vault-root path, and its "Where things live" table matches the dirs actually created.
- `${VAULT_ROOT}/START-HERE.md` exists (its Stage-6 sections may still be placeholders).
- The `<!-- dlcOS:coach-contact -->` line says how this client actually reaches their coach, or has been deleted deliberately — it is not the unedited shipped default unless the client confirmed the default is true for them.
- For an L1/L2 client: no folder-naming interview was run, and the client was told they can rename later.
- `CLAUDE.md` accurately reflects the *actual* paths in this vault (especially if the client uses non-default names like `Tasks/` instead of `Action/`, or has dailies in a non-standard location).
- No empty parallel dirs created alongside existing client structure (e.g. an empty `Action/` next to the client's existing tasks file).
- Every selected Wiki starter area has an agreed destination and `README.md`; any unavailable source is recorded under `## Source to connect` rather than treated as configured.
- No unselected Wiki starter directories were created.
- Stage-4 placeholders OK in `about-me.md` since Stage 4 fills those.

### Stage 3 — Skill install verify

Smoke-test that the **core** dlcOS skills load and respond. The plugin should already be installed before the wizard runs.

Confirm each is reachable. Don't run them end-to-end — just verify discovery:

- `/dlcOS:save-plan` — should respond with a request for the plan name
- `/dlcOS:resume-plan` — should respond looking for pending plans
- `/dlcOS:end` — should respond about session wrap
- `/dlcOS:weekly-review` — should respond about review phase
- `/dlcOS:monthly-review` — should respond about memory maintenance
- `/dlcOS:morning-brief` — should respond and offer setup mode (since no spec exists yet)
- `/dlcOS:draft` — should respond asking what to draft

Typing `/dlcOS` should also list the optional add-ons (`setup-email`, `dashboard-setup`, `setup-librarian-index`, `memory-harden`) and the vault-health skills. Don't smoke-test those here — they're not part of onboarding and several of them do real work on invocation.

If a skill fails to discover: in Claude Code run `/reload-plugins` and retry; in Codex confirm `codex plugin list` shows `dlcOS@dlcOS` as *installed, enabled* and restart the session. If still failing, stop here — the install is broken and the wizard can't continue.

**On Codex,** skip the `draft` check's subagent expectation — subagents don't exist there. The skill still runs; it does the drafting inline. Everything else behaves the same.

**Verify:** all 7 core skills respond to invocation, and `/dlcOS` lists the add-ons. Document any oddities in the daily note for the coach to follow up on.

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
1. Read `${TEMPLATES}/chatgpt-memory-export-prompt.md` and print the export prompt verbatim.
2. Tell the client how to get the output back **without shipping it to another provider**: save it to a file (e.g. `~/Desktop/memory-export.md`) and let this session read it off disk. Offer pasting-in-chat only as the second option, and don't offer it at all to a client whose stated reason for being here is privacy.
3. Wait for the export.

#### Triage the export BEFORE writing anything

**Do not skip this and do not do it silently.** Memory exports are not tidy lists of preferences. Real ones from the live runs have contained a named hospice patient's clinical and mental-health detail, a friend's terminal cancer course, family medical history, and an unresolved death with allegations about a named police officer. Caregiving, hospice, healthcare, clergy, legal, and therapy clients will hit this routinely, and for several of them confidentiality is a real obligation, not a preference. "Synthesize it" is the wrong default when the file contains someone else's worst year.

Read the export and sort every item into four buckets. Show the client the **counts and one-line labels** — not the full contents read back at them:

| Bucket | What it is | Default destination |
|---|---|---|
| **(a) Their own durable facts** | Who they are, what they do, how they work, goals, tools, preferences | `about-me.md` + Settings → Memory block |
| **(b) Their own health** | Their diagnoses, medications, mental health, treatment | Local vault only, if they want it at all — **never** the Settings → Memory block |
| **(c) Third-party sensitive** | Anything identifying about someone else: patients, clients under confidentiality, friends' or family's health, deaths, legal matters, allegations about named people | **Nothing is written by default.** Local vault only, and only per-item, only if they ask |
| **(d) Practical reference** | Passwords-adjacent notes, addresses, schedules, logistics, how-tos | Ask — often better as a normal Wiki note than as memory |

Then confirm **per category**, one at a time (`AskUserQuestion` where the harness has it, otherwise a plain lettered choice — the confirmation matters, the widget doesn't):

- **(a)** — "This is the material I'd use to write your profile. Good?" Default yes.
- **(b)** — "There's health information about you in here. I can leave it out entirely, or keep it in a local file in your vault. It will not go into the memory block that travels to Claude's servers either way." Default: leave out.
- **(c)** — "There's information in here about other people — [N items, e.g. 'a hospice patient, a friend's illness, a family matter']. That was told to you, not to me. My default is to write none of it down. Do you want any of it kept?" Default: **none.** If they do want something kept, take it item by item, and name the confidentiality question out loud if the client's role implies one ("You're describing this as hospice volunteering — is that covered by a confidentiality agreement?").
- **(d)** — "This is practical stuff. Want it as notes in your Wiki, or dropped?"

**Hard rules, not negotiable by the client's enthusiasm:**
- Bucket (b) and bucket (c) content **never** goes into the Settings → Memory block. That block is cloud-stored and travels into every conversation on every device. It is the wrong container for a patient's name.
- Bucket (c) items are written only on an explicit per-item yes.
- If the client says "just use all of it," do not. Show them what's in (c) first, then ask again. This is the one place in the wizard where you push back.
- Record in the handoff note only that triage ran and what the client chose per bucket — never the sensitive content itself.
- If the export came in as a file, offer to delete it when the stage completes.

#### Then synthesize

Using **only** the buckets the client approved, write:
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
- The paste block contains the **attribution** sentence verbatim: *"I work with Justin Bradshaw (MacCog: The Digital Life Coach), who set up this AI workspace for me."* This one is required — it's what tells a future Claude session where this workspace came from.
- The **contact line** after it says how this client actually reaches their coach, matching the `<!-- dlcOS:coach-contact -->` marker set in Stage 2. It is not required to be the shipped default, and a client for whom a booking link is untrue should not have one. What's checked here is that the line is *true*, not that it matches a fixed string.
- **The Settings step reached one of three valid resolutions** — pasted, skipped, or merged. All three pass. Step 4 above explicitly offers "skip the paste" as a supported choice; a client who takes it must not then be blocked by this verify. Record which resolution happened in the handoff note.
- If the export was triaged: the client confirmed each of the four buckets, and no bucket (b) or (c) content appears anywhere in `settings-memory-block.md`. Check this by reading the file, not by assuming.

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

### Stage 4c — Voice doc (optional, ≤3 min — scaffold now, fill now or later)

This stage stands up the voice rulebook the `dlcOS:drafter` agent reads whenever it writes something in the client's name (emails, posts, proposals). Keep it light — the goal is to *scaffold* the file and get one or two real answers, not run a full interview. Drafter works without it (neutral voice); it just sounds more like the client once filled.

1. **Scaffold the file.** If `${VAULT_ROOT}/Wiki/Knowledge/voice.md` doesn't exist, copy it from `templates/voice.md` (the fillable skeleton). If it already exists with real content, skip to the offer below.
2. **Offer — fill now or later** (single-select; `AskUserQuestion` where available):
   > "Want to set up your writing voice now, or later? The `drafter` agent uses it to sound like you instead of generic AI."
   - **(a) Quick pass now (recommended)** — ask just two things and write them into voice.md: *"In one line, how would a friend describe the way you write?"* and *"Any words, phrases, or punctuation you never want in your writing?"* (Mention em dashes as the classic example — keep or cut.) Write those two answers into the matching sections; leave the rest as skeleton prompts for them to fill anytime.
   - **(b) Later** — leave the skeleton in place. Tell them: *"It's at `Wiki/Knowledge/voice.md` — fill it whenever, or `/dlcOS:draft` will offer to help the first time you use it."*
3. Do NOT run a full register-by-register interview here — that protects the ≤45-min onboarding target. The skeleton + `/dlcOS:draft`'s first-run prompt cover the rest.

**Verify:** `Wiki/Knowledge/voice.md` exists (filled or skeleton); client knows where it lives and that `/dlcOS:draft` will help finish it.

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

### Stage 6 — Handoff (branches on capability level)

Copy `${TEMPLATES}/setup-checklist.md` to `${VAULT_ROOT}/Reference/dlcOS-setup-checklist.md` if it doesn't already exist. This is what `/dlcOS:end` nudges from every session close — better to ship it now than have `/dlcOS:end` silently create it later on the client's first session.

#### Finish START-HERE.md — every client, every level

Stage 2 dropped `${VAULT_ROOT}/START-HERE.md` in place. Now fill its two blank sections, because only now do you know what actually happened:

- **"What's here"** — list only the folders this client actually has, under the names they actually have. Don't describe folders you didn't create.
- **"What's still unfinished"** — be specific and honest. A Wiki area created but empty because the source needed a password. An add-on deferred. A memory bucket the client chose to leave out. One line each, plain language, with what it's waiting on. If nothing is outstanding, say so plainly.

This file is the deliverable that survives the client not being at the keyboard. Stage 4b's memory-model walkthrough is a **spoken script** — if the client stepped away, was overwhelmed, or was never at the machine in the first place, the entire teaching half of onboarding delivered nothing. START-HERE.md is the durable copy. Write it whether or not the conversation went well.

#### Then branch

**L1–L2 clients — the skills are the COACH's surface, not theirs.**

An L1 client may not have a command line, may never open Claude Code again, and does not benefit from memorizing six slash commands. Their surface is Obsidian plus a chat app. Teaching them `/dlcOS:save-plan` on day one produces nodding, not competence.

Walk them through **START-HERE.md on screen**, and teach exactly three things:

1. **Where to put things** — Inbox for anything unsorted; when in doubt, Inbox. Show them, in Obsidian, once.
2. **How to ask** — they can ask Claude about their own vault in plain language. Give them one real example using something from their own Stage 1 answers.
3. **How to reach you** — the `dlcOS:coach-contact` line, in whatever form is actually true for them.

Then tell them what *you* will run on their behalf, and when: the monthly memory review, and a check-in on whatever's in the unfinished list. Do not hand an L1 client a list of commands.

Write the daily-note handoff for the **coach's** records (below) — but the client's copy is START-HERE.md.

**L3+ clients — full skill handoff.**

Write a handoff summary to `${VAULT_ROOT}/Reference/Dailies/<today>.md` (create if needed) and talk them through it:

```markdown
## dlcOS Onboarding — <date>

**Capability level:** L<N>
**Vault root:** ${VAULT_ROOT}
**Settings → Memory resolution:** pasted / skipped / merged
**Memory export triage:** ran / not applicable — buckets kept: <a / a+d / etc.>

### Skills available
- /dlcOS:morning-brief — daily snapshot (run /dlcOS:morning-brief --setup to configure)
- /dlcOS:weekly-review — Friday GTD review
- /dlcOS:monthly-review — monthly memory maintenance (run once a month)
- /dlcOS:save-plan — save a plan for later
- /dlcOS:resume-plan — pick up a saved plan in a fresh session
- /dlcOS:draft — draft something in your voice
- /dlcOS:end — wrap a session, write daily note

### Add-ons available when they're wanted
- /dlcOS:setup-email — connect Fastmail or Gmail (drafts only, never sends)
- /dlcOS:dashboard-setup — the dashboard web app on their own machine (macOS or Linux)
- /dlcOS:setup-librarian-index — local semantic search over the vault

### Still unfinished
<!-- mirror START-HERE.md's unfinished list -->

### Office Hours
<!-- day/time if the coach runs them, else delete -->

### Reach the coach
<!-- whatever the dlcOS:coach-contact marker says -->
```

End with: "Run `/dlcOS:morning-brief --setup` when you're ready to configure your daily brief — that's the next thing we'll do, but not today."

**Verify:**
- `${VAULT_ROOT}/START-HERE.md` exists with both formerly-blank sections filled, naming this client's real folders and real outstanding items.
- Handoff written to today's daily note.
- **L1–L2:** client can say where an unsorted thought goes, and how to reach their coach. They are *not* expected to name any slash command.
- **L3+:** client can articulate when to use each skill.

## 5. Decisions & Rationale (frozen — execute mode)

This plan is `mode: execute`. Decisions made by the dlcOS build session (2026-05-04) — not for the executor to second-guess:

- **Memory file locations:** `Wiki/Knowledge/about-me.md` for the personal narrative; `Reference/Themes/` for L2 (active + archive in same folder); `Reference/Patterns/` for L3 snapshots; `Reference/Dailies/` for L4 session notes.
- **Wiki starter packs are part of Stage 2.** The client chooses up to 3; setup creates only those destinations and may import a small confirmed starting batch. Recurring sync and large historical imports remain Phase 2.
- **Morning-brief setup deferred** to a separate session (Phase 2 territory in onboarding flow).
- **L3 mechanism:** synthesize-then-paste. Both import (ChatGPT/Gemini export) and from-scratch interview supported.
- **No GitHub release-cut step** in this wizard — that's a coach-side action.
- **Structural questions are gated on capability level** (added 2026-08-30, from a live L1 run). Folder naming is jargon presented as a preference; an L1 client has no basis to answer it. L1–L2 get defaults plus a rename offer, L3+ get the interview.
- **Both `CLAUDE.md` and `AGENTS.md` are written for every client** (added 2026-08-30). Assume more than one tool. `CLAUDE.md` keeps the dlcOS runtime markers; `AGENTS.md` carries the vault map, preferences, and memory routing for everything else.
- **Memory-export triage is mandatory and non-silent** (added 2026-08-30). Exports routinely contain third-party clinical, legal, and end-of-life detail. Four buckets, per-category confirmation, nothing from buckets (b)/(c) in cloud-stored memory, per-item yes required for (c).
- **The coach-contact CTA is data, not a constant** (added 2026-08-30). Attribution stays required verbatim; the contact line comes from the `dlcOS:coach-contact` marker and must be true for this client.
- **START-HERE.md is the durable half of Stage 4b** (added 2026-08-30). A spoken walkthrough delivers nothing if the client isn't at the keyboard.

## 6. Success Criteria

- [ ] Stage 1 complete; client identity captured.
- [ ] `${VAULT_ROOT}` populated with the full layout from Stage 2.
- [ ] Client was offered the curated Wiki starter list; each selection has a destination + README (or client explicitly chose none).
- [ ] All 7 core skills respond; add-ons appear in the `/dlcOS` list.
- [ ] `Wiki/Knowledge/about-me.md` written, no placeholders.
- [ ] Settings → Memory resolved — pasted, skipped, or merged (all three count).
- [ ] Backup paste block at `Wiki/Knowledge/settings-memory-block.md`, carrying the attribution sentence and a *true* contact line.
- [ ] If a memory export was imported: triage ran, all four buckets confirmed with the client, no third-party or client-health content in the Settings block.
- [ ] `AGENTS.md` written alongside `CLAUDE.md`, both pointing at the same real paths.
- [ ] `START-HERE.md` written, with the client's real folders and a truthful unfinished list.
- [ ] Client can name the 4 memory layers *(L3+; for L1–L2 it's enough that they know where things go and how to reach the coach)*.
- [ ] One real plan saved + pointer in CLAUDE.md.
- [ ] Handoff doc in today's daily note.
- [ ] `Reference/dlcOS-setup-checklist.md` exists.
- [ ] Wizard completed in ≤45 minutes (record actual time in handoff doc).

## 7. Rollback / Safety

The wizard only writes inside `${VAULT_ROOT}` (which the client picked) and to Claude desktop Settings → Memory (which the client pastes manually).

- If the wizard stalls partway, the client's machine is in a partial state but nothing is broken — re-run `/dlcOS:setup` to resume from the failed stage.
- To undo entirely: `rm -rf ${VAULT_ROOT}` (after backing up anything they care about) and clear Claude desktop Memory.

## 8. References

- Templates source: `${TEMPLATES}` — resolves to `~/.claude/plugins/marketplaces/dlcOS/templates/` (canonical) or `<repo-root>/templates/` (dev checkout). **Never** the plugin install cache; it ships no `templates/` dir. Every bare `templates/<x>` reference in this plan means `${TEMPLATES}/<x>`.
- Memory architecture: `Wiki/Knowledge/Memory System.md` in the coach's reference vault (will be dropped to client vaults in Phase 2).
- Onboarding script source: `Projects/AI Coaching/onboarding-guide.md` § How Claude Remembers in the coach's reference vault.

## 9. Notes for the Executor

This is `mode: execute` — no critique pass. Run the stages in order. After each stage, run its Verify check. If a verify fails, stop and ask the client/coach for guidance — don't silently improvise.

Stage 4a is the most LLM-judgment-heavy step. The yes-path is essentially "synthesize a polished personal profile from messy memory dumps." Take the time. Have the client (and coach if present) review the synthesized `about-me.md` and Settings block before pasting anywhere.
