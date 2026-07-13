# THM-M-1041 proof-phase blocker at current base

Item: `S56-M-1041-PROOF`

Recorded at: `2026-07-14T02:42:47+08:00` (`Asia/Shanghai`)

Base revision: `53dced5833f17a55f667239e756fc93c99810c44`

Base tree: `f0c4bdb31a84f0b4221b8392c9c95be1441914dc`

## Verdict

`blocked`. No placeholder-free proof body for the exact frozen contraction
Hille--Yosida equivalence exists in this repository or its pinned dependency
closure. Neither `ForwardPackage` nor `ConversePackage` is inhabited, so the
minimal root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse leaf is `M1041-C-YOSIDA-APPROX`. The checked theorem
`root_of_directionPackages` only composes these two complete packages after a
caller supplies them. It does not implement either package and cannot receive
root proof credit.

Closing the exact root requires new formal proofs of generator closedness and
density; construction of the Laplace/Bochner resolvent with both inverse laws
and its contraction estimate; and the Yosida-approximation construction of a
limiting semigroup, including laws, strong continuity, contraction, and exact
generator identification. Pinned mathlib supplies supporting analysis APIs but
no C0-semigroup generator or terminal Hille--Yosida theorem.

The audited `mrdouglasny/hille-yosida` revision
`680e9499ee866763e737c8d888c1248684ced667` is outside the pinned Lake closure
and only provides prospective pieces of the forward route. The later discovery
`TauCetiProject/TauCeti` at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` also supplies prospective forward
pieces only, uses different Lean/mathlib pins, and is outside the dependency
closure. Neither candidate provides generator closedness, the complete
two-sided resolvent package, or the converse generation theorem. Neither was
fetched, imported, built, or credited.

The root vector remains `[H2, M4, R4]`; the execution item remains `[ ]`;
accepted receipt IDs remain empty. This artifact is blocker evidence, not a
proof receipt or state-change request. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is absent.

## Validation

All commands ran in this worker clone. The automation-provided pinned `.lake`
link was read but not modified. No `lake update`, `lake build`, dependency
clone/fetch, or other dependency mutation ran. Lean object output was isolated
under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234, lifecycle `planned`, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | Immutable candidate classifications and fail-closed root decision passed. |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and direction packages remain `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-mathlib terminal-theorem search below | 1 | Expected no-match result; zero Hille--Yosida/C0-generator declarations found. |
| Scoped prohibited-token scan over owned `*.lean` files | 1 | Expected no-match result; zero `sorry`, `admit`, axiom declarations, `sorryAx`, unsafe declarations, or oracle tokens found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-blocker.json` | 0 | Existing structured blocker is valid JSON; this current-base note refreshes its stale base binding without changing its substantive verdict. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is correctly absent. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-53dced58.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=2 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=2 LEAN_PATH="$tmp:$lean_path" \
  "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned-mathlib search:

```bash
rg -n -i \
  'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Input SHA-256 values are
`4e211bd1...14699` for `Statement.lean`, `41805cc5...df73e` for
`ObligationTree.lean`, `24154c2f...3c1c2` for `obligation-registry.json`,
`5b7c2dd0...f0699` for `typed-graphs.json`, and `321626c8...2d81` for
`lake-manifest.json`.

## Retry condition

Resume only after placeholder-free implementations of both frozen direction
packages and all required children are available in the pinned closure, or
after an immutable compatible exact proof has been integrated and passes
exact-type, provenance, placeholder, axiom, composition, and trust checks.
