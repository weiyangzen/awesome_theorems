# Anchor audit record

Item: `S56-M-1138-ANCHOR_AUDIT`  
Base revision: `d16846c4969f0161ce4deb072fd4ba49becebb56`

## Result

The repository-local and pinned-mathlib searches found no declaration whose type closes
`Stage1Instances.THM_M_1138.HarmonicWeakMaximumPrinciple`. The closest general anchors are the
exact `HarmonicContOnCl` hypothesis package and the compact extreme-value theorem. Their missing
bridge is mathematical, not syntactic: the latter finds a maximizer on `closure U`, but the pinned
library has no general real finite-dimensional harmonic theorem moving an interior maximizer to
`frontier U`.

`Complex.exists_mem_frontier_isMaxOn_norm` is a close shape analogue, but it is a maximum-modulus
theorem for complex-differentiable maps and cannot replace the ordered-value result for a real
harmonic function. The complex-plane mean-value theorem covers only `Complex -> Real` on balls.
Neither candidate broadens to the arbitrary positive dimension and arbitrary bounded connected
open domain frozen by the statement phase.

The public Lean repository search returned one plausibly relevant project,
`mccorvie/lean-harmonic`, pinned for this audit at commit
`f3b75687e0ff790ab135811db54d5c2e4ea2170b`. Its sole substantive Lean source has SHA-256
`145c3614edd1e7227c25ed9eb8eb13ead1b6fcc8385055188eee7426650ea4a2`, contains no maximum-principle
declaration, uses a 2023 nightly toolchain, and is not an integration candidate. The broader GitHub
repository query returned mostly unrelated meanings of "harmonic"; GitHub's code-search endpoint
was unavailable without authentication, so this is a bounded negative audit rather than a claim of
global search exhaustiveness.

The root remains `M4 / formalization_debt`. This audit grants no proof credit and does not claim
theorem completion.

## Commands and results

All commands ran in the worker clone. Existing pinned Lake artifacts were used without update,
build, clone, or fetch.

| Command | Exit | Result |
|---|---:|---|
| `rg -n -i 'maximum|isMax|le.*frontier|frontier.*le' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | found generic extrema and the complex maximum-modulus family; no real harmonic root match |
| `rg -n 'theorem|lemma|maximum|Maximum|IsMax|frontier|closure' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Harmonic --glob '*.lean'` | 0 | harmonic core contains definitions, regularity, and constructions, but no maximum principle |
| GitHub repository API query `"maximum principle" harmonic language:Lean` | 0 | total count 0 at cutoff |
| GitHub repository API query `harmonic language:Lean` | 0 | 16 repositories; manual relevance screening identified only `mccorvie/lean-harmonic` for source inspection |
| `git ls-remote https://github.com/mccorvie/lean-harmonic.git refs/heads/main` | 0 | immutable inspected revision `f3b75687e0ff790ab135811db54d5c2e4ea2170b` |
| raw immutable source retrieval and `sha256sum` for `LeanHarmonic.lean` | 0 | SHA-256 `145c3614edd1e7227c25ed9eb8eb13ead1b6fcc8385055188eee7426650ea4a2` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1138/AnchorAudit.lean` | 0 | all six candidate types elaborated; the four theorem probes reported only `propext`, `Classical.choice`, and `Quot.sound` where applicable |
| `python3 -m json.tool Stage1_Instances/THM-M-1138/anchor-audit.json >/dev/null` | 0 | structured audit parses |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1138` | 0 | rank 343, planned, L0/rework-required, theorem incomplete |
| scoped prohibited-token scan of `AnchorAudit.lean` and `anchor-audit.json` | 1 | no match; exit 1 is the clean no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1138 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Master acceptance, obligation-tree construction, proof implementation, and all theorem-completion
gates remain outside this phase.
