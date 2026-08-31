# Environment

*Subject: **the machines.** Answers: **What runs where?***

*Canonical location for the practical setup — which machines exist, what runs on them, how they're reached, and the gotchas that have already cost someone an afternoon.*

*This is the file an assistant should read before touching anything technical, and update after it learns something the hard way.*

---

## Machines

<!-- Name, hardware, OS, where it physically lives, what it's for. Include hostnames and any fixed addresses or DHCP reservations. -->

## What Runs Where

<!-- Services, daemons, scheduled jobs. Which machine each runs on, and what breaks if it stops. -->

## Access

<!-- How each machine is reached, and from where. Which direction the trust runs — this is the detail people always get wrong when debugging. -->

## Monitoring

<!-- What watches what, how often, and where alerts land. Note explicitly if a machine has no monitoring of its own. -->

## Gotchas

<!-- Things that have already gone wrong, and the fix. Each entry: the symptom first (that's what you'll be searching for), then the cause, then the fix. -->

---

*One home per fact. If a gotcha is really a settled choice, it belongs in `decisions.md` instead.*
