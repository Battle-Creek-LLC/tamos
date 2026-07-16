---
name: tldr
description: Compress a wordy message or output into a terse, scannable TL;DR (tables, bullets) without losing decision-relevant content. Use when asked to summarize, condense, "tl;dr", or shorten existing prose.
---

Produce a TL;DR of wordy input.

## Step 0 — pull the rules

Read `/Users/jstockdi/projects/bcl/tamos/artifacts/tldr.md` and apply its RULES, SHAPE, and AVOID.

## Source

Compress, in this order of preference:
1. The text passed to the skill, if any.
2. The content the user just pasted or referenced this turn.
3. The most recent long assistant message or command output.

If none exists, ask which message to compress — don't guess.
