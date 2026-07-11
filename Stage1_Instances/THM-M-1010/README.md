# THM-M-1010 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Skorokhod representation theorem. The
metadata label `已验证` is untrusted discovery input and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | weak convergence of Borel probability measures on a Polish space implies a common-space coupling converging almost surely | Exact Lean binders and elaboration belong to the statement phase |
| Topology and measure | Polish topology, Borel measurable space, probability measures, weak convergence against bounded continuous functions | Compatibility of mathlib's topology and measurable-space instances must be checked |
| Construction | existential common probability space with measurable `XSeq n` and `X` | No particular sample space or construction is frozen yet |
| Marginals | the pushforward law of `XSeq n` is `muSeq n`, and the law of `X` is `mu` | `Measure.map` side conditions and equality orientation remain statement obligations |
| Convergence | `XSeq n` tends to `X` almost surely in the topology of `S` | Convergence in distribution or probability is not an acceptable substitute |
| Generalizations | separable-support and non-Polish variants | Excluded from the canonical root unless later supplied by checked transports |
| Foundations | Lean 4 kernel and pinned mathlib | Import, environment, axiom, and TCB fingerprints remain open |

The root deliberately uses the standard Polish-space form: it is strong enough to express the
named theorem without silently claiming broader variants whose hypotheses differ. Constant and
Dirac cases are included. Existing random variables are not inputs; the conclusion constructs new
representatives on a single probability space.

## Open phase DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only intake is addressed here. Later phases must freeze the exact expression, audit formal anchors,
build the typed obligation graphs, close proof bodies, validate trust and provenance, and obtain
independent release evidence in that order.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the statement gate: there is no elaborated expression hash, environment fingerprint, checked
transport, or mutation record. The theorem is not complete.

## Validation

The exact intake checks and results are recorded in `validation.md`. They establish manifest
membership, repository-standard consistency, JSON syntax, and dossier-local hygiene only. No Lean
declaration or kernel result is claimed.
