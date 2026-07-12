# Scope map

## Provisional included claim

- The one-dimensional torus, represented by a source-compatible circle model and Haar measure.
- Real- or complex-valued periodic functions in `L^p`, for `1 < p < infinity`.
- The conjugate-function operator, equivalently the circular Hilbert transform only after a checked
  convention bridge, defined by a principal-value kernel or Fourier multiplier.
- Strong `L^p` boundedness: membership of the conjugate function in `L^p` and a norm estimate with a
  constant depending only on `p`.

## Frozen formal conventions

The Lean target uses `AddCircle (1 : Real)` with `AddCircle.haarAddCircle`, complex-valued `Lp`
equivalence classes, `p : ENNReal` with `1 < p` and `p != top`, and Fourier multiplier `i` on
negative modes, `-i` on positive modes, and zero at mode zero. It asserts existence of a
nonnegative real `C_p` and an `Lp` conjugate `g` satisfying the coefficient identity and norm bound.

## Source-review decisions still required

An independently inspected source must confirm or challenge the selected period, measure,
complexification, multiplier sign, zero-mode convention, and non-sharp existential bound. Any
principal-value formulation needs a later checked bridge rather than silent identification.

The ordered binders must make `p`, its endpoint hypotheses, `f`, and any bound constant explicit.
Boundary treatment must cover constant functions, the zero Fourier mode, null-set changes, and the
excluded endpoints `p = 1` and `p = infinity`.

## Explicit exclusions

- The real-line Hilbert transform as a substitute for the periodic conjugate-function theorem.
- Only the `L^2` Fourier-basis isometry as a substitute for the full `1 < p < infinity` result.
- Kolmogorov's weak-type endpoint theorem, Fatou boundary limits, or Fourier-series convergence.
- Boundedness of an arbitrary assumed operator packaged as a hypothesis or structure field.
- Identification of principal-value and Fourier-multiplier forms without a checked transport.
- The repository label `已验证` as human-source or kernel-proof evidence.

No canonical Lean target is frozen at intake. Availability of `L^p`, Haar measure, and Fourier-basis
APIs does not supply the missing conjugate-function construction or its strong-type bound.
