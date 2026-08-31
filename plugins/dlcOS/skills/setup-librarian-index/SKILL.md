---
name: setup-librarian-index
description: "Optional add-on. Provision a local semantic-search index over the vault so the `dlcOS:librarian` agent upgrades from keyword-grep mode to ranked semantic search. Installs the agent-library MCP server, builds the initial index, wires a daily re-index job, and writes the `dlcOS:librarian-index` marker. Use when the user says /dlcOS:setup-librarian-index, 'set up semantic search', 'make librarian smarter', or picks up the librarian-index add-on from Pending Plans. Technical add-on — needs a working `uv` (or pip) toolchain; not part of base setup."
---

# /dlcOS:setup-librarian-index — Provision Semantic Search (optional add-on)

Without an index, the `dlcOS:librarian` agent runs in **keyword mode** (grep + light synthesis, confidence capped at medium). This add-on installs a local semantic index so librarian runs in **semantic mode** (ranked hybrid retrieval, higher-confidence synthesis). Everything stays local — no vault content leaves the machine.

This is a technical add-on. If the user isn't comfortable with a terminal, offer to do it together on a screen-share, or skip it — librarian works fine in keyword mode.

## Step 0 — Resolve VAULT_ROOT

Read the `<!-- dlcOS:vault-root -->` marker in the project `CLAUDE.md` **or `AGENTS.md`** — check both, since a Codex-driven vault may only carry `AGENTS.md`. Take the absolute path after it as `VAULT_ROOT`. If neither has the marker, stop and tell the user to run `/dlcOS:setup` first.

## Step 1 — Check prerequisites

```bash
command -v uv || echo "no uv"      # preferred installer
command -v python3 || echo "no python3"
```

- If `uv` is present, use it (Step 2a).
- If only `pip`/`python3` is present, use pip (Step 2b).
- If neither, stop: tell the user they need Python 3 + `uv` (recommend `uv` — https://docs.astral.sh/uv/) before this add-on can run. Don't try to install a toolchain for them.

## Step 2 — Install the agent-library CLI + MCP server

**2a (uv — preferred):**
```bash
uv tool install agent-library      # core only; the markdown index needs no torch/vision extras
```

**2b (pip fallback):**
```bash
python3 -m pip install --user agent-library
```

Verify: `libr --help` runs.

## Step 3 — Build the initial index

```bash
libr add "$VAULT_ROOT" --name vault     # adds + indexes; re-running picks up changed files (mtime-based)
libr list                               # confirm the `vault` source is registered
```

Note for the user: the index DB lives at `~/.librarian/index.db` (outside the vault, not in git). Size scales with vault size. The first build can take a few minutes; subsequent re-indexes are incremental.

## Step 4 — Wire the MCP server into this project

The librarian agent reaches the index through the `agent-library` MCP server. Add it at project scope so it only runs in this vault. Create or update `${VAULT_ROOT}/.mcp.json`:

```json
{
  "mcpServers": {
    "agent-library": { "command": "libr", "args": ["serve", "stdio"] }
  }
}
```

If `.mcp.json` already exists, merge the `agent-library` entry into the existing `mcpServers` object rather than overwriting. After writing it, the MCP server loads on the next session start in this vault. The user must approve the new MCP server when prompted.

## Step 5 — Schedule daily re-indexing

There's no filesystem watcher — the index only refreshes when `libr add` re-runs. Schedule a daily job so recall stays current (up to ~24h staleness between runs is expected and fine).

**macOS (launchd)** — write `~/Library/LaunchAgents/com.dlcos.librarian-reindex.plist` running daily, e.g. at 3:30 AM:
```
libr add "$VAULT_ROOT" --name vault
```
Load it: `launchctl load ~/Library/LaunchAgents/com.dlcos.librarian-reindex.plist`

**Linux (cron)** — add a crontab line:
```
30 3 * * *  libr add "<VAULT_ROOT>" --name vault >> ~/.cache/dlcos/librarian-reindex.log 2>&1
```

Adapt the exact mechanism to the user's OS; the job is just a daily `libr add "$VAULT_ROOT" --name vault`.

## Step 6 — Write the marker

Add the marker to the project `CLAUDE.md` (near the other `dlcOS:` markers) so the librarian agent knows the index exists and switches to semantic mode:

```
<!-- dlcOS:librarian-index -->  (semantic index provisioned; librarian uses ranked search. Delete this line to force keyword-only mode.)
```

Also remove the `setup-librarian-index` line from the `<!-- dlcOS:addons-start -->` block in CLAUDE.md so it stops appearing as a pending add-on.

## Step 7 — Verify

1. Start a fresh session in the vault (so the MCP server loads).
2. Ask librarian a conceptual question about something in the vault.
3. Confirm its Notes block reports `mode: semantic` (not keyword) and that it cited real files.

If it still reports keyword mode: check that the `agent-library` MCP server actually loaded (was it approved?), that `libr list` shows the `vault` source, and that the `dlcOS:librarian-index` marker is present in CLAUDE.md.

## Gotchas (worth telling the user)

- **Pre-1.0 tool; treat the DB as disposable.** On a major `libr` upgrade, the safest reset is `libr index clobber && libr add "$VAULT_ROOT" --name vault`.
- **Deletions linger.** `libr add` doesn't purge deleted files from the index; a periodic full rebuild clears them.
- **Recent edits (<24h) may not be indexed yet** between cron runs — that's expected; librarian's keyword pass and the parent's own grep cover the fresh stuff.

## What this skill does NOT do

- ❌ Install a Python toolchain for the user (they bring `uv`/`pip`).
- ❌ Send any vault content anywhere — the index is fully local.
- ❌ Make librarian mandatory — keyword mode remains the default and works without this add-on.
