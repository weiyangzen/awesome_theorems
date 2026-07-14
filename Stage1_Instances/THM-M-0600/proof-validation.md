# THM-M-0600 proof-phase blocker

Item: `S56-M-0600-PROOF`  
Date: `2026-07-15` (`Asia/Shanghai`)  
Base revision: `e04243daf889845e1649146b8777095223d800ba`

## Verdict

`blocked`: the exact Morse lemma proof phase is not complete. The frozen
remaining root cut and first failed proof-body availability gate is
`M0600-T-ENGINE`, and no declaration inhabits its `MorseNormalFormEngine`
interface. The first unavailable central analytic body is
`M0600-L-SPLITTING`, the parameterized smooth splitting lemma that must remove
mixed and higher-order terms while retaining a smooth invertible coordinate
change.

The repo-local theorem
`Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine` is a real checked
composition body, but it consumes the missing engine as an explicit premise.
It cannot be credited as an unconditional proof of
`Stage1Instances.THM_M_0600.MorseLemmaTarget`. The pinned mathlib declarations
for Sylvester diagonalization, signature accounting, and a smooth local inverse
are ingredients only: none constructs nonlinear normal coordinates or proves
the exact neighborhood identity.

Closing the engine requires the frozen chart and derivative transports, smooth
second-order Taylor factorization, sign/index accounting, parameterized
splitting and finite induction, inverse-function application, construction of
every `SmoothLocalCoordinates` field, and transport of the quadratic identity
throughout an open target neighborhood. An assumed engine, a pointwise Taylor
approximation, or a quadratic-form-only result would be a hidden premise or a
weaker substituted theorem. No such shortcut, placeholder, axiom, or fake
result was added.

The assigned phase is therefore not genuinely self-tested as complete, so
`.stage1-worker-selftest.json` is deliberately absent. Root machine debt
remains `M3`, with the analytic engine itself at `M4`; `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`.

## Validation Evidence

All commands ran in this worker automation clone and reused the pre-existing
canonical pinned Lake artifacts. No Lake update/build, dependency clone/fetch,
or `.lake` mutation was performed. The temporary `Statement.olean` was created
under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` for 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok` for 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0600` | 0 | Rank 638; lifecycle `planned`; lane `hard_statement_first_partial_verification`; `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-0600/check_obligation_tree.py` | 0 | Passed 18 obligations and 44 typed edges; denominator `071b0844...e93f981`; root open M3 and `M0600-T-ENGINE` remains M4. |
| `LEAN_BIN=$(cd Formalizations/Lean && lake env which lean); LEAN_PATH=$(cd Formalizations/Lean && env -u LEAN_PATH lake env printenv LEAN_PATH); LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" --trust=0 -o /tmp/.../Statement.olean Stage1_Instances/THM-M-0600/Statement.lean; cd Stage1_Instances/THM-M-0600; LEAN_NUM_THREADS=1 LEAN_PATH="/tmp/...:$LEAN_PATH" "$LEAN_BIN" --trust=0 ObligationTree.lean` | 0 | Exact statement and conditional composition elaborated; the axiom report was exactly `[propext, Classical.choice, Quot.sound]`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Exact immutable mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | Exact mathlib tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `rg -n '\\b(sorry\|admit\|sorryAx\|implemented_by\|native_decide)\\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)\\b' Stage1_Instances/THM-M-0600/Statement.lean Stage1_Instances/THM-M-0600/ObligationTree.lean` | 1 | Expected no-match exit: no prohibited executable placeholder, bodyless declaration, unsafe escape, or native oracle. |

## Reopen Condition

Resume after a placeholder-free implementation of the frozen smooth splitting
and normal-form packages, or after an immutable compatible Lean 4 Morse-lemma
body becomes available for pinned exact-type integration. This record is
actionable blocker evidence only and claims no proof receipt, item completion,
M0 status, validation/release result, master acceptance, or theorem completion.
