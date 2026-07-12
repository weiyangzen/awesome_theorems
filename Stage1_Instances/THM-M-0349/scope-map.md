# Scope map

## Provisional included claim

- The one-dimensional torus, represented by a source-compatible circle model and Haar measure.
- Real- or complex-valued periodic functions in `L^p`, for `1 < p < infinity`.
- The conjugate-function operator, equivalently the circular Hilbert transform only after a checked
  convention bridge, defined by a principal-value kernel or Fourier multiplier.
- Strong `L^p` boundedness: membership of the conjugate function in `L^p` and a norm estimate with a
  constant depending only on `p`.

## Decisions required at statement freeze

The exact source must determine the circle parametrization and measure normalization; real or
complex scalars; whether functions are equivalence classes or chosen measurable representatives;
the sign and zero-mode conventions; the principal-value or Fourier-multiplier definition and their
relationship; whether existence almost everywhere is included; the form and sharpness of `C_p`;
and whether the result is an operator norm theorem or a pointwise-function theorem.

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
