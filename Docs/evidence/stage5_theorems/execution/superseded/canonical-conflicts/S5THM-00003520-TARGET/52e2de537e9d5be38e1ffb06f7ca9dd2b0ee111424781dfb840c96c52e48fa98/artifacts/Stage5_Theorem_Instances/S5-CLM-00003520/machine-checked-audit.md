# Machine-checked audit

The target package is prepared for a trust-zero Master replay.  The declared
root is `rank_3_3_transport`; its expression digest is bound in
`machine-closure.json`.  The declaration census is content addressed to the
pinned provider source and contains no unresolved placeholder or claim-specific
oracle.  Dependency edges are acyclic and the remaining machine cut set is
empty.

This worker record is semantic/evidence preflight only.  The required command
is the task-local checker with `--no-lean`; Lean, Lake, and Elan are reserved
for the canonical Master after harvest.
