# Artifact — proposal

Inherits `register-declarative.md`.

APPLIES WHEN:  asking a buyer to commission scoped work.

RULES:
- Mark certainty as `firm` or `estimate` on the date and the price, and put any
  claim you can't stand behind in Assumptions.
- Put the buyer's time in one table as person-hours, totalled; a process step
  may repeat a row's hours and may not add any.
- Name each buyer-supplied input under "What I need from you" with what happens
  to scope if it doesn't arrive.
- Add a Risks entry for each buyer-supplied input whose late arrival moves the
  delivery date.
- Name who performs each step under "The process"; a step no person performs
  names none.
- Where the source material gives no price, date, duration, person-hours, buyer,
  or deliverable, leave a `{{TOKEN}}` naming the gap.
- State one total price; a schedule that sums to it is part of that price.
- Put a second priced engagement in a second proposal.

SHAPE:
```
# <engagement name>

- **For:** <buyer, company>
- **From:** <author, org>
- **Date:** <date>

## What you'll have at the end
<the deliverable, and the date it lands> (firm | estimate)

## What it covers
- **<outcome>** — <the question it answers>

## How it runs
| Your commitment | Person-hours |
|---|---|
| <item> | <n>h |
| **Total** | **<n>h** |

### The process
- **<step>** — <who does what> *(your time: <n>h, if the step uses any)*

## What I need from you
- **<input or access>** — <what happens to scope if this one doesn't arrive>

## Assumptions, exclusions and risks
### Assumptions
- <a statement of fact the buyer can confirm or contradict>
### Exclusions
<what is not covered; the engagement that covers it, where one is named>
### Risks
- **<risk>** <consequence, and who controls it>

## Price
<price, or {{PRICE}} if the source material gives none> (firm | estimate),
<fee basis>. Includes <what is in the price>.

## Next step
<one action the buyer can start today>
```

AVOID:
- Hedged scope ("may include", "as appropriate", "up to").
- Listing capabilities or credentials where an outcome belongs.
