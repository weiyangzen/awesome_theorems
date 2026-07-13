# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `f3a2545c7e6634696c48f725a9581e7e248c8877`

Base tree: `a9ade4224e40322a81336ccd63462829ffedc8eb`

## Verdict

`blocked`. No placeholder-free proof body for the exact frozen contraction
Hille--Yosida equivalence exists in the repository or pinned dependency
closure, and this recheck found no valid shortcut through the statement. The
tracked `proof-blocker.json` remains substantively accurate: neither
`ForwardPackage` nor `ConversePackage` is inhabited, so the minimal root cut is

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The right-neighborhood filter used by `IsGenerator` is nontrivial on
`NNReal`, and normed-space limits are unique. The zero generator with the
identity semigroup is a consistent special case, not a way to prove the
universally quantified target. Thus no contradiction, vacuous filter, or
degenerate-domain argument closes the root.

Pinned mathlib contains the `LinearPMap`, topology, bounded-operator, and
integration substrate, but no strongly continuous semigroup generator API or
terminal Hille--Yosida theorem. The only audited external candidate remains
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667`. It is outside the pinned Lake
closure and supplies only prospective pieces of the forward resolvent route,
not generator closedness/density, the complete two-sided resolvent package,
or the converse generation theorem. It was not fetched or credited.

Closing the exact target therefore requires new formal proofs of generator
closedness and density, the Laplace/Bochner resolvent with both inverse laws
and its norm estimate, and the Yosida-approximation semigroup construction
with exact generator identification. `root_of_directionPackages` only checks
composition after those two direction packages are supplied; returning it
would substitute a conditional theorem for the required root.

The execution item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and
accepted receipt IDs remain empty. This artifact is blocker evidence, not a
proof receipt. It makes no audit, validation, release, or theorem-completion
claim. Because the assigned proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.

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
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Completed with no diagnostics; the frozen statement record retains exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d` and all three mutations remain distinguished. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | Immutable candidate classifications and fail-closed root decision passed. |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and conditional composition elaborated with no diagnostics. The tracked obligation-tree validation records the machine-derived axiom set `[propext, Classical.choice, Quot.sound]`. |
| `rg -n -i 'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match result: no pinned terminal Hille--Yosida declaration. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-blocker.json >/dev/null` | 0 | Tracked structured blocker is valid JSON. |
| Scoped prohibited-token scan over owned `*.lean` files | 1 | Expected no-match result: no `sorry`, `admit`, axiom declaration, `sorryAx`, unsafe declaration, or oracle shortcut. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is correctly absent. |
| `git diff --check -- Stage1_Instances/THM-M-1041 .stage1-worker-selftest.json` | 0 | No whitespace errors in tracked changes. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1041/proof-recheck-2026-07-14-head-f3a2545c.md` | 1 | Expected new-file difference exit with no whitespace diagnostic. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Current input SHA-256 values are
`4e211bd1...14699` for `Statement.lean`, `41805cc5...df73e` for
`ObligationTree.lean`, `24154c2f...3c1c2` for `obligation-registry.json`, and
`321626c8...2d81` for `lake-manifest.json`.

## Retry condition

Resume only after placeholder-free implementations of both frozen direction
packages and their required children are available, or after an immutable
compatible exact Lean 4 proof is integrated into the pinned dependency
closure and passes exact-type, placeholder, axiom, provenance, composition,
and trust checks.
