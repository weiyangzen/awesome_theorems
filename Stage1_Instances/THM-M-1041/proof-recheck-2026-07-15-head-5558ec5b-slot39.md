# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T07:20:35+08:00` (`Asia/Shanghai`)

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

## Verdict

`blocked`. The exact frozen target is the full contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof body for this target exists in the
repository or pinned dependency closure. Neither `ForwardPackage` nor
`ConversePackage` is inhabited, so the minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only the final composition after a caller
supplies both complete directions. It constructs neither direction and is not
a premise-free root proof. `target_iff_expanded` is only a definitional
transport.

The owned Lean sources and frozen inputs are unchanged since the preceding
recheck. Repository history, duplicate target `THM-M-0330`, and legacy module
`S1_M_234` contain abstract interfaces or the same conditional architecture,
not a substantive direction package. Pinned mathlib supplies functional
analysis substrate but no Hille--Yosida theorem or strongly continuous
semigroup generator API. Its bounded-algebra resolvent results do not prove
the frozen theorem about an unbounded `LinearPMap`.

The audited external candidates do not close the gap.
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667` is outside the pinned Lake closure
and supplies only prospective forward resolvent pieces. TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` is also outside the closure, uses
incompatible pins, and remains partial. Neither dependency was fetched,
built, integrated, or credited.

No shortcut through the statement was found. The right-neighborhood filter on
`NNReal` is nontrivial, and uniqueness of limits in a normed space prevents
`IsGenerator` from being vacuous. The zero-generator identity semigroup is
only a consistent special case. Both resolvent inverse laws and the norm
estimate remain substantive.

Closing the root requires new formal proofs of generator closedness and
density, a Laplace/Bochner resolvent with both inverse laws and its norm
estimate, and the Yosida-approximation semigroup construction with exact
generator identification. Alternatively, an immutable compatible exact proof
must enter the pinned dependency closure and pass exact-type, provenance,
placeholder, axiom, composition, and trust checks. Assuming a direction
package, weakening the equivalence, or replacing analytic facts by abstract
fields would substitute a different theorem and is not permitted.

The item remains `[ ]`, lifecycle remains `planned`, root vector remains
`[H2, M4, R4]`, and accepted receipt IDs remain empty. This file is blocker
evidence, not a proof receipt or item-state request. The proof phase is not
complete, so `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. Initial `git status --short` showed only
the automation-provided `Formalizations/Lean/.lake` symlink to the canonical
pinned cache. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation ran. Lean object output was isolated under `/tmp` and removed
on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234, lifecycle `planned`, `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both directions remain `M4`. |
| Isolated `lake env` discovery plus `lean --trust=0 -t0` recipe below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated. `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-mathlib topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, unsafe/oracle shortcut, `axiom`, or `opaque` declaration in owned Lean sources. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-15-head-5558ec5b-slot39.json` | 0 | The structured blocker artifact is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1041` plus `git diff --no-index --check /dev/null <new-artifact>` | 0 / 1 | No whitespace diagnostics; exit 1 from each no-index check is the expected added-file status. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-5558ec5b.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    ObligationTree.lean
```

Pinned-mathlib search:

```bash
rg -n -i \
  'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator|ContractionSemigroup' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

Scoped prohibited-token scan:

```bash
rg -n -i \
  '\b(sorry|admit|sorryAx|unsafe|oracle)\b|(^|[^A-Za-z])(axiom|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-1041 --glob '*.lean'
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages are available in the pinned closure, or after an
immutable compatible exact Lean 4 proof is pinned/imported and passes
exact-type, provenance, placeholder, axiom, composition, and trust checks.
