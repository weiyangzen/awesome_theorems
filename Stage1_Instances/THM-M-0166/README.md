# THM-M-0166 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Hopf-Rinow theorem. It starts from the
uniform `L0 / rework_required` baseline and does not treat the manifest's historical `已验证` label
as proof or source credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | On a connected finite-dimensional Riemannian manifold, metric completeness implies that every pair of points is joined by a length-minimizing geodesic | The precise mathlib object model, regularity, and elaborated expression belong to the statement phase |
| Classical equivalences | metric completeness, geodesic completeness, compactness of closed bounded subsets, and global exponential-map reachability | These are related Hopf-Rinow formulations, not interchangeable without checked bridges |
| Local geometry | geodesics, exponential map, normal neighborhoods, length and Riemannian distance | Candidate dependency surface only |
| Global argument | continuation of geodesics, minimizing limits, compactness/properness, connected-component propagation | Proof architecture only; no closure claimed |
| Degenerate boundaries | empty/disconnected manifolds, identical endpoints, zero dimension, and non-finite-dimensional or non-Riemannian spaces | No convention is silently selected; statement work must test each boundary |
| Foundations | Lean 4 kernel and pinned mathlib with an explicit classical/choice/quotient policy | Exact toolchain, imports, dependency closure, and TCB remain open |

The root deliberately freezes the forward, minimizing-geodesic consequence described by the
repository entry, rather than claiming the entire family of equivalences. The stronger equivalence
package is retained as candidate statement and proof scope. Structured binders, exclusions, and
status are in `intake.json`; source fidelity is tracked in `source_statement_crosswalk.md`.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
No dependent node is credited by this intake.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: no canonical declaration, normalized expression hash, environment
fingerprint, checked transport, or mutation result exists. The theorem is not complete.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They establish target
membership, standard consistency, JSON syntax, and local dossier hygiene only; they are not Lean
kernel evidence.
