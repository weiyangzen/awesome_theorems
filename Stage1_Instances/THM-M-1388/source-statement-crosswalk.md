# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10111-10116` supplies exactly the title `特征值问题`, the
attribution `众多数学家`, the twentieth-century date, the gloss `Sturm-Liouville特征值`, importance
`high`, and status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37749-37775` repeats the metadata and classifies the entry as a
problem/decision proposition, but explicitly leaves the exact definitions and premises, proof
route, dependencies, equivalent forms, axiom policy, machine-checked state, and artifact links
open. The rev-5.6 manifest preserves `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

The catalog contains no bibliography, equation, interval, coefficients, weighted space, endpoint
or boundary-condition convention, binder, hypothesis, theorem conclusion, incorporated definition,
proof boundary, correction history, or reviewer. It therefore does not identify a stable
proposition.

## Literal crosswalk

| Repository element | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `特征值问题` | a problem definition, existence theorem, full spectral theorem, or decision problem | a source-defined `Prop` over an operator and boundary data | title alone is not truth-valued |
| `Sturm-Liouville` | regular/singular, scalar/matrix, finite/infinite interval, separated/coupled boundary data | derivative/ODE predicates, weighted function space, unbounded operator and domain | all defining choices absent |
| `特征值` | existence, reality, simplicity, enumeration, discreteness, asymptotics, or completeness | `Module.End.HasEigenvalue`, `spectrum`, eigenspaces, source-defined differential equation | requested predicate absent |
| multiple mathematicians / twentieth century | broad historical family | immutable edition, theorem/page, definitions, proof and errata map | no pinpoint source supplied |
| `已验证` | untrusted inventory label | reviewed human source and kernel receipt would be required | no H or M credit |

## Inspected modern source-family lead

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, Section 5.4, printed pages 155-164, was
inspected outside the repository as an authoritative source-family discriminator. The
author-hosted, publisher-permitted preliminary edition has SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. The official errata
available during intake has SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e` and was searched for the
relevant section and theorem.

The section assumes a compact interval `[a,b]`, real coefficients with `r,q` continuous, `p`
continuously differentiable, and `p(x),r(x)>0`; it defines the weighted expression
`L = r^-1 (-(p f')' + q f)` and a twice-differentiable domain with separated boundary forms
parameterized by `alpha` and `beta`. Theorem 5.11 states a conjunction: countably many discrete and
simple eigenvalues accumulating only at infinity; real normalized eigenfunctions forming an
orthonormal basis; and uniform convergence of the expansion for functions in the operator domain.
Its proof depends on earlier symmetry, Green-function/resolvent, compactness, and compact symmetric
spectral-theorem results. Lemma 5.12 separately supplies lower boundedness and ordering.

This inspection establishes that the catalog gloss can expand into several materially distinct
claims. It does not select Teschl's regular separated-boundary theorem for this target. The catalog
does not cite the book, no source passage or interpretation has independent approval, and no `H0`
or canonical-statement credit is claimed.

## Candidate component crosswalk

| Candidate component | Teschl discriminator | Prospective pinned Lean surface | Missing source decision |
|---|---|---|---|
| interval and coefficients | compact `[a,b]`; regularity and strict positivity in (5.45) | real interval, continuous/differentiable predicates | regular versus singular model and exact assumptions |
| differential expression | weighted second-order expression (5.53) | `HasDerivAt`, `deriv`, function and linear-map constructions | derivative, equality and operator-domain encoding |
| boundary conditions | separated forms (5.54)-(5.55) | endpoint evaluation and source-defined boundary predicate | Dirichlet/Neumann/Robin/periodic/coupled policy |
| eigenvalue | nonzero domain element satisfying `L u = lambda u` | `Module.End.HasEigenvalue` only after a valid operator encoding | unbounded-operator and multiplicity conventions |
| discreteness and simplicity | Theorem 5.11 | spectrum/eigenspace plus source-defined sequence | exact topology, enumeration and multiplicity |
| completeness | orthonormal basis and expansion (5.70) | inner-product-space basis and convergence APIs | ambient completion and convergence topology |
| lower bound and order | Lemma 5.12, not the same numbered result | ordered real sequence | whether this is part of the target |
| abstract spectral substrate | compact symmetric resolvent route | `IsCompactOperator`, `LinearMap.IsSymmetric`, compact spectrum/Rayleigh APIs | checked bridge from the differential problem |

The API probe authenticates generic names and types only. No row is a canonical statement,
checked transport, proof body, or `M0` result.

## Neighbor target crosswalk

`Docs/researches/math_theorems.md:10087-10109` separately records Sturm-Liouville theory,
comparison, separation, and oscillation targets. Lines 10118-10130 separately record Weyl
asymptotics and the Courant min-max principle. Adjacency is evidence for keeping those scopes
separate; it is not a checked implication or shared proof credit.

## Source and statement gate

Before ordinary theorem-proof execution, accountable reviewers must select or correct one stable
truth-valued proposition, preserve an immutable primary or authoritative source, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, boundary and multiplicity
convention, proof boundary, and correction state, reconcile neighboring scopes, and independently
approve the mapping. The statement phase must then freeze minimal imports, the elaborated
expression and environment fingerprint, checked alternate transports, and removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.

Until then, `H5` records that the received catalog wording is not a stable proposition. It does not
refute established regular or singular Sturm-Liouville results. The canonical mathematical and
Lean targets remain null, and the downstream anchor audit remains open.
