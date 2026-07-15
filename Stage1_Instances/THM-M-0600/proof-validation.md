# THM-M-0600 proof-phase validation

Item: `S56-M-0600-PROOF`

Validation date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

## Implemented Body

`Proof.lean` supplies an unconditional, placeholder-free body provisionally
bound to the frozen zero-dimensional branch `M0600-S-DIMZERO`. The proof
chooses the supplied coordinates and index zero. Since `Euclidean 0` is a
subsingleton, every target
coordinate equals zero; the existing left-inverse and centeredness fields give
`base.invFun 0 = p`, and both quadratic sums are empty.

The module also checks two conditional compositions. First,
`morseNormalFormEngine_of_positiveDimension` combines that body with an
explicit `PositiveDimensionMorseNormalFormEngine` premise. Then
`morseLemmaTarget_of_positiveDimension` composes the result to the exact
canonical target. The premise is intentionally visible and receives no proof
credit. Consequently the root remains open at `M3`, with
`M0600-T-ENGINE` still the remaining root cut.

## Commands And Results

All Lean commands reused the existing canonical pinned `.lake` artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0600/check_proof.sh` | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated in a disposable directory with `--trust=0 -t0`; all three proof declarations were sorry-free; each axiom report was exactly `[propext, Classical.choice, Quot.sound]`; the structural receipt checker passed. |
| `python3 Stage1_Instances/THM-M-0600/check_obligation_tree.py` | 0 | `PASS THM-M-0600 obligation tree: 18 obligations, 44 typed edges`; frozen pre-proof graph truthfully remains open `M3`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0600` | 0 | Rank 638, planned hard-statement-first lane, theorem incomplete. |
| `rg -n --pcre2 '(?i)\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)\b\|\b(implemented_by\|native_decide)\b' Stage1_Instances/THM-M-0600/Proof.lean` | 1, expected | Empty output; no prohibited executable proof device. |
| `python3 -m json.tool Stage1_Instances/THM-M-0600/proof-receipt.json >/dev/null` | 0 | Valid structured partial-proof receipt. |
| `python3 -m json.tool Stage1_Instances/THM-M-0600/proof-blocker.json >/dev/null` | 0 | Valid structured residual blocker. |
| `python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | Valid seven-field worker packet proposing only `[_]`. |
| `git diff --check -- Stage1_Instances/THM-M-0600 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The environment is Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; the mathlib worktree was clean.
The pre-existing untracked canonical `.lake` symlink makes this nonrelease
worker evidence.

## Remaining Blocker

Every positive-dimensional case remains open. Closing it requires the frozen
smooth Taylor factorization, Hessian/Sylvester and index bridges,
parameterized splitting, finite induction, local inverse, full
`SmoothLocalCoordinates` construction, and neighborhood-wide identity.
Pinned mathlib provides ingredients but no exact terminal body for that
engine.

This is self-tested partial proof execution only. It proposes provisional
kernel closure of `M0600-S-DIMZERO`, pending master reconciliation of the
registry's planned branch fingerprint; accepted obligation closure remains
empty. It does not fully satisfy the proof node, close
`MorseLemmaTarget`, establish `M0` or theorem completion, or claim validation,
release, receipt acceptance, or master acceptance.
