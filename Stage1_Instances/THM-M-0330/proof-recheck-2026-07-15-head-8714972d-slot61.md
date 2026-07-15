# THM-M-0330 proof recheck at `8714972d`

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T15:03:18+08:00` (`Asia/Shanghai`)

Base revision: `8714972d4cf7ae256a92b9e35032c9df1bf5745c`

Base tree: `080d14e14102a733c6992aa0644e3c65d755e91b`

## Verdict

`blocked`. The assigned proof item remains `[ ]`; lifecycle remains `planned`;
the frozen root remains `[H3, M4, R4]`; and theorem completion remains false.
This is target-scoped blocker evidence, not a proof receipt. Because the proof
phase is incomplete, no workspace-root `.stage1-worker-selftest.json` is
written.

The frozen root is
`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget`, the complete
real-Banach-space contraction Hille-Yosida equivalence. Neither exact
direction package has a placeholder-free inhabitant in the repository or
pinned dependency closure. The minimal open root cut remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` is only a checked conditional composition from
caller-supplied `ForwardPackage` and `ConversePackage` arguments. It constructs
neither. `target_iff_expanded` is only a definitional transport.

The exact proof inputs and dependency pins are unchanged since the prior
`229ca98e` recheck. The only later target change integrated that blocker
evidence pair. Repository history, exact duplicate `THM-M-1041`, and legacy
module `S1_M_234.lean` provide definitions, abstract interfaces, transports,
or conditional composition only. A search across all `9676` Lean sources in
the pinned package cache found no Hille-Yosida theorem or strongly continuous
semigroup generator API.

The audited external candidate `mrdouglasny/hille-yosida` at immutable commit
`680e9499ee866763e737c8d888c1248684ced667` remains outside the pinned closure.
It contains useful forward Laplace-resolvent pieces but omits generator density
and closedness, the left inverse on the whole generator domain, and the
converse generation theorem. Its converse work contains commented former
axioms and a placeholder rather than a terminal proof. Its real-time bundled
semigroup API would also need substantive checked transports to the frozen
`NNReal` and `LinearPMap` definitions. TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` likewise does not supply the exact
two packages and uses incompatible pins. Neither candidate was fetched,
cloned, built, integrated, or credited in this run.

Closing the exact root requires new formal proofs of generator density and
closedness, a Laplace/Bochner resolvent with both inverse laws and the `1/a`
estimate, and the Yosida-approximation construction with strong semigroup
convergence and exact generator identification. Alternatively, an immutable,
compatible exact proof must enter the pinned closure. Assuming a direction
package, weakening the equivalence, or replacing the analytic predicates by
abstract fields would add an unproved premise or prove a substituted theorem
and was rejected.

The older intake projection in `instance.json` remains `[H1, M4, R4]`, while
the frozen obligation graph records `[H3, M4, R4]`. This proof worker reports
that pre-existing difference and does not rewrite another phase's artifact.

## Validation

All commands ran inside this worker clone. Initial status contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned cache. No `lake update`, `lake build`, dependency clone/fetch,
or `.lake` mutation ran. Temporary Lean output was isolated under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank `823`; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | Expression SHA-256 `5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`; all three mutations killed. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges pass; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both direction packages remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match across all `9676` pinned Lean sources. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 229ca98e..HEAD --` proof inputs and dependency pins | 0 | Statement, composition, registry, graphs, audit, validation specs, Lake manifest, and toolchain are unchanged. |
| `python3 -m json.tool <current blocker JSON>` | 0 | Structured blocker artifact parses as JSON. |
| Target-specific blocker invariant assertions | 0 | Identity, base/tree, `[ ]` state, false completion flags, empty proof/receipt lists, exact root cut, changed paths, command results, and self-test absence pass. |
| `git diff --check` plus no-index checks of both new artifacts | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent, as required for an incomplete proof phase. |

The narrow kernel replay used only the pinned executable and existing package
objects:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0330
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0330-proof-head-8714972d-slot61.XXXXXX)
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
  timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 --root="$target" \
      -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lp" \
  timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 --root="$target" \
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

Resume after placeholder-free implementations of every child needed for both
frozen direction packages enter the pinned closure, or after an immutable,
compatible exact Lean 4 proof is pinned/imported and passes exact-type,
provenance, placeholder, axiom, composition, and trust checks. Until then,
proof-phase completion and a worker `[_]` receipt would be false.
