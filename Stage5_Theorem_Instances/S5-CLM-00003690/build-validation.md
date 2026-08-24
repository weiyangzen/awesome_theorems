# Build and validation record

Worker mode is task-local semantic/evidence preflight (`--no-lean`).  The
required command is recorded in `current-validation.json`; it checks exact
owned paths, sealed semantic evidence, placeholder-free Lean surfaces,
provider provenance comments, M0/R0 records, and strict-dominance release
shape.  Canonical Master alone runs Lean/Lake/Elan trust-zero compilation.

Replay matrix: clean source replay `pass`; import-substitution mutation
`reject`; local-shadow mutation `reject`; placeholder/oracle mutation `reject`;
deletion of each readability field `reject`; duplicate prose deletion `pass`.
