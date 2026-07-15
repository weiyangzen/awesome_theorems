# THM-M-0330 proof-phase recheck at current base

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T12:07:12+08:00` (`Asia/Shanghai`)

Base revision: `ca77dec5478e55c429f8f55a078eeef45356771b`

Base tree: `bb9cc1b79fee7404df2dd6eef0eea47f998059f1`

## Verdict

`blocked`. No placeholder-free inhabitant of either exact direction package is
present in the repository or pinned dependency closure. The frozen target is
the full contraction Hille--Yosida equivalence for every partially defined
real-linear operator on every real Banach space. Its minimal open root cut is:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` is only a kernel-checked conditional composition:
it requires complete `ForwardPackage` and `ConversePackage` arguments and
constructs neither. `target_iff_expanded` is only a definitional transport.

The proof-relevant target sources and their hashes are unchanged from the last
recheck. The only intervening target changes were integration of that blocker
evidence pair. A repository search again found only definitions, abstract
interfaces, transports, or conditional adapters. A search of every Lean source
in the pinned package cache found no Hille--Yosida theorem or strongly
continuous-semigroup generator API.

The audited external candidate `mrdouglasny/hille-yosida` is outside the pinned
closure and in any event does not supply generator density or closedness, the
left inverse on the entire domain, or the converse generation theorem. This
recheck did not clone, fetch, build, integrate, or credit any external project.

Closing the target requires new formal proofs of generator density and
closedness, a Laplace/Bochner resolvent with both inverse laws and its
contraction estimate, and the Yosida-approximation construction with strong
semigroup convergence and exact generator identification. Assuming either
direction package, weakening the equivalence, or replacing the analytic
predicates with abstract fields would add an unproved premise or substitute a
different theorem, and was rejected.

The item remains `[ ]`; lifecycle remains `planned`; the frozen graph's root
vector remains `[H3, M4, R4]`; accepted receipt IDs remain empty; and theorem
completion remains false. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone against base `ca77dec5`. Initial status
showed only the automation-provided untracked `Formalizations/Lean/.lake`
symlink. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation ran. The temporary Lean object was written below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank 823; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 1 | Root Lake environment could not resolve `HEAD` in `.lake/packages/flt-regular`; no repair or dependency mutation was attempted. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | 19 obligations and 40 typed edges passed; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both directions remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; this lexical scan is supporting evidence, not a transitive provenance proof. |
| `git diff --stat 443b8bbc..HEAD -- Stage1_Instances/THM-M-0330 Formalizations/Lean/lake-manifest.json Formalizations/Lean/lean-toolchain` | 0 | Only the prior `443b8bbc` blocker evidence pair was added; proof inputs and dependency pins did not change. |
| `python3 -m json.tool Stage1_Instances/THM-M-0330/proof-recheck-2026-07-15-head-ca77dec5-slot78.json` | 0 | Structured blocker artifact is valid JSON. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0330/proof-recheck-2026-07-15-head-ca77dec5-slot78.{md,json}` (run once per file) | 1 each | Expected diff-found status with no whitespace-error output. |
| `git diff --check -- Stage1_Instances/THM-M-0330` | 0 | No whitespace errors in tracked scoped changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The standard statement checker failed before invoking Lean because the shared
`flt-regular` checkout has no resolvable `HEAD`. Worker rules prohibit repairing
or fetching that cache. The narrow nonmutating fallback invoked the pinned Lean
executable through `lake env` and existing package objects:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-lake-env-head-ca77dec5-slot78.XXXXXX)
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
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages enter the pinned closure, or after an immutable,
compatible, exact Lean 4 proof is pinned/imported and passes exact-type,
provenance, placeholder, axiom, composition, and trust checks. The pinned
`flt-regular` artifact must also be restored before the standard statement
mutation checker can replay.
