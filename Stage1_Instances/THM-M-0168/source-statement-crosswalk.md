# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` name `伯恩斯坦定理`, attribute it
to Sergei Bernstein in 1910, and gloss it as "an entire-plane minimal graph is a plane." They give
no publication, edition, theorem number, page, definition of minimality, regularity hypothesis,
dimension qualifier, or proof. Their `已验证` label is untrusted metadata under rev-5.6 and gives
no human-source or machine-proof credit.

## Source discovery boundary

The classical Bernstein literature and modern minimal-surface texts, including Robert Osserman's
*A Survey of Minimal Surfaces*, are candidate source families for the two-dimensional entire-graph
theorem and its analytic proof. No stable edition was inspected during this intake, so an exact
chapter/theorem/page, wording, invoked lemmas, and errata are deliberately not asserted. The
repository's year is retained only as repository metadata; the original publication has not been
identified here. These leads support `H1` discovery status, not `H0`.

## Crosswalk

| Repository/source component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "entire plane" | domain is all of Euclidean `R^2` | total function `R^2 -> R`, not a local-domain wrapper | included; encoding open |
| "graph" | embedded surface `(x,y) |-> (x,y,u(x,y))` in `R^3` | graph parametrization or set plus regularity bridge | included |
| "minimal" | zero-mean-curvature entire graph, commonly expressed by the minimal-surface PDE | derivatives, gradient, norm, divergence, and checked geometric/PDE bridge | included; exact notion open |
| "is a plane" | `u` is affine, so its graph is an affine plane | coefficients `a,b,c` and extensional equality; transport to geometric plane | included |
| dimension | the classical two-dimensional graph case | exact `R^2` domain and `R^3` graph | explicit; no higher-dimensional broadening |
| regularity | sufficient differentiability for the selected classical statement | exact `C^k`, smooth, weak, or variational hypotheses | unresolved pending source audit |

## Proof-boundary map for later review

Candidate classical routes use the minimal-surface equation together with global conformal or
complex-analytic structure, estimates for the Gauss map, or a Liouville-type argument to force the
normal (and hence the tangent plane) to be constant. This is only a route hypothesis for organizing
the later source audit. It is not an accepted proof reconstruction, and no individual lemma is
credited before a pinpoint source is inspected and mapped.

Before `H0`, an independent reviewer must inspect a stable primary proof source and a suitable
modern exposition; record exact bibliographic identity, theorem/page, definitions, regularity and
global hypotheses, dimension restrictions, proof dependencies, and errata; and approve a
row-by-row source-to-Lean mapping. The anchor-audit node must separately search pinned mathlib and
credible external Lean 4 projects. The intake's repository search is not that audit.
