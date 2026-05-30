# Artifact — PR review

Inherits `register-declarative.md`.

APPLIES WHEN:  producing a code review (any diff, PR, or changeset).

RULES:
- Group findings by severity: blocking, then optional. Label each.
- Quote the offending line before critiquing it.
- One finding per point. Don't bundle a bug and a nit in one bullet.
- Propose the fix, don't just name the problem.
- Tag certainty per finding (inherited): `verified` you reproduced it vs
  `believed` from reading.
- No praise-padding. Omit "great work" preambles; note strengths only if they
  change a decision.

SHAPE:
```
## Blocking
- `path/to/file.py:42` — <one-line problem>. <proposed fix>. [verified]
    > offending line quoted here

## Optional
- `path/to/file.py:88` — <nit>. <suggestion>. [believed]
```

AVOID:
- Restating the diff back to the author.
- Mixing style nits into correctness findings.
- "Consider maybe possibly" — state the finding or drop it.
