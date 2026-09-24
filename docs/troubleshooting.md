# Troubleshooting

Things that go wrong, and how to fix them. If none of these match, email Justin at **justin@maccog.com** or book time at **support.maccog.com**.

---

## "I ran `/plugin install` but the dlcOS skills don't show up"

You probably skipped the marketplace step. Both commands are required:

```
/plugin marketplace add Digital-Life-Coach/dlcOS
/plugin install dlcOS@dlcOS
```

Run `/plugin list` after — you should see `dlcOS` listed. If you do but the skills still don't appear, run:

```
/reload-plugins
```

Then try `/dlcOS:` again. The slash menu should populate.

---

## "`/plugin marketplace add` fails with `xcode-select: note: No developer tools were found`"

macOS only, on a machine that has never had git installed. `/plugin marketplace add` clones the repo, and there is no git binary to do that with.

Run:

```
xcode-select --install
```

A GUI dialog pops up — accept it and let it finish (a few minutes, needs internet). Ignore the `sudo xcode-select --switch path/to/Xcode.app` line the error suggests; that command points at an *existing* Xcode install at a nonstandard path, which doesn't apply here — you have no Xcode/CLT install at all yet. Once the installer finishes, retry:

```
/plugin marketplace add Digital-Life-Coach/dlcOS
```

You only need the small Command Line Tools package this installs, not the full Xcode app.

---

## "`/dlcOS:setup` says it can't find the wizard plan"

**Claude Code:** the wizard plan lives at `~/.claude/plugins/marketplaces/dlcOS/plans/dlc-setup.md`. That path only exists if you ran `/plugin marketplace add Digital-Life-Coach/dlcOS` (not just `/plugin install`).

Check it with:

```
ls ~/.claude/plugins/marketplaces/dlcOS/plans/dlc-setup.md
```

If the file is missing, re-run the marketplace add command. If it exists but the skill still can't find it, run `/reload-plugins` and try again.

**Codex:** on a normal install (added from the GitHub URL), the marketplace clone lives at:

```
ls ~/.codex/.tmp/marketplaces/dlcOS/plans/dlc-setup.md
```

If your registration uses a local path instead (a dev checkout), the `source` line under `[marketplaces.dlcOS]` in `~/.codex/config.toml` points at the marketplace root:

```
awk '/^\[marketplaces\.dlcOS\]/{f=1;next} /^\[/{f=0} f' ~/.codex/config.toml
```

If `[marketplaces.dlcOS]` isn't in `~/.codex/config.toml` at all, re-run `codex plugin marketplace add https://github.com/Digital-Life-Coach/dlcOS`.

---

## "Every dlcOS command shows up twice in Codex"

**Cause pinned 2026-09-06: it's a Codex iOS app display bug, not an install problem.** The same machine, same session state, shows each skill once in the Mac app and twice in the iOS app's slash-command autocomplete. Codex's `skills/list` API (codex 0.151.0, `forceReload: true`) returns each skill exactly once, resolved to the plugin cache copy — the Mac client deduplicates at presentation, the iOS client does not. Nothing to fix locally; either listed entry runs the same skill. Workarounds: force-quit and reopen the iOS app; report to OpenAI as "Codex iOS displays every skill in a git-installed plugin twice; Mac shows each once."

Background you still need: a git-sourced marketplace add leaves a full staging clone at `~/.codex/.tmp/marketplaces/dlcOS/`, and installing the plugin copies it again to `~/.codex/plugins/cache/dlcOS/dlcOS/<version>/`. Two copies of every skill exist on disk by design. **Do not delete the `.tmp/marketplaces` clone**: it's the only copy holding `plans/` and `templates/`, and `/dlcOS:setup` and `/dlcOS:end` read from it.

The real hazard is the trees **diverging**: skills execute from the cache, but templates and plans are read from the clone — so a hotfix landed in one tree splits behavior between skills. Divergence happens when someone edits one tree in place (a coach hotfix) or upgrades the marketplace without reinstalling the plugin. Rule for coaches: **never hand-edit skill files on a client machine in one tree only.** Update both, or better, ship the fix upstream and run:

```
codex plugin marketplace upgrade dlcOS
codex plugin remove dlcOS@dlcOS
codex plugin add dlcOS@dlcOS
```

To check whether your two trees match:

