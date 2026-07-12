# THM-M-1085 proof-phase blocker

Item: `S56-M-1085-PROOF`  
Base revision: `410d43b85faead588dace9d83e6bc4c4c7e0eaf1`  
Attempt date: 2026-07-12 (Asia/Shanghai)

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body was added, no frozen
obligation was marked closed, and no worker self-test manifest was written.

The exact root is `Stage1Instances.THM_M_1085.SlepianTarget`: the finite lower-orthant form of
Slepian's comparison for two centered jointly Gaussian vectors, including singular covariance
matrices. The existing `ObligationTree.lean` proves only conditional definitional composition:
`slepianTarget_of_pointwise` accepts `PointwiseComparison`, which is definitionally the entire root.
It therefore supplies no mathematical proof body.

The first unresolved root cut is the covariance-interpolation branch frozen by the predecessor:

- `M1085-N-LAWS` and `M1085-N-MATRIX`: reduce arbitrary random-vector presentations to finite
  Gaussian laws and recover their covariance matrices;
- `M1085-C-INTERPOLATION` and `M1085-C-SMOOTHER`: construct the interpolating Gaussian laws,
  including singular endpoints, and smooth lower-orthant cutoffs;
- `M1085-L-INTERPOLATION-ID`: prove the Gaussian covariance derivative identity;
- `M1085-L-MIXED-SIGN`, `M1085-L-MONOTONE`, and `M1085-L-LIMIT`: establish the mixed-derivative
  sign, integrate the comparison, and pass to the exact indicator events.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains useful Gaussian-law and
multivariate-Gaussian infrastructure. In particular it supplies `HasGaussianLaw.isProbabilityMeasure`,
`multivariateGaussian`, `covarianceBilin_multivariateGaussian`, and
`covariance_eval_multivariateGaussian`. It does not contain Slepian's inequality, a Gaussian
covariance-interpolation derivative theorem, or an orthant comparison theorem. The accepted anchor
audit found no exact repo-local, pinned-dependency, or indexed public Lean candidate. Consequently
these APIs do not inhabit any of the root-critical analytic leaves, and importing or wrapping them
alone cannot close the target.

Implementing those measure-theoretic differentiation and limiting results from scratch is beyond a
truthful bounded proof-phase attempt. Replacing them by assumptions, `sorry`, an axiom, or an
expected-supremum/strict-threshold variant would violate the frozen target and the worker contract.

## Commands and exact results

All commands ran in the worker clone. The existing pinned `.lake` link was reused; no update,
build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets ordered at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1085` | 0 | Confirmed rank 527, `planned`, `L0 / rework_required`, and `theorem_complete: false`. |
| `rg -n 'slepian\|Slepian\|Gaussian.*cov\|cov.*Gaussian' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/Mathlib` | 0 | No Slepian or Gaussian comparison declaration; matches were covariance infrastructure only. |
| `rg -n 'Gaussian.*inequal\|comparison\|orthant\|multivariateGaussian.*measure\|Gaussian.*cdf' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability --glob '*.lean'` | 0 | No orthant comparison or covariance-interpolation theorem was found. |
| temporary isolated copies, then `cd Formalizations/Lean && lake env lean -R "$TMP" -o "$TMP/Stage1_Instances/THM-M-1085/Statement.olean" "$TMP/Stage1_Instances/THM-M-1085/Statement.lean"` and `LEAN_PATH="$TMP:$(lake env printenv LEAN_PATH)" lake env lean -R "$TMP" "$TMP/Stage1_Instances/THM-M-1085/ObligationTree.lean"` | 0 | The exact statement and conditional composition elaborated. The latter still requires an inhabitant of `PointwiseComparison`, definitionally the whole target. Temporary files were removed. |

The worktree's pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease
evidence but was not modified.

## Reopen condition

Resume this proof item only when placeholder-free Lean bodies are implemented for the frozen
law/matrix reduction, singular Gaussian interpolation, derivative identity, sign, monotonicity, and
indicator-limit obligations, or when an immutable compatible dependency providing those exact
bodies is pinned and exact-type checked. Until then the root remains open at `M4`,
`root_closed=false`, and `theorem_complete=false`; this item cannot truthfully receive `[_]`.
