# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10404-10409` supplies exactly the title `随机动力系统`, Ludwig
Arnold, 1998, the gloss `随机微分方程的动力学`, importance "high," and status `已验证`. The record
entered the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` and contains no
bibliographic identifier or theorem statement.

`Docs/Stage0_Blueprint.md:38726-38751` repeats the gloss while explicitly leaving definitions and
premises, proof route, dependencies, equivalent formulations, axioms, machine status, and artifact
links open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`.

## Bibliographic candidate

The attribution and year strongly match Ludwig Arnold, *Random Dynamical Systems*, Springer
Monographs in Mathematics, Springer, 1998, DOI `10.1007/978-3-662-12878-7`. Crossref confirms the
author, title, publisher, year, and electronic ISBN `978-3-662-12878-7`. This identifies a book, not
one target proposition. Publisher-accessible front matter describes the available text as a
corrected second printing from 2003, so alignment with the original 1998 printing and any
correction delta must remain part of the source audit.

The publisher's chapter records sharpen the ambiguity:

- Chapter 1, *Basic Definitions. Invariant Measures*, DOI
  `10.1007/978-3-662-12878-7_1`, pages 3-47, says Section 1.1 defines a random dynamical system or
  cocycle and lists distinct results including Theorems 1.1.6, 1.3.2, 1.4.5, 1.5.10, and 1.6.4.
- Chapter 2, *Generation*, DOI `10.1007/978-3-662-12878-7_2`, pages 49-107, lists different
  generation and converse theorems. Its summary names Theorems 2.2.1, 2.2.2, and 2.2.13 for random
  differential equations; Theorems 2.3.26, 2.3.29, and 2.3.30 for semimartingale-driven stochastic
  differential equations; and additional continuity, smoothness, and invariant-measure results.

These publisher summaries were inspected on 2026-07-12. They are bibliographic discovery evidence,
not `H0`: the full edition, definitions, exact theorem text, assumptions, proof boundary,
corrections, and errata have not been frozen or independently reviewed.

A closely matching primary article is Ludwig Arnold and Michael Scheutzow, *Perfect cocycles
through stochastic differential equations*, **Probability Theory and Related Fields** 101(1)
(1995), 65-88, DOI `10.1007/BF01192196`. Its full publisher PDF was inspected on 2026-07-12
(1,046,566 bytes; observed SHA-256
`5e2317952b360b4417ee8318f049fbf1b529c2887efaeeb5e86a9dd2304c8581`). Theorem 28 constructs a
global semimartingale RDS from a sufficiently regular semimartingale helix; Theorem 30 gives a
converse under its stated regularity and local-characteristic hypotheses; Theorem 31 perfects a
very crude continuous cocycle under topological and measure-action assumptions. This is a stronger
primary candidate than a title match alone, but it still does not resolve which, if any, of these
three propositions the 1998 catalog entry intends. No theorem in the article is selected or given
H credit at intake, and its exact source audit and independent review remain downstream work.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `随机动力系统` | a measurable cocycle over a measure-preserving base system, or a theorem about one | exact base action, time object, state space, cocycle fields, measurability, and one `Prop` conclusion | topic/family only |
| "stochastic differential equations" | an SDE with a specified driver, coefficients, filtration, integral, and solution notion | stochastic integral and SDE interfaces, adapted solution, existence/uniqueness and version policy | all choices absent |
| "dynamics" | generation, cocycle perfection, invariant measures, regularity, stability, attractors, or asymptotics | one source-selected conclusion with exact binders and boundary cases | no conclusion selected |
| Ludwig Arnold / 1998 | likely provenance for the monograph and its many RDS results | immutable source locator and statement crosswalk | book identified; theorem unresolved |
| `已验证` | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Neighbor and substitution boundary

The repository separately schedules random attractors and multivalued random dynamical systems, so
neither may be folded into this target. It also separately schedules coupling/synchronization.
Likewise, Arnold's book definition of an RDS is not itself the catalog's missing truth-valued
theorem, and no one generation theorem may be chosen merely because the gloss mentions stochastic
differential equations.

## Source gate

Before the target can leave `H5`, an accountable reviewer must preserve an immutable primary or
authoritative edition, select one exact theorem and incorporated definition chain, transcribe every
domain, ordered binder, hypothesis, conclusion, exceptional set, local/global qualifier, and
degenerate case, inspect the proof boundary and errata, and justify why it represents
`THM-M-1424`. A second qualified reviewer must approve that mapping. The selected proposition's
human-proof status must then be classified afresh rather than inherited from `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks generic APIs for `Filtration`, `Adapted`, `StronglyAdapted`, `ProbabilityTheory.Kernel`,
`MeasurePreserving`, and `Flow`. Mathlib's `Flow` is a deterministic continuous monoid action and
must not be confused with a random cocycle. A bounded exact-topic search found no RDS/SDE or
semimartingale target interface; a generic `cocycle` search returned unrelated cohomological and
gluing uses. This is intake discovery only, not the downstream immutable anchor audit or an absence
claim about all external Lean projects.

The canonical module, expression, expression hash, checked transports, and mutation tests remain
null. No H0, M0, R0, audit completion, or theorem completion is claimed.
