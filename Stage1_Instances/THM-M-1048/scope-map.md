# Scope map

## Included claim

- A state-space-valued stochastic process and a specified linear operator `A` on test functions.
- The compensated process `f(X_t) - f(X_0) - integral_0^t (A f)(X_s) ds` is a martingale for each
  admissible test function `f`.
- A characterization of a Markov law/process through the relevant martingale problem.
- Existence, uniqueness in law, and Markov conclusions only to the extent asserted by the selected
  exact source theorem.

## Decisions required before statement freeze

The statement phase must select a primary theorem and fix the state space, path space and sample
regularity; time domain; filtration and completion/right-continuity conventions; operator and its
domain; measurability and integrability hypotheses; initial point or distribution; meaning of
solution and uniqueness; and whether the conclusion is Markov, strong Markov, existence, or
well-posedness. It must also cover degenerate operator domains and exceptional/null-set semantics.

## Explicit exclusions

- Substituting a generic theorem saying every martingale is a Markov process (which is false).
- The narrower diffusion-specific Stroock-Varadhan target assigned separately as `THM-M-1049`.
- A single finite-state or discrete-time example in place of the general characterization.
- Assuming the desired Markov property or martingale-problem solution as structure fields.
- Treating mathlib's component APIs, the legacy `已验证` label, or a prose citation as closure.

The exact Lean object model is open. A later phase must use concrete probability, filtration,
conditional-expectation, integration, and path-law interfaces and record any missing API precisely.
