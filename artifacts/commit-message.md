# Artifact — commit message

Inherits `register-declarative.md`.

APPLIES WHEN:  writing a git commit subject and body.

RULES:
- Subject: imperative mood, ≤50 chars, no trailing period ("Add retry to fetch").
- Blank line, then body wrapped at 72 chars.
- Body explains *why*, not *what* — the diff already shows what changed.
- Reference the issue/ticket if the task names one; don't invent or hunt for one.

SHAPE:
```
Add retry to flaky upload path

Uploads failed ~2% of the time under packet loss; the caller had no
retry, so transient 503s surfaced as hard errors. Retry 3x with backoff.

Closes #214
```

AVOID:
- Past tense or "fixed stuff" subjects.
- Restating the diff line-by-line in the body.
- Bundling unrelated changes under one message.
