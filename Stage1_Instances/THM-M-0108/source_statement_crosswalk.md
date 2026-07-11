# Source-statement crosswalk

## Primary source identified

W.-L. Chow, "On compact complex analytic varieties," *American Journal of
Mathematics* 71 (1949), no. 4, pp. 893-914. DOI: `10.2307/2372375`.

This bibliographic anchor does not establish `H0`. The exact numbered result
and pages containing the projective analytic-to-algebraic assertion, the
paper's meanings of variety and equivalence, its assumptions, and any errata
must be inspected from an immutable copy during source audit. The repository's
discovery metadata says 1937; that date is not adopted because it conflicts
with this publication record and requires resolution.

## Crosswalk

| Source-side component | Frozen target meaning | Intake assessment |
|---|---|---|
| compact complex analytic variety in projective space | closed complex-analytic subvariety of finite-dimensional `CP^n` | compact/closed equivalence and source terminology need audit |
| algebraic character | common zero locus of homogeneous complex polynomials | exact source conclusion and reducedness convention unresolved |
| ambient projective coordinates | projective space over `Complex`, with explicit finite `n` | native Lean model unresolved |
| equality/equivalence of varieties | equality of carriers or structured analytic/algebraic equivalence, as the source actually states | must not be guessed at intake |

## Legacy crosswalk

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_032.lean` describes the right
informal direction, but its `StatementShape` is built from predicates that the
file itself labels placeholders. Its properness and projective-spectrum lemmas
are infrastructure anchors only. They neither encode the analytic input nor
close Chow's theorem, so they receive no rev-5.6 statement or proof credit.

## Fidelity risks

"Variety" may encode irreducibility or reducedness, while modern versions are
often stated for arbitrary closed analytic subsets. "Algebraic" may mean a
set-theoretic homogeneous zero locus or a structured algebraic subvariety.
These choices affect the proposition and must be settled by pinpoint source
inspection and checked transports in later phases.
