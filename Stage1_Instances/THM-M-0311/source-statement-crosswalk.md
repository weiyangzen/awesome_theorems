# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Frigyes Riesz and Ernst Fischer, gives the year 1907, and
states only `L^2空间的完备性` ("completeness of L^2 spaces"). Stage0 repeats that gloss while leaving
the definitions, assumptions, proof route, axioms, and artifact links open. The rev-5.6 manifest
retains `已验证` only in the explicitly untrusted source-status field. These records establish the
intended topic, not `H0`, exact statement identity, or machine closure.

## Candidate primary-source genealogy

- Ernst Fischer, "Sur la convergence en moyenne", *Comptes rendus hebdomadaires des seances de
  l'Academie des sciences* **144** (1907), 1022-1024.
- Frigyes Riesz, "Sur les systemes orthogonaux de fonctions", *Comptes rendus hebdomadaires des
  seances de l'Academie des sciences* **144** (1907), 615-619.

These bibliographic records are candidate primary anchors for the historical theorem family. This
intake has not pinned and inspected immutable scans, reconciled terminology and pagination, mapped
their Fourier-series formulations to the repository's abstract L^2-completeness gloss, checked
later corrections, or obtained independent review. They therefore support only `H1`, not `H0`.

## Crosswalk

| Repository/source component | Mathematical meaning to freeze | Required Lean component | Intake status |
|---|---|---|---|
| `L^2` | square-integrable scalar functions modulo equality almost everywhere | `MeasureTheory.Lp` at exponent `(2 : ENNReal)` | pinned API probed; scalar and source convention open |
| "space" | normed quotient over a specified measure space | measurable space, `Measure`, scalar normed field, quotient representation | family located; exact binders open |
| "completeness" | every Cauchy sequence has an L^2 limit | `CompleteSpace (Lp E 2 mu)` or an explicitly equivalent convergence proposition | candidate encoding only |
| Riesz-Fischer | abstract completeness or Fourier coefficient realization | checked source-to-formal bridge and alternate encoding | historical relationship unresolved |
| 1907 / Riesz / Fischer | historical provenance | no Lean proposition or proof credit | candidate sources identified |
| `已验证` | untrusted inventory label | no formal counterpart | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.MeasureTheory.Function.LpSpace.Complete`, checks `MeasureTheory.Lp`, and
synthesizes `CompleteSpace` instances for real- and complex-valued L^2 over an arbitrary measure.
The candidate implementation is documented in mathlib's
`Mathlib/MeasureTheory/Function/LpSpace/Complete.lean`, including
`MeasureTheory.Lp.instCompleteSpace`. This is a discovery lead only: the anchor-audit phase must
inspect its exact declaration, terminal proof body, axioms, imports, and provenance after the
source-faithful statement is frozen.

The statement phase freezes the repository gloss, rather than the unresolved historical variant,
as `Stage1Instances.THM_M_0311.RieszFischerTarget`. It quantifies over every measurable carrier and
measure, asserts both real and complex `Lp` completeness at exponent two, and retains zero, empty,
and infinite-measure cases. The fully qualified direct form has a checked `iff`; structural
mutations are distinguished by `check_statement.py`.

Before `H0`, an independent reviewer must still inspect immutable primary editions, record pinpoint
statement and definition boundaries, assumptions and errata, and approve the historical-source to
repository-gloss mapping. The statement gate therefore resolves the exact Lean target but does not
resolve or claim the human-source genealogy.
