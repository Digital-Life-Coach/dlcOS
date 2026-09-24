---
name: email-ingest
description: "Optional add-on. Archive a client's Sent-folder threads into Wiki/Emails/ as clean, searchable markdown conversations — one file per thread, full history, participants and dates in frontmatter. Works with whatever mailbox connection the client already has: Fastmail (fully wired), or Microsoft 365 / Google Workspace via Claude's own connectors (best-effort — Anthropic doesn't publish fixed tool names for those, so this skill detects what's actually available in the session and adapts). Read-only; never sends or deletes. Supports incremental runs (--days N, default 90) and --dry-run. Use when the user says /dlcOS:email-ingest, 'archive my sent email', 'pull my email into the vault', or wants old email conversations searchable alongside their notes."
---

# /dlcOS:email-ingest — Email → Vault Archive (optional add-on)

*Invoke as `/dlcOS:email-ingest`*

Pulls threads from the client's Sent folder — whatever mailbox connection they
already have working in this session — and writes each one as a clean
markdown conversation in `Wiki/Emails/`: sender, recipient, and body text,
with quoting and signatures stripped out. Once ingested, those conversations
are just vault content: `librarian` can search them, `/dlcOS:draft` can
reference them, and they show up in weekly reviews like anything else the
client wrote.

Read-only. It never sends, deletes, or modifies anything in the mailbox.

**Arguments:**
- `--days N` — How far back to look (default: 90)
- `--dry-run` — Show what would be ingested without writing files
- `--full` — Ignore the state file, re-process everything in the date range

---

## Step 0 — Resolve VAULT_ROOT and find out what mail access actually exists

Read the `<!-- dlcOS:vault-root -->` marker in the project `CLAUDE.md` **or
`AGENTS.md`**. Take the absolute path after it as `${VAULT_ROOT}`.

**Don't gate on a single hardcoded provider — check what this session can
actually reach right now,** because connector availability is inconsistent
enough that a marker alone isn't reliable proof of a live connection:

1. **Fastmail** — check for `mcp__fastmail__*` tools (`search_email`,
   `read_thread`, `read_email`). If present, this is the fully-specified path
   — use Steps 1a/2a/3a below. This is the one provider with a documented,
   stable tool contract, set up via `/dlcOS:setup-email`.
2. **Microsoft 365 / Outlook, or Google Workspace / Gmail** — these connect
   through Claude's own Settings → Connectors (claude.ai), and are *supposed*
   to auto-propagate into a Claude Code session once connected there — but
   Anthropic doesn't publish fixed tool names for them, and propagation is
   known to be unreliable (a connector can show "connected" while exposing
   zero tools to this session). ⚠ INFERRED 2026-09-23, unconfirmed as a
   general rule: the one live case observed so far — a Microsoft 365
   connector reachable from Claude Code — was a session opened from the
   **desktop app's Code tab**, not a standalone `claude` run in a plain
   terminal. If this run is happening in a bare terminal and no connector
   tools show up, that may be why; a Code-tab session in the desktop app is
   the more promising place to try. This would be confirmed by testing the
   same client's connector from both session types and comparing. So: **look
   at your own available tools right now** for anything mail-related from a
   Microsoft/Outlook or Google/Gmail-named connector — a search-or-list-messages
   tool and a get-message-or-thread-content tool are the two you need. If you
   find them, use the adaptive path in Steps 1b/2b/3b, working from that
   tool's own parameter schema rather than the fixed examples below (those
   are Fastmail-specific). If a mail tool exists but you're unsure it's the
   right one, a cheap way to check is a small read-only test call (list a
   couple of recent messages) before committing to the full run.
3. **Nothing found for either** — stop. Tell the client no working mail
   connection is visible in this session. If they believe one is set up,
   have them check `/mcp` (Fastmail) or their claude.ai Settings → Connectors
   page (Microsoft/Google) and confirm it shows connected there; if it does
   but nothing shows up here, this is a known connector-propagation issue
   independent of dlcOS — sometimes fixed by starting a fresh session. If
   nothing is set up at all, point Fastmail users to `/dlcOS:setup-email`;
   for Microsoft/Google, there's no dlcOS setup skill for it today — direct
   them to claude.ai's own connector settings.

