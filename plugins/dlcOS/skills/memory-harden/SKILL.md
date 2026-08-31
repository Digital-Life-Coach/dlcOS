---
name: memory-harden
description: Make Claude Code's hidden local memory folder visible inside the vault and lock it against new shard files. Symlinks the client's `~/.claude/projects/<project>/memory/` directory into `${VAULT_ROOT}/Reference/Memory/` (real files live in the vault, git-trackable and Obsidian-readable) and chmods the folder read-only so Claude can still edit `MEMORY.md` in place but can never silently create a new fragment file there. Use when the user says "/dlcOS:memory-harden", "set up my memory system", "I want to see what Claude is remembering", "stop it from making random memory files", or as a first-week follow-up for any client who wants to control what agents keep as context. Safe to run once, safe to re-run (idempotent), safe on both brand-new and already-onboarded vaults.
---

# /dlcOS:memory-harden — Memory Visibility + Shard Lockdown

*Invoke as `/dlcOS:memory-harden`*

## Why this exists

Claude Code keeps a local memory folder per project at `~/.claude/projects/<sanitized-cwd>/memory/`. It's outside the vault, inside a dot-directory, invisible in Finder and Obsidian by default. Left alone, Claude can create new files there any time it decides something is worth remembering — and with no visibility or friction, that habit fragments into duplicate/stale shard files over time (this happened to the coach's own vault: 23 duplicated/stale files by the time anyone noticed). Clients like Ted specifically want to see and control what an agent keeps as durable context. This skill fixes both problems at once with two operations:

1. **Symlink the whole `memory/` directory into the vault**, not just `MEMORY.md`. The real folder lives at `${VAULT_ROOT}/Reference/Memory/`; the hidden path becomes a symlink to it. Anything Claude writes there is now a plain file the client can see in Obsidian, edit, or delete.
2. **Lock the vault-side folder read-only (`chmod 555`)** once `MEMORY.md` exists in it. On macOS/APFS, editing or fully overwriting an *existing* file only needs write permission on the file itself — confirmed empirically (coach session, 2026-08-18): `Edit` and `Write` both succeed in-place on an existing file inside a `555` directory (same inode, no rename). Creating a *new* file needs write permission on the *directory* and fails with `EACCES` once locked. So `MEMORY.md` stays fully editable forever, and no sibling shard file can ever be created next to it — without any hook, script, or justification workflow the client would have to understand.

This is filesystem-level prevention, not a policy the agent has to remember to follow. It works even for a client whose `CLAUDE.md` says nothing about memory routing.

**Note for the coach's own vault:** `Wiki/Knowledge/Memory System.md` already flags the directory-level symlink as unfinished hardening for the coach's own setup ("Not yet done"). This skill is scoped to dlcOS *clients* — do not run it against the coach's own vault without a separate decision, since the coach's memory folder legitimately holds many shard files by design (`feedback_*.md`, `project_*.md`, etc.) that a lockdown would freeze in place.

---

## Step 0 — Resolve VAULT_ROOT

Same technique as `/dlcOS:setup` Step 0: walk up from cwd to the nearest `CLAUDE.md` **or `AGENTS.md`**, grep for:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

If not found, ask the client where their vault lives, or tell them to run `/dlcOS:setup` first — this skill assumes a vault already exists.

---

## Step 1 — Locate the live project memory directory

Don't guess the sanitized-path transform (it's not a simple `/`→`-` substitution — other characters get folded too, e.g. `justin+brain` → `justin-brain`). Instead, find it by matching the actual cwd against the current session's own transcript, which is 100% reliable regardless of what characters are in the vault path:

```bash
PROJECT_DIR=$(grep -l "\"cwd\":\"${VAULT_ROOT}\"" ~/.claude/projects/*/*.jsonl 2>/dev/null | head -1 | xargs dirname)
```

