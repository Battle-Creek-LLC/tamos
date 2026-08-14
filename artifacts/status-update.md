# Artifact — status update

Inherits `register-declarative.md`.

APPLIES WHEN:  reporting progress or handing off mid-task.

RULES:
- Lead with state: `done` | `in-progress` | `blocked`.
- Surface blockers first — they are what the reader can act on.
- Say what changed since the last update, not the whole history.
- End with the single next action and who owns it.
- A skipped check maps to `in-progress`, never `done`.

SHAPE:
```
**blocked** — auth migration

Since last update: moved 3 of 5 endpoints to the new token flow.
Blocker: staging secret not provisioned; can't test /refresh.
Next: @jonah to provision STAGING_JWT_KEY, then I finish the last 2.
```

AVOID:
- Narrating process ("first I opened the file, then I…").
- Burying the blocker under a progress recap.
