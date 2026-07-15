# THM-M-0330 proof recheck at `e5011e2c`

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: 2026-07-15T14:03:03+08:00

Base revision: `e5011e2cf96da7561c96e5a2a89f67bc09e82fc5`

Base tree: `7d5e730e9f4454aefcd880ef597d33e2e9073176`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; lifecycle remains
`planned`; the frozen root remains `[H3, M4, R4]`; audit completion and theorem
completion remain false. This is current-base blocker evidence, not a proof
receipt. Because no proof package was implemented, the workspace-root
`.stage1-worker-selftest.json` is deliberately absent.

The exact root is
`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget`. Its minimal open cut
is unchanged:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

`ObligationTree.lean` contains a kernel-checked conditional composition from
arguments of types `ForwardPackage` and `ConversePackage`. It constructs
neither argument. `target_iff_expanded` is definitional transport only. Neither
declaration is a premise-free proof of the root.

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`. Closing the
forward package requires generator-domain density and closedness, a
Laplace/Bochner resolvent, both inverse laws, and the `1/a` estimate. Closing
the converse package requires bounded Yosida approximants, approximate
semigroups, contraction estimates, a strong C0 limit, and exact identification
of its generator graph.

The proof-relevant owned inputs and dependency pins are unchanged from
`230f719d`. A search of all `9644` Lean source files in the existing pinned
package cache found no Hille-Yosida, Yosida, C0-semigroup, or semigroup-generator
declaration. Duplicate target `THM-M-1041` has the same conditional
architecture. Legacy `S1_M_234.lean` explicitly supplies definitions,
abstract proposition fields, and projection wrappers rather than the missing
analytic proof bodies.

The audited external candidate `mrdouglasny/hille-yosida` remains bounded to
immutable revision `680e9499ee866763e737c8d888c1248684ced667`. It lies outside
the pinned closure and supplies only partial forward infrastructure: it omits
generator density and closedness, the left inverse on the full domain, and the
converse generation theorem. No external source was fetched, cloned,
integrated, or credited. Assuming either direction package, weakening the
equivalence, or replacing the analytic predicates with abstract fields would
add an unproved premise or prove a substituted theorem and was rejected.

The older intake projection in `instance.json` remains `[H1, M4, R4]`, while
the frozen obligation graph records `[H3, M4, R4]`. This proof worker reports
that pre-existing projection difference and does not rewrite another phase's
artifact.

## Validation

All commands ran in this worker clone. Initial status contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned cache. No `lake update`, `lake build`, dependency clone/fetch,
or `.lake` mutation ran. Temporary Lean output was created under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank `823`; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 1 | Root Lake setup failed before elaboration because `.lake/packages/flt-regular` cannot resolve `HEAD`. The cache was not repaired or mutated. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges pass; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both directions remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | The exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match over `9644` Lean sources. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 230f719d..HEAD --` proof inputs and dependency pins | 0 | Statement, composition, registry, graphs, audit, validation specs, Lake manifest, and toolchain are unchanged. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | No resolvable `HEAD`; this explains the standard checker failure and is recorded rather than repaired. |
| `python3 -m json.tool <current blocker JSON>` | 0 | The structured blocker artifact parses as JSON. |
| Target-specific blocker invariant assertions | 0 | Item, target, base/tree, `[ ]` state, open cut, false completion flags, empty receipt/closure lists, and owned changed paths agree. |
| `git diff --check` plus no-index checks of both new artifacts | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent, as required for an incomplete proof phase. |

The smallest available nonmutating Lean check explicitly reused existing
pinned package objects:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-e5011e2c-slot60.XXXXXX)
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
rg -l -i \
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

Resume when placeholder-free implementations of all children needed for both
frozen direction packages enter the pinned closure, or when an immutable,
compatible exact Lean 4 proof is pinned/imported and passes exact-type,
provenance, placeholder, axiom, composition, and trust checks. Restore the
pinned `flt-regular` artifact before replaying the standard statement mutation
checker. Until then, proof-phase completion and a worker `[_]` receipt would be
false.
