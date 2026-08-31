# Memory Index

*Lives at `Wiki/Knowledge/Memory/MEMORY.md`. This is the hub for everything durable in this vault.*

**If you are an AI working in this vault, this file is a required read before you write anything durable.** Claude Code loads it automatically because this folder is its memory directory. Every other tool — Codex, ChatGPT, or whatever comes next — is pointed here by `AGENTS.md` and must read it explicitly.

---

## The routing rule

Before writing a durable fact, work down this list and stop at the first match:

1. **A canonical file covers this subject** → write it there. Add or refresh a one-line pointer below.
2. **No canonical file fits** → create a shard in this folder (`Wiki/Knowledge/Memory/`), one fact per file, and index it below.
3. **The fact is already written somewhere** → update that copy. Do not write a second one.

**Never write the same fact in two places.** If you find a duplicate, collapse it to the canonical file and leave a link behind. Duplication is the failure mode this whole structure exists to prevent — it is how a memory system goes stale without anyone noticing.

If you genuinely cannot tell which file a fact belongs in, ask. One home per fact.

---

## Canonical files

These live one level up, in `Wiki/Knowledge/`. Each has exactly one subject. If you can't name the subject a fact belongs to, it probably doesn't need to be written down.

| File | Subject | Answers |
|---|---|---|
| [`me.md`](../me.md) | the person | Who am I? |
| [`voice.md`](../voice.md) | my output | How do I sound when I write? |
| [`preferences.md`](../preferences.md) | the work | How should work be done for me? |
| [`assistant.md`](../assistant.md) | the assistant | How should you behave? |
| [`decisions.md`](../decisions.md) | the past | What's settled, and why? |
| [`environment.md`](../environment.md) | the machines | What runs where? |

The boundaries are deliberate and they are about **subject**, not topic. "I want short answers" is the *work* (`preferences.md`). "Never patronise me" is the *assistant* (`assistant.md`). "I'm a singer" is the *person* (`me.md`). Three rules about communication, three different files, no overlap.

---

## Shards

Anything that doesn't fit a canonical subject lives here as its own file. One fact per shard, with frontmatter:

```markdown
---
name: <short-kebab-case-slug>
description: <one line, used to decide relevance later>
metadata:
  type: user | feedback | project | reference
---

<the fact. For feedback and project, add **Why:** and **How to apply:** lines.>
```

Link related memories with `[[slug]]`. A shard that later turns out to belong in a canonical file should be moved there and deleted here.

This folder is intentionally **not** write-protected — an assistant can add and remove shards. The control is that it's visible: it sits in `Wiki/Knowledge/`, in plain markdown, in your vault. Read it, edit it, delete anything you don't want kept.

---

## Index

*One line per shard. Newest first. Canonical files are in the table above and do not need listing here.*

<!-- - [Title](shard-name.md) — one-line hook -->