If this comes up empty, the running session's cwd isn't exactly `${VAULT_ROOT}` (e.g. it's a subdirectory) — retry the grep against the actual cwd reported by the environment, then confirm with the client that this matches their vault root before continuing.

**Verify:** `${PROJECT_DIR}` is a real directory and contains (or will contain) a `memory/` subdirectory.

---

## Step 2 — Idempotency check

```bash
if [ -L "${PROJECT_DIR}/memory" ]; then
  # already a symlink — check where it points
  readlink "${PROJECT_DIR}/memory"
fi
```

- **Points at `${VAULT_ROOT}/Reference/Memory`:** already hardened by this skill on a prior run. Check the lock state (`stat -f "%Sp" "${VAULT_ROOT}/Reference/Memory"` should show no `w` bits beyond owner-read). If locked, tell the client it's already set up and stop. If unlocked (someone ran `chmod` to add a shard manually), ask whether to relock now.
- **Points somewhere else:** stop. Something else set this up — don't overwrite without asking the client what's there.
- **Not a symlink (normal case, first run):** continue to Step 3.

---

## Step 3 — Move existing content into the vault

```bash
mkdir -p "${VAULT_ROOT}/Reference/Memory"
```

If `${PROJECT_DIR}/memory/` already has files in it (MEMORY.md from onboarding, or anything Claude has already written this week — expected for a client hardening an existing vault, e.g. mid-tenure clients, not just brand-new ones), move them over rather than discarding:

```bash
# only if the source dir exists and has content
mv "${PROJECT_DIR}/memory/"* "${VAULT_ROOT}/Reference/Memory/" 2>/dev/null
```

If `${VAULT_ROOT}/Reference/Memory/MEMORY.md` still doesn't exist after that move (truly fresh vault, nothing written yet), create a starter file so Claude Code has somewhere to write on its first memory save, and so the folder isn't empty when it gets locked in Step 5:

```markdown
# Claude's Local Memory Index

This is Claude Code's own built-in memory file for this vault — separate from your primary memory setup (Settings → Memory + `Wiki/Knowledge/about-me.md`, built during onboarding).

You can read, edit, or clear anything here any time. This folder is locked read-only on purpose (see `Reference/Memory/README.md`) so Claude can update this file but can't quietly create new ones next to it.
```

Write that to `${VAULT_ROOT}/Reference/Memory/MEMORY.md` (only if it doesn't already exist — never overwrite real content).

Also write `${VAULT_ROOT}/Reference/Memory/README.md`:

```markdown
# Reference/Memory/

This folder is Claude Code's local memory directory for this vault, made visible here (it's normally hidden in `~/.claude/`) and symlinked back so Claude reads/writes it in exactly the same place it always did.

**It's locked read-only** (`chmod 555`) so Claude can keep editing `MEMORY.md` but can't create new files here without you knowing. If you (or your coach) ever want to intentionally add something, unlock it first:

    chmod 755 "Reference/Memory"

...make the change, then relock:

    chmod 555 "Reference/Memory"

This is separate from your primary L3 memory — see `Wiki/Knowledge/about-me.md` and Claude desktop's Settings → Memory. Set up by `/dlcOS:memory-harden`.
```

If `${VAULT_ROOT}` is a git repo, mention to the client that this folder is now vault content and worth committing along with the rest of their setup — don't run a commit yourself unless that's already their established workflow.

---

## Step 4 — Swap in the symlink

```bash
rm -rf "${PROJECT_DIR}/memory"   # now empty/redundant — content already moved in Step 3
ln -s "${VAULT_ROOT}/Reference/Memory" "${PROJECT_DIR}/memory"
```

**Verify before locking:**
- `test -L "${PROJECT_DIR}/memory"` is true
- `readlink "${PROJECT_DIR}/memory"` equals `${VAULT_ROOT}/Reference/Memory`
- `test -f "${VAULT_ROOT}/Reference/Memory/MEMORY.md"` is true

If any of these fail, stop — don't proceed to locking a folder that isn't correctly wired yet.

---

## Step 5 — Lock the folder

```bash
chmod 555 "${VAULT_ROOT}/Reference/Memory"
```

**Verify the lock actually holds** — don't just trust the chmod exit code. Try to write a real throwaway file into it and confirm it's rejected:

```bash
touch "${VAULT_ROOT}/Reference/Memory/.memory-harden-lock-test" 2>&1
```

Expect a `Permission denied` failure. If the write *succeeds*, the lock didn't take (e.g. running as an account with elevated permissions bypassing it) — delete the test file, tell the client the lockdown could not be verified, and don't report success.

Then confirm `MEMORY.md` is still editable through the normal tool path (an `Edit` or `Write` call on `${VAULT_ROOT}/Reference/Memory/MEMORY.md` should still succeed) — this is the whole point of using `chmod 555` over something stricter, so don't skip this check.

---

## Step 6 — Report

Tell the client, plainly:

> "Claude's local memory file now lives at `Reference/Memory/MEMORY.md` in your vault — you can open it in Obsidian any time to see exactly what it's kept, and edit or clear it yourself. The folder's locked so Claude can update that one file but can't quietly create new ones next to it."

Point out where the README lives if they ever want the manual unlock/relock steps.

---

## What this does NOT do

- Doesn't touch Settings → Memory or `about-me.md` — those remain the client's primary L3 memory, untouched by this skill.
- Doesn't run on the coach's own vault (see the note in Step 0's preamble) — that memory folder is designed around many shard files and a separate route-check hook already governs it.
- Doesn't delete or rewrite any existing shard file content found during Step 3 — legacy shards (if any exist on a mid-tenure client) move into the vault and stay fully readable/editable; the lock only prevents *new* ones going forward.
- Doesn't wire itself into `/dlcOS:setup` automatically — it's a standalone, separately-invoked skill for now.
