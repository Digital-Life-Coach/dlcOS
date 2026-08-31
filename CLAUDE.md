# CLAUDE.md — dlcOS

## What dlcOS is (core components, clarified 2026-07-05)

dlcOS is a combo of three components:

1. **Splashtop Streamer** — remote access/support channel
2. **Support App** — client-side helper app
3. **The skills repo** — this one: vault scaffold, skills (weekly-review, morning-brief, draft, end, save/resume-plan, vault-lint/sweep, promote-lessons, setup), agents, templates. Ships for **both Claude Code and Codex** as of v2.2.0.

*(Moved from GTD/TASKS.md 2026-07-21 — was the "dlcOS core components clarified" HQ Dashboard note.)*

## Related

- Collaborators: justinsail, jimdamico, templetongroup (Tony), gabesterr, charlieShepard
- Plugin manifests: `plugins/dlcOS/.claude-plugin/plugin.json` (Claude Code) **and** `plugins/dlcOS/.codex-plugin/plugin.json` (Codex)
- Marketplaces: `.claude-plugin/marketplace.json` (Claude Code) **and** `.agents/plugins/marketplace.json` (Codex)

## ⚠️ Dual-harness packaging — keep the two manifests in lockstep

**AI-agnostic is the principle: the vault is the product, the model is switchable.** The same `skills/` directory serves both harnesses; only the packaging differs.

| | Claude Code | Codex |
|---|---|---|
| marketplace | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` |
| manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` |
| `source` in marketplace | string (`"./plugins/dlcOS"`) | **object** (`{"source":"local","path":"./plugins/dlcOS"}`) |
| skills field | `"skills": "./skills/"` | identical |
| `SKILL.md` frontmatter | `name` + `description` | identical |
| subagents | `"agents": [...]`, auto-discovered as `dlcOS:<name>` | **subagents exist** (`spawn_agent`, `features.multi_agent`), but there is **no named-agent registry** — the `agents` field is ignored. Hand the agent file's contents to `spawn_agent` instead. |

**Every version bump must touch BOTH manifests.** There's no shared source; they drift silently, and a stale Codex version installs the wrong number with no error. Check with:

```bash
grep -h '"version"' plugins/dlcOS/.claude-plugin/plugin.json plugins/dlcOS/.codex-plugin/plugin.json
```

**Validate both before release.** Codex ships its own authoritative validator — use it, don't eyeball the manifest:

```bash
claude plugin validate plugins/dlcOS
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/dlcOS
codex plugin marketplace add . && codex plugin add dlcOS@dlcOS && codex plugin list | grep dlcOS@
```

⚠️ **`codex plugin add` succeeding does NOT mean the manifest is valid.** The v2.2.0 manifest installed and enabled cleanly while missing a required field (`interface.defaultPrompt`) — the official validator caught it, the install path didn't. Same shape as the npm-vs-native remote-control bug: the happy path reports success and the defect surfaces somewhere else later.

Codex's `plugin-creator` skill (`~/.codex/skills/.system/plugin-creator/`) is the schema source of truth. Required in `interface`: `displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `capabilities` (array), and `defaultPrompt`. Top-level keys are allow-listed — an unknown key is a hard error.

**What doesn't port, and shouldn't be papered over:** the *named agent registry*. Codex has real subagents — `spawn_agent`, hierarchical task names, inter-agent messaging, `SubagentStart`/`SubagentStop` hooks, `features.multi_agent` stable and on by default — but they're anonymous and inherit the parent's tools, defined by the task you hand them rather than by a persona file the harness discovered. So `subagent_type: dlcOS:drafter` has no equivalent; passing `agents/drafter.md` to `spawn_agent` does.

The three agent-using skills carry a three-way harness note (Claude `subagent_type` → Codex `spawn_agent` + agent file → inline). **Don't write a skill that *requires* a named subagent without that ladder.**

Genuinely Claude-only in practice: the librarian/drafter **companion-memory loop** (`/dlcOS:promote-lessons` writing `~/.claude/agents/<name>-learned.md`), because it depends on a persistent named agent identity to attach lessons to. If that matters on Codex, it needs a different home — a vault file the spawn prompt reads, not a harness path.

⚠️ **Verify before asserting a capability gap.** The claim "Codex has no subagents" was made here on 2026-08-31 from weak evidence (no `agents/` dir in bundled plugins) and was wrong — `codex features list | grep multi_agent` and `strings` on the real binary both showed otherwise. The `codex` on PATH may be a cmux shim; the real binary is under the npm global prefix or `~/.codex/packages/standalone/`.
- Client-facing docs: `docs/client-quickstart.md`, `docs/skills-reference.md`, `docs/troubleshooting.md`
