# Scope map

## Preserved theorem family

- A complex-valued function on the whole complex plane.
- Entire holomorphicity under a source-selected convention.
- Nonconstancy of that function.
- At most one complex value outside its range.

These bullets delimit the recognizable Little Picard theorem. They are not an accepted canonical
statement or a proof.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative source edition and exact theorem/definition
   locators, map all incorporated assumptions and the proof boundary, inspect corrections and
   errata, and obtain independent source review.
2. Freeze "entire" as a function `f : Complex -> Complex` differentiable everywhere, analytic on
   all of `Set.univ`, or another source-faithful encoding, with a checked transport between any
   credited forms.
3. Freeze nonconstancy as the absence of `c` with `f = Function.const Complex c`, the absence of
   one value taken at every input, or an explicit pair of inputs with distinct outputs. Binder order
   and constructive/classical transports must be recorded.
4. Freeze "at most one exception." Candidate forms are `((Set.range f)ᶜ).Subsingleton`,
   `((Set.range f)ᶜ).encard <= 1`, pairwise equality of omitted values, or existence of a value `a`
   such that every `w != a` lies in the range. The last form permits `a` itself to be attained and
   therefore covers the surjective case; demanding an actually omitted value would be stronger.
5. Decide whether the source root is only the range conclusion or includes an equality/classification
   of the omitted set, a multiplicity statement, or a named exceptional value. The catalog gloss
   supplies none of those strengthenings.
6. Resolve boundary cases explicitly: constant functions are excluded; affine nonconstant and
   surjective entire functions must be admitted. Pinned `Complex.range_exp` supplies the sharp
   one-exception example for the exponential; it is boundary evidence and cannot define or prove
   the general conclusion.

## Explicit exclusions

- Big Picard near an essential singularity (`THM-M-0229`).
- Liouville's theorem for bounded entire functions (`THM-M-0224`).
- The open mapping theorem (`THM-M-0235`) or the fundamental theorem of algebra alone.
- A theorem for polynomials, exponentials, meromorphic functions, punctured domains, or arbitrary
  Riemann surfaces substituted for the global entire-function theorem.
- A conclusion that assumes a chosen omitted value, claims every function omits exactly one value,
  or adds infinite-preimage/multiplicity conclusions absent from the catalog.
- The untrusted `已验证` label, a theorem name, a nearby API, or the first main theorem of value
  distribution used as H0 or M0 evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies global complex differentiability,
analyticity, range, subsingleton/cardinality, Liouville, open-mapping, and early value-distribution
interfaces. A bounded repo-local and pinned-source search found no exact Little Picard terminal
declaration. That result is intake discovery only, not an exhaustive external anchor audit or a
global absence claim.
