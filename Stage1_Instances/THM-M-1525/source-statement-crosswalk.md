# Source-statement crosswalk

## Candidate primary sources

- Erwin Schrodinger, "Quantisierung als Eigenwertproblem (Vierte Mitteilung)," *Annalen der
  Physik* 81 (1926), 109-139. This is a historical primary candidate for the time-dependent
  equation; the exact equation/page, notation, assumptions, and any corrections have not yet been
  inspected from a stable scan.
- M. H. Stone, "On one-parameter unitary groups in Hilbert Space," *Annals of Mathematics* 33
  (1932), 643-648. This is a primary candidate for a rigorous autonomous self-adjoint-generator
  formulation, but its exact theorem text and its mapping to differentiable domain vectors remain
  to be inspected.

These bibliographic anchors are discovery leads, not `H0` evidence. The statement phase must select
the precise human theorem being formalized and record edition/scan, theorem or equation/page,
definitions, assumptions, and errata. An independent source review remains required.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Schrodinger equation" | time evolution `i hbar psi' = H psi` | typed equality in a complex Hilbert space | included; units and derivative open |
| Hamiltonian | self-adjoint energy operator, generally unbounded | operator plus explicit domain/self-adjointness API | included; representation open |
| initial state | datum at time zero | domain-qualified vector and initial equality | included; regularity open |
| solution/evolution | one-parameter evolution satisfying the equation | function `Real -> H`, differentiability, existence/uniqueness | included; exact strength open |
| conservation | unitary/norm and possibly energy preservation | checked consequences with hypotheses | conditional; source anchor open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_193.lean` inventories useful mathlib APIs and gives
a historical proposition-level normalization. Its Hamiltonian is bounded, while its key analytic
conditions are bare `Prop` fields and its solution contains further `Prop` fields. Consequently its
`StatementShape` does not establish the physical or analytic theorem and receives no rev-5.6 proof
credit. Its upstream searches and imports must be repeated against the pinned revision during the
later statement and anchor-audit phases.

Before `H0`, an independent reviewer must approve a row-by-row mapping from one exact source claim
to the Lean expression, including operator domains, differentiability, quantifier scope, units,
degenerate cases, assumptions, and errata.
