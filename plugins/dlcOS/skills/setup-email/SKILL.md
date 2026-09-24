---
name: setup-email
description: "Optional add-on. Connect the client's email — Fastmail (first-class, via Fastmail's hosted MCP server and OAuth), Google Workspace, or Microsoft 365 (both read-only via their desktop connector out of the box, or full draft-writing after standing up the client's own Google Cloud project or Azure app registration) — so Claude can read their inbox and, where the provider allows it, save drafts for them. Drafts only: this add-on never configures a send path, and /dlcOS:draft never sends. Writes the `dlcOS:email-enabled` marker that unlocks the 'Save to my email Drafts' option in /dlcOS:draft. Use when the user says /dlcOS:setup-email, 'connect my email', 'let Claude read my inbox', 'save drafts to my email', or picks up the email add-on from Pending Plans. Not part of base /dlcOS:setup — run this after base setup."
---

# /dlcOS:setup-email — Connect Email (optional add-on)

*Invoke as `/dlcOS:setup-email`*

Connects the client's mailbox so Claude can read what's in it and **put drafts
into their Drafts folder**. It does not set up sending, and `/dlcOS:draft`
will not send. The client presses send, in their own mail app, always.

This is a moderately technical add-on but not a hard one — for Fastmail it's a
browser login and one command. Coach present is recommended, mostly so someone
is there to talk through the "what does it get to see" question honestly.

---

## Step 0 — Resolve VAULT_ROOT

Read the `<!-- dlcOS:vault-root -->` marker in the project `CLAUDE.md` **or `AGENTS.md`** (check both). Take
the absolute path after it as `${VAULT_ROOT}`. If the marker is missing, stop
and tell the client to run `/dlcOS:setup` first — there's no vault to attach
this to.

---

## Step 1 — Say what this actually does, before doing it

Do not skip this. Email is the most sensitive thing most clients will ever
connect, and a client who agrees without understanding will feel misled later.
Say it plainly:

> "This lets Claude read your email — not just the messages you show it, the
> mailbox. It's how it can answer 'did Sarah ever reply about the invoice'
> without you going to find it. Two things it does *not* do: it can't send
> anything, and it can't delete anything. When it writes an email for you, the
> draft lands in your Drafts folder and sits there until you send it yourself.
>
> The part worth thinking about: when you ask Claude something that makes it
> read a message, that message's contents go to Anthropic to answer you, the
> same as anything else you paste into a conversation. Your whole mailbox isn't
> uploaded anywhere, and nothing is read unless a question calls for it — but
> the messages it does read do leave your machine.
>
> If that's not a trade you want, we skip this. Everything else in dlcOS still
> works, and `/dlcOS:draft` will just save drafts as files instead."

Then ask, single-select (`AskUserQuestion` where available, otherwise plainly): **connect it** / **not now**.

"Not now" is a completely normal answer, especially for a privacy-motivated
client. Take it at face value, say the add-on stays available, and stop here.
Do not re-pitch.

**If the client's mailbox is subject to someone else's confidentiality** —
they're a therapist, a lawyer, a doctor, a hospice volunteer, clergy, or they
handle HR — say so out loud before they answer, and treat "not now" as the
sensible default rather than the timid one. This is the same judgment call as
the third-party bucket in `/dlcOS:setup` Stage 4a, and it applies with more
force here, because an inbox is not a curated export.

---

## Step 2 — Pick the provider

Ask which email they want connected. Three answers, and only the first is
fully wired:

| Provider | Read | Draft-writing | Mechanism |
|---|---|---|---|
| **Fastmail** | ✅ | ✅ | Fastmail's own hosted MCP server, OAuth login in a browser. One command, no cloud project, no password on disk. **The easy path — recommend it if the client has a choice.** |
| **Google Workspace / Gmail** | ✅ | ⚠️ Possible, but you have to build it | Read-only out of the box via the Claude desktop Google Workspace connector. Draft-writing needs the client's own Google Cloud project + Gmail API + OAuth client, feeding a locally-run Gmail MCP server — see Step 3b. Roughly 30–45 minutes of console work. |
| **Microsoft 365 / Outlook** | ✅ | ⚠️ Possible, but you have to build it | Read-only out of the box via Claude's Microsoft 365 connector. Draft-writing needs the client's own Azure app registration + Microsoft Graph API + OAuth client, feeding a locally-run Outlook/Graph MCP server — see Step 3c. Roughly 30–45 minutes of console work, same shape as Gmail Tier 2. |
| **Anything else** (iCloud, generic IMAP) | ❌ | ❌ | No path today. Say so plainly; don't improvise an IMAP script. |

