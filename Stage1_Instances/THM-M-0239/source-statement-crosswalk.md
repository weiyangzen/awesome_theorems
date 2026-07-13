# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1724-1729` supplies exactly the title `雅可比反演定理`, Carl
Jacobi, the year 1834, the gloss `阿贝尔积分的反演`, high importance, and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, bibliography,
definition, ordered binder, hypothesis, conclusion, proof boundary, correction history, reviewer,
or formal artifact.

`Docs/Stage0_Blueprint.md:6626-6651` repeats those fields and explicitly leaves the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine state, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Fixed exposition lead

Encyclopedia of Mathematics, "Jacobi inversion problem," fixed MediaWiki revision `55795`
(parent `55794`, timestamp `2024-05-26T08:15:17Z`) was inspected. The decoded 8,466-byte wikitext,
hashed without an added newline, has SHA-256
`5abb3e7b95df16d0c1c553de1636db480e907fb9fc05eba0d0661428fc9e76f4`.

The entry describes first-kind Abelian differentials on a compact Riemann surface `F` of genus
`p >= 1`. It formulates simultaneous inversion of `p` sums of path integrals in `p` variable
points, explains that the equations are congruences modulo the period lattice, and describes a
theta-function solution with normal and exceptional cases. It also says Jacobi observed the
higher-genus formulation in 1832, which conflicts with the catalog's unexplained 1834 date. The
entry cites Springer, *Introduction to Riemann Surfaces* (1957), Chapter 10, and other literature.

This is a stable, content-hashed exposition lead, not H0. It presents an inversion problem and
several solution claims rather than selecting one repository theorem; its cited source texts and
proofs were not inspected; path, period, theta, exceptional-case, translation, correction, and
historical-date mappings lack independent review.

## Modern exact-statement lead

Yukitaka Abe, *A generalization of Riemann's theta functions for singular curves*,
arXiv:`1909.11952v1` (2019), abstract, states that for a compact Riemann surface `X` of genus `g`,
Jacobi's inversion theorem is surjectivity of the Abel-Jacobi map
`X^(g) -> J(X)`, where `X^(g)` is the degree-`g` symmetric product and `J(X)` is the Jacobi
variety. The inspected version-1 PDF has SHA-256
`f47855f3d065708b405d2e99fac55993edb4f12d6c2ce4d26cd1510afbc05f42`.

This precisely corroborates a likely root shape but is not the classical proof source or H0. Its
introduction also calls the map biholomorphic, wording that needs careful source review because
special divisors produce nontrivial fibers in the usual higher-genus formulation. The intake
therefore credits only the abstract's surjectivity sentence as a secondary statement lead and does
not import the stronger wording.

## Clause crosswalk

| Repository/source component | Prospective mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| "Abelian integrals" | integrals of first-kind differentials, multivalued modulo periods | compact complex curve, holomorphic one-forms, path integrals, homology and period lattice | family identified; definitions and source mapping open |
| genus `g` surface | compact connected Riemann surface, usually `g >= 1` | complex one-manifold, compactness, connectedness, genus invariant | general manifold substrate only |
| `g` solution points | unordered effective degree-`g` divisor / symmetric product | geometric `X^(g)`, not only `Sym X g` as a type | combinatorial `Sym` API probed; geometric quotient open |
| Jacobian | period quotient, `Pic^0`, or divisor-class model | concrete Jacobian/Picard variety plus checked equivalences | absent from target record and no exact pinned API located |
| Abel-Jacobi map | sum of normalized integrals or `D - gP0` class | exact map, base point, normalization and well-definedness | candidate only |
| inversion theorem | surjectivity/existence for every Jacobian point | `Function.Surjective` only after the map and target are frozen | modern statement lead; not canonical or elaborated |
| explicit inversion | theta zeros and symmetric Abelian functions, with exceptional cases | genus-`g` Riemann theta, zero divisor, multiplicity and period laws | potentially stronger source boundary; open |
| Carl Jacobi / 1834 | historical attribution | immutable primary edition and passage | catalog preserved; EoM says 1832; unresolved |
| `已验证` | untrusted inventory label | accepted source review and kernel receipt would be required | no H or M credit |

## Neighbor and alternate-form boundary

`THM-M-0238` separately owns elliptic-integral inversion. `THM-M-0240` separately owns the
catalog's broadly worded Abel-Jacobi theorem. Their future definitions, artifacts, and receipts do
not transfer. A source reviewer must decide whether they are dependencies, overlaps, or distinct
claims before any shared formal object receives credit.

The surjectivity, effective-divisor representative, period-congruence, and explicit theta forms
are plausible relatives. No equality, iff, implication, or proof-boundary inclusion is credited
until one source-approved root is transcribed and the required Lean transports elaborate.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`Sym`, complex-manifold and compactness interfaces, `jacobiTheta₂`, commutative group-scheme
infrastructure, a ring Picard group, and elliptic-curve Jacobian-coordinate points. These APIs do
not jointly construct the target. A bounded search found repo-local planning text that explicitly
marks an Abel-Jacobi/Jacobian bridge as missing and no exact target declaration in pinned mathlib.
This is discovery-only evidence, not the downstream immutable anchor/provenance audit.

## Source gate

Before H0 or statement acceptance, accountable reviewers must preserve a lawful immutable source
edition, select the exact surjectivity, divisor-class, integral-congruence, or explicit-theta root,
map every incorporated definition, binder, hypothesis, conclusion, proof transition, exceptional
case and historical claim, audit corrections and errata, reconcile neighboring targets, and
independently approve fidelity. Only then may the statement phase elaborate and fingerprint the
same exact Lean proposition and mutation-test its assumptions, domain, binder scope, and boundary
cases.
