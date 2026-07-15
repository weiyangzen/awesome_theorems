# THM-M-0330 proof-phase recheck at current base

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T15:36:42+08:00` (`Asia/Shanghai`)

Base revision: `d03d302bba800ecaf216835c488381f045efbbfe`

Base tree: `8c7b74f4ffba9a954a510096902571e859629811`

## Verdict

`blocked`. No placeholder-free inhabitant of either exact direction package is
present in the repository or pinned dependency closure. The assigned proof
phase remains `[ ]`; lifecycle remains `planned`; the frozen root remains
`[H3, M4, R4]`; audit completion and theorem completion remain false. This is
blocker evidence, not a proof receipt, so `.stage1-worker-selftest.json` is
deliberately absent.

The exact root is
`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget`. It characterizes,
for every partially defined real-linear operator on every real Banach space,
existence of an exact strong-right-derivative contraction-semigroup generator
by density, closedness, and a bounded two-sided resolvent for every positive
parameter. Its minimal open cut is:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` is only a checked conditional composition from
complete `ForwardPackage` and `ConversePackage` arguments; it constructs
neither. `target_iff_expanded` is only definitional transport.

The proof inputs and dependency pins are unchanged from base `350285c4`.
Repository history, duplicate target `THM-M-1041`, and legacy module
`S1_M_234.lean` contain definitions, abstract interfaces, transports, or
conditional composition, not either substantive direction package. A fresh
search of all `9676` Lean files in the pinned package cache found no
Hille-Yosida theorem or strongly-continuous-semigroup generator API.

The audited external candidates remain discovery evidence only.
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667` lies outside the pinned closure and
omits generator density and closedness, the left inverse on the whole domain,
and the converse generation theorem. TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` likewise lies outside the closure,
uses incompatible pins, and does not supply the exact packages. No dependency
was fetched, cloned, built, integrated, or credited.

Closing the root requires new formal proofs of generator density and
closedness, a Laplace/Bochner resolvent with both inverse laws and the `1/a`
estimate, and the Yosida-approximation construction with strong semigroup
convergence and exact generator identification. Assuming either package,
weakening the equivalence, or replacing the analytic predicates with abstract
fields would add an unproved premise or substitute a different theorem and was
rejected.

## Validation

All commands ran in this worker clone. Initial status showed only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. Existing
pinned artifacts were reused. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation ran. Temporary Lean output was created below
`/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank `823`; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | Exact expression SHA-256 `5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`; all three mutations killed. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges passed; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both directions remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match over `9676` Lean source files. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 350285c4..HEAD --` proof inputs and pins | 0 | Statement, composition, registry, graphs, audit, validation specs, Lake manifest, and toolchain are unchanged. |
| `python3 -m json.tool` on the paired structured artifact | 0 | Blocker JSON parses successfully. |
| Target-specific blocker assertions | 0 | Identity/base, `[ ]` state, open cut, false completion flags, empty proof/receipt lists, changed paths, and self-test absence agree. |
| Scoped whitespace checks | 0 | No whitespace errors in either new artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent, as required for the incomplete phase. |

The smallest nonmutating Lean replay explicitly reused the existing pinned
executable and package objects:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-d03d302b-slot79.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lp=$(printf '%s:' \
  "$repo/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean" \
  "$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
cd "$mathlib_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$lp" \
  timeout --foreground 600 lake env lean --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lp" \
  timeout --foreground 600 lake env lean --trust=0 -t0 --root="$target" \
    "$target/ObligationTree.lean"
```

Pinned-package search:

```bash
rg -n -i \
  'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator|ContractionSemigroup' \
  Formalizations/Lean/.lake/packages --glob '*.lean'
```

Scoped prohibited-token scan:

```bash
rg -n -i \
  '\b(sorry|admit|sorryAx|unsafe|oracle)\b|(^|[^A-Za-z])(axiom|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-0330 --glob '*.lean'
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree
`32c9eace926573a9981787ae97643e520353c893`.

## Retry Condition

Resume after placeholder-free implementations of every child needed for both
frozen direction packages enter the pinned closure, or after an immutable,
compatible exact Lean 4 proof is pinned/imported and passes exact-type,
provenance, placeholder, axiom, composition, and trust checks. Until then,
proof-phase completion and a worker `[_]` receipt would be false.
