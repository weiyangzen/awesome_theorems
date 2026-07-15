# THM-M-0330 proof recheck at `350285c4`

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T15:17:57+08:00` (`Asia/Shanghai`)

Base revision: `350285c48208616b6e3ad74154d9183d16523cfa`

Base tree: `c4edebc115ec954e4940ed5faaa3ffacd4e56091`

## Verdict

`blocked`. The assigned proof item remains `[ ]`; lifecycle remains `planned`;
the frozen root remains `[H3, M4, R4]`; audit completion and theorem completion
remain false. This is current-base blocker evidence, not a proof receipt. No
workspace-root `.stage1-worker-selftest.json` is emitted because the proof
phase is not genuinely complete.

The exact root is
`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget`. Neither exact
direction package has a placeholder-free inhabitant in the repository or
pinned dependency closure, so the minimal open root cut remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` is a kernel-checked conditional composition from
caller-supplied `ForwardPackage` and `ConversePackage` arguments. It constructs
neither argument. `target_iff_expanded` is definitional transport only.

The proof inputs and dependency pins are byte-identical to the original proof
blocker and the latest integrated recheck. Repository history, duplicate
target `THM-M-1041`, and legacy module `S1_M_234.lean` provide definitions,
abstract interfaces, transports, or conditional composition only. Search
across all `9676` Lean sources in the current pinned package cache found no
Hille-Yosida or strongly-continuous-semigroup generator API.

Fresh branch-metadata queries confirm that `mrdouglasny/hille-yosida` remains
at `680e9499ee866763e737c8d888c1248684ced667` and TauCeti remains at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`. Both are outside the pinned Lake
closure. The first contains parts of a forward Laplace-resolvent route but no
proof of generator density or closedness, no left inverse over the whole
domain, and no converse generation theorem. TauCeti has a closer `NNReal` and
`LinearPMap` interface and a density theorem, but uses incompatible Lean and
mathlib revisions and still lacks generator closedness, the full left inverse,
and the entire Yosida/converse package. Nothing was cloned, fetched, built,
integrated, or credited.

Closing the exact root requires new formal proofs of generator density and
closedness, the Laplace/Bochner resolvent with both inverse laws and its
contraction estimate, and the Yosida-approximation construction with strong
semigroup convergence and exact generator identification. Assuming either
direction package, weakening the equivalence, or replacing the analytic facts
with abstract fields would add an unproved premise or prove a substituted
theorem, and was rejected.

The older intake projection in `instance.json` remains `[H1, M4, R4]`, while
the frozen obligation graph records `[H3, M4, R4]`. This proof worker reports
that pre-existing projection difference and does not rewrite another phase's
artifact.

## Validation

All commands ran in this worker clone. Initial status contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned cache. No `lake update`, `lake build`, dependency clone/fetch,
or `.lake` mutation ran. Temporary Lean objects were created below `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank `823`; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | Expression SHA-256 `5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges pass; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both directions remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match over all `9676` Lean sources. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 229ca98e..HEAD --` proof inputs and dependency pins | 0 | All substantive proof inputs and pins are unchanged; the only later target commit integrated the preceding blocker pair. |
| `git ls-remote` for both audited external main branches | 0 | Revisions remain `680e9499...d667` and `c7e69c3c...94fa`; no clone, fetch, build, integration, or proof credit followed. |
| `python3 -m json.tool <current blocker JSON>` | 0 | The structured blocker artifact parses as JSON. |
| Target-specific blocker invariant assertions | 0 | Identity/base, `[ ]` state, false completion flags, empty proof/receipt lists, root cut, changed paths, and self-test absence passed. |
| `git diff --check` plus no-index checks of both new artifacts | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent, as required for an incomplete proof phase. |

The narrow trust-level-zero check reused the pinned executable and existing
package objects without mutating `.lake`:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-head-350285c4-slot63.XXXXXX)
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
  timeout --foreground --kill-after=10s 600 lake env lean --trust=0 -t0 \
    --root="$target" -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lp" \
  timeout --foreground --kill-after=10s 600 lake env lean --trust=0 -t0 \
    --root="$target" "$target/ObligationTree.lean"
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
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`.

## Retry Condition

Resume after placeholder-free implementations of every child needed for both
frozen direction packages enter the pinned closure, or after an immutable,
compatible exact Lean 4 proof is pinned/imported and passes exact-type,
provenance, placeholder, axiom, composition, and trust checks. Until then,
proof-phase completion and a worker `[_]` receipt would be false.
