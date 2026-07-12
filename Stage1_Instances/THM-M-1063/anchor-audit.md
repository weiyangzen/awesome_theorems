# Anchor audit

Item: `S56-M-1063-ANCHOR_AUDIT`  
Target: `AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple`

## Immutable environment

- Repository base: `45aefb41a1978e4156e78f7fe59c590530703225`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; the local checkout was clean.
- The Lake manifest contains mathlib and the ordinary mathlib support packages, plus
  `flt-regular`; it contains no Brownian-motion or Donsker dependency.

## Pinned mathlib candidates

| Candidate | Exact source | Audit result |
|---|---|---|
| scalar CLT, variance one | `Mathlib.Probability.CentralLimitTheorem`, `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum` | Kernel-checked theorem. Its codomain is `Real` and it proves convergence of one normalized partial sum to `gaussianReal 0 1`. It supplies only the time-one finite-dimensional leaf, not path-space convergence. |
| scalar CLT, general variance | same module, `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` | Kernel-checked theorem. It is again real-valued and therefore cannot close the continuous-map-valued target. |
| convergence vocabulary | `Mathlib.MeasureTheory.Function.ConvergenceInDistribution`, `MeasureTheory.TendstoInDistribution` | Exact conclusion vocabulary used by the target, but a structure/definition rather than a Donsker proof. |
| Gaussian-process vocabulary | `Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def`, `ProbabilityTheory.IsGaussianProcess` | Exact finite-dimensional Gaussian predicate used inside the local Brownian predicate. It neither constructs Brownian motion nor proves convergence. |
| weak-convergence metric | `Mathlib.MeasureTheory.Measure.LevyProkhorovMetric`, `MeasureTheory.LevyProkhorov.eq_convergenceInDistribution` | Useful topology bridge. It supplies neither uniform tightness of polygonal laws nor identification of their limit. |

An exact and broad source search for `donsker`, `invariance principle`, `functional central
limit`, `brownian`, and `wiener` found no Donsker theorem and no Brownian/Wiener declaration in the
pinned `Mathlib` source tree. The only `wiener` source hit was unrelated analytic number theory.
Mathlib's documentation backlog names Donsker's theorem, but a wishlist row is not a declaration.

`AnchorAudit.lean` checks all candidate names and their current types. `#print axioms` reports only
`propext`, `Classical.choice`, and `Quot.sound` for both scalar CLTs and the Levy-Prokhorov bridge;
these are ordinary Lean foundations, not placeholders or candidate-specific axioms. The terminal
proof bodies are present in the pinned mathlib source modules above. No candidate is type-equal to
the frozen path-space target, so no wrapper can turn these anchors alone into Donsker's theorem.

## External Lean 4 candidate

Mathlib's pinned downstream registry identifies
`https://github.com/RemyDegenne/brownian-motion`. The GitHub commit endpoint resolved its `master`
branch on 2026-07-12 to immutable commit
`bdf5ea0c34f9e6d75bce5f0609a968d6e9e99e8e`. Its recursive commit tree and raw sources were
inspected without cloning or changing `.lake`.

At that revision the project has Brownian construction and continuity infrastructure, notably
`BrownianMotion/Gaussian/BrownianMotion.lean`, including
`IsPreBrownianReal.exists_continuous_modification`. It imports a newer mathlib Brownian API and
builds with `leanprover/lean4:v4.31.0`. Its `lakefile.toml` also requires the separate moving Git
dependency `RemyDegenne/kolmogorov_extension4`. A bounded scan of all Lean sources whose paths
contain `Brownian`, `Gaussian`, or `Continuity` found no match for `Donsker`, `functional central`,
`central limit`, `invariance principle`, or `TendstoInDistribution`. The recursive tree likewise
contains no Donsker/CLT module.

Classification: relevant Brownian infrastructure only, `external_upstream_anchor_only`. It is not
in this repository's dependency closure, uses an incompatible Lean toolchain, and exposes no
terminal theorem with the frozen polygonal-walk convergence type. Consequently it provides no M0
credit and is not an integration candidate for closing the root at the audited revision.

## Audit verdict and root cut

The bounded anchor inventory is complete for pinned mathlib, repository-local Lean sources, the
existing Lake closure, and the credible external Brownian project named by mathlib itself. There
is no exact formal candidate. The nearest checked mathlib result is the scalar CLT; the external
project supplies Brownian construction infrastructure only.

The next obligation phase must therefore plan a new functional-CLT proof. Its irreducible root cut
includes: measurability and continuity of the polygonal path variable; finite-dimensional
convergence (partly supported by the scalar CLT/characteristic-function machinery); uniform
tightness in `C([0,1], Real)` under only a finite second moment; identification and uniqueness of
the Brownian path law; and composition into `TendstoInDistribution`. Current classification stays
`H2 / M4 / R4`: this phase claims an audit receipt only, not proof, M0, H0, audit completion for the
whole theorem, or theorem completion.

## Validation

Commands and exact results are recorded in the anchor-audit section of `validation.md`.
