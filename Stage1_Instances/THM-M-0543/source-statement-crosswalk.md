# Source-statement crosswalk

## Repository record and candidate sources

The repository record supplies the title "de Rham theorem", the phrase "de Rham cohomology and
singular cohomology are isomorphic", and the year 1931. Its `已验证` label is explicitly untrusted
under rev-5.6.

Candidate historical primary evidence is Georges de Rham, *Sur l'analysis situs des varietes a n
dimensions*, Journal de Mathematiques Pures et Appliquees (9) 10 (1931), 115-200. A candidate
modern source for an exact comparison statement is Raoul Bott and Loring W. Tu,
*Differential Forms in Algebraic Topology*, Graduate Texts in Mathematics 82, Springer (1982),
the de Rham theorem chapter. These are discovery anchors only: the documents, precise theorem and
page, definitions, hypotheses, proof boundaries, edition, and errata have not yet been independently
inspected, so they provide no `H0` credit.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "de Rham cohomology" | cohomology of the smooth differential-form complex | bundled forms, exterior derivative, closed/exact quotient or complex cohomology | included; concrete model open |
| "singular cohomology" | cohomology of the underlying space with real coefficients | singular chains/cochains and cohomology in degree `k` | included; ordinary/smooth-singular bridge open |
| "isomorphic" | degreewise natural linear isomorphism | a concrete `LinearEquiv`/categorical isomorphism induced by comparison maps | included; exact result type open |
| integration | cochain map sending a form to its integrals over smooth simplices | simplex integration and a cochain-map declaration | intended construction; API open |
| Stokes compatibility | integration annihilates the differential/boundary discrepancy | checked chain/cochain compatibility and descent | necessary bridge; proof open |
| all smooth manifolds | source-specific manifold hypotheses and all admitted degrees | manifold typeclasses, topology assumptions, ordered binders | scope frozen broadly; exact hypotheses open |

## Existing Lean boundary

Repo-local searches at this intake found differential-form infrastructure, including
`Mathlib.Analysis.Calculus.DifferentialForm.Basic`, and historical Stage1 audit material in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_109.lean`. That file explicitly treats its de Rham
objects as abstract statement/audit scaffolding and defers the singular-cohomology bridge. Searches
for `de Rham theorem`, `deRhamTheorem`, and related spellings did not locate a concrete accepted
terminal comparison theorem in the pinned repo. This is scoped discovery evidence, not the required
immutable anchor audit and not proof of external absence.

Before `H0`, an independent reviewer must verify the chosen edition, theorem/page, definitions,
every hypothesis, coefficient and sign convention, proof boundaries, and errata. Before statement
credit, each approved component must map row by row to an elaborated Lean expression, including
checked transports for any smooth-singular/ordinary-singular or coefficient encoding change.
