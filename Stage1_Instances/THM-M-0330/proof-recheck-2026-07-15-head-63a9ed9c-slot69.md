# THM-M-0330 proof-phase recheck at current base

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T12:59:16+08:00` (`Asia/Shanghai`)

Base revision: `63a9ed9c4aae594da31423142b0658129d5452a7`

Base tree: `7bee4fac4489bad36fd615a023df13bb294d1781`

## Verdict

`blocked`. The exact frozen proposition is the full contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof of this proposition is present in the
repository or pinned dependency closure. Neither `ForwardPackage` nor
`ConversePackage` is inhabited, so the minimal open root cut remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` checks only the final composition after both
complete directions are supplied. It constructs neither direction and is not
a premise-free proof. `target_iff_expanded` is only a definitional transport.

The proof inputs and dependency pins are byte-identical to the last integrated
recheck. The only target changes between that base and this one are integration
of that blocker-evidence pair. Repository-wide search found only definitions,
abstract interfaces, transports, or conditional adapters. Search over every
Lean source in the pinned package cache found no Hille--Yosida theorem or
strongly continuous-semigroup generator API.

The audited external candidate `mrdouglasny/hille-yosida` remains at immutable
revision `680e9499ee866763e737c8d888c1248684ced667`. It is outside the pinned
closure and supplies only pieces of the forward resolvent route. It omits
generator density and closedness, the left inverse on the whole domain, and the
converse. Fresh remote queries for TauCeti and the `jagg-ix/HilleYosida` fork
timed out without output; no source was cloned, fetched, built, integrated, or
credited.

Closing the exact target requires new proofs of generator density and
closedness, a Laplace/Bochner resolvent with both inverse laws and its
contraction estimate, and the Yosida-approximation construction with strong
semigroup convergence and exact generator identification. Assuming either
direction package, weakening the equivalence, or replacing the analytic facts
with abstract fields would add an unproved premise or substitute a different
theorem and was rejected.

The item remains `[ ]`; lifecycle remains `planned`; the frozen graph's root
vector remains `[H3, M4, R4]`; accepted receipt IDs remain empty; and theorem
completion remains false. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. Initial status showed only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran. Lean
objects were isolated below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank 823; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 1 | Lake could not resolve `HEAD` in the incomplete shared `flt-regular` checkout; no repair or dependency mutation was attempted. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | 19 obligations and 40 typed edges passed; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both direction packages remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; lexical supporting evidence only. |
| `git diff --quiet b6d7de19..HEAD --` proof inputs and dependency pins | 0 | `Statement.lean`, `ObligationTree.lean`, registry, typed graphs, anchor audit, Lake manifest, and toolchain are unchanged. |
| `git diff --stat b6d7de19..HEAD -- Stage1_Instances/THM-M-0330 ...` | 0 | Only the preceding blocker-evidence pair was added. |
| `git ls-remote https://github.com/mrdouglasny/hille-yosida.git refs/heads/main` | 0 | Main remains at `680e9499ee866763e737c8d888c1248684ced667`; nothing was fetched or integrated. |
| Timed `git ls-remote` for TauCeti and the `jagg-ix/HilleYosida` fork | 124 each | Both fresh queries timed out without output; no clone, fetch, integration, or proof credit followed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0330/proof-recheck-2026-07-15-head-63a9ed9c-slot69.json` | 0 | Structured blocker artifact is valid JSON. |
| `git diff --no-index --check /dev/null` for each new artifact | 1 each | Expected diff-found status with no whitespace-error output. |
| `git diff --check -- Stage1_Instances/THM-M-0330` | 0 | No whitespace errors in the tracked scoped diff; the no-index checks cover the new files. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The standard statement checker cannot currently replay because the shared
`Formalizations/Lean/.lake/packages/flt-regular` checkout has no resolvable
`HEAD`. Worker rules prohibit repairing it. The smallest nonmutating fallback
used the pinned executable through `lake env` and existing package objects:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-head-63a9ed9c-slot69.XXXXXX)
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
