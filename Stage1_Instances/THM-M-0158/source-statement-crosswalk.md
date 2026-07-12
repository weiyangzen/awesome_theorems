# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` give the Chinese title
`魏因加滕方程`, attribute it to Julius Weingarten (1861), and gloss it only as "the derivative
formula for a surface normal vector." They provide no publication, edition, theorem number, page,
hypotheses, formula, or proof. Their `已验证` label is untrusted metadata under rev-5.6 and gives no
human-source or machine-proof credit.

## Candidate primary exposition

Manfredo P. do Carmo, *Differential Geometry of Curves and Surfaces*, Prentice-Hall (1976), in the
chapter treating the Gauss map and the fundamental forms, is a candidate modern proof source for
the local Weingarten equations. The exact section proposition/page, edition wording, conventions,
and errata have not been inspected in a stable copy. This bibliographic lead is therefore discovery
evidence only, not `H0`. The original 1861 publication is not identified by the repository and must
not be invented from the attribution.

## Crosswalk

| Repository/source component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "surface" | regular local parametrization into Euclidean `R^3` | open parameter domain, differentiable map, rank-two derivative | included; exact API open |
| "normal vector" | chosen differentiable unit field orthogonal to both coordinate tangents | inner product, unit and orthogonality hypotheses or derived cross-product normal | included; construction choice open |
| "derivative" | partial derivatives `N_u,N_v`, equivalently the differential of the Gauss map | Fréchet/partial derivative and tangent-basis coordinate map | included; encoding open |
| first fundamental form | Gram matrix `I = [[E,F],[F,G]]` | finite matrix/linear map and checked invertibility from regularity | included |
| second fundamental form | coefficients `e,f,g` from second derivatives paired with `N` | second derivative or derivative-of-tangent encoding | included; sign convention provisional |
| Weingarten equation | coefficient matrix `-I^-1 II`, or `S = -dN` with matrix `I^-1 II` | checked equality plus transport between local and invariant forms | human scope frozen; formal target open |

## Proof-boundary map for later review

The expected human derivation differentiates `<N,N> = 1` to show the derivatives of `N` are
orthogonal to `N`, hence tangent; differentiates `<N,x_u> = <N,x_v> = 0`; obtains the four inner
products with `x_u,x_v`; and solves the resulting Gram-matrix linear systems. These steps are a
proof-route hypothesis for source comparison, not an accepted proof reconstruction.

Before `H0`, an independent reviewer must inspect a stable source, record exact edition,
section/theorem/page, definitions, all regularity and orientation assumptions, sign and matrix
conventions, proof boundary, and errata, then approve a row-by-row source-to-Lean mapping. The later
anchor-audit node must separately search pinned mathlib and credible external Lean 4 projects; the
repository-local negative search performed at intake is not a complete formal-candidate audit.
