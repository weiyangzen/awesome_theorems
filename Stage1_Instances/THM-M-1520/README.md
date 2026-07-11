# THM-M-1520 rev-5.6 intake

This planned instance disambiguates the queue label "Liouville's theorem" as the classical
Hamiltonian result: Hamiltonian flow preserves phase-space (Liouville) volume. It does not cover
the unrelated complex-analysis, ODE, or Arnold-Liouville theorems.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Geometric model | finite-dimensional symplectic manifold `(M, omega)` | exact mathlib structures and universe parameters remain open |
| Dynamics | smooth Hamiltonian, its Hamiltonian vector field, and local flow | sign convention and local-flow API must be frozen next |
| Exact root | pullback of `omega^n / n!` by each defined flow map equals itself | no Lean expression or elaboration fingerprint yet |
| Equivalent route | zero divergence in canonical coordinates | candidate reduction, not a credited equivalence |
| Stronger route | flow preserves `omega`, hence its top exterior power | candidate proof architecture only |
| Measure corollary | invariance of induced volume on measurable sets | requires a checked form-to-measure bridge |
| Exclusions | other theorems named Liouville; quantum/empirical claims | never interchangeable with this target |
| Trust boundary | Lean 4 kernel and pinned mathlib | exact toolchain, dependency closure, and foundation profile remain open |

The structured claim, binders, hypotheses, boundary cases, and exclusions are in `intake.json`.
The source-to-statement relationship and its unresolved audits are in
`source_statement_crosswalk.md`. Later phases must not silently replace the geometric claim with
only a Euclidean special case or with the assumption that an arbitrary map preserves volume.

## Open task DAG

1. `S56-M-1520-STATEMENT`: select minimal pinned imports; freeze the sign convention, local versus
   complete flow semantics, exact Lean expression, environment fingerprint, and mutation tests.
2. `S56-M-1520-ANCHOR_AUDIT`: inspect mathlib and external Lean candidates at immutable revisions;
   complete primary-source pinpoint and errata review.
3. `S56-M-1520-OBLIGATION_TREE`: freeze typed proof, provenance, trust, evidence, documentation,
   and workflow graphs without collapsing form, flow, and measure bridges.
4. `S56-M-1520-PROOF`: implement or pin/import exact proof bodies with no weakened substitute.
5. `S56-M-1520-VALIDATION`: run kernel, axiom, provenance, composition, and hermetic replay gates.
6. `S56-M-1520-RELEASE`: reconcile accepted evidence and independently decide completion.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
the exact-statement gate: the repository has neither a canonical Lean declaration nor an elaborated
expression/environment fingerprint for this target. No historical "verified" label is accepted as
proof credit, and the theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish target membership, standard integrity,
JSON syntax, dossier structure, and the absence of forbidden proof devices only. No Lean theorem is
introduced in this intake phase.
