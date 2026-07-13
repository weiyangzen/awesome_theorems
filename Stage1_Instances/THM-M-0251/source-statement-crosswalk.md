# THM-M-0251 source-statement crosswalk

## Repository Record

The complete source record is `Docs/researches/math_theorems.md:1808-1813`. All six lines were
introduced in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the record block has SHA-256
`826894d6e724080b981ba10d47a93ba3a39c2c13f5980d0f76cf5fb011877baa`.

| Repository field | Literal value | Evidentiary assessment |
|---|---|---|
| Title | `内函数-外函数分解` | Identifies a result family, not one proposition |
| Proposer | Arne Beurling | Uncited attribution; cannot select a theorem or variant |
| Time | 1949 | Uncited date; cannot supply edition, theorem, page, or assumptions |
| Statement | `Hardy空间的内-外分解` | Omits every binder, premise, definition, and exact conclusion |
| Importance | high | Scheduling metadata only |
| Formal status | `已验证` | Explicitly untrusted by the rev-5.6 manifest; no proof credit |

`Docs/Stage0_Blueprint.md:6950-6975` repeats the gloss and explicitly leaves the formal system,
logical foundation, exact definitions and premises, proof process, dependencies, alternate forms,
axioms, machine status, and artifact links open. The manifest preserves the source label only as
`source_status_untrusted`, starts the target at `L0 / rework_required`, rejects legacy proof credit,
and records `theorem_complete=false`.

## Source Admission Boundary

The repository gives no bibliography. Beurling's 1949 paper *On two problems concerning linear
transformations in Hilbert space*, Acta Mathematica 81, 239-255, DOI
`10.1007/BF02395019`, is a bibliographic candidate matching the catalog author and year. It is not
accepted here: the catalog does not cite it, no lawful immutable primary copy or pinpoint theorem
was admitted, no incorporated definition or assumption map was produced, and no correction audit
or independent review established what relationship it has to the intended target. The attribution
may instead reflect or conflate individual-function factorization with related invariant-subspace
theory.

No other primary source is selected. In particular, the intake has no named source that supports
the `H1` minimum evidence contract and no stable exact proposition to classify. The worker therefore
proposes `H5` for the received catalog target: it is presently ill-posed as a theorem execution
object. There is no edition/theorem/page crosswalk or H0 packet. This classification neither
refutes nor calls mathematically open the standard inner-outer factorization results found in the
literature; it says only that the repository has not truthfully selected one of them.

## Statement Component Crosswalk

| Catalog phrase | Candidate component | Required source decision | Intake status |
|---|---|---|---|
| `Hardy空间` | analytic Hardy class `H^p` | domain, exponent and range, analytic or boundary model, measure, scalar field | absent |
| `内函数` | bounded analytic function with unimodular boundary values a.e. | exact predicate, boundary-limit theorem, normalization | absent |
| `外函数` | analytic function defined by an integral representation or cyclicity property | exact predicate and any checked equivalence | absent |
| `内-外` | product `f = I * O` | binder order, nonzero premise, equality domain, factor membership | absent |
| `分解` | existence, possibly uniqueness | uniqueness relation, normalization, zero case, explicit factor components | absent |
| Beurling / 1949 | historical identity | cited work, exact locator, correction history, attribution reconciliation | unresolved |
| `已验证` | catalog status | accepted primary-source review or kernel evidence | rejected as evidence |

Until every required decision has an approved pinpoint source mapping, the canonical mathematical
claim, quantifiers, hypotheses, conclusion, and alternate encodings remain null or empty.

## Lean Crosswalk

| Pinned module / declaration | What it supplies | What it does not supply |
|---|---|---|
| `Mathlib.Analysis.Complex.UnitDisc.Basic` / `Complex.UnitDisc` | unit-disk carrier | Hardy space, boundary values, inner/outer predicates, factorization |
| `Mathlib.MeasureTheory.Function.LpSpace.Basic` / `MeasureTheory.MemLp` | generic measurable Lp membership | analytic Hardy membership or boundary identification |
| `Mathlib.Analysis.Complex.CanonicalDecomposition` / `Complex.canonicalFactor` | one meromorphic canonical factor | full product, Hardy membership, inner/outer root, uniqueness |
| `Complex.analyticOnNhd_canonicalFactor` | analyticity away from the pole | analytic Hardy factor on the selected domain |
| `Complex.canonicalFactor_ne_zero` | a local nonvanishing property under disk hypotheses | nonzero source function or factorization existence |
| `Complex.norm_canonicalFactor_eval_circle_eq_one` | norm one on a circle | almost-everywhere boundary predicate or full inner factor |

The canonical-decomposition module explicitly contains `TODO: Formulate the canonical
decomposition.` A successful probe of these declarations is evidence only that nearby APIs
elaborate in the pinned environment. It creates no target declaration, source transport, proof
body, statement fingerprint, obligation ID, or machine-closure credit.

## Required Crosswalk For Statement Work

A statement-phase retry must add an independently reviewed record for the exact source edition and
stable locator, each incorporated definition, every ordered binder and premise, the exact
factorization and uniqueness conclusion, every boundary or degenerate case, correction/errata
status, dependent source IDs, and the relationship to each encoded Lean subexpression. Any
alternate formulation requires a checked transport in its credited direction.