Say plainly at the start of the run which provider you found and are using,
so the client isn't guessing.

---

## Step 1a — Fastmail: find the vault owner's name

Read `${VAULT_ROOT}/Wiki/Knowledge/about-me.md` and take the client's first
name from it. This is the name their own sent messages get labeled with, and
the name used when a reply comes back addressed to them (Step 4).

## Step 1b — Microsoft/Google: same, plus a schema check

Do the same about-me.md lookup. Then, before querying anything, inspect
whichever connector tool you found: read its parameter schema (arguments,
what it returns) since you're working without a fixed spec here. Look
specifically for whether it can filter by folder/label (Sent) and by date,
and what shape it returns a thread/conversation in — you'll need this to
adapt Steps 2b/3b correctly for what's actually in front of you.

---

## Step 2a — Fastmail: query Sent threads

Check the state file first, unless `--full` was passed:

- Read `${VAULT_ROOT}/Wiki/Emails/.email-ingest-state.json`
- If `last_email_date` exists, use it as the cutoff (incremental mode)
- Otherwise, use `--days N` (default 90) to compute the cutoff

Call `mcp__fastmail__search_email` with a query scoped to the Sent folder and
the cutoff, e.g. `in:sent after:90d` for a relative window, or `in:sent
after:<YYYY-MM-DD>` for an absolute one from the state file. Page through
`nextCursor` until `hasMore` is false, collecting every result.

Collect the unique `threadId` values across all pages — that's the full set
of threads to archive.

## Step 2b — Microsoft/Google: query Sent threads (adaptive)

Same window logic (state file cutoff, or `--days N`). Use the connector's own
search/list tool, scoped to the Sent folder or "from: me," in whatever way its
schema supports (a query string, a folder parameter, an `is:sent` qualifier —
check what you found in Step 1b). Page through however that tool paginates.
Collect the unique thread or conversation identifiers it returns.

If the tool has no obvious way to scope to Sent specifically, say so in the
run summary and ask the client whether to proceed against the whole mailbox
instead — don't silently widen scope.

---

## Step 3a — Fastmail: fetch each thread

For each unique `threadId`, call `mcp__fastmail__read_thread`. It already
returns every message in the thread, sorted, with the quoted-reply chain
stripped from each `bodyText` — most of the cleanup work the old JMAP version
of this skill had to do by hand is already done by the server.

**Filter out noise** before composing: drop messages from
`noreply@`/`notifications@`/`monitoring@`/`mailer-daemon@`-style senders.

**Long messages:** `read_thread` truncates a very long `bodyText`. If a
message looks cut off (ends mid-sentence with no natural stop), call
`mcp__fastmail__read_email` with that message's `id` for the full body rather
than settling for the truncated version.

## Step 3b — Microsoft/Google: fetch each thread (adaptive)

For each thread/conversation ID, call whatever detail-fetch tool you found.
If it returns full raw content (headers, HTML, quoted history all mixed in)
rather than Fastmail's already-cleaned `bodyText`, you'll need to do more of
the cleanup work by hand in Step 4 — HTML-to-text conversion and quoted-reply
stripping — since there's no guarantee the connector does it server-side the
way Fastmail's does. Apply the same noise-sender filter as Step 3a.

---

## Step 4 — Compose thread markdown (same for every provider)

For each thread, create a markdown file:

**Filename:** `YYYY-MM-DD Subject Line Here.md` using the earliest message
date.
- Keep original casing and spaces — Obsidian handles them natively
- Strip "Re: " / "Fwd: " / "RE: " prefixes for the filename and `#` heading
- Remove filesystem-invalid chars: `/\:*?"<>|`
- **Replace `[` and `]` with `(` and `)`.** Both are filesystem-legal, but
  Obsidian's `[[wikilink]]` parser stops at the first literal `[` or `]` —
  a bracketed subject like `[Case #123]` would produce a filename the index
  step can never link to. Swap before the 80-char cap so a truncated bracket
  can't slip through unmatched.
