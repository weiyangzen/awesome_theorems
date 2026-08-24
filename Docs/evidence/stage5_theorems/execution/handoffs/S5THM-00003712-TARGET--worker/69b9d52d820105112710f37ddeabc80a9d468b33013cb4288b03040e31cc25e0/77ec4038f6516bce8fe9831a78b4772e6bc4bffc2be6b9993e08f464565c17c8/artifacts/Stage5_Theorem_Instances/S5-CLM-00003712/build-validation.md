# Build validation

Worker validation is intentionally limited to the claim-prescribed task-local
semantic/evidence preflight with `--no-lean`. No Lean, Lake, or Elan command was
invoked. The canonical Master must perform cold offline from-source elaboration
of `Statement.lean`, `Proof.lean`, and `Audit.lean` at trust 0 after harvest,
then replace worker-provisional expression and dependency observations with
recomputed values before acceptance.

The prescribed preflight passed with semantic-environment digest
`e341e417d563d1309d1e402ee27e6436aea528e4514abad0227de705a0acaf9f`.