**The marker rule that governs all four rows:** the `dlcOS:email-enabled` marker means *Claude Code can create a draft in this mailbox*. It gets written only where the Draft-writing column says ✅ **and you have verified it end-to-end**. A read-only connector is a genuinely useful thing to have — it just isn't this marker, and writing it anyway would make `/dlcOS:draft` offer an option that fails. That advertise-what-doesn't-work bug is the reason this skill exists; don't reintroduce it.

If the client has more than one address, ask which one this is for, and set up
exactly one. A second can be added later; two half-configured mailboxes is a
worse outcome than one that works.

---

## Step 3a — Fastmail (the supported path)

Fastmail runs a first-party MCP server at `https://api.fastmail.com/mcp`. It
speaks OAuth, so the client logs in through their browser and no password or
app-specific token ever gets written into a config file on disk.

Add it at **user scope** — the client's mail is theirs across every project,
not a per-vault thing:

```bash
claude mcp add --transport http --scope user fastmail https://api.fastmail.com/mcp
```

Then, in a fresh Claude Code session, run `/mcp`, select `fastmail`, and
authenticate. The browser opens; the client logs in to Fastmail and approves
the scopes. Have the client read the scope list on the consent screen out loud
before approving — that screen is the real answer to "what can it see," and
it's better coming from Fastmail than from you.

**If the client is on a headless machine** (a Linux appliance with no browser),
the OAuth callback has nowhere to land. Do the auth on a machine with a
browser, or skip the add-on on that host. Don't try to hand-copy tokens.

Verify:

```
/mcp
```