- Max 80 chars for the subject portion
- Collision: append ` 2`, ` 3` if the file already exists

**File format:**

```markdown
---
type: email
source: fastmail  # or microsoft365 / gmail — whichever connector this run used
thread_id: <threadId>
subject: "Re: Website redesign proposal"
participants: [client@example.com, other-party@example.com]
date_start: 2026-03-15
date_end: 2026-04-02
message_count: 7
last_updated: 2026-04-05
tags: [email]
---

# Website redesign proposal

---

### 2026-03-15 09:32 — Alex (the vault owner)
Hey Jane, here's what I'm thinking for the redesign...

---

### 2026-03-15 14:15 — Jane Doe
Love this direction! A few questions...

## Related
```

**Format rules:**
- Subject is the ONLY visible heading — clean and scannable
- ALL metadata (participants, dates, message count, **and which connector
  sourced this thread**) lives in frontmatter only — no `*Last updated*` line
  in the body
- Messages separated by `---`, each with a `### Sender Name` header and a
  timestamp line
- **Recipient/sender labeling:** the vault owner's own messages are labeled
  with their first name from Step 1, not their full name. Other senders use
  their display name, falling back to their email address if no display name
  is present.
- On Fastmail, body text comes pre-cleaned (`bodyText`) — skip HTML-to-text
  and quote-stripping. On Microsoft/Google (Step 3b), do that cleanup
  yourself if the connector handed back raw content: strip blockquotes →
  strip style/script tags → convert br/div/p to newlines → strip remaining
  tags → THEN unescape HTML entities (order matters, unescape after
  tag-stripping) → then remove `>`-quoted lines, `On ... wrote:` blocks, and
  `---------- Forwarded message ----------` / Outlook `From:/Sent:/To:`
  header blocks.
- **Extract system metadata (before signature detection):** support-ticket
  systems append machine-generated tracking tokens that confuse the signature
  scorer below. Pre-strip these lines and store useful ones in frontmatter as
  `ticket_ref:`. Patterns to match:
  - `thread::\S+::` (hosting-provider ticketing)
  - `ref:_\S+:ref` (Zendesk/Salesforce)
  - `\[ref:.*?\]` (Salesforce case refs)
  - Lines that are pure hex/base64 gibberish (>20 non-space chars, no spaces,
    no real words)
  - `---+ Please reply above this line ---+` and similar markers — strip
    everything below them
  - `\[Ticket ?#?\d+\]` (generic ticket refs)
- **Strip email signatures:** heuristic scoring from the bottom of the
  message up. Sign-off phrases ("Best regards", "Cheers", "Thanks") score +3
  **only if the line is under 40 chars** — this stops "Thanks for the update,
  here's what I think..." from being misread as a sign-off. Phone numbers,
  URLs, addresses, and job titles score +2. Short ambiguous lines score 0.
  Long content lines score -2. Cut when the cumulative score reaches ≥3 **and**
  the current line itself scores > 0 — only advance the cut into
  signature-like lines. Stop scanning once a negative-scoring (content) line
  follows a found cut point, so a high-momentum signature can't eat real
  content above it. Also strip the RFC `-- ` separator and trailing
  single-letter sign-offs.
- **Attachments:** strip inline image references (`[image:...]`,
  `<image001.png>`, CID refs, object-replacement characters). Keep only
  attachment filenames if referenced in the text.
- If a message's body is empty after cleanup, **skip it entirely** — there's
  no such thing as an intentionally blank email; if cleanup removed
  everything, it was all signature and quoting.
- `## Related` section at the bottom, empty for now.

---

## Step 5 — Update the email index

**File:** `${VAULT_ROOT}/Wiki/Emails/index.md`

Group threads by month (newest first). Each entry:

```markdown
- [[YYYY-MM-DD Subject Line Here]] — Other Participant Name (N messages)
```

