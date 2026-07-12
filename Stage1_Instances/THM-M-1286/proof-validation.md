# THM-M-1286 proof-phase attempt

Item: `S56-M-1286-PROOF`  
Date: `2026-07-12`  
Base revision: `b057c8113d3f265874a1fdf670b1ab3558dc8a28`

## Verdict

`blocked`: the exact Pólya-Szegő target has no eligible terminal proof body in the repository or
pinned dependency closure. The immediate root cut remains `M1286-C-REARRANGE` and
`M1286-L-GRADIENT`. The first unavailable package is the construction of a measurable, `MemLp`,
symmetric decreasing rearrangement equimeasurable with the input. The second package requires the
weak-gradient estimate through the frozen coarea, isoperimetric, approximation, and lower
semicontinuity route.

`ObligationTree.lean` contains one real nonterminal proof body,
`exactTarget_of_packages`. It checks exact composition of the two packages into the canonical root,
but accepts both packages as premises and therefore closes neither package nor the root. The narrow
Lean run confirms that this conditional body elaborates and reports only `propext`,
`Classical.choice`, and `Quot.sound`; it does not supply either missing analytic theorem.

No Lean source was added because a short declaration of either absent package would merely assume
the mathematical content. No weaker, conditional, or differently encoded theorem was substituted.
The assigned proof deliverable is not complete, so `.stage1-worker-selftest.json` is deliberately
absent.

## Narrow validation evidence

All successful Lean commands reused the canonical pinned Lake artifacts. No update, build,
dependency clone/fetch, or mutation of `.lake` was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; baseline L0; lifecycle planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges pass; denominator `e586a1f...ddaa4`; root is open at M4 because both analytic packages remain open. |
| `cd Formalizations/Lean && lake env lean -R ../.. -o /tmp/thm-m-1286-proof/Stage1_Instances/THM-M-1286/Statement.olean ../../Stage1_Instances/THM-M-1286/Statement.lean` | 0 | The exact statement compiled into an isolated temporary olean under Lean 4.29.0. |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-1286-proof lake env lean ../../Stage1_Instances/THM-M-1286/ObligationTree.lean` | 0 | Conditional composition elaborated; its axiom report is `[propext, Classical.choice, Quot.sound]`. |
| `rg -n -i 'polya.?szego\|pólya.?szegő\|schwarz symmetric\|symmetric decreasing rearrangement\|symmetricDecreasingRearrangement\|equimeasur' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean' --glob '!Stage1_Instances/THM-M-1286/**'` | 0 | Only neighboring THM-M-1285 statement/interface material was found; no terminal proof body appeared. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

An initial invocation of the obligation checker and `sha256sum` from `Formalizations/Lean` used
root-relative paths and exited 2 because those paths did not exist from that working directory. The
commands were rerun from the repository root and passed. This operator path error did not affect the
Lean checks or any source file.

The statement SHA-256 is
`ef428b6d6fbb5a05b9112291cd5e113ff02d58776a03b2765837bd3ddc2039bb`. The conditional-composition
source SHA-256 is `31690c4c88849ca069648df8cbc72aaec44ce139e83a9fabda1b5b26093a4d6b`.
The obligation-registry file SHA-256 is
`c7d331ee666db5ca093880b051d0959395d35735bb2c337dfd7d5c7a91215d20`.

## Reopen condition

Resume only after either a complete assumption-free implementation of both root-cut packages and
their frozen analytic dependencies, or discovery of an eligible immutable Lean 4 proof that can be
pinned, exact-type transported, and checked in the repository closure. Until then the root remains
`M4`, `root_closed=false`, and theorem completion remains false.
