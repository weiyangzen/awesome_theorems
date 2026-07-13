# Scope map

## Preserved catalog scope

The repository fixes only the label `赫维茨定理`, Adolf Hurwitz, 1903, and the gloss
`傅里叶级数的绝对收敛`. The preserved topic boundary is therefore a Hurwitz result concerning
Fourier coefficients or series and absolute convergence. The intake does not silently replace this
with a familiar theorem that happens to share the Hurwitz name.

The bibliographic match for the attribution and year is Hurwitz's paper *Über die Fourierschen
Konstanten integrierbarer Funktionen*, *Mathematische Annalen* 57 (1903), 425-446. The inspected
paper does not expose one theorem literally named "absolute convergence of Fourier series." It
contains several candidate results, so the catalog-to-source root remains open.

## Source candidate branches not credited

- On page 436, Hurwitz notes that the bilinear Parseval coefficient series is absolutely
  convergent even when its mixed products are separated.
- On pages 438-440, Hurwitz derives an absolutely convergent Fourier expansion for an indefinite
  integral of a Riemann-integrable function, with endpoint and additive-constant conventions.
- Pages 429-436 establish a general Parseval identity for Riemann-integrable functions.
- Pages 441-442 give uniqueness up to a function "of integral zero" and Fejer recovery at
  continuity points.
- Pages 442-446 prove the sign-change result now commonly called the Sturm-Hurwitz theorem.

Each branch differs in binders, hypotheses, conclusion, and proof architecture. None is selected or
credited as the exact root at intake.

## Proposition-changing decisions

An approved statement phase must fix all of the following from a reviewed source crosswalk:

- whether the root is about a function's own Fourier series, the series for an indefinite
  integral, a coefficient-product series, or a sign-change consequence;
- the function domain (`[0, 2*pi]`, a periodic real function, or `AddCircle T`), scalar field, and
  Riemann versus Lebesgue integrability convention;
- real sine/cosine coefficient pairs versus complex coefficients indexed by integers, including
  normalization and treatment of the zero coefficient;
- the exact regularity hypotheses, if the intended result is a later sufficient criterion for
  absolute summability rather than one of Hurwitz's 1903 statements;
- whether "absolute convergence" means summability of coefficient norms, pointwise absolute
  convergence of evaluated terms, uniform absolute convergence, or absolute convergence of a
  bilinear coefficient series;
- ordered binders, endpoint periodicity, additive integration constant, equality at endpoints,
  almost-everywhere versus pointwise equality, and every zero-function or zero-period case; and
- which implication or equivalence is the root, and which neighboring results are only lemmas or
  corollaries.

## Explicit exclusions

- The complex-analysis Hurwitz theorem on zeros of locally uniformly convergent holomorphic
  functions is unrelated.
- The Routh-Hurwitz stability criterion and Hurwitz matrix/determinant results are unrelated.
- The Hurwitz zeta formula, Riemann-Hurwitz theorem, Hurwitz's irrational number theorem, and
  Hurwitz-Radon results are unrelated.
- The Sturm-Hurwitz sign-change theorem cannot replace an absolute-convergence root without an
  accepted catalog correction.
- Fejer convergence, Parseval/Plancherel, Fourier inversion, Riemann-Lebesgue, and Poisson summation
  remain neighboring results, not interchangeable targets.
- A premise that already assumes `Summable (fourierCoeff f)` may support a convergence corollary
  but cannot serve as proof that Hurwitz hypotheses imply absolute summability.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies `fourierCoeff`,
`hasSum_sq_fourierCoeff`, `tsum_sq_fourierCoeff`, and
`hasSum_fourier_series_of_summable` in `Mathlib.Analysis.Fourier.AddCircle`. The intake probe checks
these interfaces and an `AddCircle (2 * Real.pi)` specialization. It does not encode the source's
Riemann-integrability predicate, select one source theorem, prove coefficient summability, compile
a real/complex coefficient transport, or provide a target proof body. Formal anchor and provenance
audits remain downstream.
