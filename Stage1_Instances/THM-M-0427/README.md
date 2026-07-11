# THM-M-0427 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Artin L-functions. It does not inherit proof
credit or accepted state from the legacy `S1-M-081` Lean file or from the source label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | The Artin L-function attached to a finite-dimensional complex representation of the Galois group of a finite Galois extension of number fields | The source queue says only "L-functions of Galois representations"; source pinpoints and the exact analytic claim remain open |
| Definition layer | Euler factors using inertia invariants and Frobenius conjugacy classes, and their Euler product | No concrete Lean Artin Euler-factor API is credited |
| Analytic layer | Meromorphic continuation and functional equation as the classical Artin theorem package | Artin holomorphy for nontrivial irreducibles is explicitly excluded because it is a conjecture in general |
| Specializations | Trivial representations/Dedekind zeta and one-dimensional abelian characters/Hecke L-functions | These are candidate reductions, not proof credit |
| Lean discovery | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_081.lean` and adjacent mathlib representation, ramification, Frobenius, Dirichlet-L, and Dedekind-zeta APIs | The legacy file is an abstract model and anchors, not the exact theorem |
| Foundations | Lean 4 kernel with pinned mathlib; classical mathematics expected | Exact toolchain, imports, axioms, and environment fingerprint are deferred to the statement phase |

The canonical claim, ordered mathematical data, exclusions, and provisional Lean target are recorded
in `intake.json`. Source genealogy and the unresolved claim-to-statement choices are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first failed theorem gate is
the exact-source/exact-statement gate: the manifest wording does not distinguish the definition,
meromorphic continuation, and functional equation, and no normalized Lean expression or checked
transport is frozen. The theorem is not complete.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Every successor remains open and is owned by its separate rev-5.6 node.

## Validation

The commands in `validation.md` establish target membership, standard consistency, JSON syntax, and
local dossier hygiene only. No Lean theorem or kernel closure is claimed.
