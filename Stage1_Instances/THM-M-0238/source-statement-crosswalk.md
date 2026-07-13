# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1717-1722` supplies exactly the title `阿贝尔定理`, attribution
to Niels Abel, 1827, the gloss `椭圆积分的反演`, high importance, and status `已验证`. All six
uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, bibliography, definitions,
hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:6599-6624` repeats those fields and explicitly leaves the formal system,
precise definitions and premises, proof route, dependencies, equivalent forms, axioms, machine
status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Primary-source lead

Niels Henrik Abel, *Recherches sur les fonctions elliptiques*, *Journal fur die reine und
angewandte Mathematik* 2 (1827), pages 101-181, DOI `10.1515/crll.1827.2.101`, is the inspected
historical lead. Crossref metadata confirms the title, journal, year, volume/issue, page range, and
DOI. The Goettingen Digitisation Centre volume manifest identifies Abel, the article, and its 81
scanned journal pages; its PDF was retrieved outside the repository and hashed. The opening printed
page 101 was inspected and discusses elliptic functions as functions contained in elliptic
integrals and the historical work of Euler, Lagrange, and Legendre.

This is discovery evidence, not H0. No exact theorem passage, full incorporated definition chain,
complete proof, continuation and branch conventions, translation relationship, corrections or
errata, or independent source review was established. The scan is not stored in this dossier.

## Literal crosswalk

| Repository element | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| `阿贝尔定理` | which of several Abel-named results is intended | exact root ID and source proposition | elliptic-integral family selected by the gloss; exact proposition open |
| `椭圆积分` | Legendre form, cubic/quartic differential, parameters and nonsingularity | integrand, curve, differential, integral/primitive, paths and branches | all definition choices open |
| `反演` | local inverse, continued inverse, quotient-valued inverse, or uniformization | exact left/right inverse equations with domains and equivalences | relation and direction open |
| elliptic function output | single-valued meromorphic function and period lattice | `PeriodPair`, lattice, periodicity, meromorphicity | adjacent pinned APIs checked; no inverse bridge |
| Abel, 1827 | historical provenance | immutable source record and node crosswalk | primary bibliographic lead inspected; no H0 mapping |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H or M credit |

## Neighbor and alternate-form boundary

The next repository record, `THM-M-0239`, separately names Jacobi inversion and glosses it as
inversion of Abelian integrals. `THM-M-0240` separately names Abel-Jacobi and glosses it through the
Jacobian of an algebraic curve. Their scopes, sources, generalized genus, divisor maps, and future
formal artifacts cannot be transferred here.

Legendre elliptic functions, Jacobi `sn/cn/dn`, a Weierstrass `P` uniformization, and an elliptic
curve or complex-torus statement may encode related genus-one mathematics. No such form is credited
as equal, iff, or implication until one source-approved root and kernel-checked transports exist.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`PeriodPair`, `weierstrassP`, its derivative identity, lattice periodicity, meromorphicity, pole
order, and cubic differential equation. The four printed axiom reports contain only `propext`,
`Classical.choice`, and `Quot.sound`. This authenticates relevant substrate, not the target: the
probe states no integral, inverse relation, transport, or target theorem and supplies no proof-body
credit.

## Source and statement exit gate

Before H0 or statement acceptance, accountable reviewers must preserve an immutable lawful source
edition, select and transcribe an exact proposition with every incorporated definition, binder,
hypothesis, conclusion, branch and boundary case, map its proof and corrections, reconcile the two
neighbor targets, and independently approve the source-to-Lean crosswalk. The statement phase must
then elaborate the exact expression, compile all credited transports, and mutation-test removed
hypotheses, changed domains, changed binder scope, and boundary cases. Until then the canonical
statement and expression remain null.
