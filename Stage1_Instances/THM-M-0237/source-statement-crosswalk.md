# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1710-1715` supplies exactly the Chinese title "Riemann-Roch
theorem," attribution to Bernhard Riemann and Gustav Roch, 1865, the gloss "divisor theory of
compact Riemann surfaces," high importance, and status `已验证` ("verified"). All six uncited lines
entered the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no
bibliography, formula, definitions, assumptions, proof boundary, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:6572-6597` repeats the gloss and explicitly leaves the formal system,
precise definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Human-source candidates

- Gustav Roch, *Ueber die Anzahl der willkurlichen Constanten in algebraischen Functionen*,
  Journal fur die reine und angewandte Mathematik, issue 64 (1865), pages 372-376,
  DOI `10.1515/crll.1865.64.372`. Crossref metadata confirms the title, date, journal, issue, page
  range, DOI, and publisher. The article text was not obtained or inspected in this intake.
- Otto Forster, *Lectures on Riemann Surfaces*, Springer (1981),
  DOI `10.1007/978-1-4612-5961-9`, ISBN `9781461259633` / `9781461259619`. Bibliographic metadata
  was inspected, but an exact theorem/page and incorporated definition chain were not.

These are discovery candidates, not accepted H0 records. H0 requires a lawful immutable source
copy, exact theorem and definition locators, every assumption and conclusion mapped, correction and
errata review, dependent source IDs, and an independent reviewer.

## Crosswalk

| Repository phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "compact Riemann surface" | nonempty connected compact complex one-manifold under an exact source convention | topological carrier, complex one-manifold structure, `CompactSpace`, separation/countability assumptions | general manifold substrate probed; exact surface object open |
| "divisor" | finite integer combination of points, with sign and support conventions | finitely supported integer-valued function or checked equivalent divisor structure | no compact-surface divisor interface selected |
| `deg(D)` | sum of coefficients, with invariant representation | integer degree map | definition and coercions open |
| `L(D)` / `ell(D)` | meromorphic functions satisfying `(f)+D >= 0`, or sections of `O(D)`; dimension over `Complex` | meromorphic-function divisor/order bridge or global sections plus finite-dimensionality | absent from catalog; source and Lean object model open |
| genus `g` | topological genus, `dim H^0(K)`, or another proved-equivalent convention | natural/integer invariant plus checked bridges | convention open |
| canonical divisor `K` | divisor of a nonzero meromorphic differential or canonical bundle class | differential/line-bundle/divisor object and choice-independence theorem | convention and existence open |
| Riemann-Roch conclusion | candidate `ell(D)-ell(K-D)=deg(D)+1-g` for every divisor `D` | binder-complete equality with explicit integer coercions | recognizable standard shape, not source-selected or elaborated |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Duplicate-target and alternate-form boundary

`THM-M-0105` has catalog gloss "divisor theory of algebraic curves" and `THM-M-0175` has "the
divisor dimension formula on algebraic curves." Their provisional Hartshorne citations, algebraic
scheme scopes, legacy Lean modules, debt classifications, and receipts do not transfer to this
compact-Riemann-surface target. An algebraic-curve theorem may correspond to the analytic theorem
only after the exact base field, analytification, divisor, cohomology, and comparison transports are
kernel checked.

The divisor formula, `ell(D)-ell(K-D)` form, line-bundle Euler characteristic, Serre-duality form,
and analytic index form are plausible relatives. None is credited as equal, iff, or implication
until the statement phase compiles the required transport against one source-approved root.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
the general complex manifold model, manifold structure, compact-space class, manifold
differentiability, and plane-domain meromorphic predicates. The latter are functions on a normed
field, not meromorphic functions on an arbitrary compact Riemann surface. The pinned
`Mathlib/Geometry/Manifold/Complex.lean` TODO explicitly identifies holomorphic vector/line bundles
and finite-dimensional section spaces as undeveloped directions. A bounded exact-topic search found
only other target files and no terminal compact-surface theorem. No canonical target, expression
fingerprint, proof body, trust result, anchor-audit completion, or machine-proof credit follows.
