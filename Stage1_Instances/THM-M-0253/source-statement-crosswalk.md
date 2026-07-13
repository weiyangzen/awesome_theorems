# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1822-1827` supplies exactly the title `插值序列定理`, attribution
to Lennart Carleson, the year 1958, the gloss `Hardy空间的插值序列` ("interpolating sequences
for Hardy spaces"), importance "high," and status `已验证`. Git blame attributes all six uncited
lines to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, formula, definition, ordered binder, hypothesis, conclusion, theorem locator, proof
boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7004-7029` repeats those fields while explicitly leaving the formal
system, foundation, precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Primary-work discovery lead

Crossref and OpenAlex metadata observed on 2026-07-13 identify:

> Lennart Carleson, *An Interpolation Problem for Bounded Analytic Functions*, American Journal of
> Mathematics 80(4), October 1958, pages 921-930, DOI `10.2307/2372840`.

This title, author, date, and subject make the paper a strong candidate for the intended primary
work. ZbMATH record `Zbl 0085.06504` supplies the full page range; Crossref supplies only the first
page. The metadata services reported the work as closed access, with no open repository copy or PDF.
JSTOR returned an access/error page rather than the article. Accordingly, the paper's theorem text,
last page, exact definitions, assumptions, conclusion, proof nodes, and corrections were not
inspected. Metadata identity is not statement evidence, and the repository itself does not cite the
paper. The candidate is therefore recorded as a lead supporting `H1`, not accepted `H0` evidence.

No claim is made that the catalog's plural "Hardy spaces" exactly denotes the paper's bounded-
analytic (`H^infinity`) problem. A future source audit must establish that identity rather than
infer it from standard terminology.

OpenAlex exposes an OCR-derived introduction fragment saying that the paper starts with points in
the unit disc and interpolation by a bounded analytic function, seeks a simple explicit condition,
and makes that condition necessary when the prescribed values range over arbitrary bounded
sequences. This narrows the candidate family but does not reveal a reliable displayed condition or
complete theorem. OCR text and reconstructed metadata are not substitutes for an inspected source
page.

As a secondary source lead only, Alberto Dayan's open arXiv paper *Interpolating Matrices*,
`arXiv:1912.03765v1`, page 1, defines `H^infinity` interpolation by arbitrary bounded data and states
the Carleson 1958 equivalence with a positive infimum of products of pseudohyperbolic distances.
That later restatement helps distinguish the 1958 product criterion from a separate
separation-plus-Carleson-measure characterization, but it is not admitted as the canonical root,
and its wording must not override the uninspected primary theorem.

## Component crosswalk

| Repository component | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Hardy spaces" | possibly bounded analytic functions on the unit disc; exponent and model not stated | analytic functions plus a bounded-range or norm predicate | paper title suggests bounded analytic functions; exact `H^p` choice open |
| "sequence" | ordered points, a set with an enumeration, or an evaluation family | `ℕ -> Complex.UnitDisc`, injectivity, or another sourced index type | indexing, distinctness, repetitions, and accumulation open |
| "interpolating" | surjectivity of evaluation onto a data space, perhaps with a uniform norm bound | quantified data and an existential analytic function | data space, norm, constants, and quantifier order open |
| theorem title | characterization of the interpolation property | one implication, an `iff`, or a conjunction of geometric/measure criteria | exact conclusion not supplied |
| Carleson / 1958 | candidate paper above | immutable source identity and pinpoint crosswalk | bibliographic match only; full text and theorem locator uninspected |
| `已验证` | untrusted inventory label | source review plus kernel evidence would be required | no H or M credit |

## Candidate formulations not credited

Classical literature associates bounded-analytic interpolation with several formulations involving
unit-disc evaluation, uniform pseudohyperbolic separation, Blaschke products, and Carleson-type
conditions. Intake does not assert their exact formulas, equivalence, constants, or attribution to
a particular page. It also does not extend the result to finite `p`, the upper half-plane, other
function spaces, vector data, or several variables. Those are source questions, not harmless Lean
encoding choices.

## Pinned Lean boundary

Pinned mathlib contains `Complex.UnitDisc`, `AnalyticOnNhd`, `Bornology.IsBounded`, sequence and
injectivity primitives, and `Complex.canonicalFactor`. That factor has a pole at its parameter and
is not directly the zero-at-the-point Blaschke factor in the candidate separation product. The
module contains a TODO to formulate the canonical decomposition. A bounded lexical
search found no exact Hardy-space or Carleson interpolating-sequence declaration. The intake probe
checks adjacent APIs only and declares no target or proof body.

## Source gate

Before exact statement freeze, accountable reviewers must lawfully preserve an immutable primary
or authoritative edition, locate the exact theorem and all incorporated definitions, map every
domain, binder, data-space and norm clause, hypothesis, conclusion, normalization, constant, and
boundary case, inspect corrections and errata, reconcile the catalog's Hardy-space wording, and
independently approve fidelity to `THM-M-0253`. Only then may the statement phase choose minimal
imports, serialize the elaborated expression and environment, compile credited transports, and run
the four required mutation classes.
