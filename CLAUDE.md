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
| subagents | `"agents": [...]`, auto-discovered | **no equivalent** — field is ignored |

**Every version bump must touch BOTH manifests.** There's no shared source; they drift silently, and a stale Codex version installs the wrong number with no error. Check with:

```bash
grep -h '"version"' plugins/dlcOS/.claude-plugin/plugin.json plugins/dlcOS/.codex-plugin/plugin.json
```

**Validate both before release:**
```bash
claude plugin validate plugins/dlcOS
codex plugin marketplace add . && codex plugin add dlcOS@dlcOS && codex plugin list | grep dlcOS@
```

**What doesn't port, and shouldn't be papered over:** Codex has no subagent mechanism. The four agents don't auto-load there, and the librarian/drafter companion-memory loop (`/dlcOS:promote-lessons`) is Claude-only in practice. The three skills that spawn agents carry inline fallbacks — the agent markdown ships in the Codex plugin cache too, so "read the agent file and do it inline" is a real instruction, not a shrug. Don't write a skill that *requires* a subagent without a fallback.
- Client-facing docs: `docs/client-quickstart.md`, `docs/skills-reference.md`, `docs/troubleshooting.md`
