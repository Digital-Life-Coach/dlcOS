---
name: memory-harden
description: Set up the vault's canonical memory system and make Claude Code's hidden memory folder visible inside it. Seeds the six canonical memory files in `${VAULT_ROOT}/Wiki/Knowledge/` (me, voice, preferences, assistant, decisions, environment), writes the routing hub at `Wiki/Knowledge/Memory/MEMORY.md`, symlinks `~/.claude/projects/<project>/memory/` to that folder so shards land in the vault as plain markdown, and wires `AGENTS.md` to point every tool at the same rules. Use when the user says "/dlcOS:memory-harden", "set up my memory system", "I want to see what Claude is remembering", "stop it from scattering the same fact everywhere", or as a first-week follow-up for any client. Safe to run once, safe to re-run (idempotent), and it migrates vaults set up by earlier versions that used `Reference/Memory/`.
---

# /dlcOS:memory-harden — Canonical Memory + Visible Shards

*Invoke as `/dlcOS:memory-harden`*

## Why this exists

**The failure mode is duplication, not sprawl.** Observed in a live client vault: the same communication-style rule was written three times — in `AGENTS.md`, in `Wiki/Knowledge/me.md`, and in a memory shard — in a vault whose own rules said *one home per fact*. Nothing had gone wrong mechanically. There was simply no rule saying *which file wins*, so every agent that learned the fact wrote it wherever it happened to be looking.

An earlier version of this skill attacked a different problem — Claude creating too many shard files — by `chmod 555`-ing the memory folder. That was the wrong lever, for three reasons found in the field:

1. **It freezes deletes as well as adds.** `unlink` needs write permission on the directory, so a memory that turns out to be wrong can only be blanked, never removed.
2. **Its documented unlock needs a command line.** The README told the client to `chmod 755`, edit, then `chmod 555`. Most dlcOS clients don't use a terminal, so the one operation described as theirs was in practice only available to the coach.
3. **It pushed writes somewhere worse.** With new files blocked, the only writable target left was `MEMORY.md` itself, which then accumulated the content the shards were supposed to hold.

So this version keeps the half that worked and drops the half that didn't:

- **Keep the symlink.** Visibility was the real win — shards become plain markdown in the vault, readable in Obsidian, editable and deletable by the client.
- **Drop the lock.** The folder stays writable. Sprawl is bounded by a *routing rule* instead of a permission bit.
- **Add canonical files.** Six named files with one subject each, so most durable facts have an obvious home and a shard is the exception rather than the default.
- **Put the rule where every tool reads it.** In `AGENTS.md`, not `CLAUDE.md` — see Step 6.

**Harness neutrality is a requirement, not a nice-to-have.** Claude Code auto-loads `MEMORY.md` because that folder is its memory directory. Codex, ChatGPT and everything else will never see it unless `AGENTS.md` tells them to open it explicitly. A memory system only one harness can read is not a memory system — it's a Claude feature. Design for the client's *actual* agent, which on a Codex-remote-control box is not Claude.

---

## Step 0 — Resolve VAULT_ROOT

Same technique as `/dlcOS:setup` Step 0: walk up from cwd to the nearest `CLAUDE.md`, grep for:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

If not found, ask the client where their vault lives, or tell them to run `/dlcOS:setup` first — this skill assumes a vault already exists.

**Do not run this against the coach's own vault** without a separate decision. That vault legitimately holds many purpose-built shard files whose conventions predate this skill.

---

## Step 1 — Locate the live project memory directory

Don't guess the sanitized-path transform (it's not a simple `/`→`-` substitution — other characters get folded too, e.g. `justin+brain` → `justin-brain`). Find it by matching the actual cwd against the current session's own transcript:

```bash
PROJECT_DIR=$(grep -l "\"cwd\":\"${VAULT_ROOT}\"" ~/.claude/projects/*/*.jsonl 2>/dev/null | head -1 | xargs dirname)
```

