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
| compact complex analytic variety in projective space | `IsClosedComplexAnalyticProjectiveSubset Z`: the quotient preimage of `Z` in the punctured homogeneous-coordinate cone is closed and is locally cut out near every point by finitely many `AnalyticOnNhd Complex` functions | the reduced modern carrier formulation is frozen; compact/closed source terminology still needs audit |
| algebraic character | `IsHomogeneousPolynomialCutOut Z`: one family of `MvPolynomial (Fin (n + 1)) Complex`, each homogeneous of some degree, has exactly `Z` as its simultaneous projective zero locus | the reduced set-theoretic conclusion is frozen; any nonreduced structured-space strengthening remains uncredited |
| ambient projective coordinates | `Projectivization Complex (Fin (n + 1) -> Complex)`, with `n : Nat` explicit | the quotient carrier and nonzero representative map now elaborate in `Statement.lean`; no independent projective topology instance is postulated |
| equality/equivalence of varieties | equality of membership for every nonzero homogeneous-coordinate representative | exact for the selected reduced carrier formulation; equality or equivalence of structured analytic/algebraic spaces requires a later checked transport |

## Statement-phase selection

`Statement.lean` resolves the intake's primary-carrier branch rather than
inventing an abstract analytic predicate. Analyticity has explicit local
equation data on the homogeneous-coordinate cone, and algebraicity has
explicit homogeneous polynomial equations. This is a reduced, set-theoretic
formulation of the conventional theorem and includes reducible subsets, the
empty and full subsets, and `n = 0`.

The source audit remains open. In particular, this phase does not claim that
Chow's 1949 terminology includes precisely this reduced convention, nor does
it transport this target to nonreduced analytic subspaces, closed subschemes,
or an analytification equivalence. Those alternatives remain visible rather
than silently broadening the frozen target.

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
inspection before crediting a stronger structured-space interpretation. The
statement phase selects the reduced-carrier interpretation explicitly; it
does not erase the remaining source-fidelity and transport debt.
