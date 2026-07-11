# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Dense small points force a special subvariety | S. Zhang, *Equidistribution of small points on abelian varieties*, Annals of Mathematics 147 (1998), 159-165, Theorem 1.1 and its Bogomolov-conjecture application | None identified | Primary proof anchor located; exact hypotheses, errata, and node mapping remain open: `H1`, `M4` |
| Curve case underlying the general result | E. Ullmo, *Positivite et discretion des points algebriques des courbes*, Annals of Mathematics 147 (1998), 167-179 | None identified | Primary source anchor located; it is a branch/special case, not a substitute for the general root |
| Special subvarieties have arbitrarily small points | Torsion density plus vanishing of the canonical height on torsion points; source pinpoint still required | Future Lean converse branch | Standard converse, but neither a source-to-node proof nor a checked formal bridge is credited |
| Non-special lower-bound formulation | Contrapositive of the density statement after fixing the canonical-height and Zariski-closure conventions | Future alternate encoding | Candidate transport only; positivity, strictness, and base-field details require checking |
| Essential-minimum formulation | Zhang's successive-minima/equidistribution framework | Future alternate encoding | Candidate equivalent formulation only |

The canonical statement uses geometric points and the Neron-Tate height attached to
an ample symmetric line bundle. The statement phase must decide the precise base
change, topology, height codomain, special-locus predicate, and quantifier order.
It must then elaborate the expression and mutation-test removal of ampleness,
symmetry, geometric integrality, torsion, and the boundary cases `X = A` and
zero-dimensional `X`.

Discovery links, not immutable evidence receipts:

- Zhang: <https://doi.org/10.2307/120986>
- Ullmo: <https://doi.org/10.2307/120987>

No `H0` or machine-completion claim is made. Independent source review, exact
page/theorem premise mapping, correction/errata search, immutable source hashes,
and a repository/pinned-mathlib Lean search remain required.

