# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Recorded at: `2026-07-15T05:08:55+08:00` (`Asia/Shanghai`)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. The repository and pinned dependency closure still contain no
placeholder-free proof of the exact frozen contraction Hille--Yosida
equivalence. Neither `ForwardPackage` nor `ConversePackage` is inhabited, so
the minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only the final composition after a caller
supplies both complete directions. It is not a proof body for either package
or the root.

Repository history and the duplicate target `THM-M-0330` contain only the
same conditional architecture or legacy abstract interfaces. Pinned mathlib
has no Hille--Yosida theorem or strongly continuous semigroup generator API.
Its unbounded-operator, topology, integration, and bounded-operator APIs are
substrate rather than terminal proof bodies.

The external heads are unchanged. `mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667` remains outside the pinned Lake
closure and has only prospective forward resolvent pieces. TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` now exposes useful forward
density and resolvent declarations, but uses incompatible Lean/mathlib pins
and still lacks generator closedness, the left inverse, Yosida approximation,
and the converse generation theorem. Neither candidate was fetched, built,
integrated, or credited.

No shortcut through the statement was found. The right-neighborhood filter on
`NNReal` is nontrivial and normed-space limits are unique, so `IsGenerator` is
not vacuous. The zero generator with the identity semigroup is only a
consistent special case. Assuming either direction package, weakening the
equivalence, or replacing analytic predicates with abstract fields would add
an unproved premise or substitute another theorem.

The execution item therefore remains `[ ]`, its root vector remains
`[H2, M4, R4]`, and accepted receipt IDs remain empty. Because this proof
phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks ran in this worker clone using the automation-provided pinned
`.lake` artifacts. No `lake update`, `lake build`, dependency clone/fetch, or
dependency mutation ran. Lean object output was isolated under `/tmp` and
removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | Immutable candidate classifications and fail-closed root decision passed. |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e...b39c42`; root and both direction packages remain `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and conditional composition elaborated with no diagnostics. The tracked obligation-tree validation records `[propext, Classical.choice, Quot.sound]` for the conditional composition. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 124 | The full four-elaboration mutation checker timed out after 180 seconds under concurrent worker contention. Its source input is unchanged and direct statement elaboration passed, but no fresh mutation-check result is claimed. |
| `rg -n -i 'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator|ContractionSemigroup' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match result: no pinned terminal Hille--Yosida declaration or semigroup-generator API. |
| Scoped prohibited-token scan over owned `*.lean` files | 1 | Expected no-match result: no `sorry`, `admit`, axiom declaration, `sorryAx`, unsafe declaration, or oracle token. |
| `git ls-remote` for both recorded external candidates | 0 | Re-observed the immutable heads above; no dependency fetch or mutation. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is correctly absent. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-a1a7e939.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=2 LEAN_PATH="$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=2 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Exact input SHA-256 values are
recorded in the paired JSON artifact.

## Retry condition

Resume after placeholder-free implementations of both frozen direction
packages and all required children become available, or after an immutable
compatible exact Lean 4 proof is integrated into the pinned dependency
closure and passes exact-type, placeholder, axiom, provenance, composition,
and trust checks. This artifact is blocker evidence, not a proof receipt or
state-change request.
