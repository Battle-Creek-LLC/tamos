# Use cases — what TAMOS governs, and how to engage it

**Ask for an artifact and its module loads. Ask for anything else and it stays
out.** The line is drawn on *intent*, not on phrasing: "anything wrong with
this?" engages `pr-review` as reliably as "review this PR", while "shorten the
timeout to 5s" engages nothing, because it is a code edit rather than a request
for prose. This page is the vocabulary that sits on that line.

Two things are always on once the plugin is installed, with no words required:

- **`core.md` + `register-declarative.md`** — every answer the agent gives you is
  governed: answer first, certainty tagged (`verified` / `believed` / `guessed`),
  no throat-clearing, failures reported plainly.
- **`AGENT-STYLE.md`** — the registry, so the agent can find the right module.

Everything below is a **producing skill**. Say the words; the module loads.

## The vocabulary

| Say this | Engages | You get |
|----------|---------|---------|
| "tl;dr", "summarize", "condense this", "too long — the gist" | `tldr` | bottom line, then a table or bulleted deltas |
| "write the commit message", "what should I call this commit" | `commit-message` | imperative subject ≤50 chars, body explaining *why* |
| "review this", "does this look ok?", "anything wrong with this?", "thoughts?" | `pr-review` | findings split blocking / optional, each with a fix and a certainty tag |
| "status update", "where are we on X", "what's left", "write up the handoff" | `status-update` | `done`/`in-progress`/`blocked`, blocker first, one next action |
| "A or B?", "which way should we go?", "should we X or Y" | `elicitation` | one recommendation, tagged, plus an `Option \| Gives up` table |
| "review this spec", "check these requirements" | `spec-review` | requirements-quality findings — ambiguity, gaps, untestable clauses |
| "research X and report back" | `research-report` | cited findings, assumptions marked |
| "add a comment explaining this" | `code-comment` | a comment stating the constraint, not narrating the code |

Any skill is also directly invocable by name: `/tamos:tldr`, `/tamos:pr-review`.
Use that when you want the module for certain and don't want to phrase around it.

## How reliably each one engages

Measured against the shipped plugin, not asserted: 54 sessions in a live repo with
mid-task triggers, plus 224 sessions across the conditions that produced this
design. Method, data and caveats in `.exp/routing/`.

**Overall: 37/38 (97%) of asks engaged the right module. 0 false fires in 16 decoy
sessions.** Before this release the same suite scored 13/38 (34%).

| Module | Engages | |
|--------|---------|--|
| `tldr` | 8/8 | reliable |
| `commit-message` | 8/8 | reliable |
| `status-update` | 6/6 | reliable |
| `elicitation` | 4/4 | reliable |
| `spec-review` | 2/2 | reliable (small n) |
| `code-comment` | 2/2 | reliable *when you ask for it* — see below |
| `pr-review` | 7/8 | reliable; the miss was an oblique mid-task ask |

Direction is `verified`; exact magnitudes are `believed` — n=2 per fixture, one
model, and the prompts were written by the same person who wrote the fix.

## How you phrase it barely matters now

This was the main worry going in — that TAMOS would only respond to jargon and
miss you whenever you talked like a person. Measured on the shipped plugin:

| Register | Example | Before | Now |
|----------|---------|--------|-----|
| **jargon** | "tl;dr this", "write a commit message for this diff" | 4/10 | **10/10** |
| **natural** | "what should I call this commit?" | 4/12 | **12/12** |
| **oblique** | "anything wrong with this?" | 3/10 | **10/10** |
| **embedded** | "ok that's a lot — condense it" (mid-task) | 2/6 | **5/6** |

Speak normally. Oblique asks land as reliably as jargon; only triggers buried
mid-task after other work still slip occasionally. If you want a module for
certain, name it or use `/tamos:<module>`.

The precision side of the trade holds: across 16 decoy sessions TAMOS did not
fire on "shorten the timeout to 5s" or "why is my commit failing". It engages when you
ask for an artifact and stays out otherwise.

## Known gap — comments the agent writes on its own

`code-comment` engages reliably when **you ask** for a comment (2/2 measured).

The gap is the case where nobody asks: the agent writes code mid-task and should
apply the comment rules unprompted. Nothing consults a prose module during an
edit, and no skill description changes that — a skill fires on a request, and
there is no request. The fix is a `PostToolUse` hook on Edit/Write; it is not
built yet. Until then, comments written during ordinary coding are governed only
by the always-on layer, not by `artifacts/code-comment.md`.

## What TAMOS deliberately ignores

It stays out of asks that aren't for an artifact. Verified over 80 decoy
sessions — 16 on the shipped plugin, 64 across the configurations tested to get
there — with zero false fires in every one:

- "shorten the timeout to 5 seconds" — a code edit, not a `tldr`
- "why is my commit failing?" — debugging, not a `commit-message`
- "is there a status endpoint?" — a code question, not a `status-update`
- "summarize what this function does" — explaining code, not compressing prose

The declarative register still governs how those answers are written. The
artifact modules stay out.
