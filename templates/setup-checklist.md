# Setup Checklist

Optional things worth setting up, checked by `/dlcOS:end` at the close of every session. Anything marked `pending` gets a one-line nudge; `done` and `dismissed` items go quiet.

**To dismiss something you don't want:** change its status to `dismissed` (just edit the word below, or tell Claude "dismiss the semantic search reminder" and it'll do it for you). To bring a dismissed item back, change it to `pending`.

| Item | Run | Status |
|---|---|---|
| See what Claude remembers locally, edit or clear it | `/dlcOS:memory-harden` | pending |
| Semantic search over your vault (faster, better `librarian` results) | `/dlcOS:setup-librarian-index` | pending |
| A daily morning brief (tasks, projects, inbox count) | `/dlcOS:morning-brief --setup` | pending |
| Add another Wiki area beyond what you started with | ask Claude — "add a Wiki area for ___" | pending |

*Auto-updated by `/dlcOS:end`: memory-harden, semantic search, and morning-brief flip to `done` automatically once their setup marker exists — no need to update those by hand.*
