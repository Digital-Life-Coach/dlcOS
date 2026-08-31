---
name: dashboard-setup
description: "Install a client's own dlcOS Dashboards — a Bun+Hono operator surface (Today/GTD/Orchestrator/Starts) running on the client's own machine (macOS or Linux) against their own vault, never Justin's hardware. Interviews for which modules to run and for network shape (laptop-only / phone-anywhere / VPN comfort), resolves to one of three supported topologies, writes the client's entry-point server file + a launchd plist (macOS) or systemd user unit (Linux) + 1Password item wiring, and verifies bun + cmux are present first. Use when the user says /dlcOS:dashboard-setup, 'set up my dashboard', 'I want the Today/GTD dashboard', or picks up the dashboards add-on from Pending Plans. Optional add-on, not part of base /dlcOS:setup — run this after base setup, with the coach present."
---

# dashboard-setup — Install the Client's Own Dashboards

*Invoke as `/dlcOS:dashboard-setup`*

Ships a client's own copy of `Work/Dashboards` — the Bun + Hono + HTMX operator
hub Justin runs on his own Mac at `hq.macjustin.com` — generalized so a dlcOS
client runs it on **their own machine against their own vault**. Not
multi-tenant on Justin's hardware; each client's data never leaves their
machine. Supported hosts: macOS (launchd) and Linux (systemd user units) —
the latter covers the Linux-appliance delivery path in
`docs/linux-appliance-setup.md`. Full
design background: `Reference/Plans/2026-08-18-dlcos-dashboards.md` in
Justin's vault (not shipped to clients — reference for the coach only).

This is a technical add-on, coach-run. It needs a terminal, `bun`, and cmux on
the client's machine. If the client isn't comfortable with a terminal, do it
together on a screen-share.

---

## Step 0a — Detect the platform FIRST

Everything downstream branches on this, so resolve it before anything else:

```bash
uname -s
```

- `Darwin` → `${PLATFORM}=macos`. Service manager is **launchd**; unit goes to `~/Library/LaunchAgents/`.
- `Linux` → `${PLATFORM}=linux`. Service manager is **systemd user units**; unit goes to `~/.config/systemd/user/`. Confirm systemd is actually the init system (`ps -p 1 -o comm=` returns `systemd`) — if it isn't (a container, or a non-systemd distro), stop and say so plainly rather than writing a unit file nothing will read.
- Anything else → stop. Tell the client this add-on supports macOS and systemd Linux only, and that base dlcOS still works fine without it.

Say the detected platform out loud so the client knows which path they're on.

---

## Step 0 — Resolve VAULT_ROOT

Walk up from the current working directory to find the nearest **`CLAUDE.md` or `AGENTS.md`** (both carry the same dlcOS markers — check both).
Grep for:

```
<!-- dlcOS:vault-root --> /absolute/path/to/vault
```

Take that path as `${VAULT_ROOT}`. If the marker is missing, stop and tell the
client to run `/dlcOS:setup` first — the dashboard needs a vault to point at.

---

## Step 1 — Locate the dashboards payload

The dashboard source (`shared/`, `hq/`, `today/`, `starts/`, `orchestrator/`,
plus each module's `package.json`) is not part of the plugin's skill/agent
tree — like the `/dlcOS:setup` wizard plan, it's a payload that ships
alongside the marketplace clone. Look for it at:

1. `~/.claude/plugins/marketplaces/dlcOS/dashboards/` — canonical path, present
   once the client has run `/plugin marketplace add Digital-Life-Coach/dlcOS`.
2. If running from a development checkout: `<repo-root>/dashboards/`.

**Known gap (2026-08-24):** as of this writing, `dashboards/` has not yet been
published into the public dlcOS repo — only `Work/Dashboards/` in Justin's own
vault exists today. **If neither path above exists, stop here and tell the
user plainly:** "The dashboards code hasn't shipped to the public repo yet —
this add-on isn't installable today. I'll flag it back to Justin." Do not
attempt to reconstruct the payload by copying out of Justin's private vault
into the client's machine over an ad-hoc channel; that's a packaging job, not
a per-client setup step. This section exists so the skill is ready the moment
that gap closes — check `Reference/Plans/2026-08-18-dlcos-dashboards.md` §6
step 6 in Justin's vault for the current status before telling a client this
still isn't available.

Once found, call this path `${DASHBOARDS_PAYLOAD}`.

---

## Step 2 — Verify prerequisites

```bash
command -v bun || echo "no bun"
osascript -e 'id of application "cmux"' 2>/dev/null || echo "no cmux"
```

- **`bun` missing:** tell the client to install it (`curl -fsSL https://bun.sh/install | bash`), then re-run this skill. Don't half-install — if `bun` isn't there, stop before touching any files.
- **`cmux` missing:** the dashboard's launch buttons (▶ start session) need it. Tell the client to install cmux first (see the coach-setup-checklist in Justin's vault for the current install source), then re-run. If the client explicitly doesn't want cmux, note that launch buttons will fail with a copyable command instead — proceed only if they accept that tradeoff.

