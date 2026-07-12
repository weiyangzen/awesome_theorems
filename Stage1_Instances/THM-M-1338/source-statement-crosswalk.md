# Source-statement crosswalk

## Repository record

The repository catalog at `Docs/researches/math_theorems.md` records exactly:

| Field | Catalog value | rev-5.6 interpretation |
|---|---|---|
| title | Bihari-LaSalle inequality | theorem-family locator only |
| attribution | Bihari/LaSalle | no exact work or result selected |
| date | 1956 | discovery key, not source fidelity |
| statement | nonlinear Gronwall inequality | topic gloss, not a proposition |
| formalization status | verified | explicitly untrusted metadata |

The Stage0 projection adds no binder, hypothesis, conclusion, source edition, or formal artifact.

## Primary-source candidates

The strongest exact-year match found is I. Bihari, *A generalization of a lemma of Bellman and its
application to uniqueness problems of differential equations*, Acta Mathematica Academiae
Scientiarum Hungaricae 7(1), 81-94 (1956), DOI `10.1007/BF02022967`. Crossref and Springer metadata
were inspected on 2026-07-13 (Asia/Shanghai). They establish bibliographic identity only. The
publisher reports paid access and did not deliver the article PDF or main theorem text to this
worker, so the generalized lemma's exact page/formula and the article's internal definitions and
proof have not been inspected.

J. LaSalle's *Uniqueness Theorems and Successive Approximations*, Annals of Mathematics 50(3), 722
(1949), DOI `10.2307/1969559`, is a bibliographic candidate for the attribution history, not the
catalog's exact-year source and not an accepted source for the root. The relationship between the
Bihari and LaSalle formulations requires a source review; the combined name does not license their
silent conflation.

## Component crosswalk

The following table records a candidate modern result family for future source comparison. Every
row is open and confers no exact-statement or proof credit.

| Catalog/candidate component | Possible mathematical role | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| nonlinear Gronwall | scalar integral comparison beyond a linear response | functions `Real -> Real`, ordered inequalities | family identified; root variant open |
| initial value | additive constant such as `u0` at a base time | explicit real binder and nonnegativity premise | binder and zero case open |
| time weight | nonnegative integrable coefficient | `IntervalIntegrable` plus pointwise or a.e. sign | regularity and equality mode open |
| response `omega` | nonnegative/nondecreasing nonlinear modulus | real function with source-selected continuity, sign, and monotonicity | exact assumptions open |
| hypothesis | `u` is bounded by initial value plus an interval integral | `intervalIntegral` and an inequality over an interval | endpoint and integrability conventions open |
| reciprocal transform | integral of `1 / omega` from a normalization point | interval integral plus reciprocal and domain proof | normalization and zero behavior open |
| inverse transform | invert the monotone auxiliary function | `StrictMonoOn`/inverse or source-faithful generalized inverse | inverse convention and range open |
| conclusion | transformed pointwise upper bound | quantified inequality with cutoff/domain proof | exact formula and quantifier order open |
| uniqueness application | use the bound when the initial separation is zero | possible later corollary, not necessarily root | excluded until source selection |

## Lean and evidence boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.Analysis.ODE.Gronwall` and interval-integral infrastructure. The local probe checks
`gronwallBound`, `le_gronwallBound_of_liminf_deriv_right_le`,
`norm_le_gronwallBound_of_norm_deriv_right_le`, `intervalIntegral.integral_mono_on`, and
`intervalIntegral.integral_comp_mul_deriv`. These interfaces make later work plausible but do not
encode the nonlinear reciprocal-transform conclusion.

A bounded source-name search over repo-local Lean and pinned mathlib returned no Bihari, LaSalle,
nonlinear Gronwall, or generalized Gronwall declaration. This is not the later immutable external
anchor audit and does not establish global absence.

Before `H0`, an independent reviewer must inspect and hash the complete selected primary edition,
pinpoint the exact result and definitions, map every assumption and conclusion, check errata and the
Bihari/LaSalle naming relationship, and approve the crosswalk. Before statement credit, those rows
must map to one elaborated Lean expression with checked boundary mutations. The first downstream
blocker is therefore exact source-result selection and review, not Lean proof search.