If this comes up empty, the running session's cwd isn't exactly `${VAULT_ROOT}` (e.g. it's a subdirectory) — retry against the actual cwd reported by the environment, then confirm with the client before continuing.

---

## Step 2 — Idempotency and migration check

```bash
if [ -L "${PROJECT_DIR}/memory" ]; then readlink "${PROJECT_DIR}/memory"; fi
```

- **Points at `${VAULT_ROOT}/Wiki/Knowledge/Memory`:** already on the current layout. Skip to Step 3 and treat everything as a top-up — seed only what's missing, never overwrite.
- **Points at `${VAULT_ROOT}/Reference/Memory`:** set up by an earlier version. **Migrate** — see below.
- **Points somewhere else:** stop. Something else set this up; ask the client what's there.
- **Not a symlink (normal first run):** continue to Step 3.

### Migrating from `Reference/Memory/`

The old location was locked, so unlock it before moving anything:

```bash
chmod 755 "${VAULT_ROOT}/Reference/Memory"
mkdir -p "${VAULT_ROOT}/Wiki/Knowledge/Memory"
mv "${VAULT_ROOT}/Reference/Memory/"* "${VAULT_ROOT}/Wiki/Knowledge/Memory/" 2>/dev/null
rmdir "${VAULT_ROOT}/Reference/Memory" 2>/dev/null
```

The old `README.md` in that folder describes the lock and is now wrong — delete it; Step 4 writes a correct one. Existing shards move across untouched. Tell the client the folder moved and why, and check for links to the old path elsewhere in the vault before finishing.

---

## Step 3 — Seed the canonical files

The six canonical files live in `${VAULT_ROOT}/Wiki/Knowledge/`. Full versions are in the plugin's `templates/` directory — copy each one that is **missing**, and never overwrite a file that already has content.

| File | Subject | Answers |
|---|---|---|
| `me.md` | the person | Who am I? |
| `voice.md` | my output | How do I sound when I write? |
| `preferences.md` | the work | How should work be done for me? |
| `assistant.md` | the assistant | How should you behave? |
| `decisions.md` | the past | What's settled, and why? |
| `environment.md` | the machines | What runs where? |

The boundaries are about **subject**, not topic, and that distinction is the whole design. "I want short answers" is the *work*. "Never patronise me" is the *assistant*. "I'm a singer" is the *person*. Three communication-adjacent rules, three different files, no overlap. If you can't name the subject a fact belongs to, it probably doesn't need writing down.

**Two collisions to check for before copying:**

- **`me.md` already exists.** That's the pre-v2 name for `me.md`. Rename it (`git mv` if the vault is a repo), then grep the vault for links to the old name and fix them.
- **`preferences.md` already exists with different content.** Some vaults used this name for personal tastes — food, TV, products. That is *not* this file's subject. Ask the client which they want: move the taste content into `me.md`, or keep it as a separate `tastes.md`. Don't silently merge them.

---

## Step 4 — Write the memory hub

```bash
mkdir -p "${VAULT_ROOT}/Wiki/Knowledge/Memory"
```

Write `${VAULT_ROOT}/Wiki/Knowledge/Memory/MEMORY.md` from the plugin's `templates/MEMORY.md` — **only if it doesn't exist**. If it does, merge: keep every existing index line, add the routing rule and canonical-files table above it.

The parts that must survive any edit:

1. A line stating this file is a **required read before writing anything durable**, and that non-Claude tools must open it themselves.
2. The three-step routing rule — canonical file first, shard if nothing fits, update-don't-duplicate if it already exists.
3. The canonical files table.
4. The shard frontmatter schema.
5. The index.

Also write `${VAULT_ROOT}/Wiki/Knowledge/Memory/README.md`:

```markdown
# Wiki/Knowledge/Memory/

This folder is Claude Code's memory directory for this vault, made visible here (it's normally hidden away in `~/.claude/`) and symlinked back so Claude reads and writes in exactly the same place it always did.

Everything in it is a plain markdown file. Read it, edit it, delete anything you don't want kept — it's yours.

`MEMORY.md` is the hub: it holds the rule for where durable facts go, and an index of the shard files in this folder. The canonical memory files it points to live one level up in `Wiki/Knowledge/`.

This folder is deliberately **not** locked. An earlier version made it read-only to stop new files appearing; that also blocked deleting the wrong ones, and needed a terminal to undo. Visibility does the job better than a permission bit.

Set up by `/dlcOS:memory-harden`.
```

---

## Step 5 — Swap in the symlink

```bash
rm -rf "${PROJECT_DIR}/memory"   # content already moved
ln -s "${VAULT_ROOT}/Wiki/Knowledge/Memory" "${PROJECT_DIR}/memory"
```

**Verify:**
- `test -L "${PROJECT_DIR}/memory"` is true
- `readlink "${PROJECT_DIR}/memory"` equals `${VAULT_ROOT}/Wiki/Knowledge/Memory`
- `test -f "${VAULT_ROOT}/Wiki/Knowledge/Memory/MEMORY.md"` is true

---

## Step 6 — Wire AGENTS.md (do not skip)

**This is the step that makes the system work for anything other than Claude.**

`${VAULT_ROOT}/AGENTS.md` must contain a memory section naming `Wiki/Knowledge/Memory/MEMORY.md` as a required read, plus the three-step routing rule in short form. The plugin's `templates/agents-md-starter.md` has the block to use.

If `AGENTS.md` doesn't exist, create it from that template and make sure `CLAUDE.md` imports it with `@AGENTS.md` — see `templates/claude-md-starter.md`.

**Then check for duplication, because this is where it starts.** If `AGENTS.md` already describes tone and conduct inline, that content now belongs in `assistant.md`. Move it and leave a link. A summary in one file and the real rules in another will drift, and then nobody knows which is current. Link, don't copy.

---

## Step 7 — Verify

The write test is the **opposite** of the old version's. Creating a file here must now **succeed**:

```bash
touch "${VAULT_ROOT}/Wiki/Knowledge/Memory/.probe" && rm "${VAULT_ROOT}/Wiki/Knowledge/Memory/.probe" && echo OK
```

If it fails, a stale `chmod 555` survived the migration — `chmod 755` the folder and re-test.

Then confirm the routing rule actually resolves: pick one fact already written in the vault, and check it appears in exactly one canonical file. If it appears in two, you've found live duplication — fix it now, with the client, and it becomes the worked example that teaches them the system.

---

## Step 8 — Report

Tell the client, plainly:

> "Your memory now lives in six named files in `Wiki/Knowledge/` — one for you, one for your voice, one for how you want work done, one for how the assistant should behave, one for decisions you've already made, and one for your machines. `Wiki/Knowledge/Memory/MEMORY.md` is the index that tells any AI which file a new fact belongs in. Anything that doesn't fit becomes its own small file in that folder, and you can read or delete any of it in Obsidian."

Say explicitly that the rules live in `AGENTS.md`, so Codex and ChatGPT follow them too — not just Claude.

---

## What this does NOT do

- **Doesn't lock anything.** Earlier versions did; see *Why this exists* for why that was removed.
- **Doesn't fill the canonical files in.** It seeds the structure. `/dlcOS:setup` Stage 4a and `/dlcOS:monthly-review` populate and maintain the content.
- **Doesn't touch `Reference/Themes/`** — `/dlcOS:monthly-review` owns L2.
- **Doesn't overwrite existing content, ever.** Every write in Steps 3 and 4 is create-if-missing or merge.
- **Doesn't run on the coach's own vault** — see Step 0.
