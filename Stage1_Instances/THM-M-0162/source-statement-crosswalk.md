# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` give the Chinese title
`弗雷内-塞雷公式`, attribute the result to Jean Frenet and Joseph Serret (1852), and describe it
only as "the moving-frame equations for a space curve." They provide no publication, edition,
theorem number, page, hypotheses, displayed formula, or proof. Their `已验证` label is untrusted
metadata under rev-5.6 and supplies no human-source or machine-proof credit.

## Candidate proof source

Manfredo P. do Carmo, *Differential Geometry of Curves and Surfaces*, Prentice-Hall (1976), in the
opening chapter on curves and the Frenet formulas, is a candidate modern proof source. Its exact
section proposition/page, edition wording, regularity assumptions, sign conventions, and errata
have not been inspected in a stable copy. This bibliographic lead is discovery evidence only, not
`H0`. The original Frenet and Serret publications are not identified by the repository and are not
invented here from the attribution.

## Crosswalk

| Repository/source component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "space curve" | sufficiently differentiable map from an interval into oriented Euclidean `R^3` | interval domain, curve, derivatives, Euclidean structure | included; exact API open |
| moving frame | the ordered orthonormal frame `(T,N,B)` | unit tangent, normalized tangent derivative, oriented cross product | included; construction open |
| curvature | `kappa = ||T'||`, positive where `N` is defined | norm, positivity, division by nonzero scalar | included |
| torsion | signed rotation of the binormal, provisionally `tau = -<B',N>` | derivative and inner product with fixed sign | included; source convention unverified |
| frame equation for `T` | `T' = kappa N` | checked vector equality | included |
| frame equation for `N` | `N' = -kappa T + tau B` | checked decomposition in the Frenet basis | included |
| frame equation for `B` | `B' = -tau N` | product-rule/cross-product derivative and checked vector equality | included |

## Proof and evidence boundary

The expected derivation differentiates the orthonormality relations of `T`, `N`, and `B`, uses
`T' = kappa N` by definition, identifies the remaining coefficient with the selected torsion
convention, and uses the orientation `B = T x N`. This is a proof-route hypothesis for later source
comparison, not an accepted proof reconstruction.

The repository-local and pinned-mathlib name search at intake found no exact named Frenet-Serret
declaration. That narrow negative result is not a complete formal-candidate audit and grants no
machine status. Before `H0`, an independent reviewer must inspect a stable source, record exact
edition/section/page and all definitions, assumptions, signs, proof boundaries, and errata, then
approve the row-by-row source-to-Lean mapping. The dependent statement phase must elaborate the
exact target before any proof candidate receives credit.
