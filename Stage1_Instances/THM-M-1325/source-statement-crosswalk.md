# Source-statement crosswalk

## Source candidates

Richard L. Bishop, "A relation between volume, mean curvature and diameter," *Notices of the
American Mathematical Society* 10 (1963), p. 364, is the historical Bishop comparison candidate.
Mikhail Gromov's *Structures metriques pour les varietes riemanniennes* (CEDIC/Fernand Nathan,
1981) is the historical globalization candidate. These bibliographic anchors require inspection
of stable copies; neither is accepted as an exact theorem/page crosswalk at intake.

Modern textbook statements will be useful for locating the standard monotonic ratio formulation,
but cannot replace verification of the selected primary genealogy. No `H0` claim is made.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Bishop-Gromov volume comparison" | volume-ratio monotonicity | named canonical declaration | included; exact source anchor open |
| `Ric >= (n-1)k` | Ricci tensor lower bound relative to the metric | pointwise bilinear-form inequality | included; sign/normalization open |
| geodesic ball `B(p,r)` | ball centered at an arbitrary manifold point | Riemannian distance ball and measurability | included; open/closed convention open |
| `V_k(r)` | ball volume in the simply connected `n`-model of curvature `k` | model-space construction or source-exact volume function | included; representation open |
| ratio is nonincreasing | for `0 < r <= R`, the small-radius ratio is at least the large-radius ratio | ordered-field/extended-real inequality with nonzero-denominator facts | included; radius domain open |

## Identity and substitution guard

The canonical family is ratio monotonicity, not merely the corollary
`Vol(B(p,r)) <= V_k(r)`. The statement phase must inspect the sources and freeze the strongest
source-faithful version supported by their hypotheses. It must not broaden a local curvature
assumption, omit completeness, or evade model-space geometry by postulating the conclusion.

No repository-local Lean candidate is credited at intake. The anchor-audit phase must search the
pinned mathlib revision and credible external Lean 4 projects and record exact declarations,
types, revisions, dependencies, axioms, and terminal proof provenance. Before `H0`, an independent
reviewer must verify edition, pinpoint statement, assumptions, notation, genealogy, and errata.
