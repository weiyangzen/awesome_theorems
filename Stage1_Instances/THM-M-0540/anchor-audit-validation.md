# Anchor-audit validation record

Item: `S56-M-0540-ANCHOR_AUDIT`  
Base revision: `db900270f2f4923a9b799f36bb75ca392d869647`

## Result

The pinned `Mathlib.AlgebraicTopology.SingularHomology.Basic` source defines
`singularHomologyFunctor` as `singularChainComplexFunctor` followed by the degree-`n` homology
functor. Consequently its specialization to `ModuleCat Int` is an exact, dependency-legal anchor
for the frozen construction identity. `AnchorAudit.lean` checks that specialization with an `rfl`
body. `#print axioms` reports only the expected foundational `propext`, `Classical.choice`, and
`Quot.sound`, with no target-specific axiom. The source is pinned at mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, source SHA-256
`655867a11ed5ec706a554ac32f8f273c5227cafd4b47f0de42d84e24b0d33c7c`, under Apache-2.0.

The local statement-phase witness is recorded but receives no later-phase proof credit here.
Sourcegraph also located `facebookresearch/atlas-lean` at immutable commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its `Section1.lean` contains an `rfl` theorem for the
same construction in `AddCommGrpCat`; it uses the same Lean and mathlib pins, but is only near-exact
because the canonical target uses `ModuleCat Int` and an explicit `homologyFunctor` expression.
There is no reason to integrate it when the exact mathlib anchor is already pinned locally.

This phase therefore records an `M0-W` candidate for the ordered proof phase. It does not itself
promote the planned root, accept a proof receipt, establish H0/R0, or claim theorem completion.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. No dependency update, build, clone, or fetch was
performed, and the automation-provided `.lake` symlink was not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0540` | 0 | rank 597; planned; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/AnchorAudit.lean` | 0 | three declarations checked; exact wrapper elaborated; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/Statement.lean` | 0 | prerequisite exact target re-elaborated |
| `rg -n -i 'singular.?homology|singularHomologyFunctor' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | pinned dependency hits are in mathlib; terminal definition is `Basic.lean:47-49` |
| Sourcegraph API query recorded in `anchor-audit.json` | 0 | 78 matches in mathlib4 and atlas-lean; response hash `266ab066...8627` |
| GitHub REST repository query recorded in `anchor-audit.json` | 0 | complete zero-result response; hash `08c082fd...2600` |
| GitHub REST code query recorded in `anchor-audit.json` | 0 | response captured with HTTP 403 rate-limit blocker; hash `ff4efb0e...a6b4` |
| immutable raw inspection of `atlas-lean@34ffed3...` | 0 | toolchain v4.29.0, mathlib exact same pin, Section1 SHA-256 `0335e69f...40c8` |
| `python3 -m json.tool Stage1_Instances/THM-M-0540/anchor-audit.json` | 0 | JSON valid |
| forbidden-token scan of owned Lean files | 0 | no `sorry`, `admit`, or `axiom` token |
| `git diff --check -- Stage1_Instances/THM-M-0540` | 0 | no whitespace errors |

## Open gates

Master acceptance of this receipt is still required. The later obligation-tree phase must model the
definitional anchor, and the proof/validation phases must independently decide and validate any
`M0-W` promotion. Human primary-source pinpointing and errata review also remain open outside this
formal-anchor-only assignment.