Do not proceed to Step 3 until both checks pass (or the client has explicitly accepted the no-cmux tradeoff).

---

## Step 3 — Module selection

Tell the client:

> "Your dashboard is a small set of surfaces you pick from. Each one is independent — pick any combination."

Present as a menu:

```
=== DASHBOARD MODULES — pick any ===

a) 📋 GTD (HQ)       Your task/project action surface — capture, P1/P2/P3,
                     quick-batch triage from your morning brief. (recommended)
b) ✅ Today          A single ordered day-plan: pick tasks from backlog,
                     work them, reorder, done. (recommended)
c) ⚡ Starts          One-click session launcher — active projects, pending
                     plans, skills, favorite directories.
d) 🔭 Orchestrator   Read-only system status — live Claude Code sessions,
                     pending plans, git state, scheduled jobs. Also carries
                     the shareable cheat-sheet card if you use those.

Starter pack (recommended for most people): a + b
Everything: a + b + c + d
```

Wait for the client's choices. Default if they say "starter" or "recommend": **a + b** (GTD + Today — the daily-use core; Starts and Orchestrator are useful but more operator-flavored).

Record the choice as a set, e.g. `MODULES = ["hq", "today"]` (internal keys: `hq`→a, `today`→b, `starts`→c, `orchestrator`→d).

**Cheat sheets are not a separate toggle.** The public share-link viewer (`/sheets/:slug`) is always wired in regardless of module choice — it's harmless with no cheat sheets created yet, and useful the moment the client makes one via `/cheat-sheet`. The cheat-sheets *card* (list + delete) only renders inside Orchestrator, so it's only visible if `d` was picked.

---

## Step 4 — Network-shape interview

This is the build-scope question, not a comfort question — ask it straight,
one at a time:

1. "Do you want the dashboard on your laptop, in the house?"
2. "Do you want to reach it on your phone, wherever you are — not just at home?"
3. "If yes to phone-anywhere: are you comfortable running a VPN app on your phone? (Tailscale installs an always-on VPN profile — some people don't want that alongside a work VPN or just don't want the icon in their status bar.)"

Resolve per this table (same as `Reference/Plans/2026-08-18-dlcos-dashboards.md` §5 decision 5):

| Q1 (laptop) | Q2 (phone) | Q3 (VPN OK) | Topology | Notes |
|---|---|---|---|---|
| no | no | – | **localhost-only** | Bind `127.0.0.1`. Reachable only from the machine itself. |
| yes | no | – | **LAN** | Bind `0.0.0.0`. Reachable at `<hostname>.local:PORT` on the home network. Local password only. |
| any | yes | yes | **Tailscale** | Install Tailscale on the host machine + the client's phone. MagicDNS name, no public surface, no login needed — covers the LAN case for free. |
| any | yes | no | **NOT AVAILABLE YET** | See below. |

**If the answers land on row 4:** stop and tell the client plainly: "That combination — reachable from your phone anywhere, without a VPN — needs a public hostname with real login security, and that part of the build isn't done yet. I can set you up with Tailscale instead (same phone reach, but it does install a VPN profile), or with LAN-only for now and revisit this once the public-hostname path ships. Which would you like?" Re-run this step with their new answer. Do not attempt to build a Cloudflare Tunnel + auth path yourself — it's explicitly out of scope (plan §5 decision 5, §9).

Record the resolved topology as `TOPOLOGY` (`localhost` / `lan` / `tailscale`).

---

## Step 5 — Verify prerequisites, again if Tailscale

If `TOPOLOGY = tailscale`:

```bash
command -v tailscale || echo "no tailscale"
```

