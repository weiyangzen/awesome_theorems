# Source-statement crosswalk

## Repository evidence

Stage0 supplies only "Ginibre-Velo NLW theorem", `NLW的局部适定性`, year 1985, and the authors Jean
Ginibre/Giorgio Velo. It explicitly leaves definitions, hypotheses, proof route, formal system,
axioms, and artifacts open. Consequently `已验证` is not a source receipt or machine proof.

The statement phase should inspect 1985 Ginibre-Velo primary publications and bibliographies for
the exact local Cauchy theorem. The well-known nearby nonlinear Klein-Gordon literature makes the
NLW/Klein-Gordon distinction a mandatory check. No title, theorem number, page, or edition has been
verified at intake, so no candidate is credited as H0.

## Crosswalk

| Repository phrase | Source question | Required Lean surface | Intake status |
|---|---|---|---|
| "Ginibre-Velo NLW theorem" | exact publication, theorem, and attribution | declaration tied to immutable citation | open |
| `NLW` | wave versus Klein-Gordon; dimension, sign, nonlinearity | spacetime function, derivatives, Laplacian, nonlinear term | unspecified |
| local well-posedness | existence interval, uniqueness class, continuous dependence | explicit solution predicate and quantified conclusions | family only |
| initial data | Sobolev/energy indices and compatibility assumptions | concrete function-space membership and traces | unspecified |
| 1985 | publication versus preprint chronology and errata | edition/revision evidence | unverified metadata |

## Acceptance boundary

The next phase must quote and cross-check the primary theorem and surrounding definitions. Any
Klein-Gordon/NLW mismatch must be reconciled rather than silently generalized. H0 requires exact
edition/theorem/page, assumption and conclusion rows, errata review, and independent review. No
Lean terminal theorem is identified or credited here.

