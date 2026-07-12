# THM-M-1024 proof-phase attempt

Item: `S56-M-1024-PROOF`  
Attempt date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `c69176e94b59c24862294d8331b61eb1661c53bd`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target `Stage1Instances.THM_M_1024.LevyKhintchineTarget` re-elaborates in the pinned
Lean environment. The existing `root_of_packages` declaration also kernel-checks, with the axiom
report `[propext, Classical.choice, Quot.sound]`, but it is only conditional logical composition:
forward existence, converse realization, and uniqueness remain explicit premises.

The frozen registry's first unavailable analytic package is `M1024-N-EXPONENT`. Pinned mathlib
contains characteristic-function and convolution infrastructure but no Levy-Khintchine,
infinite-divisibility, or Levy-measure theorem family. The prerequisite audit's immutable LeanLevy
candidate proves a theorem only over `Real`, with open-ball compensation and scalar covariance,
using an incompatible newer toolchain. It is not pinned in this Lake environment and supplies no
checked adapter to the all-dimensional closed-ball target.

The immediate semantic root cut remains `M1024-T-FORWARD`, `M1024-T-CONVERSE`, and
`M1024-T-UNIQUENESS`. Supplying these as assumptions, importing the real-only result as though it
were exact, or weakening the target would violate the frozen theorem. The root therefore remains
open at `M4`, and `.stage1-worker-selftest.json` is deliberately absent because the assigned proof
deliverable is incomplete.

## Narrow validation evidence

All checks ran in this worker clone using the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or intentional `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1024` | 0 | rank 500; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1024/check_obligation_tree.py` | 0 | 24 obligations and 66 typed edges passed; denominator `09ae507f...b44921`; root open `M3` in the pre-proof freeze |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1024/Statement.lean` | 0 | exact canonical statement and structural mutations elaborated; explicit target printed |
| temporary `Statement.olean`, then `LEAN_PATH=Stage1_Instances/THM-M-1024:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) $(cd Formalizations/Lean && lake env which lean) Stage1_Instances/THM-M-1024/ObligationTree.lean` | 0 | conditional composition elaborated; `#print axioms root_of_packages` reported exactly `propext`, `Classical.choice`, and `Quot.sound`; temporary output removed |
| `rg -n -i '\\b(LevyKhintchine\|Levy.Khintchine\|IsInfinitelyDivisible\|infinitely divisible\|IsLevyMeasure)\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no theorem-family occurrence in pinned mathlib; exit 1 is the expected no-match result |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum Stage1_Instances/THM-M-1024/{Statement.lean,ObligationTree.lean,obligation-registry.json}` | 0 | `197a7197...81a87`, `a731c59b...87977`, `805d0275...8ee5` |
| `python3 -m json.tool Stage1_Instances/THM-M-1024/proof-blocker.json >/dev/null` | 0 | structured blocker record is valid JSON |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase has no self-test manifest |
| `git diff --check -- Stage1_Instances/THM-M-1024` | 0 | no scoped whitespace errors |

Preflight `git status --short` reported only the clone's pre-existing untracked
`Formalizations/Lean/.lake` reuse path. The scoped final status contains only this blocker record
and execution report.

## Reopen condition

Resume after implementing the frozen analytic packages without placeholders, or after locating an
immutable compatible all-dimensional Lean 4 proof whose exact type, terminal bodies, dependency
closure, axioms, license, and provenance can all be validated in the pinned environment.
