# Borwein sine series: full study

## FS-statement

The series is

\[
\sum_{n=1}^{\infty}
  \frac{(2/3+(1/3)\sin n)^n}{n}.
\]

Every term is nonnegative.  A crude bound by `1/n` is insufficient because
the coefficient can approach one; the proof must quantify how often integer
arguments approach maxima of sine.

## FS-local-decay

Write `δ_n` for the distance from `n` to `π/2 + 2πℤ`.  Near a maximum,
`1 - sin n` is comparable to `δ_n²`.  Away from a fixed neighbourhood of the
maxima there is uniform exponential decay.  Within it,

\[
a_n \ll n^{-1}\exp(-c n\delta_n^2).
\]

This is the analytic reduction used by the proof DAG.

## FS-return-counting

For a dyadic block `N ≤ n < 2N`, divide returns according to
`2^{-j-1} < δ_n ≤ 2^{-j}`.  Ordinary spacing bounds the count at each
level.  At the very smallest scales, a lower bound for rational approximation
to `π` rules out two excessively close returns and supplies a minimum possible
`δ_n`.  Summing `N⁻¹ exp(-cN 2^{-2j})` times these counts yields a block
bound whose sum over dyadic `N` converges.

## FS-formalization-map

`PU-01` fixes the frozen proposition. `PU-02` expands the positive answer.
`PU-03` records coefficient range and nonnegativity. `PU-04` performs the
exponential majorization. `PU-05` converts closeness to a Diophantine return.
`PU-06` partitions/counts returns. `PU-07` sums the majorant. `PU-08` closes
the biconditional. `PU-09` and `PU-10` provide the bidirectional crosswalk and
trust audit.

## FS-downstream

The completed statement supplies the Stage6 alias
`S6-CLM-00003985` / `S6-VAR-00006196`, records a reusable pattern for
nonnegative power series with almost-periodic coefficients, and demonstrates
the boundary between a sorry-backed source statement and a claim-owned proof.

## FS-exceptional-cases

The proof does not discard finitely many small indices: they are summable as a
finite prefix.  Zero is absent because the index is positive naturals.  Exact
sine maxima cannot occur at an integer.  Extremely close approximate maxima
are retained and bounded through the quantitative irrationality input rather
than assumed away.

## FS-trust-boundary

No conclusion is drawn from the source theorem body.  JSON authority seals
only protect dossier integrity; they do not prove mathematics.  Only the
Master's independent trust-zero elaboration of integrated Lean bytes can turn
this provisional candidate into an accepted theorem.
