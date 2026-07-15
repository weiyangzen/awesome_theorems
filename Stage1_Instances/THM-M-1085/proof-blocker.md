# THM-M-1085 proof-phase boundary

Item: `S56-M-1085-PROOF`
Base revision: `3d3099d0d4002093cf89da97132bdf954605810b`
Attempt date: 2026-07-15 (Asia/Shanghai)

## Verdict

This phase now has self-tested partial proof progress, but the exact Slepian root remains open.
`LawReduction.lean` implements the frozen finite-law and covariance-matrix normalizations without
placeholders. It transports lower-orthant probabilities, coordinate means, and covariances to the
pushforward laws; constructs their covariance matrices; proves positive semidefiniteness without a
nonsingularity premise; and identifies each centered Gaussian presentation with the canonical
possibly singular `multivariateGaussian` having that covariance matrix.

The exact bridge `slepianTarget_of_law` then reduces the frozen target, including its different
sample spaces, to `LawSlepianTarget`, the same lower-orthant comparison over finite Gaussian laws.
This is a checked reduction and does not inhabit `LawSlepianTarget`.

## First failed gate

The first failed proof gate is an exact repo-local body for the Gaussian-law orthant comparison.
The covariance interpolation route still needs:

- `M1085-C-INTERPOLATION` and `M1085-C-SMOOTHER`: the singular Gaussian path and smooth lower-
  orthant approximants;
- `M1085-L-INTERPOLATION-ID`: the Gaussian covariance derivative identity;
- `M1085-L-MIXED-SIGN`, `M1085-L-MONOTONE`, and `M1085-L-LIMIT`: the sign, integration, and exact
  indicator-event limit;
- terminal packaging into `M1085-T-COMPARISON` and the root.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the Gaussian and
multivariate-Gaussian substrate used here, but no Slepian, orthant-comparison, or covariance-
interpolation derivative theorem. The accepted bounded anchor audit found no exact pinned or
indexed Lean candidate. Substituting an expected-maximum theorem, a strict-threshold variant, a
positive-definite-only statement, `sorry`, or an axiom would not close the frozen target.

## Reopen condition

Continue by implementing the analytic comparison bodies above or by pinning an immutable,
compatible dependency that supplies the exact finite-law comparison and passes exact-type,
placeholder, axiom, provenance, and composition checks. Until then the accepted registry remains
unchanged, `root_closed=false`, root debt remains `M4`, and `theorem_complete=false`.

The worker `[_]` handoff applies only to the new local proof bodies toward `M1085-N-LAWS` and
`M1085-N-MATRIX`. Their frozen formal targets remain planned prose fingerprints, so this worker
claims no whole-node closure. This is not validation, release, master acceptance, audit completion,
or theorem completion.
