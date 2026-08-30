# Memory Export Prompt

*Used during `/dlcOS:setup` Stage 4a (yes-path). Run this against ChatGPT or Gemini to dump everything they remember about you, so the wizard can synthesize it into your `about-me.md` and Settings → Memory paste block.*

*Source: `claude.com/import-memory`. If Anthropic updates their import flow, refresh this template.*

---

## ⚠️ Read this before you paste anything

**Pasting the export into a chat sends every word of it to that model provider.** If part of why you're here is that you'd rather your life not sit on someone else's servers, that's exactly the wrong first move — and it's easy to avoid.

**Preferred: keep it local.** Save the export to a file and let your Claude Code session read it off your own disk. Nothing leaves your machine.

1. Run the prompt below in ChatGPT / Gemini.
2. Copy the output into a plain text file — e.g. `~/Desktop/memory-export.md`.
3. In your Claude Code session, say: *"Read `~/Desktop/memory-export.md`."*
4. Delete the file when the wizard is done with it.

**Second-best: paste it in chat.** Fine if you're not privacy-motivated and the export holds nothing sensitive. It does mean the whole export goes to the provider.

**Also worth knowing before you start:** these exports routinely contain more than you remember putting in them — other people's health, things told to you in confidence, family medical history, unresolved legal or personal matters involving named people. Stage 4a walks you through sorting that before anything gets written down. You do not have to hand over the whole file to get value out of it; you can hand over only the parts you want.

---

## Paste this into ChatGPT (or Gemini)

```
Please output everything you have stored in your memory about me. Include:

1. Personal facts (name, location, role, family, etc.)
2. Professional context (work, projects, clients, goals)
3. Preferences (communication style, working preferences, format preferences)
4. Recurring patterns or things I've asked you to remember
5. Tools, systems, and apps I use
6. Anything else you've inferred or learned about me over time

Format the output as a structured markdown document with clear sections. Be comprehensive — I'm migrating this context to a different AI system and don't want to lose anything. If a memory is from a specific conversation or context, note that. If you're not sure whether something is a memory vs. an inference, include it and label it.

Output only the memory content — no preamble, no summary, no commentary.
```

---

## What happens next

1. Get the export onto your machine (file preferred — see the warning above).
2. Point your Claude Code session at it.
3. The wizard **triages before it writes**: it sorts the export into your own durable facts, your own health information, anything about other people that was told to you in confidence, and plain practical reference — then asks you category by category what to keep and where it goes. Your health and other people's private information never go into the cloud-stored Settings → Memory block.
4. Then it synthesizes, dedupes, and writes your `about-me.md` plus your Settings → Memory paste block.

*If you don't have a ChatGPT or Gemini history, no problem — pick the "no" path in Stage 4a and the wizard runs a structured interview from scratch.*
