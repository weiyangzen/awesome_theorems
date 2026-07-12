# THM-M-1520 rev-5.6 statement

This planned instance disambiguates the queue label "Liouville's theorem" as the classical
Hamiltonian result: Hamiltonian flow preserves phase-space volume. `Statement.lean` freezes the
canonical-coordinate, complete-flow version and elaborates it against pinned mathlib. It does not
cover the unrelated complex-analysis, ODE, or Arnold-Liouville theorems.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Geometric model | canonical phase space `R^n x R^n` | represented by an L2 product of two `EuclideanSpace`s |
| Dynamics | `C2` Hamiltonian and a global `C1` flow solving Hamilton's equations | sign convention is `X_H = (dH/dp, -dH/dq)` |
| Exact root | every time map is `MeasurePreserving` for `volume` | `Stage1.THM_M_1520.LiouvilleStatement` |
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

1. `S56-M-1520-STATEMENT`: worker-elaborated canonical-coordinate global-flow target, environment
   fingerprint, and four negative identity mutations; master acceptance remains pending.
2. `S56-M-1520-ANCHOR_AUDIT`: inspect mathlib and external Lean candidates at immutable revisions;
   complete primary-source pinpoint and errata review.
3. `S56-M-1520-OBLIGATION_TREE`: freeze typed proof, provenance, trust, evidence, documentation,
   and workflow graphs without collapsing form, flow, and measure bridges.
4. `S56-M-1520-PROOF`: implement or pin/import exact proof bodies with no weakened substitute.
5. `S56-M-1520-VALIDATION`: run kernel, axiom, provenance, composition, and hermetic replay gates.
6. `S56-M-1520-RELEASE`: reconcile accepted evidence and independently decide completion.

## Intake verdict

Lifecycle remains `planned`; provisional root vector is `[H2, M3, R3]`. The exact Lean statement
elaborates, but this node proves no proposition. The next failed gate is the source/anchor audit, and
the full proof, composition, trust, hermetic, readability, and release gates remain open. No
historical "verified" label is accepted as proof credit, and the theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish target membership, exact elaboration,
the printed kernel expression fingerprint, and negative mutation behavior. `Statement.lean`
introduces definitions and a `Prop`, not a theorem or proof.