```
diff -rq ~/.codex/.tmp/marketplaces/dlcOS/plugins/dlcOS/skills ~/.codex/plugins/cache/dlcOS/dlcOS/*/skills
```

---

## "A skill says it can't find my vault"

The skills find your vault by looking for a marker line in your `CLAUDE.md`:

```
<!-- dlcOS:vault-root --> /absolute/path/to/your/vault
```

Open the `CLAUDE.md` at the top of your vault and confirm that line exists, with an absolute path (no `~`, no relatives). The wizard adds it during Stage 2 — if you skipped or interrupted that stage, it might be missing.

To fix: edit `CLAUDE.md` and add the line near the top. Use the actual path to your vault folder.

---

## "Stale plugin registration" / "the plugin shows but acts like an old version"

Two-step fix:

```
/plugin uninstall dlcOS@dlcOS
/plugin install dlcOS@dlcOS
/reload-plugins
```

If you see directory-source registrations for old plugins (e.g., something pointing to `/Users/.../somewhere/`), clear those first via `/plugin list` and `/plugin remove`.

---

## "I pasted the memory block into Settings → Memory and Claude doesn't seem to know it"

A few common causes:

1. **You pasted into the wrong app.** The Settings → Memory paste block goes into the **Claude desktop app** (claude.ai/download), not Claude Code. They're different apps.
2. **You hit save?** After pasting, scroll down and confirm the change was saved. Some versions show a "Save" button; others auto-save.
3. **You're in a different account.** Claude desktop and Claude Code need to be signed into the same account. Check the account menu in each.

To verify it took: in Claude desktop, ask "what do you remember about me?" — Claude should reference the about-me content.

---

## "Office Hours nudge isn't appearing in `/dlcOS:end`"

Two possibilities:

1. **Your coach hasn't set up an Office Hours calendar yet.** The nudge is silent if no calendar is configured — that's by design, not a bug.
2. **The config line is missing from your `CLAUDE.md`.** It looks like:
   ```
   <!-- dlcOS:office-hours-ical --> https://calendar.google.com/calendar/ical/<id>/public/basic.ics
   ```
   If it's not there, your coach can paste in the iCal URL during a session.

---

## "Update check in `/dlcOS:end` shows nothing / fails silently"

Until the first formal release of dlcOS is cut on GitHub, the update check is a no-op (it gracefully handles the missing release). This is expected during the v1 launch window. Once releases start, you'll see "Update available: vX.Y.Z" at session close when one's ready.

---

## "Granola / email ingest skills aren't there"

Correct — they're not in v1. Granola meeting ingest and email ingest are Phase 2 features. v1 focuses on plan workflow + GTD + memory. Your coach will let you know when Phase 2 lands.

---

## What the wizard actually touches on your machine

If something feels weird after running `/dlcOS:setup`, here's the full list of places the wizard writes or changes things. Nothing else on your Mac is modified.

**Inside your vault folder** (the path you gave the wizard in Stage 2):
- Creates `CLAUDE.md` with the `<!-- dlcOS:vault-root -->` marker and your identity block.
- Creates `Inbox/`, `Action/`, `Wiki/Knowledge/`, `Reference/Themes/`, `Reference/Patterns/`, `Reference/Dailies/`.
- Writes `Wiki/Knowledge/about-me.md` (your L3 memory narrative).
- Writes `Wiki/Knowledge/settings-memory-block.md` (a backup of the paste block).
- Drops template files into `Inbox/` and `Action/` (do-now, ideas, thoughts, TASKS, PROJECTS, SOMEDAY, IDEAS, COMPLETED).

**Outside your vault**:
- You paste a memory block into **Claude desktop → Settings → Memory** during Stage 4a. That edit lives in your Claude account, not your filesystem. To remove it later: open Settings → Memory and delete the block.
- The wizard does NOT install Obsidian, Granola, or any other app. If those came up in conversation, you (or your coach) installed them manually.
- The wizard does NOT modify `~/.claude/CLAUDE.md`, your shell rc files, launchd jobs, or anything in `/etc`.

**Rollback** if you want to start over: delete the vault folder (or just the files above), remove the Settings → Memory paste block, and re-run `/dlcOS:setup`.

---

## Last resort

Email Justin at **justin@maccog.com** with:

1. What you were trying to do.
2. The exact command you ran (or what you said to Claude).
3. What it said back. A screenshot is faster than retyping.

Or book time at **support.maccog.com**.
