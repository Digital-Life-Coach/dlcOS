# dlc-setup wizard plan

PLACEHOLDER. The full setup-wizard-as-plan lands in Step 7 of the dlcOS v1 build.

When complete, this file walks a new client through:

1. Identity capture (writes to `${VAULT_ROOT}/about-me.md` + seeds Claude memory)
2. Vault scaffold (Inbox/, GTD/, Wiki/, Reference/Dailies/ + empty-state templates + starter `CLAUDE.md` with `<!-- dlcos:vault-root -->` and `<!-- dlcos:office-hours-ical -->` lines)
3. Skill install verification (smoke test all 5 dlc-* skills)
4. Memory seeding (capability level L1-L5, coaching context)
5. (reserved for `dlc-inbox-triage` walkthrough in v1.1)
6. Brief preview (run `dlc-morning-brief` setup conversation; per-client brief spec written)
7. First save-plan demo (round-trip via dlc-resume-plan)
8. Handoff (post-onboarding checklist + when-to-use-which-skill + Office Hours pointer)

Target run time: ≤45 minutes on a fresh macOS account.
