# THM-M-0996 release-phase decision

Item: `S56-M-0996-RELEASE`

Base revision: `b62c08f262435e44a30ad3fc88a4712e3954afc7`

Decision timestamp: `2026-07-15T14:20:00+08:00`

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`; the authoritative
root vector remains `H2/M4/R4`; `audit_complete=false`; and
`theorem_complete=false`. No receipt is accepted and neither `AUDIT-Z` nor
`THEOREM-Z` is issued.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE` because
`S56-M-0996-VALIDATION` is provisional `[_]` worker evidence with
`accepted=false` and `release_grade=false`, not a master-accepted predecessor.
The first mathematical theorem failure is `M0996-L-GENERAL.kernel_closure`.
`GeneralSetEnlargementBound halfspaceProfile` remains an explicit premise of
every available root composer, so there is no premise-free declaration of
`GaussianIsoperimetricTarget`.

## Evidence reconciliation

The selected statement faithfully expresses the finite-dimensional standard
Gaussian enlargement comparison against an equal-measure unit half-space. A
fresh target-scoped replay elaborates the statement, one conditional
obligation-tree composition, and 34 genuine partial proof bodies under
`--trust=0`. Those bodies cover useful coordinate, Gaussian-CDF, half-space,
profile, dimension, and conditional-composition facts.

They do not close a frozen obligation. The six supported nodes retain
`planned:v1` fingerprints, the registry records zero closed obligations, and
the authoritative graph cut remains `M0996-L-HALFSPACE` and
`M0996-L-GENERAL`. The current proof replay succeeds even though the historical
validation receipt records an earlier Lake-resolution failure; the current
result does not rewrite that receipt or turn same-worker warm evidence into
dependency acceptance.

The intake authority stays `H2/M4/R4`. Later provisional proof and validation
evidence supports only a nonaccepted `H2/M3/R4` observation. The weaker state
controls because the graph still has empty evidence links, planned validation
IDs, pending source crosswalks, and incomplete provenance.

`AUDIT-Z` independently fails: the primary theorem/page, hypotheses,
conventions, corrections, and errata have not received pinpoint inspection or
independent H0 acceptance; required readable nodes and independent R0 review
are also open. `THEOREM-Z` additionally fails exact-root, foundation, complete
transitive trust/provenance, immutable-input, cold/offline, SBOM/license,
distinct-runner, independent-verifier, protected-CI, and deterministic-bundle
gates.

## Self-test

The release checker binds the current target, manifest, blueprint, execution
DAG, toolchain, registry, graph, proof receipt, validation receipt, and release
decision hashes. It delegates the current trust-zero `Statement ->
ObligationTree -> Proof -> Validation` replay to the target validation verifier,
whose Lean children run under Bubblewrap network denial with disposable target
outputs. The replay is warm nonrelease evidence: no `lake update`, `lake build`,
dependency clone, or dependency fetch is performed, and the shared `.lake`
symlink is not clean immutable release input.

The scoped command record is stored in `release-receipt.json`. Structural,
target-manifest, obligation-graph, direct statement elaboration, partial proof
replay, predecessor validation, release reconciliation, JSON, source hygiene,
and whitespace checks all pass for this negative decision. Passing those checks
proves that the verdict is internally consistent; it does not prove the theorem
or satisfy a release gate.

## Retry boundary

Implement `M0996-L-GENERAL` and its analytic prerequisites without placeholders,
freeze exact fingerprints and complete child-to-parent provenance/composition
evidence, and obtain dependency-ordered master acceptance. Then close independent
H0/R0 and `AUDIT-Z`, full foundation/TCB and supply-chain evidence, immutable
cold/offline reproduction, two distinct signed runners, an independent minimal
verifier, protected adversarial CI, deterministic bundling, `THEOREM-Z`, and
final master acceptance.
