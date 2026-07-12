# Scope map

## Source-justified scope

- Object: a stationary Gaussian process, with neither index set nor state space specified.
- Claimed result: an upper bound, with the bounded quantity and mode of control unspecified.
- Attribution: Xavier Fernique; the repository gives 1975 but no publication or theorem locator.
- Domain: probability theory and stochastic processes.

This is all that the repository source presently fixes. Intake does not choose a more convenient
Fernique theorem merely because mathlib already provides it.

## Decisions required at statement freeze

The statement phase must identify and inspect a primary source, then freeze whether the theorem is
about exponential integrability of a Gaussian measure on a separable Banach space, boundedness or
continuity of sample paths, a tail/moment bound for a process supremum, or another Fernique result.
For a process statement it must also freeze the index set and metric, stationarity convention,
separability/measurability and path assumptions, centeredness, covariance hypotheses, the random
variable being bounded, constants, and whether the conclusion is almost-sure, integrability, tail,
or expectation control. Empty index sets, degenerate covariance, zero processes, and infinite
suprema require explicit treatment.

## Explicit exclusions

- Substituting Borell-TIS, Dudley's entropy bound, Sudakov minoration, or Slepian's lemma.
- Replacing a process-supremum assertion by Fernique exponential integrability without a checked
  source and formal transport between the two statements.
- Encoding the desired bound as a field or hypothesis of an abstract process package.
- Treating the repository label `已验证`, a theorem name, or a successful candidate probe as proof
  of the exact target.

The later formal target must expose the actual Gaussian measure or process, hypotheses, quantified
constants, and conclusion selected from the primary source.
