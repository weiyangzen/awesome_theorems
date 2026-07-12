# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10146-10151` supplies exactly the title `Fredholm择一定理`,
attribution to Erik Fredholm, the year 1903, the gloss `线性边值问题的可解性` ("solvability of
linear boundary-value problems"), importance `high`, and status `verified`. Git history places all
six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37884-37909` repeats the metadata while explicitly leaving the formal
system, exact definitions and premises, proof route, dependencies, equivalent statements, axiom
policy, machine status, and artifact links open. The rev-5.6 manifest preserves `verified` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The record contains no equation, operator order or domain, boundary conditions, function spaces,
compactness/Fredholm hypothesis, scalar parameter, adjoint problem, ordered binders, conclusion,
theorem/page locator, proof boundary, corrections, or reviewer. It identifies a theorem family but
does not freeze one stable proposition.

## Historical source lead

Crossref identifies Ivar Fredholm, "Sur une classe d'equations fonctionnelles," *Acta
Mathematica* 27 (1903), pages 365-390, DOI `10.1007/BF02421317`. The title, author, and year make
this a strong historical discovery lead. The accessible metadata describes a work on functional
equations, not an exact repository-approved ODE boundary-value statement.

No complete immutable scan was available in the repository or admitted by this worker. Consequently
no numbered theorem, displayed equation, page-level statement, incorporated definition, assumption,
proof passage, correction, translation, or source-to-catalog genealogy has been approved. The DOI
metadata is a search lead only and does not support `H0`.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| linear boundary-value problem | scalar higher-order ODE, first-order system, unbounded operator realization, or integral-equation reduction | differential operator/domain plus boundary functionals | order, domain, and regularity absent |
| solvability | existence for one forcing, existence for every forcing, range membership, or unique solvability | `Exists`, `Function.Surjective`, or membership in operator range | quantifiers and uniqueness absent |
| alternative | nonzero homogeneous solution versus solvability/uniqueness | disjunction with kernel and range predicates | exact branches absent |
| adjoint compatibility | forcing orthogonal to every adjoint homogeneous solution | inner product/pairing and adjoint kernel | adjoint and boundary conventions absent |
| compact reduction | `(I - lambda K)u = f` with compact `K` | continuous-linear-map algebra and `IsCompactOperator K` | reduction and parameter convention absent |
| spectral form | nonzero eigenvalue versus resolvent membership | `HasEigenvalue ... mu` / `mu in resolventSet ...` | pinned candidate exists; source match absent |
| Erik Fredholm, 1903 | original functional/integral-equation work or later BVP reformulation | provenance only | exact genealogy and result open |
| `verified` | untrusted inventory label | no declaration or proof body | explicitly rejected as evidence |

## Pinned formal candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Normed.Operator.FredholmAlternative` documents
`IsCompactOperator.hasEigenvalue_or_mem_resolventSet` as the Fredholm alternative. Its visible
contract takes a compact continuous linear endomorphism `T` of a complete normed space over a
nontrivially normed field and a nonzero scalar `mu`; it concludes that `mu` is an eigenvalue of `T`
or belongs to its resolvent set. The nearby theorem
`IsCompactOperator.hasEigenvalue_iff_mem_spectrum` supplies the associated nonzero-spectrum result.

These declarations are real pinned candidates, not a source-statement match. The later anchor audit
must inspect exact elaborated types, bodies, dependencies, axioms, and provenance after the source
selects a root. If the selected result is a differential BVP alternative, it must additionally
formalize and check the operator realization, compact or Fredholm reduction, adjoint-boundary
identification, and source-specific transport. The probe supplies none of those bridges.

## Neighbor-target boundary

The catalog separately schedules `THM-M-0315`, named in Chinese as the Fredholm alternative with
the compact-operator-equation gloss, and `THM-M-1161`, Fredholm integral equations with a
potential-theory gloss. It also places this target beside generic ODE boundary-value, Sturm-Liouville,
Green-function, shooting, and finite-difference records. These records expose possible relationships,
but they do not establish equivalence or allow status, statement, source, or proof evidence to move
between owned targets.

## Required source admission

The statement phase must preserve and hash one lawful complete edition, select an exact result and
proof boundary, transcribe every definition, binder, hypothesis, alternative branch, conclusion,
parameter dependency, and boundary case, reconcile the integral/operator/BVP genealogy, audit
corrections and translations, and obtain independent review. It must then elaborate and
mutation-test that same expression in Lean. Until then the canonical mathematical and Lean targets
remain null and the human-source classification remains `H1`.
