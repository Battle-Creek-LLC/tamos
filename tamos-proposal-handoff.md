# Handoff — finish the TAMOS `add-proposal-module` branch

## Context

Repo: `/Users/jstockdi/projects/bcl/tamos`
Branch: `add-proposal-module`, branched from `main` at `56f0ceb`. Unpushed.

TAMOS is a style guide for agent prose, organised in tiers. Read `AGENT-STYLE.md`
first — it holds the registry and the cascade rule. Then `docs/contributing.md`,
which defines the process you must follow.

Two commits are on the branch:

- `4d1f689` — adds `artifacts/proposal.md`, `skills/proposal/SKILL.md`, and the
  registry row in `AGENT-STYLE.md`
- `955463f` — adds an anti-antithesis rule to `register-declarative.md`, and
  fixes three instances the new rule surfaces (one in that register, two in the
  proposal module)

`TAMOS-IMPROVEMENTS.md` is untracked in the working tree and predates this work.
Leave it alone.

## What the branch adds, and why

### 1. `artifacts/proposal.md` — a new Tier-2 module

Governs client-facing documents that ask a buyer to commission scoped work.

Every pre-existing Tier-2 module governs agent-to-developer output. A proposal
addresses a buyer, which changes how the declarative register's certainty rule
works in practice. The module's central delta:

> certainty is expressed as named exclusions and correctable assumptions, and the
> `verified|believed|guessed` tags are dropped — they read as hedging to a buyer.

**This is the decision most likely to be challenged.** `contributing.md` rule 4
forbids contradicting an inherited rule. The claim is that this *specialises* the
inherited certainty rule rather than contradicting it — it says how that rule
manifests in this artifact. If a validator finds that unconvincing, the fix is
either to reword the delta so the specialisation is explicit, or to relocate the
rule. Do not carve out an exception.

### 2. Anti-antithesis rule in `register-declarative.md`

> State what is true and stop. Don't define a thing by contrast with what it
> isn't ("X, not Y" / "X rather than Y"); replace the rejected half with a
> concrete number, noun, or consequence.

**Placement is deliberate and is the second thing likely to be challenged.** It
went in the declarative register, not `core.md`, because the guide's own rules
use the construction heavily and legitimately — "Comment the *why*, not the
*what*", "Say what changed since the last update, not the whole history". In a
terse imperative the contrast disambiguates and compresses. The defect only
appears in descriptive prose written for a human reader, so the rule is scoped
to output. Existing artifact modules keep their contrasts, intentionally.

If `dogfood-inspector` flags the modules' own "X, not Y" lines, that scoping
argument is the answer — but check whether the rule's wording makes the scope
clear enough to survive without the argument. If it doesn't, tighten the wording.

## Work remaining

1. **Run the five adversarial validators.** `contributing.md` says a module ships
   only after surviving all five. `/tamos:tamos-validate` runs them, or invoke
   the agents in `agents/` individually: `contradiction-hunter`, `bloat-auditor`,
   `ambiguity-attacker`, `cascade-breaker`, `dogfood-inspector`. Expect the two
   decisions above to take the most fire. Fix what they land; push back in the PR
   description on what they get wrong.

2. **Consider one addition to `artifacts/proposal.md` — not yet written.** A
   three-way register split for proposals, proposed but never agreed:

   | Work described | Register | Example |
   |---|---|---|
   | Machine or automated work | Impersonal | "Automated analysis does the collection" |
   | Judgement | First person | "**I** find where the system contradicts the plan" |
   | Buyer obligation | Second person | "**You** grant read-only access" |

   The argument for it: direct address assigns agency, and in a scope document
   hiding the actor is how delivery disputes start. The split also reinforces
   what the buyer is paying for — the machine collects, the advisor thinks.
   Decide whether this earns a RULES line or is too situational to enforce.

3. **Open the PR** to whatever remote `main` tracks. The user intends to submit
   this to the TAMOS maintainers. The PR description should carry the rationale
   for both contested decisions, since `contributing.md` requires rationale to
   live in the PR rather than in the module.

## Constraints

- Tier-2 modules use exactly four slots, in order: `APPLIES WHEN`, `RULES`,
  `SHAPE`, `AVOID`. No other sections.
- RULES are imperatives only. No rationale — it goes in the PR or `docs/`.
- A module states only its **delta** over what it inherits. Re-stating an
  inherited rule is a defect (`cascade-breaker` checks this).
- Every file in the repo, including docs, is held to the register it preaches
  (`dogfood-inspector` checks this).
- Do not add rationale prose to `core.md` or either register.

## Working example to test against

A real proposal written under this module is at
`/Users/jstockdi/projects/bcl/smartlandlord/docs/proposal-technology-assessment.md`.
It is a live client document with a `{{PRICE}}` placeholder. Read it to check
the module's SHAPE against something real, but **do not edit it** — it belongs
to a separate engagement and is not part of this branch.
