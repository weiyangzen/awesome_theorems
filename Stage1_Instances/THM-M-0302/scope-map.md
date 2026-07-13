# Scope map

## Preserved theorem family

The repository fixes target `THM-M-0302`, the name "John-Nirenberg inequality," Fritz John and
Louis Nirenberg, the year 1961, and the gloss "exponential integrability of BMO functions."
Together these identify the classical Euclidean BMO exponential-integrability theorem family.
Importance "high" and `已验证` are catalog metadata, not source or kernel evidence.

Bibliographic metadata matches John and Nirenberg's 1961 paper *On functions of bounded mean
oscillation*. No primary theorem text, pinpoint locator, or incorporated definition chain was
admitted here, so intake preserves the family without asserting an exact proposition.

## Proposition-changing decisions

The statement phase must source-freeze:

- the carrier `R^n`, a positive dimension range, Lebesgue measure, and real or complex values;
- locally integrable functions versus almost-everywhere equivalence classes;
- admissible cubes, orientation and endpoint convention, nonzero finite volume, and set averages;
- the exact BMO seminorm or bound, quotient by almost-everywhere constants, and normalization;
- whether the root is averaged exponential integrability, a distribution-tail inequality, or an
  explicitly source-proved equivalence with checked directions;
- centering at each cube average, the absolute value or norm, and integrability versus a numerical
  upper bound for the exponential average;
- the exponential coefficient and leading bound, their positivity, existential or explicit form,
  and dependence on dimension, scalar convention, and the BMO normalization;
- how division by a zero BMO seminorm is avoided or handled for constant functions;
- all universes, ordered binders, quantifier dependencies, hypotheses, and conclusion clauses.

These choices yield inequivalent propositions. This is a resolution ledger, not a canonical
statement.

## Candidate encodings not credited

- On every nondegenerate cube, the exponential of a dimensionally normalized centered oscillation
  has uniformly bounded set average.
- The measure of the set where centered oscillation exceeds a threshold decays exponentially.
- A checked equivalence or derivation connecting those two forms under source-selected constants.

No candidate is asserted or credited at intake. In particular, the distribution form cannot be
silently substituted merely because it is commonly called the John-Nirenberg inequality.

## Boundary cases

Source review must explicitly resolve dimension zero; empty, null, degenerate, open, closed, and
half-open cubes; infinite-measure sets; constant functions; zero and infinite BMO seminorm; raw
functions versus almost-everywhere representatives; real versus complex values; strict versus
non-strict distribution thresholds; zero or negative thresholds; local integrability of the
exponential; and positivity and dependence of all constants. No case is silently excluded.

## Explicit exclusions

- A BMO definition, structure field, or hypothesis that assumes the desired exponential bound.
- A one-cube estimate, bounded function lemma, or Chebyshev/Markov implication without the
  source-mapped John-Nirenberg estimate.
- A dyadic, martingale, BMOA, bounded-domain, interval-only, homogeneous-space, discrete, or
  one-dimensional specialization presented as the classical source theorem.
- Generic set-average, box-volume, exponential-integral, or Markov APIs by themselves.
- Numerical sampling, an oracle, an unchecked certificate, or the catalog's `verified` label.

## Neighboring target boundary

`THM-M-0254` separately catalogs "functions of bounded mean oscillation" with the vague gloss "a
characterization of BMO functions." Its dossier identifies this target as the owner of the explicit
John-Nirenberg/exponential-integrability reading. That neighbor is discovery evidence only and
transfers no source, statement, receipt, or proof credit. `THM-M-0301` and `THM-M-0363` own
BMO-`H^1` duality, not exponential integrability.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies set averages, Euclidean box
volumes, exponential-integral facts, and Markov inequalities. A bounded exact-topic search found no
target-specific BMO or John-Nirenberg declaration. This is intake discovery, not the downstream
immutable anchor audit or a global absence claim.
