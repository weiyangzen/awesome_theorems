# THM-M-0311 anchor-audit validation

Item: `S56-M-0311-ANCHOR_AUDIT`  
Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact useful
candidate `MeasureTheory.Lp.instCompleteSpace` in
`Mathlib.MeasureTheory.Function.LpSpace.Complete`. Its type covers every measure and every complete
scalar normed additive group when `1 <= p`. The local audit wrapper specializes it to real and
complex scalars at exponent two and elaborates with exactly the frozen
`Stage1Instances.THM_M_0311.RieszFischerTarget` type.

The transitive axiom report for both the upstream instance and wrapper is `propext`,
`Classical.choice`, and `Quot.sound`. The audited terminal instance body invokes
`completeSpace_lp_of_cauchy_complete_eLpNorm` and `cauchy_complete_eLpNorm`; the pinned module has no
`sorry`, `admit`, declared `axiom`, or `unsafe` marker. The nearby `lp.completeSpace` theorem is only
an alternate sequence-space family and is not credited to the canonical measure-theoretic root.

Four bounded GitHub repository searches for Riesz-Fischer/L2/Lp completeness Lean projects each
returned `total_count: 0`. This negative search is explicitly non-exhaustive, but no external
dependency is needed because the immutable pinned mathlib candidate already closes the exact root.
This phase records an `M0-P candidate`; accepted `M0`, audit completion, and theorem completion wait
for the obligation, proof-integration, trust, provenance, and release phases.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0311` | 0 | rank 813, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; immutable dependency worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0311/AnchorAudit.lean)` | 0 | exact audit-copy wrapper elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0311/check_anchor_audit.py` | 0 | pin, source declarations/body, placeholder scan, wrapper, and fail-closed ledger status matched |
| four GitHub repository API searches recorded in `anchor-audit.json` | 0 | each returned `total_count: 0` on `2026-07-12` |
| `python3 -m json.tool Stage1_Instances/THM-M-0311/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0311 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, dependency clone/fetch, build, or `.lake` mutation was performed.
