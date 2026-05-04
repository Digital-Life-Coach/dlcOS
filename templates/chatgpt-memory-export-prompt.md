# Memory Export Prompt

*Used during `/dlcOS:setup` Stage 4a (yes-path). Paste this into ChatGPT or Gemini to dump everything they remember about you. Bring the output back into the Code session — the wizard will synthesize it into your `about-me.md` and Settings → Memory paste block.*

*Source: `claude.com/import-memory`. If Anthropic updates their import flow, refresh this template.*

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

## What to do with the output

1. Copy the entire response from ChatGPT / Gemini.
2. Come back to your Claude Code session and paste it as your next message.
3. The wizard takes it from there — synthesizes, dedupes, writes your `about-me.md`, and builds your Settings → Memory paste block.

*If you don't have a ChatGPT or Gemini history, no problem — pick the "no" path in Stage 4a and the wizard runs a structured interview from scratch.*
