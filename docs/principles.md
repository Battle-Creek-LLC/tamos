# Principles

Five ideas justify every terse rule in the enforced layer. Reference-layer
prose: not loaded at run time, written so a maintainer can edit the rules
without guessing at intent.

## 1. Two registers, never conflated

Agent prose flows in two directions, and they optimize for opposite things.

- **Imperative register — human → agent.** Prompts, specs, instructions.
  Optimized for *constraint and disambiguation*. Its failure mode is
  under-specification: the agent fills the gap with a guess.
- **Declarative register — agent → human.** Reviews, reports, commits, docs.
  Optimized for *scannability and calibrated confidence*. Its failure mode is
  confident filler: prose that reads complete but asserts more than was verified.

A rule that improves one register often harms the other. "Add more context"
helps a prompt and bloats a report. TAMOS keeps them in separate modules so a
rule always knows which direction it serves.

A mixed artifact (a CLAUDE.md, an issue an agent both reads and writes) leads
with the imperative and footnotes the prose.

## 2. Token economy: enforce little, reference much

Context is rent. Anything loaded every turn — system prompt, CLAUDE.md — pays
that rent forever, so it must be dense. Anything loaded on demand — a file an
agent opens only when it is about to write a PR body — costs nothing until used.

So TAMOS splits every rule into two layers:

- **Enforced layer:** the imperative, stripped of rationale. Always on. Dense.
- **Reference layer:** the *why*, the examples, the edge cases. On demand.

The common mistake is putting rationale in the enforced layer. The agent only
needs `Don't restate the prompt back`. The *because it signals padding* is for
the human and lives here.

## 3. Dogfooding is the consistency check

A style guide for terse agent writing that is itself bloated has failed its
own first rule. If a section cannot be stated as a handful of imperatives, the
section is not crisp enough yet. The enforced layer of TAMOS is written in the
declarative register it preaches — that is intentional, and the
`dogfood-inspector` agent exists to keep it honest.

## 4. Calibrated confidence over fluent confidence

The single highest-leverage rule in the declarative register: distinguish what
was **verified** (ran it, here is the output) from what is **believed** (this
should work) from what is **guessed**. Fluent prose hides this distinction;
TAMOS forces it into the open with a controlled vocabulary. Confident hedging
("it appears that probably…") is banned because it claims both certainty and
deniability at once.

## 5. The reader might be another agent

Unlike Chicago's reader, TAMOS's reader is often a model with no memory of
context, processing text probabilistically. That justifies things a human
style guide would call verbose: repeating key constraints, naming referents
instead of "it/this," and writing self-contained chunks. Redundancy that buys
disambiguation is not bloat.