`fastmail` should show as connected. Then ask Claude, in that session, to
search for something innocuous the client knows exists ("find the most recent
email from my bank"). If it comes back with a real result, the connection is
live.

---

## Step 3b — Google Workspace / Gmail

Two tiers. Ask which one the client wants **before** starting, because the
second is a real project and the first takes five minutes.

### Tier 1 — read-only (five minutes, no cloud project)

The client enables the **Google Workspace connector inside the Claude desktop
app** and logs in with Google.

- ✅ In the **desktop app's chat**, Claude searches and reads their Gmail, and
  can draft text in-chat for them to copy.
- ❌ In a **standalone Claude Code CLI session** (`claude` run in a plain
  terminal), nothing is connected.
- ⚠️ In a **Claude Code session opened from inside the desktop app's Code
  tab** — the setup path this whole product uses — the connector *may* also
  expose read tools there, since Claude Code's own docs describe connectors
  set up at claude.ai as auto-propagating into Claude Code sessions. ⚠
  INFERRED 2026-09-23, unconfirmed for Gmail specifically: confirmed once for
  a Microsoft 365 connector (see Step 3c), not yet observed for Gmail. This
  propagation is also documented as unreliable — a connector can show
  "connected" while exposing zero tools to a given session (Claude Code
  GitHub issues #92904, #62401) — so treat a working read in one session as
  "it worked this time," not a guarantee. It would be confirmed by testing a
  real client's Gmail Tier 1 connection from a Code-tab session and checking
  whether a Gmail search/read tool actually appears.
- Either way, the "Save to my email Drafts" option in `/dlcOS:draft` still
  won't appear on Tier 1 — that requires a *create-draft* tool, which nothing
  above provides. Drafts save as markdown files regardless of what read
  access looks like.

Do **not** write the `dlcOS:email-enabled` marker on Tier 1. Record it in the
vault as a known read-only setup (Step 5) and stop.

For most clients this is the right stopping point. Copying a draft into Gmail
once a day is a small tax; standing up a cloud project is not.

### Tier 2 — draft-writing (a Google Cloud project, ~30–45 min)

Worth it when the client lives in Gmail and drafts constantly. Only do this
with the coach driving; it's console work, not a wizard.

The shape: Google doesn't hand out Gmail write access to third-party apps
casually, so the client stands up **their own** app, in **their own** Google
Cloud project, and authorizes it to their own mailbox. Nothing goes through
MacCog's credentials, and the client can revoke it from their own account page.

1. **Create a Google Cloud project.** console.cloud.google.com → new project.
   Name it something the client will recognize a year from now
   (`<name>-claude-mail`), not `My First Project`. Free tier is fine; Gmail API
   usage at one person's scale costs nothing.
2. **Enable the Gmail API** on that project. APIs & Services → Library → Gmail
   API → Enable.
3. **Configure the OAuth consent screen.** User type **External** unless the
   client is on Workspace and you can use Internal — Internal is simpler and
   skips verification, so prefer it when available. Fill the app name, support
   email, and developer email. On External, leave it in **Testing** and add the
   client's own address under **Test users**. Testing mode is correct here: the
   app has exactly one user. Note the consequence — on External + Testing,
   refresh tokens expire every 7 days and the client has to re-authorize. If
   that's unacceptable and Internal isn't available, stop and use Tier 1.
4. **Add scopes.** `gmail.readonly` and `gmail.compose`. **Not** `gmail.send`,
   and **not** `https://mail.google.com/` (full access, includes delete).
   `gmail.compose` is precisely "create drafts, don't send" — the scope this
   whole add-on is built around. If a setup guide tells you to grab full
   access, it's wrong for this purpose.
5. **Create an OAuth client ID**, type **Desktop app**. Download the JSON.
   Store it outside the vault (`~/.config/dlcos/gmail-oauth.json`, `chmod 600`)
   — it is a credential, and the vault syncs.
6. **Wire a Gmail MCP server** in Claude Code pointed at that credentials file,
   at user scope. Whichever server the client uses, check two things before
   trusting it: it must expose a *create draft* tool, and it must not expose a
   send tool. If it exposes send, either configure that tool off or don't use
   it — a send capability sitting in the toolset contradicts what you told the
   client in Step 1.
7. **Authorize.** First run opens a browser; the client approves the scopes on
   their own project's consent screen. They'll see an "unverified app" warning
   naming their own app — that's expected on External+Testing, and it's worth
   pausing to explain rather than clicking past, because it looks alarming and
   the client will remember it.

Then Step 4 (marker) and Step 5 (verify) apply normally — but **only after** a
real draft has landed in their Drafts folder. If any step above didn't finish,
fall back to Tier 1 and don't write the marker.

**Tell the client the maintenance cost up front:** on External + Testing they
re-authorize weekly, and if they ever delete the Cloud project the integration
dies silently. A client who wasn't told this reads both as breakage.

---

## Step 3c — Microsoft 365 / Outlook

Two tiers, same shape as Gmail. Ask which one the client wants before
starting.

### Tier 1 — read-only (five minutes, no cloud project)

The client enables the **Microsoft 365 connector in the Claude desktop app**
and signs in with their Microsoft account.

- ✅ In the **desktop app's chat**: search and read mail, calendar, and files.
- ⚠️ **A Claude Code session opened from the desktop app's Code tab may also
  reach it for reading.** ⚠ INFERRED 2026-09-23, unconfirmed as a general
  rule: observed once, live — a client's Microsoft 365 connector, set up
  through the desktop app, was reachable by mail-search/read tool calls from
  that same client's Code-tab session (see `/dlcOS:email-ingest`, which
  detects and uses this when present). Matches Claude Code's documented
  connect-at-claude.ai-then-auto-appears-in-Claude-Code behavior, but that
  same documentation and open Claude Code issues (#92904, #62401) describe
  the hand-off as unreliable — some sessions show "connected" with zero tools
  exposed. Treat one working case as real but not load-bearing until it's
  been seen more than once; confirmed further by trying it with another
  client's Microsoft connector and checking whether tools appear.
- ❌ **No draft-writing on Tier 1.** Nothing about the read access above
  implies a create-draft tool exists. `/dlcOS:draft` will save drafts as
  markdown and the client copies them into Outlook.

Do **not** write the `dlcOS:email-enabled` marker on Tier 1. Record it as a
read-only setup (Step 5) and stop.

For most clients this is the right stopping point, same reasoning as Gmail
Tier 1.

### Tier 2 — draft-writing (an Azure app registration, ~30–45 min)

Worth it when the client lives in Outlook and drafts constantly. Coach-driven
console work, same shape as Gmail Tier 2: the client stands up **their own**
app in **their own** Azure tenant and authorizes it to their own mailbox.
Nothing goes through MacCog's credentials.

1. **Register an app.** portal.azure.com → **App registrations** → **New
   registration**. Name it something the client will recognize later
   (`<name>-claude-mail`). Under **Supported account types**, a personal
   Microsoft account is the simple case; a work/school account may involve
   the organization's own consent or Conditional Access policy — if the
   client is on a managed work tenant, check with their IT before assuming
   this will just work.
2. **Set it up as a public client.** Under **Authentication**, add a platform
   of type **Mobile and desktop applications** — this gets you the
   authorization-code-with-PKCE flow, no client secret to store on disk.
3. **Add Microsoft Graph API permissions (delegated).** `Mail.Read` and
   `Mail.ReadWrite`. **Not** `Mail.Send` — `Mail.ReadWrite` covers creating
   and editing drafts but does not grant the ability to send. If a setup
   guide tells you to add `Mail.Send` for this, it's wrong for this purpose.
4. **Wire an Outlook / Microsoft Graph MCP server** in Claude Code pointed at
   this app's client ID, at user scope. Whichever server the client uses,
   check two things before trusting it: it must expose a *create draft*
   tool, and it must not expose a send tool. If it exposes send, configure
   that tool off or don't use it.
5. **Authorize.** First run opens a browser; the client signs in and approves
   the scopes on their own app's consent screen.

Then Step 4 (marker) and Step 5 (verify) apply normally — but only after a
real draft has landed in the client's Drafts folder. If any step above didn't
finish, fall back to Tier 1 and don't write the marker.

**If the client has a choice of provider** — some do, especially the ones
consolidating a personal mailbox — this is the moment to mention that Fastmail
gets them draft-writing in five minutes with no cloud project. Mention it once.
Nobody switches email providers on a coach's say-so, and pushing it twice reads
as a sales pitch.

---

## Step 4 — Write the marker (draft-writing paths only)

Add to the project `CLAUDE.md`, near the other `dlcOS:` markers — and mirror the same line into `AGENTS.md` if that file exists, so a Codex-driven vault (which auto-loads only `AGENTS.md`) sees it too:

Only reachable from **Fastmail** (Step 3a), **Gmail Tier 2** (Step 3b), or
**Microsoft 365 Tier 2** (Step 3c), and only after a draft has actually landed
in the client's Drafts folder.

```
<!-- dlcOS:email-enabled --> fastmail  (or: gmail, microsoft365. Claude Code can read this mailbox and create drafts in it. It cannot send. Delete this line to turn the integration off in /dlcOS:draft.)
```

Also remove the `setup-email` line from the `<!-- dlcOS:addons-start -->` block
in `CLAUDE.md` — it's no longer pending.

Mirror both changes into `${VAULT_ROOT}/AGENTS.md` if it exists, so a Codex or
Cursor session knows the mailbox is connected and knows the same drafts-only
rule applies to it.

---

## Step 5 — Verify with a real draft, then clean up

Don't declare this done on a connection check. Round-trip it:

1. Run `/dlcOS:draft` and ask for something trivial — a two-line note to the
   client's own address.
2. Confirm the "Save to my email Drafts" option now appears (it reads the
   marker from Step 4).
3. Choose it.
4. Have the client open their mail app and **see the draft sitting in Drafts**.
   This is the moment the feature becomes real to them.
5. Have them delete it.

Then note in `${VAULT_ROOT}/Reference/Dailies/<today>.md`:

```markdown
## Email add-on — <date>
**Provider:** Fastmail / Google Workspace / Microsoft 365
**Tier:** draft-writing / read-only
**Mechanism:** Fastmail hosted MCP (user scope, OAuth) / desktop connector / client-owned Google Cloud project + Gmail MCP
**Drafts round-trip verified:** yes / no / n-a — provider has no draft path
**Marker written:** yes / no — <reason if no>
**Client was told the ceiling before connecting:** yes
**Client understood the read-access trade-off:** yes
```

---

## Step 6 — Tell them the two things that matter

1. **Nothing sends itself.** If they ever see an email leave their account that
   they didn't press send on, that's not this — tell the coach immediately.
2. **How to turn it off.** Delete the `dlcOS:email-enabled` line from
   `CLAUDE.md` to stop `/dlcOS:draft` offering it, and revoke access at the
   provider to cut the connection entirely — Fastmail's own settings, the
   client's Google Account permissions page (or deleting the Cloud project
   outright), or their Microsoft account's app permissions. They can do both
   without the coach. Say this out loud — a client who knows how to leave is a
   client who's comfortable staying.

---

## Push-back conditions

- **Client asks you to enable sending.** No. This add-on has no send path by
  design, and `/dlcOS:draft` refuses to send without an explicit per-message
  instruction. If they want an email sent, they send it.
- **Client wants an IMAP password stashed in a config file** to get around the
  unsupported-provider answer. Don't. A plaintext mail password on disk is a
  worse outcome than the missing feature.
- **`/mcp` shows connected but searches return nothing.** Usually the OAuth
  grant covers a different account than the one they meant. Check which address
  authenticated before debugging anything else.

## What this skill does NOT do

- ❌ Configure sending, autoresponders, or any unattended mail action.
- ❌ Triage, file, archive, or delete mail. Reading and drafting only.
- ❌ Archive sent mail into the vault. That was the old v1.1 sketch; it's a
  separate ingest job, not part of connecting a mailbox.
- ❌ Support IMAP generally or iCloud.
- ❌ Get draft-writing working on Tier 1 for Google or Microsoft — that needs Tier 2's own cloud project, on both providers.
- ❌ Run the Google Cloud or Azure console steps unattended. Tier 2 is coach-driven, in the client's own account, on the client's own credentials, on either provider.
- ❌ Write the `dlcOS:email-enabled` marker on any path where Claude Code cannot
  actually create a draft.

## References

- `/dlcOS:draft` — the consumer of the `dlcOS:email-enabled` marker.
- `templates/claude-md-starter.md` — where the marker and the add-on line live.
