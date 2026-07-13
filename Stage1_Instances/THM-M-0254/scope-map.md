# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0254`, the label "functions of bounded mean oscillation," the
attribution Fritz John and Louis Nirenberg, the year 1961, and the gloss "characterization of BMO
functions." Importance "high" and status `已验证` are catalog metadata, not source or kernel
evidence. Intake preserves only the bounded-mean-oscillation characterization family.

The matching bibliographic record is John and Nirenberg's 1961 paper *On functions of bounded mean
oscillation*. That title identifies the subject but does not turn the catalog gloss into one exact
theorem. Primary-text inspection and a pinpoint theorem selection remain open.

## Proposition-changing decisions

An approved source correction must select one truth-valued root and freeze:

- whether the theorem is the BMO definition, the John-Nirenberg distribution estimate,
  exponential integrability, equivalence of mean-oscillation exponents, or another sourced
  characterization;
- whether the carrier is `R^n`, a complex domain or boundary, an interval, a space of homogeneous
  type, or another source-specified measure space;
- the dimension range, real or complex scalar field, measurable and locally integrable function
  model, and equality almost everywhere;
- cubes or balls, their orientation and endpoint convention, admissible radii or side lengths,
  measurability, and whether the averaging family is centered, uncentered, dyadic, or unrestricted;
- the average, mean-oscillation functional, absolute value or norm, exponent, supremum, and the
  extended-real or real-valued finiteness convention;
- whether BMO is a raw function predicate, seminormed space, or quotient modulo almost-everywhere
  constants, including the zero-seminorm theorem;
- every distribution threshold, exponential coefficient, leading constant, dimension dependence,
  and strict or non-strict inequality in a quantitative reading;
- whether a characterization is one implication or an equivalence and the checked directions for
  every credited alternate formulation; and
- all universes, ordered binders, quantifier dependencies, hypotheses, and conclusion clauses.

These choices produce inequivalent propositions. They are a resolution ledger, not a canonical
statement.

## Candidate families not credited

- The definition or membership criterion using uniformly bounded mean absolute oscillation over
  Euclidean cubes.
- The John-Nirenberg distribution inequality for superlevel sets of local oscillation.
- Exponential integrability of centered BMO functions on each cube.
- Equivalence of `L^1` and `L^p` mean-oscillation seminorms.
- Analytic BMO/BMOA, boundary, interval, ball, dyadic, martingale, or homogeneous-space variants.

No family in this list is selected, asserted, or credited at intake.

## Degenerate and boundary cases

Source review must explicitly resolve dimension zero; empty or null cubes; degenerate, open,
closed, or half-open boxes; balls versus cubes; infinite-measure sets; constant functions and the
seminorm kernel; almost-everywhere representatives; real versus complex values; nonintegrable
inputs; zero or infinite BMO seminorm; zero and negative distribution thresholds; strict versus
non-strict tails; exponent endpoints; and the exact dependence and positivity of all constants.
No case is silently excluded.

## Neighboring target boundaries

`THM-M-0302` separately names the John-Nirenberg inequality, has the same authors and year, and
gives the explicit gloss "exponential integrability of BMO functions." It is the likely identity
of at least one reading of this vague entry, not automatically a child obligation or reusable proof.
Only the integration lane may decide duplication, canonical ownership, or a checked relationship.

`THM-M-0301` and `THM-M-0363` separately name BMO-`H^1` duality. Dual representation is not the
unspecified characterization here. None of these dossiers supplies inherited source, statement,
status, receipt, or proof credit.

## Explicit exclusions

A definition that stores boundedness as a field, a generic integral-average identity, a box-volume
formula, or a one-cube estimate is not the catalog theorem. A specialized dyadic, finite,
one-dimensional, bounded-domain, martingale, or holomorphic result cannot replace a general
Euclidean reading without a source-approved relationship. Numerical sampling, plots, floating-point
integration, and the catalog word `已验证` supply no theorem evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies Bochner set averages, centering
identities, and Euclidean box-volume formulas, but a bounded exact-topic search found no
target-specific bounded-mean-oscillation or John-Nirenberg declaration. This is intake discovery
only, not an exhaustive anchor audit or a global absence claim.
