# S5-CLM-00003599 process audit

This target is the single FC-SORRY variant `ATV-00003599` owned by
`S5THM-00003599-TARGET`.  The frozen source record is
`Erdos1044.erdos_1044.variants.infimum_eq_two` in
`FormalConjectures/ErdosProblems/1044.lean`, revision
`2270d31e8dd611521f979de6d86da364930b7669`.

The intake binds the record, source byte range, declaration/type hashes,
provider revision, and Stage6 alias before any proof evidence is considered.
The statement crosswalk binds source and target root-expression digests and a
transitive constant census.  Anchors are content addressed and point back to
the frozen source bytes and the three claim-owned Lean surfaces.  The proof
unit inventory is a typed DAG: source statement, semantic environment,
definition expansion, root proposition, closure, and readability review are
distinct nodes with explicit dependencies and trust boundaries.

The worker preflight is deliberately `--no-lean`.  It checks strict JSON,
authority seals, exact identity, source-byte digests, no-shadowing patterns,
empty machine/readability cut sets, and the THM-M-0387 strict-dominance
certificate.  It does not invoke Lean, Lake, Elan, a repository checkout, or a
network provider.  Canonical Master replay remains the sole trust-zero build
authority.

Mutation cases cover provider-module substitution, declaration-header
substitution, source-byte mutation, semantic-environment deletion, and cold
replay cache removal.  Every mutation is recorded as rejected, with the
unmutated trace retained as the current release trace.
