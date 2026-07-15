# THM-M-0330 proof-phase recheck at current base

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T13:12:47+08:00` (`Asia/Shanghai`)

Base revision: `34729c0dff13ac1d1a2781d9c1ea4bf7c6a35398`

Base tree: `dde7f823b850641fc7dade0380327b6ac013ac07`

## Verdict

`blocked`. No placeholder-free inhabitant of either exact direction package is
present in the repository or pinned dependency closure. The frozen target is
the full contraction Hille-Yosida equivalence for every partially defined
real-linear operator on every real Banach space. Its minimal open root cut is:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` is only a checked conditional composition: it
requires complete `ForwardPackage` and `ConversePackage` arguments and
constructs neither. `target_iff_expanded` is only a definitional transport.

The proof inputs and dependency pins are byte-for-byte unchanged since base
`63a9ed9c`; the only later target changes integrated another blocker-evidence
pair. Repository history, duplicate target `THM-M-1041`, and legacy module
`S1_M_234.lean` contain definitions, abstract interfaces, transports, or
conditional composition, not a substantive direction package. A source search
over every package in the pinned cache found no Hille-Yosida theorem or
strongly continuous-semigroup generator API.

The previously audited external candidate `mrdouglasny/hille-yosida` remains
at immutable revision `680e9499ee866763e737c8d888c1248684ced667`. It omits
generator density and closedness, the left inverse on the entire domain, and
the converse generation theorem. TauCeti main remains at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`; it likewise does not supply the
exact packages and uses incompatible pins. Both projects remain outside the
pinned Lake closure. This run queried only branch metadata; it did not clone,
fetch, build, integrate, or credit either project.

Closing the root requires new formal proofs of generator density and
closedness, a Laplace/Bochner resolvent with both inverse laws and its
contraction estimate, and the Yosida-approximation construction with strong
semigroup convergence and exact generator identification. Alternatively, an
immutable compatible exact proof must enter the pinned closure and pass exact
type, provenance, placeholder, axiom, composition, and trust checks. Assuming
either direction package, weakening the equivalence, or replacing the analytic
predicates with abstract fields would add an unproved premise or substitute a
different theorem and was rejected.

The item remains `[ ]`; lifecycle remains `planned`; the frozen graph's root
vector remains `[H3, M4, R4]`; accepted receipt IDs remain empty; and theorem
completion remains false. The older intake projection still says
`[H1, M4, R4]`; this proof worker does not rewrite that separate projection.
Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. Initial status showed only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.
The temporary Lean object was written below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank 823; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 1 | Shared `.lake/packages/flt-regular` could not resolve `HEAD`; worker rules prohibit repair or fetch. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | 19 obligations and 40 typed edges passed; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both directions remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match: no terminal Hille-Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; lexical supporting evidence only. |
| `git diff --quiet 63a9ed9c..HEAD --` proof inputs and dependency pins | 0 | `Statement.lean`, `ObligationTree.lean`, registry, typed graphs, anchor audit, validation specs, Lake manifest, and toolchain are unchanged. |
| `git ls-remote` for the two previously audited external main branches | 0 | Revisions are `680e9499...d667` and `c7e69c3c...94fa`; neither was fetched or integrated. |
| `python3 -m json.tool` on the structured blocker artifact | 0 | Structured blocker artifact is valid JSON. |
| `git diff --no-index --check /dev/null` on each new blocker artifact | 1 each | Expected diff-found status with no whitespace-error output. |
| `git diff --check -- Stage1_Instances/THM-M-0330` | 0 | No whitespace errors in the scoped tracked diff; separate no-index checks cover the new files. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The standard statement checker failed before invoking Lean because the shared
`flt-regular` checkout has no resolvable `HEAD`. The smallest nonmutating
fallback invoked the pinned Lean executable through `lake env` and existing
package objects:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-lake-env-head-34729c0d-slot72.XXXXXX)
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
