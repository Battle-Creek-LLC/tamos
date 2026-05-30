# Artifact — code comment

Inherits `register-declarative.md`.

APPLIES WHEN:  writing an inline comment in source code.

RULES:
- Comment the *why*, not the *what*. The code already says what.
- Delete a comment that restates its line. Redundant comments rot.
- A `TODO` carries an owner and a condition ("TODO(jonah): remove after v2 ships").
- Match the surrounding comment density and idiom; don't over-annotate.
- Note the non-obvious: invariants, gotchas, why the obvious approach was rejected.

SHAPE:
```
# Retry only on 503; a 400 here means a malformed payload we can't fix by retrying.
for attempt in range(3):
    ...
```

AVOID:
- Restating code ("# increment i" above `i += 1`).
- Decorative banners and commented-out dead code.
- Bare `TODO` with no owner or condition.
