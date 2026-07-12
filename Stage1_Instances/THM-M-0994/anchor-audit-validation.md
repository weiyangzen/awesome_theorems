# Anchor audit validation

Item: `S56-M-0994-ANCHOR_AUDIT`  
Base revision: `28bf820a9c304cb6e04fd040a0d3384d9ac0b15d`

The immutable mathlib candidate is the composition of Hoeffding's lemma
`hasSubgaussianMGF_of_mem_Icc` and the independent finite-sum bound
`HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun`. `AnchorAudit.lean` checks that composition with
the frozen target's binders and hypotheses. The checked conclusion retains the upstream `NNReal`
variance proxy, so this audit does not pretend that the exact root has already been proved.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0994/AnchorAudit.lean` | 0 | candidate composition elaborated; both terminal declarations and wrapper report only `propext`, `Classical.choice`, `Quot.sound` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to `lake-manifest.json` |
| `rg -n -i 'hoeffding\|hasSubgaussianMGF_of_mem_Icc\|measure_sum_ge_le_of_iIndepFun' <all non-mathlib pinned package paths> -g '*.lean' -g '*.md'` | 1 | no distinct candidate in the immutable external dependency closure |
| `sha256sum .lake/packages/mathlib/Mathlib/Probability/Moments/SubGaussian.lean .lake/packages/mathlib/LICENSE AwesomeTheorems/Stage1/S1_M_274.lean` | 0 | hashes match `anchor-audit.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-0994/anchor-audit.json` | 0 | structured audit is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets |
| `python3 scripts/stage1_target.py show THM-M-0994` | 0 | rank 274, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0994` | 0 | no whitespace errors |

The search made no network fetch and does not claim exhaustive coverage of every public Lean 4
repository. It truthfully covers mathlib, repo-local sources, and every external project already
pinned in this Lake closure. The node is self-tested pending master acceptance; exact proof and
theorem completion remain false.
