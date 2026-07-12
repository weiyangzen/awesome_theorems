# Exact Lean statement

The canonical proposition for this instance is the standard characterization already delimited by
the accepted intake: a process is Gaussian exactly when every finite-dimensional restriction has a
Gaussian law. The repository source phrase, "the theory of Gaussian processes", does not determine
any stronger proposition. Accordingly, no existence, covariance, continuity, comparison, or bound
theorem is silently substituted here.

## Frozen target

- Module: `Stage1_Instances/THM-M-1082/Statement.lean`.
- Minimal import: `Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def`.
- Declaration: `AwesomeTheorems.THM_M_1082.gaussianProcess_iff_finiteDimensionalGaussian`.
- State spaces: arbitrary types `Ω`, `E`, and `T`; `Ω` has a measurable space; `E` has measurable,
  topological, additive-commutative-monoid, and real-module structures.
- Ordered explicit binders: `X : T -> Ω -> E`, then `P : Measure Ω`.
- Conclusion: `ProbabilityTheory.IsGaussianProcess X P` iff every `I : Finset T` gives
  `HasGaussianLaw (fun ω => I.restrict (X · ω)) P`.
- Boundary convention: `I = empty` is included. Degenerate Gaussian measures are not excluded by
  the target; their treatment is inherited from pinned mathlib's `IsGaussian` predicate.
- Foundation/computation profile: no new axiom, oracle, unsafe declaration, or computation is used;
  the wrapper is a `Prop` theorem proved by structure construction and projection.

The right side is a credited alternate encoding with relationship `iff`; `Statement.lean` is its
kernel-checked witness. This freezes the finite-dimensional characterization only. A future
pinpoint human-source audit is still required for `H0` and is not claimed by the statement phase.

## Environment fingerprint

- Repository base revision: `7c40b39aac30d12a21a2ca13ebe9406d4d57b383`.
- Toolchain: `leanprover/lean4:v4.29.0`.
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- Lake manifest SHA-256: recorded in `statement-validation.md` from the validation run.
- Fixed options: Lean defaults; no local `set_option` directives.
- Normalized elaborated declaration type: the `#print` output recorded and hashed in
  `statement-validation.md`.

The source tree uses the canonical pinned `.lake` symlink supplied by the worker clone. Validation
does not update, fetch, clone, or otherwise mutate dependencies.
