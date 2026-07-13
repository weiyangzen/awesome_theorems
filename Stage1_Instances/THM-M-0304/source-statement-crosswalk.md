# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2181-2186` supplies exactly the name `莫里定理`, attribution
Charles Morrey, year 1940, gloss `Sobolev函数的Holder连续性`, importance `高`, and status
`已验证`. Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula,
definition, domain, exponent, ordered binder, hypothesis, conclusion strength, proof boundary,
correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:8386-8411` repeats the gloss while expressly leaving the formal system,
foundations, exact definitions and premises, proof path, dependencies, alternate statements,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`.

## Separate same-gloss target

`Docs/researches/math_theorems.md:9087-9092` separately records `Morrey不等式` with the same
attribution, year, gloss, importance, and status. Rev-5.6 retains it as the distinct PDE target
`THM-M-1242`. The records may be aliases, may need source-selected different variants, or may need
deduplication, but no accepted decision exists. The `THM-M-1242` dossier and all `THM-M-1237`
Sobolev artifacts are discovery inputs only; no target scope, status, or proof credit transfers.

## Human-source leads, not H0 evidence

Crossref metadata identifies the plausible historical source:

- C. B. Morrey, Jr., "Functions of several variables and absolute continuity, II,"
  *Duke Mathematical Journal* **6**(1), 1940,
  DOI `10.1215/S0012-7094-40-00615-9`. The publisher locator is
  `https://projecteuclid.org/journals/duke-mathematical-journal/volume-6/issue-1/Functions-of-several-variables-and-absolute-continuity-II/10.1215/S0012-7094-40-00615-9.full`.
- Charles B. Morrey, Jr., "A correction to a previous paper: 'Functions of several variables and
  absolute continuity, II,' vol. 6 (1940), pp. 187-215," *Duke Mathematical Journal* **9**(1),
  1942, DOI `10.1215/S0012-7094-42-00911-6`.

The publisher blocked both article bodies in this worker environment, so no theorem, page, formula,
definition chain, proof boundary, or correction content was inspected. Crossref's correction title
is evidence that an erratum exists, not evidence that its mathematical effect has been resolved.
These are bibliographic discovery leads only. A modern exposition such as L. C. Evans, *Partial
Differential Equations*, second edition, section 5.6.3, is likewise only a discovery lead until an
immutable copy, exact theorem and page, source relationship, and correction status are approved.

## Component crosswalk

| Repository phrase | Proposition-changing source choice | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Sobolev functions" | order, exponent, domain, weak-derivative model, norm, scalars, AE quotient | concrete Sobolev data or predicate using `MemLp` and a distributional derivative relation | family only; encoding open |
| "Holder continuity" | exponent, constant, local/domain/closure scope, representative existence and agreement | `HolderOnWith` plus a concrete AE representative relation | generic API present; theorem absent |
| Morrey theorem | compact-support inequality, local estimate, or bounded-domain embedding consequence | exact source-matched proposition and checked transports | variant not selected |
| supercritical regime | whether `p > n`, higher-order analogue, and endpoint policy | typed exponent relation and positivity facts | familiar candidate only |
| quantitative conclusion | gradient seminorm or full Sobolev norm, pointwise/supremum terms, constant dependencies | concrete inequality rather than an opaque proposition field | absent |
| 1940 attribution | exact original theorem and historical scope | provenance only, no machine credit | plausible paper located; text uninspected |
| 1942 correction | corrected formulas, premises, proof steps, and impact on the target | source invalidation and mapping input | existence located; contents uninspected |
| `已验证` | catalog status | no Lean expression or kernel evidence | rejected as evidence |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
elaborates five smooth-function derivative-norm inequalities and the generic Holder predicate and
continuity implication. The Sobolev inequalities require smoothness and compact support; they do
not construct a Holder representative of a source-selected Sobolev class. A bounded exact-topic
search finds only Morrey prose in the proof of Rademacher's theorem and no target-specific
declaration. This is discovery-only substrate evidence, not the later immutable anchor audit or a
global absence claim.

Before `H0`, a qualified independent reviewer must approve an immutable exact source, the original
and correction relationship, every definition and assumption, theorem and proof locators, all
errata, and a node-specific mapping. Before the statement gate, the duplicate-target boundary and
every open scope choice in `scope-map.md` must be frozen and elaborated without borrowing another
target's root.
