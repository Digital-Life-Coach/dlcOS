---
name: setup
description: Onboard a new dlcOS client end-to-end. Builds the vault scaffold, verifies the 6 dlcOS skills install correctly, synthesizes the client's L3 memory layer (about-me.md + Claude Settings → Memory paste block) from their ChatGPT/Gemini export OR a from-scratch interview, walks them through the 4-layer memory model, and runs a save-plan round-trip. Use when the user says "/dlcOS:setup", "set me up", "onboard me", "I'm new to dlcOS", or this is their first session with the plugin installed. Target run time ≤45 minutes; coach should be present.
---

# setup — dlcOS Onboarding Wizard

*Invoke as `/dlcOS:setup`*

This skill consumes the wizard plan at `<marketplace-root>/plans/dlc-setup.md` and walks a new client through onboarding. Plan is `mode: execute` so `/dlcOS:resume-plan` skips the critique pass and runs the stages directly.

---

## Step 0 — Resolve VAULT_ROOT (or accept that it doesn't exist yet)

Walk up from the current working directory to find the nearest `CLAUDE.md`. Grep for:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

**If found:** use that path as `${VAULT_ROOT}`. The client has run setup before — confirm with them whether they're re-running intentionally (e.g., disaster recovery) or whether `/dlcOS:setup` was invoked by mistake. If re-running, proceed; the wizard is idempotent and will re-build / overwrite as needed.

**If not found:** that's expected for a brand-new client. Stage 1 of the wizard will collect the vault root path; Stage 2 will write the marker into the new `CLAUDE.md`.

---

## Step 1 — Greet and frame

Tell the client:

> "Welcome to dlcOS. I'm going to walk you through onboarding — should take about 45 minutes. We'll build your vault, verify the skills work, set up your memory across all 4 layers, and end with a quick demo of the plan workflow. Your coach should be on the call with you for this."

Confirm:
- Coach is present (or client wants to proceed solo — note this).
- Client has Claude desktop installed alongside Claude Code.
- Client has a rough idea where they want their vault to live (e.g., `~/Documents/<name>-vault`).

If anything is missing, pause and tell them what to do before continuing.

---

## Step 2 — Locate the wizard plan

The wizard plan lives in the marketplace clone, not the plugin install cache. Find it at one of:

1. `~/.claude/plugins/marketplaces/dlcOS/plans/dlc-setup.md` — created when the client ran `/plugin marketplace add Digital-Life-Coach/dlcOS`. **This is the canonical path.**
2. If running from a development checkout: `<repo-root>/plans/dlc-setup.md`.

Use the marketplace path first; fall back to the repo path. If neither exists, the marketplace was never added — tell the client to run `/plugin marketplace add Digital-Life-Coach/dlcOS` (not just `/plugin install`) and try again.

Note: the plugin install cache (`~/.claude/plugins/cache/dlcOS/dlcOS/<version>/`) contains only the plugin subdirectory and does NOT include `plans/`. Don't look there.

---

## Step 3 — Copy plan to client vault and create pointer

Once `${VAULT_ROOT}` is established (which may not happen until Stage 1 of the wizard runs and Stage 2 creates the CLAUDE.md marker), copy the wizard plan to the client's vault:

```
cp ~/.claude/plugins/marketplaces/dlcOS/plans/dlc-setup.md ${VAULT_ROOT}/Reference/Plans/dlcOS-setup.md
```

Add a line under `## Pending Plans` in `${VAULT_ROOT}/CLAUDE.md`:

```
- [`dlcOS-setup`](Reference/Plans/dlcOS-setup.md) — onboarding wizard, in-progress
```

This keeps the wizard re-resumable: if the session ends partway, the client (or coach) can run `/dlcOS:resume-plan dlcOS-setup` in a fresh session and continue from where they left off.

**Note:** for a brand-new client, `${VAULT_ROOT}` and `Reference/Plans/` may not exist when this skill first invokes. Sequence the copy AFTER Stage 2 of the wizard creates the directory structure. In practice: hold off on the copy until Stage 2 verify passes, then copy + create pointer.

---

## Step 4 — Hand off to the wizard plan

Read `${VAULT_ROOT}/Reference/Plans/dlcOS-setup.md` (or the plugin-install copy if Stage 2 hasn't run yet) and execute its stages in order. The plan is `mode: execute` — no critique pass needed.

After each stage:
- Run the stage's Verify check.
- Mark the stage complete in the plan file (append `> Done <timestamp> — <note>` under the stage).
- If a verify fails, STOP. Don't silently improvise. Tell the coach what failed and ask how to proceed.

---

## Step 5 — Close out

When all 6 stages pass:

1. Update plan frontmatter: `status: complete`, `completed: <timestamp>`.
2. Append an `## Outcome` section summarizing what shipped, total wizard runtime, any oddities.
3. Remove the pointer from `${VAULT_ROOT}/CLAUDE.md` `## Pending Plans`.
4. Move the plan file to `${VAULT_ROOT}/Reference/Plans/archive/dlcOS-setup.md`.
5. Tell the client + coach: "You're set up. Run `/dlcOS:morning-brief --setup` when you're ready to configure your daily brief — but not today."

---

## What This Skill Does NOT Do (v1)

- **Wiki scaffolding beyond `Wiki/Knowledge/about-me.md`** — Phase 2 owns Meetings/, Mindsera/, Clients/ and the Granola + email ingests.
- **Morning-brief setup** — deferred to a follow-up session. Wizard mentions it in Stage 6 handoff.
- **Scheduled actions (cron/launchd)** — Phase 2.
- **Claude desktop Settings → Memory automation** — there's no API. The wizard outputs a paste block; the client manually pastes it into Settings.
- **Critique the plan each run** — `mode: execute` skips the critique. The plan content was reviewed at build time.
- **Re-install the dlcOS plugin** — the client must already have run `/plugin marketplace add Digital-Life-Coach/dlcOS` and `/plugin install dlcOS@dlcOS` before invoking `/dlcOS:setup`.
