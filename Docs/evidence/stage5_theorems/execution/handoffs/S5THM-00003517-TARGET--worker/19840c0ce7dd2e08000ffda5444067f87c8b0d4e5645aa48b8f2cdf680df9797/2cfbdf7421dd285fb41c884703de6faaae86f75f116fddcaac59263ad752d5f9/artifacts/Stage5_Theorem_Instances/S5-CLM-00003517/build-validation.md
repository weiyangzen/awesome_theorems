# Build validation

The frozen command is `complete-target-semantic-proof-debt`.  It checks strict
JSON, content-addressed source bindings, exact provider imports, forbidden
Lean constructs, M0 machine closure, R0 readability, and the provisional
release conjunction.  Each of `Statement.lean`, `Proof.lean`, and `Audit.lean`
is then elaborated by the pinned Lean toolchain with `--trust=0` and a cold
from-source environment.  Standard output and error digests are recorded in
`receipts/current-validation.json`.
