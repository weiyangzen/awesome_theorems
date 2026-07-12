# Scope map

## Preserved theorem family

The repository fixes only target `THM-M-1355`, the title `线性系统的稳定性` (stability of linear
systems), the gloss `线性系统的稳定性判据` (a stability criterion for linear systems), the
twentieth century, an attribution to many mathematicians, high importance, and untrusted status
`已验证`. Intake preserves a classification family linking a linear system to a stability notion.
It does not turn the gloss into a particular spectral or Lyapunov criterion.

## Decisions required at statement freeze

An approved statement phase must freeze all of the following from an immutable source:

1. Continuous time, discrete time, a time scale, or a semigroup; autonomous versus time-varying,
   switched, delayed, or periodic dynamics.
2. Homogeneous state evolution versus affine, forced, input-output, or controlled dynamics, and the
   exact distinction between internal and BIBO or input-to-state stability.
3. Finite-dimensional real or complex coordinates versus a normed or Banach space, including the
   matrix/operator carrier, topology, norm, dimension, universes, and typeclass assumptions.
4. The system equation, time and solution domain, initial-value policy, equilibrium, and whether an
   arbitrary equilibrium is translated to zero by a checked transport.
5. Bounded, Lyapunov, asymptotic, exponential, uniform exponential, marginal, robust, or another
   stability predicate, with exact locality and quantifier order.
6. A spectral/eigenvalue, Jordan, matrix-exponential, Lyapunov matrix inequality, characteristic-
   polynomial, fundamental-matrix, resolvent, or frequency-domain criterion.
7. Necessary, sufficient, or iff direction; all regularity, well-posedness, diagonalizability,
   controllability, observability, positivity, or coercivity assumptions.
8. Every boundary convention and excluded case, plus all checked alternate-form transports.

These choices produce inequivalent propositions. They are a resolution ledger, not a statement.

## Candidate roots not credited

- For a finite-dimensional continuous-time autonomous system `x' = A x`, all trajectories are
  bounded for forward time iff the eigenvalues have nonpositive real part and every eigenvalue on
  the imaginary axis is semisimple.
- The same system is globally asymptotically or exponentially stable iff every eigenvalue has
  strictly negative real part, with a source-specific exponential norm estimate.
- A finite-dimensional discrete-time system is asymptotically stable iff its eigenvalues lie
  strictly inside the unit disk; bounded stability needs a separate boundary semisimplicity clause.
- Hurwitz stability is equivalent to existence of a positive-definite solution of a source-selected
  continuous Lyapunov matrix inequality or equation.
- A time-varying fundamental matrix or a `C0` semigroup obeys a source-selected uniform exponential
  estimate under assumptions not present in the catalog.

None of these candidates is selected, conjoined, weakened, or credited at intake.

## Boundary cases

Source review must explicitly dispose of the zero-dimensional state space; the zero and identity
operators; zero initial state; eigenvalues on the imaginary axis or unit circle; nilpotent Jordan
parts; repeated, defective, and nonnormal matrices; empty or non-point spectrum; real matrices with
complexified eigenvalues; forward versus two-sided time; local versus global behavior; and the
relationship among bounded, asymptotic, and exponential stability.

For time-varying or infinite-dimensional variants it must also address the evolution-family or
semigroup existence policy, unbounded-operator domains, continuous/residual spectrum, and whether
pointwise decay is upgraded to uniform exponential decay. Inputs, outputs, forcing, switching, and
delays may not be silently ignored.

## Neighbor and substitution exclusions

- `THM-M-1342` covers general Lyapunov equilibrium-stability theory, not this unspecified linear-
  system classification.
- `THM-M-1344` covers transfer between a nonlinear system and its linearization. Stability of the
  linear system may be an input there, but cannot replace the nonlinear conclusion.
- `THM-M-1352` through `THM-M-1354` concern periodic systems, Floquet theory, its principal-matrix
  theorem, and characteristic exponents; they do not select this generic root.
- `THM-M-1356` is the Routh-Hurwitz coefficient criterion, and `THM-M-1357` is the Nyquist
  frequency-domain criterion. Neither may be absorbed merely because both contain the word
  "stability."
- A continuous-time Hurwitz theorem may not substitute for a discrete-time, nonautonomous,
  semigroup, or controlled-system theorem, or conversely.
- Eigenvalue, spectrum, matrix exponential, Jordan, norm, and ODE APIs are substrate, not closure.
- An assumed stability field, numerical eigenvalue computation, simulated trajectory, phase plot,
  or the label `已验证` supplies no proof credit.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or accepted proof state is frozen at intake.
