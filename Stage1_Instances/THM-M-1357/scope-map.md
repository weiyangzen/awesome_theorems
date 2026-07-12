# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1357`, the title "Nyquist stability criterion," the gloss
"stability of a feedback system," attribution to Harry Nyquist, and the year 1932. Intake preserves
that control-theory theorem family. It does not turn the attribution into a primary-source citation
or the untrusted status label into human-source or kernel evidence.

## Proposition-changing decisions

Before a canonical root can be frozen, an approved source selection must decide:

- the feedback topology and sign convention, including where the loop transfer function is
  measured and whether the characteristic function is `1 + L`, `1 - L`, or another normalized
  determinant;
- continuous or discrete time, scalar SISO or matrix MIMO scope, transfer-function or state-space
  semantics, and real or complex coefficients;
- rational, proper rational, meromorphic, delayed, or another admissible system class, with
  causality, well-posedness, and finite-dimensionality assumptions;
- internal, asymptotic, exponential, BIBO, input-output, or another stability notion, and whether
  stability uses the open or closed half-plane or disk;
- the Nyquist domain and contour, closure at infinity, orientation, mapping convention, and
  whether encirclements count `-1` by `L` or `0` by a characteristic function;
- the definitions and signs of the open-loop unstable-pole count `P`, closed-loop unstable-zero
  count `Z`, and net encirclement count `N`, including algebraic multiplicity;
- exclusions or indentations for poles, zeros, or the point `L = -1` on the contour, and the
  contribution of any detours or infinite semicircle;
- hidden pole-zero cancellations, coprimeness or minimal-realization assumptions, and the relation
  between a characteristic equation and internal closed-loop modes; and
- every ordered binder, hypothesis dependency, degenerate case, and direction of any equivalence.

These choices produce materially different propositions. This list is a resolution ledger, not a
canonical statement.

## Candidate families not credited

1. For a source-specified scalar rational open-loop transfer function and oriented right-half-plane
   contour, an argument-principle identity relates net encirclements of the critical point to the
   numbers of open-loop poles and closed-loop characteristic zeros.
2. Under source-specified properness, boundary, cancellation, and well-posedness assumptions, a
   negative-feedback closed loop is stable exactly when the Nyquist plot has the required net
   encirclement count relative to the open-loop unstable poles.
3. Generalized MIMO criteria use a determinant or return-difference matrix rather than a scalar
   loop transfer function.
4. Discrete-time variants use the unit circle and exterior-disk pole counts rather than an
   imaginary-axis Nyquist contour.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

- Replacing the target by the complex-analysis argument principle alone.
- Substituting the Routh-Hurwitz criterion (`THM-M-1356`) or the generic linear-system stability
  topic (`THM-M-1355`).
- Inferring internal stability from a transfer-function denominator without resolving hidden
  unstable cancellations or nonminimal realizations.
- Choosing SISO, MIMO, continuous-time, discrete-time, negative feedback, or a sign convention from
  memory rather than a reviewed source.
- Encoding the desired encirclement identity or stability conclusion as a structure field and
  projecting it.
- Treating a plotted locus, sampled frequency response, numerical winding computation, unchecked
  certificate, or control simulation as theorem proof.
- Crediting the catalog label `已验证`, Crossref metadata, an API typecheck, or a bounded no-match
  search as source fidelity or machine closure.

## Boundary cases

The statement phase must resolve poles or zeros on the imaginary axis or unit circle, a mapped
contour passing through the critical point, repeated poles and zeros, zero open-loop unstable poles,
zero or constant loop transfer functions, improper and nonrational systems, pure delays, positive
feedback, open-loop pole-zero cancellations, nonminimal realizations, hidden unstable modes, and
orientation or half-plane-boundary conventions.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, meromorphic divisors and orders, logarithmic
derivatives, and a complex circle parameterization provide adjacent mathematical substrate. A
bounded repository and pinned-mathlib search found no obvious named Nyquist, feedback-system,
transfer-function, encirclement, winding-number, or argument-principle declaration under the
recorded terms. The checked API probe and negative search are intake discovery inputs only, not an
exhaustive anchor audit, canonical target, or proof.
