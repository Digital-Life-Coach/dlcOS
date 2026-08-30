# dlcOS on a Linux Appliance (draft, in progress)

*Status: build-and-test in progress, first end-to-end run not yet complete. This is a working playbook, not a finished client doc — treat every step as verified only up to where this file says so.*

Alternative delivery model to the [Quickstart](client-quickstart.md), which is Mac-only. This path repurposes old x86 hardware (an old Mac Mini, a client's spare PC, a trashcan Mac Pro) as a **headless Linux appliance** running the CLI tools, syncing a vault to the client's own everyday Mac via Syncthing. The client never touches a terminal on the appliance itself — their Mac holds the vault and (eventually) a Claude Desktop session connects remotely into the appliance's CLI.

Why this exists: many prospective dlcOS clients have old Intel-era Macs sitting unused. Reusing that hardware as a dedicated appliance is a real selling point — free/cheap hardware, no local resource contention on the client's daily-driver machine — as long as we're honest that it's end-of-life consumer hardware with no warranty (see Troubleshooting below).

Test rig: a late-2012 Mac Mini (Macmini6,1, dual-core i5, 6GB RAM) — the low end of what we'd ever deliver. If it works here, it works on anything newer.

---

## 1. OS install

- Wipe to **Ubuntu Server LTS** (latest — 26.04.1 at time of writing), not Desktop. No GUI needed; everything is SSH/CLI.
- Write the ISO to an 8–16GB USB stick (`dd` from another Mac works fine; verify the checksum against Canonical's official `SHA256SUMS` before writing — don't skip this).
- Boot the target machine holding ⌥ (Option) to reach the EFI boot picker, select the USB.
- During setup: **enable OpenSSH server** on the SSH-setup screen — critical, since you'll never touch this machine with a monitor again after this.
- Use Ethernet for the install itself. Old Macs with Broadcom Wi-Fi chips (e.g. BCM4331) aren't supported by the installer's live environment.

## 2. Networking

**Wi-Fi is doable post-install**, even on old Broadcom chips, but needs extra steps the installer doesn't do for you:

- The `b43` driver (which auto-binds to older Broadcom chips) needs proprietary microcode Ubuntu can't ship by default:
  ```bash
  sudo add-apt-repository multiverse -y
  sudo apt update
  sudo apt install -y b43-fwcutter firmware-b43-installer
  sudo modprobe -r b43 && sudo modprobe b43
  ```
- This is a minimal server image — there's **no NetworkManager/`nmcli`**, only netplan + systemd-networkd. Wi-Fi needs `wpasupplicant` and a netplan file:
  ```bash
  sudo apt install -y wpasupplicant
  sudo tee /etc/netplan/99-wifi.yaml > /dev/null <<'EOF'
  network:
    version: 2
    wifis:
      <interface-name>:      # find via `ip link` — NOT necessarily wlan0
        dhcp4: true
        access-points:
          "<SSID>":
            password: "<password>"
  EOF
  sudo chmod 600 /etc/netplan/99-wifi.yaml
  sudo netplan apply
  ```
- Interface names are the "predictable" scheme (e.g. `wlp2s0b1`), not `wlan0` — check `ip link` first.
- Set a **DHCP reservation** on the client's router for the Wi-Fi interface's MAC (not the Ethernet MAC — they differ). Reservations sometimes only apply on the *next* DHCP request, not retroactively — reboot to confirm it stuck.

## 3. SSH access (for you, remote-troubleshooting)

- Generate a dedicated key per box (`ssh-keygen -t ed25519 -f ~/.ssh/id_<boxname>`), `ssh-copy-id` it over, add a `Host` alias in your `~/.ssh/config`.
- **This is your only remote-troubleshooting path on consumer Mac hardware** — no IPMI/out-of-band console like real server gear. If the box is unreachable, someone has to be physically present to power-cycle it. Mitigate with:
  - **Tailscale**, not just LAN SSH — survives the client's router/firewall changing, works from anywhere.
  - **A smart plug** (Meross/Govee/Eve) on the power feed, so you can remote-power-cycle a hung box without a client visit.
- If reservations drift or SSH breaks, `arp -a` / `nmap`-style LAN scans are unreliable with 20+ devices on a real home network — faster to just have the client read you the IP off the console screen.

## 4. CLI tooling — none of this needs sudo

```bash
# Claude Code — native installer, no Node dependency
curl -fsSL https://claude.ai/install.sh | bash

# Antigravity CLI (agy) — native Go binary, no Node dependency
curl -fsSL https://antigravity.google/cli/install.sh | bash

# Codex — needs Node; nvm avoids any sudo/global-npm-permissions mess
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install --lts
npm install -g @openai/codex
```

None of these are authenticated yet after install — each needs its own one-time login (OAuth device-code flow for `claude`/`codex`, Google OAuth for `agy`) on first real use.

**Antigravity as a pitch:** free-tier usage bundled with any Gmail account is a nice bonus and a good hook for a second/third model option once a client's monthly cap is hit elsewhere — but the free tier is thin (weekly-refresh quota, no published cap, third-party trackers seeing it shrink over time). Pitch it as a bonus, not the main value.

## 5. Syncthing (vault sync — appliance ↔ client's Mac)

```bash
sudo apt install -y syncthing
mkdir -p ~/vault
sudo systemctl enable --now syncthing@<username>.service
syncthing --device-id   # note this, you'll need it
```

On the client's Mac: install Syncthing (`brew install syncthing` or the macOS app), get its device ID from the web UI (`127.0.0.1:8384` → Actions → Show ID).

Pair them via the appliance's local REST API (its API key is in `~/.local/state/syncthing/config.xml`) rather than fighting the GUI over SSH:

```bash
API=<appliance's syncthing apikey>
CLIENT_ID=<client Mac's device ID>
curl -X POST -H "X-API-Key: $API" -H 'Content-Type: application/json' \
  http://127.0.0.1:8384/rest/config/devices \
  -d "{\"deviceID\":\"$CLIENT_ID\",\"name\":\"client-mac\",\"compression\":\"metadata\"}"
curl -X POST -H "X-API-Key: $API" -H 'Content-Type: application/json' \
  http://127.0.0.1:8384/rest/config/folders \
  -d "{\"id\":\"dlcos-vault\",\"label\":\"dlcOS Vault\",\"path\":\"/home/<user>/vault\",\"type\":\"sendreceive\",\"devices\":[{\"deviceID\":\"$CLIENT_ID\"}]}"
curl -X POST -H "X-API-Key: $API" http://127.0.0.1:8384/rest/system/restart
```

Client accepts the folder share notification on their end, points it at wherever they want the vault to live locally. Confirmed working: both sides show "Up to Date" within a couple minutes, ~19MB memory footprint on the appliance side — trivial even on 6GB RAM.

## 6. Install dlcOS

Identical to the [Quickstart](client-quickstart.md) — no GitHub account needed, repo is public:

```bash
claude plugin marketplace add Digital-Life-Coach/dlcOS
claude plugin install dlcOS@dlcOS
```

Confirmed working on this test rig with zero auth friction — same command a client would run, this proves it works headless on Linux, not just Mac.

## 7. Run the setup wizard — **not yet tested**

Intended flow: open Claude Desktop on a separate machine (doesn't have to be the appliance itself — the appliance runs the CLI only), connect remotely into the appliance's `claude` CLI session, `cd ~/vault`, run `/dlcOS:setup`.

**Open questions, not yet answered:**
- Exact mechanics of Claude Desktop's remote-CLI connection to a headless box, and whether it needs the CLI pre-authenticated (`claude login` over SSH first) or handles auth through the Desktop app's own session.
- What the actual "ceiling" is for concurrent cloud-model CLI sessions on 6GB RAM / 2012 dual-core — inference itself is remote, so the constraint is Node/V8 process overhead and CPU parallelism, not model size. No real numbers yet, needs a live load test once a CLI is authenticated.
- Backup story for the appliance itself (this vault is the *client's* copy, not primarily this box's, but the appliance should still not be a single point of failure).
- Multi-client hardware model: one box per client (simple, what this doc assumes) vs. one beefier shared box (the trashcan Mac Pro) with per-client isolation (containers/users) — undecided.

---

## Delivery model (as of 2026-08-29)

Plan is to build/image the appliance in Justin's office, then deliver it ready-to-go with a smart plug for on/off — client just plugs it in, no setup burden on their end beyond accepting the Syncthing folder share.

**Known risk, not yet mitigated:** this is 13+ year old consumer hardware with no warranty. Fine for personal/test use; a real liability question for a paying client if it fails at their site with your name on the delivery. Decide explicitly per client whether the age of the hardware is disclosed/acceptable, versus reserving old hardware for lower-stakes use and selling new hardware to clients who need reliability guarantees.
