# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md:6467-6472` contains exactly the name
`Lubotzky-Phillips-Sarnak construction`, attribution to Lubotzky, Phillips, and Sarnak, the year
1988, and the phrase `construction of Ramanujan graphs`, plus high importance and an untrusted
formalization label. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no citation, formula,
definitions, parameter restrictions, binders, theorem locator, proof boundary, errata, reviewer,
or formal artifact.

`Docs/Stage0_Blueprint.md:24089-24115` repeats the gloss while leaving the formal system,
foundations, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generic scheduling prose and the rev-5.6 manifest's
preserved `verified` label are not mathematical or machine evidence.

## Primary bibliographic lead and inspected abstract

Crossref and the publisher identify:

> A. Lubotzky, R. Phillips, and P. Sarnak, "Ramanujan graphs," *Combinatorica* 8(3), September
> 1988, pages 261-277, DOI `10.1007/BF02126799`.

The inspected publisher abstract says that a large family of explicit `k`-regular Cayley graphs
`X` is presented and lists two properties: each adjacency eigenvalue is either `+/- k` or has
absolute value at most `2 * sqrt (k - 1)`, and the girth is asymptotically at least
`(4/3) * log_(k-1) |X|`. The abstract does not state the allowed number-theoretic parameters,
exact family quantifiers, graph and Cayley conventions, group and generator construction,
bipartite branches, theorem locators, or formal meaning of the asymptotic.

The publisher page exposed only a subscription preview during intake. A PDF request returned an
HTML access page, not the article. Crossref metadata and publisher abstract responses are mutable
discovery observations; they are not an admitted immutable theorem-text edition or a substitute
for an independently reviewed statement/proof/errata crosswalk. They support provisional `H1`,
not `H0`.

## Immutable secondary discriminator

Alexander Lubotzky's author survey, *Ramanujan Graphs*, `arXiv:1711.06558v1` (15 November 2017),
defines a finite connected `k`-regular Ramanujan graph for `k >= 3` using the same nontrivial
eigenvalue bound and says that the first explicit infinite families in LPS and Margulis were for
`k = q + 1`, with `q` prime. The observed versioned PDF SHA-256 is
`cfcdc1d023eb9ab8bb7397fefa98b216cce74770fcbb9177b84ee2534f65a32e`.

This is a secondary retrospective and mentions LPS and Margulis together. It discriminates the
candidate family but cannot choose the 1988 theorem's binders, construction, branches, or girth
clause and cannot establish catalog-to-source identity or `H0`.

## Clause crosswalk

| Repository or source phrase | Candidate mathematical component | Lean surface required later | Intake status |
|---|---|---|---|
| `Ramanujan graph` | finite regular graph with source-defined trivial eigenvalues and bound `2 * sqrt (k - 1)` | graph, regularity, adjacency operator, spectrum, multiplicity, trivial-eigenvalue predicate | secondary definition and abstract only; exact 1988 definition open |
| `construction` | source-specific Cayley graphs obtained from arithmetic/projective-linear data | group/quotient, finite-field parameters, generator set, graph extraction, invariants | construction body and exact inputs unavailable |
| `explicit` | explicit algebraic family, possibly with an effective procedure | exact construction witnesses and any effectivity contract | abstract adjective only; no algorithmic claim frozen |
| large/infinite family | indexed finite graphs with source-specific cardinalities and distinctness | dependent family, size formula, unboundedness or pairwise nonisomorphism | quantifiers and equality notion open |
| `k`-regular | candidate degree `k = q + 1` for a prime `q` | `SimpleGraph.IsRegularOfDegree` or a source-faithful graph equivalent | secondary lead only; source parameter notation/order open |
| Cayley graph | graph of a candidate `PSL(2, F)` or `PGL(2, F)` carrier and generators | projective group, finite field, generator finset, inverse closure, checked graph construction | precise branch and generators open |
| spectral clause | eigenvalues are `+/- k` or bounded by `2 * sqrt (k - 1)` | Hermitian adjacency spectrum and exact trivial-spectrum exclusion | publisher abstract only; no canonical expression |
| girth clause | asymptotic lower bound with constant `4/3` | girth definition, logarithm, family limit/liminf/eventual quantifiers | catalog ownership and exact formula open |
| `verified` | untrusted inventory label | accepted source and kernel receipts would be required | no H0 or M credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
checks `SimpleGraph`, `SimpleGraph.IsRegularOfDegree`, adjacency matrices and Hermitian eigenvalues,
`Matrix.ProjectiveSpecialLinearGroup`, `Matrix.ProjGenLinGroup`, `legendreSym`, and `Real.sqrt`.
These are representation and arithmetic substrate only. They do not define the source generator
set, Cayley graph, Ramanujan condition, graph family, girth bound, or LPS theorem.

A bounded case-insensitive search of repo-local and pinned-mathlib Lean sources found no occurrence
for Lubotzky, Phillips, Sarnak, LPS graph/construction, or Ramanujan graph. This is intake discovery,
not the later immutable anchor audit and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must lawfully preserve and independently inspect an
immutable 1988 article edition; pinpoint the selected theorem, definitions, and proof; map every
parameter, premise, construction branch, spectral and girth conclusion, exception, correction, and
neighbor boundary; and approve catalog fidelity. Only then may the statement phase freeze minimal
imports, an exact Lean expression and environment fingerprint, checked encodings, and the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
