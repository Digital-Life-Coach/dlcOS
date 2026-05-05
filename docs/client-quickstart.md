# dlcOS Quickstart

Welcome. You've been invited to dlcOS — the Digital Life Coach OS. It's a small set of Claude Code skills that turn your AI workflow into something you run on your own machine, not something you have to remember to do.

This page gets you from "I just got the invite" to "the wizard is running" in about ten minutes. Your coach should be on the call with you for the wizard itself.

---

## What you need first

1. **A Mac.** dlcOS is built and tested on macOS only.
2. **Claude desktop app.** Download from claude.ai/download. Sign in with the same account you'll use for Claude Code.
3. **Claude Code.** Install per the instructions at claude.com/claude-code. Sign in.
4. **A GitHub account.** dlcOS lives in a private repo your coach has invited you to. If you don't have one, create one at github.com/join — your coach will walk you through this if needed.
5. **A terminal.** Terminal.app (built into macOS) is fine. iTerm2 if you have a preference.

If any of those is missing, stop here and finish them with your coach before continuing.

---

## Install dlcOS

Two commands, run inside Claude Code. Open Claude Code in any directory (it doesn't matter where for install — the wizard sets your real workspace later).

**Step 1 — add the marketplace:**

```
/plugin marketplace add Digital-Life-Coach/dlcOS
```

You'll see `Successfully added marketplace: dlcOS`. If you see an authentication error, your GitHub access hasn't been wired up yet — text your coach.

**Step 2 — install the plugin:**

```
/plugin install dlcOS@dlcOS
```

You'll see `✓ Installed dlcOS`. If Claude Code says some skills don't appear yet, run `/reload-plugins` and try `/plugin list` to confirm.

---

## Run the setup wizard

```
/dlcOS:setup
```

This kicks off a ~45-minute guided onboarding with your coach. The wizard will:

1. Ask you a few questions about who you are and what you want from AI coaching.
2. Build your vault (a folder on disk where your work lives).
3. Verify all five dlcOS skills are working.
4. Build your **memory** — both the narrative version (`about-me.md`) and a paste block for Claude desktop's Settings → Memory.
5. Walk you through the **four memory layers** so you understand how Claude remembers you across sessions.
6. Hand off with a checklist of what to use when.

Don't run this solo on your first try. The whole point is doing it with your coach.

---

## Two ways to use any dlcOS skill

Once you're set up:

**Type `/dlcOS:` to see all your dlcOS skills, or just talk naturally — most skills auto-trigger when you say things like "save this plan" or "wrap up the session."**

The skills are:

- `/dlcOS:save-plan` — park a plan for a future session to critique and execute
- `/dlcOS:resume-plan` — pick up a parked plan
- `/dlcOS:end` — wrap up the current session cleanly (write a daily note, optionally commit)
- `/dlcOS:weekly-review` — guided GTD review (Fridays are a good day)
- `/dlcOS:morning-brief` — a daily snapshot of what to focus on

You don't have to memorize these. The slash menu shows them; natural language works for most.

---

## After the wizard

You don't need to do anything else today. Over the next few sessions:

- Let `/dlcOS:end` write a daily note for you each time you stop working.
- The first Friday after onboarding, run `/dlcOS:weekly-review` with your coach.
- When you feel ready, run `/dlcOS:morning-brief --setup` to configure your daily brief. It's deferred from onboarding on purpose — easier to set up after you've used the system for a few days.

---

## When something breaks

See `troubleshooting.md` in this folder. Most issues are one of: stale plugin registration (run `/reload-plugins`), missing vault root marker, or the marketplace step was skipped during install.

If `troubleshooting.md` doesn't fix it, text Justin at **805-720-9276** or book time at **support.maccog.com**.
