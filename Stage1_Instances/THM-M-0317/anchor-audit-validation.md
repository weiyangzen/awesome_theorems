# Anchor-audit validation record

Item: `S56-M-0317-ANCHOR_AUDIT`  
Base revision: `7421320db3a58c93ef0168e2164305d5798294b8`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact statement
vocabulary and two proof-bearing but non-equivalent fixed-point results. The interval theorem is a
one-dimensional special case; the Banach theorem assumes contraction and metric completeness.
`AnchorAudit.lean` elaborates their types and the interval application against the existing pinned
environment. No exact Tychonoff fixed-point theorem or checked transport was found.

The external searches recorded in `anchor-audit.md` produced no exact candidate. Those are bounded
discovery results, not a claim of global absence. The root therefore remains `M4`; theorem proof and
theorem completion are false, and master acceptance remains outstanding.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets and ranks 1 through 1,546 passed |
| `python3 scripts/stage1_target.py show THM-M-0317` | 0 | rank 683, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned mathlib `rg` searches recorded in `anchor-audit.md` | 0/1 | component and special-case hits classified; exact-name searches had the expected no-match status |
| four Sourcegraph queries recorded in `anchor-audit.md` | 0 | no exact proof candidate; returned matches and full revisions were classified |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0317/AnchorAudit.lean` | 0 | all credited declarations and the interval special case kernel-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0317/Statement.lean` | 0 | frozen canonical target and mutation witnesses still elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0317/anchor-audit.json` | 0 | structured ledger parsed |
| forbidden-device scan over `Stage1_Instances/THM-M-0317` | 0 | no `sorry`, `admit`, or axiom declaration |
| `git diff --check -- Stage1_Instances/THM-M-0317 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

No `lake update`, build, dependency clone/fetch, or `.lake` mutation was performed. The untracked
`.lake` path predates this phase and points to the canonical pinned artifacts; this is worker
evidence, not a clean release receipt.
