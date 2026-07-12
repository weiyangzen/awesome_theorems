# Anchor audit validation

Item: `S56-M-1080-ANCHOR_AUDIT`  
Base revision: `45b96fd58a0e141750ae21e0ddbb3d81233b8a6a`

The pinned mathlib snapshot contains a real Azuma-Hoeffding theorem,
`measure_sum_ge_le_of_hasCondSubgaussianMGF`. `AnchorAudit.lean` checks its current type and a
transparent wrapper. It is not the frozen root: its summands are assumed conditionally
sub-Gaussian and its space is standard Borel. The frozen target instead assumes an arbitrary
measurable probability space, a martingale, and a.e. absolute increment bounds. The missing
conditional Hoeffding lemma and telescoping transport remain later proof obligations.

## Commands and results

All Lean commands used the existing pinned Lake environment. No package was fetched or updated.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1080/AnchorAudit.lean` | 0 | wrapper and three candidate declarations elaborated; all printed axiom sets are `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1080/check_anchor_audit.py` | 0 | negative status boundary, declarations, and pinned mathlib revision agree |
| `rg -n -i 'azuma\|azuma-hoeffding\|HasCondSubgaussianMGF\|measure_sum_ge_le_of_hasCondSubgaussianMGF' <non-mathlib pinned packages> -g '*.lean' -g '*.md'` | 1 | no distinct candidate in the immutable external dependency closure |
| `python3 -m json.tool Stage1_Instances/THM-M-1080/anchor-audit.json` | 0 | structured audit valid |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1080` | 0 | rank 522, planned, L0/rework-required, theorem incomplete |
| forbidden-term scan of new executable audit files | 1 | expected no-match exit; no proof placeholder, custom axiom, or unsafe declaration |
| `git diff --check -- Stage1_Instances/THM-M-1080 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Network discovery found no separate repository candidate and is not treated as exhaustive evidence.
The reproducible external claim is deliberately limited to the immutable Lake dependency closure.
This node is self-tested pending master acceptance and supplies no theorem-completion credit.
