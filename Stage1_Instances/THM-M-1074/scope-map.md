# Scope map

## Included theorem family

- A Poisson counting process `N` with a fixed nonnegative rate `lambda`.
- An iid sequence of marks or jump sizes `Y_k`, independent of the entire counting process.
- The finite random sum `X_t = sum_{k=1}^{N_t} Y_k`, with the empty sum equal to zero.
- The compound-Poisson law at each time and its characteristic-function (or Fourier-transform)
  formula, if this is the conclusion of the selected source theorem.
- Stationary independent increments and stochastic-process status, if these are conclusions of the
  selected source theorem rather than assumptions packaged into a definition.

## Decisions required at statement freeze

The selected source must fix the state space of the marks (`R`, `R^d`, or an additive topological
group), time domain, rate convention, initial value, filtration and adaptedness assumptions, and
whether equality is pointwise, almost sure, in distribution, or an equality of laws. It must also
settle whether zero rate is admitted, how the iid marks are indexed, independence from the whole
process versus each marginal, finite-dimensional versus process-level conclusions, and the precise
characteristic-function sign convention. Binder order, universes, measurability, integrability, and
the empty-sum case must follow those decisions.

## Explicit exclusions

- Merely defining `CompoundPoissonProcess` with the desired independent-increment or distribution
  conclusions stored as fields.
- An ordinary Poisson process with unit jumps as a substitute for arbitrary iid marks.
- A single compound-Poisson random variable without the time-indexed construction, unless the
  selected source establishes that this is exactly the repository target.
- An arbitrary Levy process, Poisson point process, or Poisson random measure without a checked
  specialization to the random-sum process.
- Assuming the characteristic-function identity or independent-increment conclusion that the
  theorem is meant to prove.
- Treating the metadata label `已验证` as source or kernel evidence.

The formal target must expose concrete probability measures, independence, iid marks, the Poisson
count, finite random sums, and the chosen distributional/process conclusion, or record a precise
missing-API blocker.