If missing, tell the client to install Tailscale on the host machine (https://tailscale.com/download) and on their phone, sign in to the same tailnet on both, then re-run this step. Don't proceed without it.

---

## Step 6 — Choose a port and pick a name

Ask the client what to call their dashboard install (used for the launchd
label and log file — e.g. `charlie-dashboards`). Default to a slug of their
first name if they don't care.

Pick a port not already bound. Default `8090` unless the client says another
service already uses it, in which case increment until `lsof -i :$PORT`
reports nothing.

Record `INSTALL_NAME` (e.g. `charlie`) and `PORT`.

---

## Step 7 — Copy the payload and write the client entry point

```bash
mkdir -p "${VAULT_ROOT}/../dlcOS-dashboards" 2>/dev/null || mkdir -p "$HOME/dlcOS-dashboards"
DASH_DIR="$HOME/dlcOS-dashboards"   # adjust if the client wants it elsewhere — ask, don't assume
cp -R "${DASHBOARDS_PAYLOAD}/shared" "$DASH_DIR/"
cp -R "${DASHBOARDS_PAYLOAD}/hq"     "$DASH_DIR/"
[ ... only for modules the client picked ... ]
```

Copy `shared/` always (every module depends on it). Copy `hq/`, `today/`,
`starts/`, `orchestrator/` only for the modules selected in Step 3 — a module
not copied is a module that structurally cannot be reached, which is a
stronger guarantee than an unlisted nav item.

Write `$DASH_DIR/server.ts` — the client's own entry point, modeled on
`hub/server.ts` but importing ONLY `shared/` plus the chosen modules' route
registrars (this is exactly the shape verified in
`Reference/Plans/2026-08-18-dlcos-dashboards.md` Step 3 — a process that
imports only these has no billing/contacts/WP/email routes to leak):

```ts
// server.ts — generated by /dlcOS:dashboard-setup for ${INSTALL_NAME}. Edit
// freely; re-running the setup skill will ask before overwriting.
import { Hono } from "hono";
import { serveStatic } from "hono/bun";
import { resolve } from "node:path";
import { mountLoginRoutes, requireLogin } from "./shared/cookie-auth";
import { withNav, CLIENT_GROUPS } from "./shared/nav";
import { loadSecret, OP_ITEM_REF, primeItemCache } from "./shared/secrets";
import { DASHBOARDS_ROOT } from "./shared/paths";

// Only the modules the client picked — see Step 3.
import { registerHqRoutes } from "./hq/lib/routes";
import { registerCheatSheetPublicRoute, registerCheatSheetRoutes } from "./hq/lib/cheatsheet-routes";
// import { registerTodayRoutes } from "./today/lib/routes";
// import { registerStartsRoutes } from "./starts/lib/routes";
// import { registerOrchestratorRoutes } from "./orchestrator/lib/routes";

const PORT = parseInt(process.env.PORT ?? "${PORT}", 10);
const HOST = process.env.DASH_BIND ?? "127.0.0.1"; // localhost-only default; LAN topology sets 0.0.0.0

await primeItemCache().catch((e) => console.error(`[dashboard] 1P prime failed: ${e.message}`));
const masterKey = await loadSecret(`${OP_ITEM_REF}/password`).catch(() => null);

const app = new Hono();
registerCheatSheetPublicRoute(app); // before login — public share-link viewer

if (masterKey) {
  mountLoginRoutes(app, { masterKey });
  app.use("*", requireLogin({ masterKey, publicPaths: ["/login", "/logout", /^\/sheets\/[a-z0-9-]+$/] }));
} else {
  app.use("*", (c) => c.json({ error: "dashboard unavailable — master key not loaded" }, 503));
}

app.use("*", withNav({ groups: CLIENT_GROUPS }));
app.use("/assets/*", serveStatic({ root: resolve(DASHBOARDS_ROOT, "hub/public") + "/", rewriteRequestPath: (p) => p.replace(/^\/assets/, "") }));

registerHqRoutes(app);
registerCheatSheetRoutes(app);
// registerTodayRoutes(app);
// registerStartsRoutes(app);
// registerOrchestratorRoutes(app);

app.get("/", (c) => c.redirect("/hq/"));

console.log(`[${INSTALL_NAME}-dashboard] listening on ${HOST}:${PORT}`);
export default { port: PORT, hostname: HOST, fetch: app.fetch };
```

Uncomment only the imports/registrations for modules actually selected. The
`/assets/*` line still points at `hub/public` inside the payload for the
static Tailwind build + vendor JS — that directory is part of what Step 1
copies from `${DASHBOARDS_PAYLOAD}` regardless of module choice (visual
styling is shared infrastructure, not a module).

Write `$DASH_DIR/package.json` with a `hono` dependency (pin to the same
version as the payload's `hub/package.json`) and `bun install` in `$DASH_DIR`.

---

## Step 8 — Wire tenant config and 1Password

Every deployment-specific value in `shared/tenant.ts` must be set via env —
under `DLCOS_CLIENT=1` a missing one throws instead of falling back to
Justin's own account (verified in the Step 3/4 build — this is the fail-closed
guarantee the plan asked for). Collect from the client (or leave blank if they
don't use that integration — see below):

- `PUBLIC_BASE_URL` — the client's own dashboard URL. For `localhost`/`lan`
  topology this is `http://localhost:${PORT}` or `http://<hostname>.local:${PORT}`.
  For Tailscale, the MagicDNS name (`http://<device>.<tailnet>.ts.net:${PORT}`).
- `VAULT_ROOT` — `${VAULT_ROOT}` from Step 0.
- `CLAUDE_ORG_ID`, `FRESHBOOKS_ACCOUNT_ID`, `CHARGEBEE_BASE` — **only relevant
  if HQ's brief/billing-adjacent reads touch them; for a base dlcOS client
  these are almost always unused.** If the client has no Claude org UUID /
  FreshBooks / Chargebee account of their own, set them to an obviously-inert
  placeholder (e.g. `unset`) rather than leaving them empty — DLCOS_CLIENT=1
  throws on empty, which is correct: it forces a deliberate choice instead of
  a silent Justin-shaped default.

1Password: create (or reuse) an item named `dlcOS` in a vault named `AI` in
the client's own 1Password account — matching the exact reference pattern
`shared/secrets.ts` already resolves via `OP_ITEM=dlcOS` (confirmed: this
needs zero code changes, `OP_ITEM_REF` becomes `op://AI/dlcOS` automatically).
Put the dashboard's login password in the item's main `password` field (not a
sub-field — matches the same "1Password autofill reads the main field only"
rule Justin's own item follows).

Ask the client whether they have `op` (1Password CLI) set up. If not, walk
them through installing it and creating a service account scoped to their `AI`
vault, same shape as `shared/secrets.ts`'s header comment describes. If they
decline 1Password entirely, fall back to a plain env var
`HUB_DEV_KEYS=1` / `HUB_MASTER_KEY=<password>` in the plist — tell them this
is less secure (password sits in the plist file in plaintext) and 1Password is
recommended.

---

## Step 9 — Write the service unit (branches on `${PLATFORM}`)

Same job either way: run `bun run server.ts` in `${DASH_DIR}` at login, keep it
alive, log to files, and hand it every `DLCOS_CLIENT=1` tenant env var. Only
the wrapper differs.

Fill in every env value from Steps 4/6/8 — every tenant override must actually
be present or the process refuses to boot (that's the point). `DASH_BIND` is
`127.0.0.1` for `localhost` topology, `0.0.0.0` for `lan` and `tailscale`
(Tailscale's own network boundary is the security control there, not the bind
address).

### macOS — launchd

Write `~/Library/LaunchAgents/com.dlcos.${INSTALL_NAME}-dashboard.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.dlcos.${INSTALL_NAME}-dashboard</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>export OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.config/op/service-account-token 2>/dev/null); export DLCOS_CLIENT=1; export OP_ITEM=dlcOS; export VAULT_ROOT="${VAULT_ROOT}"; export PUBLIC_BASE_URL="..."; export CLAUDE_ORG_ID="..."; export FRESHBOOKS_ACCOUNT_ID="..."; export CHARGEBEE_BASE="..."; export PORT="${PORT}"; export DASH_BIND="127.0.0.1_or_0.0.0.0"; exec /path/to/bun run server.ts</string>
  </array>
  <key>WorkingDirectory</key><string>${DASH_DIR}</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>${DASH_DIR}/log.out</string>
  <key>StandardErrorPath</key><string>${DASH_DIR}/log.err</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.dlcos.${INSTALL_NAME}-dashboard.plist
```

### Linux — systemd user unit

Write `~/.config/systemd/user/dlcos-${INSTALL_NAME}-dashboard.service` (create
the directory if needed):

```ini
[Unit]
Description=dlcOS Dashboards (${INSTALL_NAME})
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${DASH_DIR}
Environment=DLCOS_CLIENT=1
Environment=OP_ITEM=dlcOS
Environment=VAULT_ROOT=${VAULT_ROOT}
Environment=PUBLIC_BASE_URL=...
Environment=CLAUDE_ORG_ID=...
Environment=FRESHBOOKS_ACCOUNT_ID=...
Environment=CHARGEBEE_BASE=...
Environment=PORT=${PORT}
Environment=DASH_BIND=127.0.0.1_or_0.0.0.0
ExecStart=/bin/bash -lc 'export OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.config/op/service-account-token 2>/dev/null); exec /path/to/bun run server.ts'
Restart=always
RestartSec=3
StandardOutput=append:${DASH_DIR}/log.out
StandardError=append:${DASH_DIR}/log.err

[Install]
WantedBy=default.target
```

Enable and start it:
```bash
systemctl --user daemon-reload
systemctl --user enable --now dlcos-${INSTALL_NAME}-dashboard.service
```

**Linux-only gotchas — cover these with the client, they bite in this order:**

1. **A user unit dies when the user logs out**, which on a headless appliance
   means it dies the moment the SSH session ends. Fix it once:
   ```bash
   sudo loginctl enable-linger $USER
   ```
   Without this, the dashboard works during setup and is mysteriously down
   the next morning. Do this before declaring the install finished.
2. **`Environment=` values are not shell-expanded.** No `$VAR`, no `~`, no
   command substitution — write literal absolute paths. Anything that genuinely
   needs a shell (the 1Password token read) belongs inside the `ExecStart`
   `bash -lc` string, which is why it's written that way above.
3. **`StandardOutput=append:` needs systemd 240+.** On anything older, drop
   both lines and read logs with `journalctl --user -u
   dlcos-${INSTALL_NAME}-dashboard -f` instead.
4. **`bun` is often not on the unit's PATH** even when it works in the
   client's shell. Use the absolute path from `command -v bun`, same as macOS.
5. **1Password CLI on Linux** — if the client declined `op`, the fallback is
   `Environment=HUB_DEV_KEYS=1` and `Environment=HUB_MASTER_KEY=<password>`,
   with the same warning as macOS: the password sits in the unit file in
   plaintext. Tighten it with `chmod 600` on the unit file.

---

## Step 10 — Verify

```bash
sleep 3
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:${PORT}/healthz
```

Expect `200`. Then have the client open the actual URL for their topology
(`http://localhost:${PORT}/`, `http://<hostname>.local:${PORT}/`, or the
Tailscale MagicDNS URL) in a browser, log in with the master key, and confirm:

1. Only the modules they picked appear in the sidebar (no Billing/Contacts/WP
   Fleet/etc. — those routes should 404 if hit directly, since they were never
   registered).
2. A task check/star/capture action on a selected module actually writes to
   their vault (have them make one real edit and look at the file).

If `/healthz` doesn't return 200: check `$DASH_DIR/log.err` for the boot
error — the most likely cause is a `DLCOS_CLIENT=1` tenant throw from Step 8
(a missing env var), which will name the exact variable in its error message.
On Linux also check `systemctl --user status dlcos-${INSTALL_NAME}-dashboard`
and `journalctl --user -u dlcos-${INSTALL_NAME}-dashboard -n 50`, which catch
the failures that never reach the log file (bad unit syntax, `bun` not found).

**Linux — verify it survives logout.** Confirm lingering is on
(`loginctl show-user $USER --property=Linger` returns `Linger=yes`), then log
out, log back in, and re-run the `/healthz` curl. An install that only works
while you're SSH'd in is not installed.

---

## Gotchas (worth telling the client)

- **This is not on Justin's hardware.** If the client's machine is off or asleep, the dashboard is down. (A Linux appliance is the better answer here — it's always on, which is much of the point of that delivery path.) There's no fleet monitoring on client machines yet (plan §7 "Failure visibility" — open question) — if it goes down, the client notices before Justin does.
- **Update path is manual today.** A future dashboard improvement in Justin's own `Work/Dashboards/` does not automatically reach a client install (plan §7 "Update path" — open question, unresolved as of 2026-08-24). Re-running this skill with a fresh payload copy is the only path right now.
- **Cheat sheets need Orchestrator to manage, not to view.** Anyone with a share link can always view a cheat sheet regardless of module choice; only a client with Orchestrator enabled can see the list or delete one from the dashboard itself.

## What this skill does NOT do

- ❌ Build the Cloudflare Tunnel + full-auth topology (network-shape row 4) — not built yet; the skill redirects to Tailscale or LAN-only instead of attempting it.
- ❌ Support anything but macOS and systemd Linux — Step 0a stops on anything else rather than writing a unit file nothing reads.
- ❌ Install `bun`, cmux, or Tailscale for the client — it verifies they're present and tells the client what to run, same policy as `setup-librarian-index`.
- ❌ Push updates to an existing client install automatically — re-run manually.
- ❌ Touch Justin's own hub (`Work/Dashboards/hub/server.ts`, `com.maccog.hub`) in any way — this skill only ever writes into the client's own `$DASH_DIR` and their own service unit.