**The link text must be the exact filename you wrote in Step 4** — read it
back from the file you just created rather than re-deriving it from the
subject line, or the link won't resolve.

If multiple non-owner participants, list the primary one plus "et al."

Update the header count: `*N threads — last updated YYYY-MM-DD*`

---

## Step 6 — Update the state file

Write `${VAULT_ROOT}/Wiki/Emails/.email-ingest-state.json`:

```json
{
  "last_run": "<ISO8601 now>",
  "last_email_date": "<receivedAt of newest email processed>",
  "threads_ingested": <total count>,
  "threads_this_run": <count this run>,
  "source": "<fastmail | microsoft365 | gmail>"
}
```

This file is also how a client (or their coach) can tell when email was last
archived, and from which connector — there's no separate cache file to check.

**If the connector changes between runs** (e.g. the client switches from a
Microsoft connector to Fastmail), don't silently merge state — the two
sources have different thread ID spaces. Note the source mismatch to the
client and default to treating it as a fresh `--full` run for the new source,
without disturbing files already ingested from the old one.

---

## Step 7 — Update the wiki log

Append to `${VAULT_ROOT}/Wiki/log.md` (newest first):

```markdown
## [YYYY-MM-DD] email-ingest | N threads from Sent folder
- Created: N new thread files in Wiki/Emails/
- Updated: Wiki/Emails/index.md
- Source: <Fastmail | Microsoft 365 | Google Workspace> (last N days)
- Threads: [list first 5 thread subjects, then "+ N more" if > 5]
```

---

## Step 8 — Report summary

```
Email Ingest Complete
─────────────────────
Source: <Fastmail | Microsoft 365 | Google Workspace>
Date range: YYYY-MM-DD → YYYY-MM-DD
Sent emails scanned: N
Unique threads found: N
New threads written: N (skipped N existing)
Participants: N unique contacts
Top contacts: Name1 (N threads), Name2 (N threads), ...

Files written to: Wiki/Emails/
Index updated: Wiki/Emails/index.md
```

If `--dry-run`: show the same summary prefixed with "DRY RUN — no files
written," and list every thread subject that would be created.

---

## Error handling

- **No mail tool reachable at all:** see Step 0.3 — don't guess at an
  auth workaround, surface the state plainly.
- **Microsoft/Google tool found but behaves unexpectedly** (wrong data shape,
  missing fields Step 4 needs): say what's missing and stop rather than
  writing malformed thread files — this connector's contract isn't fixed, so
  a confused result is a real signal, not something to paper over.
- **Empty thread:** if a thread returns zero usable messages after filtering,
  skip it and note the skip in the run summary.
- **Existing files:** if a thread file already exists and the thread has new
  messages since, update the file — append the new messages, refresh the
  frontmatter counts.
- **Encoding:** use UTF-8 throughout; strip any stray non-printable
  characters from body text.

---

## What this skill does NOT do

- **Inbox scanning** — Sent folder only; inbox is transitory and not archived
- **Attachment downloading** — notes filenames in text, never fetches files
- **HTML rendering** — plain text only, in the final vault files
- **Send or delete** — read-only, full stop
- **Guaranteeing Microsoft 365 / Google Workspace will work** — Fastmail is
  the one provider with a documented, stable tool contract. The others ride
  whatever connector tools Claude happens to expose in this session, which is
  known to be inconsistent; treat a working run there as "it worked this
  time," not a guarantee for next time.
- **Scheduling itself** — this is a manual, on-demand skill; it does not
  install a cron job or run unattended. If a client wants it running
  automatically, that's a decision for the coach to make and configure
  explicitly, not something this skill sets up on its own.
- **Task extraction from sent commitments** — the coach's own personal setup
  scans sent messages for things like "I'll follow up..." and proposes tasks
  from them; that depends on a task-tracking format this skill doesn't
  assume every client vault has, so it's not part of the shipped version.

## References

- `/dlcOS:setup-email` — sets up the Fastmail path this skill checks for.
- `Wiki/Knowledge/about-me.md` — where the vault owner's name comes from.
