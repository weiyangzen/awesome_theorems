# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the result to Abraham Robinson, gives 1959, and says
only "axiomatization of differentially closed fields". Stage0 repeats that metadata without
definitions, hypotheses, a theorem number, page, proof, or formal artifact. The manifest therefore
correctly treats `已验证` as untrusted metadata.

## Candidate human sources

- Abraham Robinson, "On the concept of a differentially closed field", *Bulletin of the Research
  Council of Israel*, Section F, volume 8 (1959), is the historical primary-source candidate
  suggested by the repository attribution. The exact issue, page range, theorem label, formulation,
  assumptions, and corrections have not been inspected in this worker clone.
- Later presentations of the one-variable differential-polynomial criterion, often associated with
  Lenore Blum, are candidates for a simpler modern axiomatization. They are not evidence for the
  exact Robinson claim until a primary edition is pinpointed and the relationship between schemes
  is proved or independently reviewed.

These are discovery anchors only. Because the repository wording does not select among materially
different formulations, the current human status is `H2`, not `H0`.

## Claim crosswalk

| Repository phrase | Bounded mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| differential field | characteristic-zero field with one derivation satisfying Leibniz | `Field`, `CharZero`, `Differential` | pinned ingredients located |
| differentially closed | existentially closed among differential-field extensions | extension embeddings plus preservation of finite existential differential equations | exact definition open |
| axiomatization | explicit first-order scheme iff existential closedness | syntax/semantics or a transparently expanded algebraic scheme and both implications | source scheme open |
| differential equations | finite differential-polynomial equations and inequations | differential-polynomial syntax, evaluation, order, and nonvanishing predicates | no pinned interface located |
| Robinson, 1959 | historical attribution and version of the scheme | pinpoint immutable source and row-level assumption map | candidate citation only |

## Pinned formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.FieldTheory.Differential.Basic` supplies `Differential`, `Differential.deriv`, ordinary
differential fields and `DifferentialAlgebra`; core algebra supplies `Derivation` and `CharZero`.
`IntakeProbe.lean` checks these interfaces with the pinned Lean executable.

A bounded case-insensitive search for `differentially closed`, `differential polynomial`, and
`DCF` in pinned mathlib found no theorem-specific target or differential-polynomial interface.
This negative search is not the immutable anchor audit and grants no proof credit. Before `H0`, a
source reviewer must inspect an immutable primary edition, pinpoint the theorem and definitions,
map every hypothesis and boundary case, check errata, and approve each crosswalk row.
