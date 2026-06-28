---
name: draft
description: Spawn the drafter subagent for a piece of prose (email, proposal, blog post, newsletter, reply, etc.), then handle delivery — save as a markdown file, hand it to you, save to your connected email's Drafts (if email is set up), or iterate. Use when you say /dlcOS:draft, "draft an email to X", "draft a reply to Y", "draft a blog post about Z", or any drafting request where you want to pick what happens to the result. Pairs with the dlcOS:drafter subagent.
---

# /dlcOS:draft — Spawn Drafter, Confirm Delivery, Execute

Thin wrapper around the `dlcOS:drafter` subagent. Drafter returns a draft string only; this skill closes the loop by letting you pick what happens to it.

## Steps

### 1. Frame the request

Capture the brief: at minimum **topic / audience / register hint**. Optional but useful: recipient (if email), prior thread context (if reply), tone calibration (e.g. how hard to sell, if a proposal).

If the brief is too thin to draft well — e.g. "draft an email" with no recipient or topic — ask one clarifying question via `AskUserQuestion`. Don't draft on guesses.

Quick check — is this actually a drafter job? Push back if:
- The user wants a commit message → that's a different tool.
- The user wants a code comment, technical doc, or internal task description → offer to write it directly; drafter is for voice-driven prose.
- The user wants you to draft AND send autonomously → STOP. The default is always to confirm before anything leaves. Only skip confirmation if the user wrote the exact phrase "send it without asking" in the current message.

### 2. Spawn drafter

Use the `Agent` tool with `subagent_type: dlcOS:drafter` (the scoped plugin name). Pass the brief plus any context already loaded (recipient note, prior thread, facts).

Drafter returns a `**Draft:**` block followed by a metadata block (format hint, register, subject line, suggested delivery, notes).

### 3. Present the draft

Show the draft body verbatim. Below it, show the metadata block. Below that, present the action options.

### 4. Confirm action

Use `AskUserQuestion` (single-select). Options depend on whether an email integration is configured — check the project `CLAUDE.md` for a `<!-- dlcOS:email-enabled -->` marker (set by the `setup-email` add-on):

**Always available:**
- **Save as markdown file** — default for blog post / newsletter / any non-email, and the default for everything when no email integration is set up. Use the drafter's suggested path or ask.
- **Hand it to me** — just output the final draft for the user to copy; save nothing.
- **Edit — another pass** — user says what to change; re-spawn drafter with the original brief + the changes.
- **Discard** — don't save anywhere.

**Only if `dlcOS:email-enabled` marker is present AND format hint = email AND subject + recipient are known:**
- **Save to my email Drafts** — create a draft in the connected email account (never send).

If the user's original message named the destination explicitly ("draft an email to X" → they want a draft saved/handed for that email; "draft a blog post" → markdown file), pre-select that option but still confirm.

### 5. Execute

**Save as markdown file:**
- Use the path the user named, else the drafter's suggested path, else ask (default: `Inbox/drafts/YYYY-MM-DD <slug>.md`).
- Write the file with a small frontmatter block: `type: draft`, `status: drafted`, `date: <today>`, `register: <from drafter metadata>`.
- Append the drafter's metadata + Notes below the body so the context survives.
- Report the path.

**Hand it to me:**
- Output the clean draft body for easy copy. Save nothing.

**Save to email Drafts (only when `dlcOS:email-enabled`):**
- Use the email integration the setup-email add-on configured. Create a draft (never submit/send). Report a one-line confirmation. On failure, fall back to saving as markdown so the draft isn't lost.

**Edit:**
- Ask what to change. Re-spawn drafter with the original brief + an "iterate on this draft" section pointing at the prior output + the requested delta. Loop back to step 3.

**Discard:**
- Acknowledge. Save nothing.

### 6. Surface drafter's notes

If drafter included anything in its `**Notes:**` block (fact-check flags, placeholders, voice-doc-not-filled warning), pass it through verbatim after executing. Don't silently drop it — it's what the user needs to verify before the draft goes out.

## Push-back conditions

- **If the user asks to send (not draft)** — stop and confirm. This skill saves/hands off drafts; it does not send. Only send if the user explicitly says "send it without asking" in the current message AND an email integration is configured.
- **If the drafter spawn fails** — surface the failure verbatim; offer to retry or hand back for manual writing.
- **If voice.md isn't filled in** — drafter flags this in Notes. Pass it through and offer to help fill `Wiki/Knowledge/voice.md` (or run the voice stage of `/dlcOS:setup`).

## Design notes

- **Drafter returns string only by design.** This skill is the half that delivers. Keeping them separate means drafter stays usable for brainstorming and any destination without leaking junk drafts into an inbox.
- **Default destination follows the request shape, not a global default.** Email request → draft for that email (markdown or Drafts depending on integration). Blog post → markdown. Ambiguous → ask.
- **No autonomous send, ever, without explicit "send it without asking" in the current message.**

## References

- `dlcOS:drafter` — the subagent (returns string only; loads `Wiki/Knowledge/voice.md` every run).
- `templates/voice.md` — the voice rulebook the client fills; drafter's source of truth.
- `setup-email` add-on — configures the email integration that unlocks the "Save to my email Drafts" option.
