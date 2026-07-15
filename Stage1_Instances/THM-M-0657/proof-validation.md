# THM-M-0657 proof-phase validation

Item: `S56-M-0657-PROOF`

Validation date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `be35cd8f5123e9d06247b12859f3843bdd90c66f`

## Implemented bodies

`Proof.lean` supplies unconditional, placeholder-free bodies provisionally
bound to two frozen obligations. For `M0657-C-EXISTENCE`, the source model's
exact uncountable cardinality yields an `Infinite` instance; pinned
Lowenheim-Skolem then constructs a `T`-model of every requested uncountable
target cardinality. For `M0657-L-COMPLETENESS`, the source categoricity
hypothesis is transported to `T union L.infiniteTheory`, and pinned Los-Vaught
proves that working theory complete. The union is important: the canonical
target permits additional finite `T`-models, so claiming raw `T.IsComplete`
would be unjustified.

The module also checks pointwise and exact-root composition from an explicit
`UncountableCategoricityTransfer` premise. That premise is the still-open
Morley core and receives no proof credit. The exact root remains `M3`.

## Commands and results

All Lean commands reused the existing canonical pinned `.lake` artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
network request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0657/check_proof.sh` | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated in a disposable directory with `--trust=0 -t0`; all five selected declarations passed `assert_no_sorry`; their axiom closures were subsets of `[propext, Classical.choice, Quot.sound]`; the structured proof checker passed. |
| `python3 Stage1_Instances/THM-M-0657/check_obligation_tree.py` | 0 | The frozen 14-obligation registry and 56 typed edges passed; authoritative pre-proof root remains open `M3`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0657` | 0 | Rank 702, planned hard-statement-first lane, theorem incomplete. |
| `rg -n --pcre2 '(?i)\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)\b\|\b(implemented_by\|native_decide\|run_tac)\b' Stage1_Instances/THM-M-0657/Proof.lean` | 1, expected | Empty output; no prohibited executable proof device. |
| `python3 -m json.tool Stage1_Instances/THM-M-0657/proof-receipt.json >/dev/null` | 0 | Valid structured partial-proof receipt. |
| `python3 -m json.tool Stage1_Instances/THM-M-0657/proof-blocker.json >/dev/null` | 0 | Valid structured residual blocker. |
| `python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | Valid seven-field worker packet proposing only `[_]`. |
| `git diff --check -- Stage1_Instances/THM-M-0657 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The pinned environment is Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; the mathlib worktree was clean.
The scheduler-provided untracked `.lake` symlink makes this warm nonrelease
evidence.

## Remaining blocker

Morley rank, categoricity-to-stability, saturation transfer, and saturated
model uniqueness remain unimplemented, and no exact proof exists in the
audited pinned dependency closure. These packages are needed to inhabit
`UncountableCategoricityTransfer`, after which the checked terminal composition
would return the unchanged root.

This is self-tested partial proof execution only. It proposes provisional
closure of `M0657-L-COMPLETENESS` and `M0657-C-EXISTENCE`, pending integration
lane reconciliation of their planned registry fingerprints. Accepted closure
remains empty. It does not fully satisfy the proof node, close
`MorleyCategoricityTarget`, establish `M0` or theorem completion, or claim
validation, release, receipt acceptance, or master acceptance.
