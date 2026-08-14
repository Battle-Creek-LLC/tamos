# Artifact — proposal

Inherits `register-declarative.md`.

APPLIES WHEN:  writing or revising a document that asks a buyer to commission
scoped work.

RULES:
- Mark certainty this way, in place of tags: `firm` or `estimate` on each date
  and price the document states, an Assumptions entry for any claim you can't
  stand behind, and nothing on the rest — unmarked means firm.
- Cite this way, in place of file:line and URLs: name where each world-claim
  came from, in the sentence or the section carrying it ("from your intake
  call").
- Put the buyer's time in one table as person-hours, totalled; a process step
  repeats a row's hours and adds none.
- Name each buyer-supplied input under "What I need from you" with what happens
  to scope if it doesn't arrive.
- Add a Risks entry for each buyer-supplied input whose late arrival moves the
  delivery date.
- Name who performs each step under "The process"; name no actor for a step no
  person performs.
- Leave a `{{TOKEN}}` naming any value the source material doesn't give; a token
  in a table row carries into that table's total.
- State one total price; count a schedule that sums to it as part of that price.
- Put a second priced engagement in a second proposal.

SHAPE:
```
# <engagement name>

- **For:** <buyer, company>
- **From:** <author, org>
- **Date:** <date>

## What you'll have at the end
<the deliverable, and the date it lands (firm | estimate), or {{DATE}} if the
source material gives none>

## What it covers
- **<outcome>** — <the question it answers>

## How it runs
<where these commitments came from>

| Your commitment | Person-hours |
|---|---|
| <item> | <n>h |
| **Total** | **<total, carrying any row's token>** |

### The process
- **<step>** — <who does what> *(your time: <n>h, if the step uses any)*

## What I need from you
- **<input or access>** — <what happens to scope if this one doesn't arrive>

## Assumptions, exclusions and risks
### Assumptions
- <a statement of fact the buyer can confirm or contradict, and where it came
  from>
### Exclusions
<what is not covered; the engagement that covers it, where one is named>
### Risks
- **<risk>** <consequence, and who controls it>

## Price
<price (firm | estimate), or {{PRICE}} if the source material gives none>,
<fee basis>. Includes <what is in the price>.

## Next step
<one action the buyer can start today>
```

AVOID:
- Hedged scope ("may include", "as appropriate", "up to").
- Listing capabilities or credentials where an outcome belongs.
