# Anchor audit

Audit date: 2026-07-12. Canonical target:
`Stage1Instances.THM_M_0990.StatementShape` in `Statement.lean`.

## Pinned mathlib

The installed dependency is mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (commit date 2026-03-30), with Lean
`v4.29.0`. A full case-insensitive search of its `Mathlib/**/*.lean` files for
`lyapunov`, `lindeberg`, and `triangular array` returned no result.

The closest terminal theorem is
`ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` in
`Mathlib.Probability.CentralLimitTheorem`. It proves the one-dimensional i.i.d.
CLT for one sequence, with common variance and `sqrt n` normalization. It is
not an exact candidate for the frozen claim, whose row entries may have
different distributions and whose normalization is the square root of the sum
of row variances.

Useful nonterminal architecture anchors are:

| Declaration | Role | Exact closure? |
|---|---|---|
| `tendstoInDistribution_inv_sqrt_mul_sum` | centered, unit-variance i.i.d. CLT | no |
| `tendsto_charFun_inv_sqrt_mul_pow` | i.i.d. characteristic-function limit | no |
| `iIndepFun.charFun_map_fun_finset_sum_eq_prod` | finite independent-sum product | no |
| `taylor_charFun_two` | second-order characteristic-function expansion | no |
| `ProbabilityMeasure.tendsto_iff_tendsto_charFun` | Levy convergence bridge | no |

`AnchorAudit.lean` imports the same pinned CLT module and checks all six names.
No checked declaration is assigned proof credit for the Lyapunov theorem.

## External Lean 4 candidates

GitHub repository search for `Lyapunov central limit theorem Lean` returned zero
repositories. The broader immutable audit covered both repositories returned
for `central limit theorem language:Lean`:

| Repository and revision | Finding | Eligibility |
|---|---|---|
| `uw-math-ai/central_limit_theorem@0ed57e943d642eaa95fe547780024b9e3a0dfbdf` | `CLT` is an i.i.d. theorem, not triangular-array Lyapunov; its body and prerequisite lemmas contain `sorry`; toolchain is Lean `v4.13.0-rc3` and its lakefile uses an unpinned git dependency | rejected |
| `edegeltje/FreeCLT@04b5b747538ca59e355908e16effa9b6a8d79b96` | template repository about free/noncommutative probability, with no Lyapunov triangular-array target | rejected |

The first repository's immutable Git tree was enumerated through the GitHub API
and its six Lean/project files were read at the stated commit. No dependency
was cloned, fetched, or added to `.lake`.

## Verdict

The phase audit is complete but found no exact terminal Lean 4 candidate.
Machine status remains `M3`: a precise statement exists, while the substantive
triangular-array characteristic-function/Taylor proof remains formalization
debt. This is not `M0`, external anchor credit, audit-wide completion, or
theorem completion.

## Validation record

Base revision: `eb29ee11410f6ffd5721f3978c3740bf5d957b2e`.

| Command | Result |
|---|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; exact revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'lyapunov|lindeberg|triangular.?array' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1; no matches |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0990/AnchorAudit.lean` | exit 0; all six declarations printed and the boundary theorem elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0990/anchor-audit.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0990 .stage1-worker-selftest.json` | exit 0; no output |

Known failures outside this phase: no terminal proof body, obligation-tree
closure, trust/provenance closure, hermetic replay, independent validation, H0,
R0, or release evidence exists.
