# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1668-1673` supplies exactly the Chinese title "Mittag-Leffler
theorem," attribution to Magnus Mittag-Leffler, the year 1884, the gloss "partial-fraction
decomposition of meromorphic functions," high importance, and status `已验证` ("verified"). All six
uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula, definitions,
domain, hypotheses, convergence claim, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:6410-6435` repeats the gloss while explicitly leaving the formal system,
precise definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Human-source candidates

- G. Mittag-Leffler, *Sur la représentation analytique des fonctions monogènes uniformes: D'une
  variable indépendante*, Acta Mathematica 4 (1884), pages 1-79,
  DOI `10.1007/BF02418410`. Crossref metadata confirms author, title, journal, volume, year, page
  range, DOI, and publisher. Attempts to retrieve the article through Springer and Project Euclid
  returned access-control HTML rather than a PDF, so no theorem text was inspected.
- David C. Ullrich, *Complex Made Simple*, Graduate Studies in Mathematics 97, AMS (2008), Chapter
  12, "Runge's theorem and the Mittag-Leffler theorem," pages 229-243,
  DOI `10.1090/gsm/097/13`. Crossref metadata and the AMS product table of contents were inspected;
  the chapter text and exact theorem locator were not.

These are bibliographic discovery leads, not accepted `E4`/`H0` records. H0 requires a lawful
immutable source copy, exact theorem and incorporated-definition locators, every premise and
conclusion mapped, correction and errata review, dependent source IDs, and an independent reviewer.
The theorem family is provisionally H1 because it is a classical proved result, while exact source
fidelity remains open.

## Crosswalk

| Repository phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "meromorphic functions" | functions on `Complex`, a plane domain, or an open Riemann surface | `f : ℂ -> ℂ`, `MeromorphicOn f U`, or future surface API | plane/domain predicate probed; source domain open |
| pole set | discrete or locally finite subset, with an indexing and duplicate policy | set or indexed family plus local-finiteness/no-accumulation predicate | absent from catalog |
| principal part | finite sum of negative Laurent powers at each center | center, order, and coefficient data with local evaluation | no canonical representation selected |
| prescribed-data direction | construct a meromorphic function realizing every local principal part | existential function plus meromorphic and local-matching clauses | recognizable classical form, not source-selected |
| decomposition direction | express a given meromorphic function by its principal parts plus a holomorphic term | series/correction data, convergence, and equality away from poles | catalog wording may suggest this form; exact claim open |
| "partial-fraction" | finite rational identity or infinite locally convergent corrected series | `Finset` identity, `tsum`, or locally uniform convergence | finite and cotangent special-case APIs exist; not interchangeable |
| uniqueness | solutions differ by a holomorphic function, possibly after normalization | implication or quotient/equivalence statement | absent from catalog; not part of root unless selected |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Alternate-form boundary

Prescribed-principal-parts existence, decomposition of a given meromorphic function, a first Cousin
problem, a corrected locally uniform series, and uniqueness modulo holomorphic functions are closely
related formulations. None is credited as equal, iff, or implication until the statement phase
selects a source root and compiles the required transports, including every domain, convergence,
and boundary hypothesis.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `MeromorphicAt`,
`MeromorphicOn`, `meromorphicOrderAt`, and `MeromorphicOn.divisor` provide local and divisor
substrate. `Function.FactorizedRational.divisor` covers finite-support integer divisors, and
`cot_series_rep` proves the concrete cotangent Mittag-Leffler expansion. Neither is the arbitrary
prescribed-principal-parts theorem. `CategoryTheory.Functor.IsMittagLeffler` belongs to inverse
systems and is explicitly excluded as a homonym. The probe and bounded search do not elaborate a
canonical target, complete an anchor audit, establish proof-body provenance, or supply M credit.
