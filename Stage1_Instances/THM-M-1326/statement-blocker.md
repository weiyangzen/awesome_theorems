# Statement-phase blocker

## Verdict

`S56-M-1326-STATEMENT` is blocked. No canonical Lean target is claimed, and this dossier remains
`[H3, M4, R4]` with `theorem_complete=false`.

The repository source at `Docs/researches/math_theorems.md` identifies only the family “Laplacian
comparison theorem” and says “the Laplacian of the distance function.” It does not select a
curvature normalization, Laplacian sign, regular-locus versus weak interpretation, positive-model
radius restriction, or boundary convention. The intake crosswalk therefore does not supply enough
source identity to choose one of the inequivalent standard variants without inventing mathematics.

There is a second, independently sufficient blocker in the pinned formal environment. Mathlib at
the repository pin provides Riemannian manifolds and their distance through
`Mathlib.Geometry.Manifold.Riemannian.Basic`, but the checked source tree contains no declaration
for Ricci curvature, the Riemann curvature tensor, a cut locus, or a manifold
Laplace-Beltrami operator. The similarly named `Laplacian` API is for functions on inner-product
vector spaces and distributions, not for the Riemannian distance function on a manifold. Replacing
the missing geometry with arbitrary predicates/functions, or accepting the desired inequality as
a field or hypothesis, would be a substituted theorem and is prohibited.

`StatementProbe.lean` is deliberately only a positive availability probe. It is not a theorem
statement and earns no `M3` or proof credit.

## Exact retry condition

Resume the statement node only after both conditions hold:

1. an inspected, stable primary source fixes the exact theorem/page, all normalizations,
   assumptions, exceptional-set semantics, and boundary cases; and
2. pinned Lean declarations encode Ricci curvature and the chosen Laplace-Beltrami/cut-locus
   semantics, or a separately reviewed faithful definition layer is implemented without assuming
   the comparison conclusion.

## Validation evidence

Base revision: `31a50b6994ecddcae6774a19404c52d9e9881fa7`.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1326/StatementProbe.lean` | exit 0; Lean resolves `IsRiemannianManifold`, `TangentSpace`, `dist`, and `CompleteSpace` from the minimal import |
| `rg -n -i '\\bRicci\\b|RicciCurv|ricciCurv|cut locus|CutLocus|cutLocus|Laplace.Beltrami|LaplaceBeltrami|laplaceBeltrami' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1; no matches in the pinned mathlib source tree |
| `cd Formalizations/Lean && lake env lean /tmp/THM-M-1326-missing-api.lean` where the file imports `Mathlib.Geometry.Manifold.Riemannian.Basic` and checks `RicciCurvature`, `cutLocus`, and `laplaceBeltrami` | exit 1; each identifier is unknown |
| `git diff --check -- Stage1_Instances/THM-M-1326` | exit 0; no output |

The failed missing-API probe is negative diagnostic evidence only. No dependency was fetched or
updated, and the canonical `.lake` symlink was not modified.
