# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` records only the Chinese title `Bernoulli移位`, attributes it to
many mathematicians, dates it broadly to the twentieth century, and gives the phrase
`Bernoulli系统的分类` ("classification of Bernoulli systems"). It gives no definition, named
theorem, publication, page, assumptions, or conclusion. `Docs/Stage0_Blueprint.md` repeats that
phrase while explicitly leaving the precise definitions, premises, equivalences, axioms, and
machine artifact open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`.

The immediately adjacent target `THM-M-1408` is specifically the Ornstein isomorphism theorem and
has the same short gloss. This makes an unreviewed entropy-classification interpretation of
`THM-M-1407` especially unsafe: it could duplicate a different repository target rather than
identify this one.

## Component crosswalk

| Repository/source phrase | Possible mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `Bernoulli移位` | coordinate shift on a product probability space | a function or measurable equivalence induced by index reparameterization | Named object/family only; index and direction open |
| Bernoulli system | alphabet/base probability space and i.i.d. product law | `Measure.infinitePi`, product measurable space, base probability assumptions | Base category and nondegeneracy open |
| classification | isomorphism relation and a complete invariant, possibly entropy | measure-preserving conjugacy plus a source-selected invariant | Exact equivalence relation and invariant absent |
| dynamical property | invariance, ergodicity, mixing, or entropy formula | `MeasurePreserving`, `Ergodic`, or later source-specific predicates | No property is selected by the record |
| `已验证` | untrusted inventory label | no proposition and no proof object | Explicitly rejected as evidence |

## Source work required

Human-source status is `H4`, not `H0`. A later source/statement audit must preserve an immutable
primary or authoritative source, record edition and content hash, pinpoint the exact theorem and
definitions, transcribe every ordered binder, assumption, and conclusion, audit errata, reconcile
the result with `THM-M-1408`, and obtain independent review. Historical background or a textbook
definition alone cannot identify the repository's classification claim.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded source-name
search found no Bernoulli-shift declaration. `Mathlib.Probability.ProductMeasure` does provide
generic `Measure.infinitePi` and coordinate/reindexing results;
`Mathlib.Dynamics.Ergodic.Ergodic` provides generic `MeasurePreserving` and `Ergodic` predicates.
`IntakeProbe.lean` checks only these encoding APIs. Mathlib's occurrences of "Bernoulli" concern
probability distributions and are not a Bernoulli dynamical-shift theorem. These facts are
feasibility evidence only and give no statement, anchor-audit, or proof credit.
