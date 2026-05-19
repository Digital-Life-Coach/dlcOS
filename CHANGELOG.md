# Changelog — dlcOS

| Date | Summary |
|------|---------|
| 2026-05-18 | **v1.0.0 — first public release.** 5 core skills (`setup`, `save-plan`, `resume-plan`, `end`, `weekly-review`, `morning-brief`), guided setup wizard, 13 templates, client-facing docs (quickstart, skills reference, troubleshooting). `end` is now worktree-aware: detects sessions spawned in a git worktree (common when Claude Code launches from the macOS app), commits to the worktree branch, then merges back to `main` and removes the worktree — fixes the "commits never reached main" bug surfaced by Charlie 2026-05-17. Pending-Plans seeds v1.1 add-ons (`setup-email`, `setup-dashboard`). |
| 2026-05-02 | v0.2.0 — namespace rename: plugin `dlc` → `dlcOS`, marketplace `dlcos` → `dlcOS`, all skills lose `dlc-` prefix. Now invoked as `/dlcOS:save-plan` etc. Two skills ported (save-plan, resume-plan); 4 placeholders remain. |
| 2026-05-02 | v0.1.0 — repo bootstrapped. Initial scaffold: README, LICENSE (MacCog client-use), CHANGELOG, .gitignore, plugin manifests, 6 skill placeholders. |
