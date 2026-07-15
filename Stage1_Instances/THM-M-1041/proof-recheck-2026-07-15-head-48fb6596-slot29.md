# THM-M-1041 proof recheck at `48fb6596`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Base revision: `48fb6596b1844f4183c411142415d872ff21e842`

Base tree: `eb8dfff0e90b5ce5b11ac2096777060d62874064`

Recorded: 2026-07-15 14:52:53 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target is the real Banach-space contraction Hille--Yosida
equivalence in `Statement.lean`. A genuine proof must implement both
`ForwardPackage` and `ConversePackage` from `ObligationTree.lean`. The existing
`root_of_directionPackages` declaration is only conditional composition: it
consumes those packages as premises and constructs neither one.

The frozen minimal open root cut remains
`{M1041-F-ASSEMBLE, M1041-C-ASSEMBLE}`. Its fourteen substantive descendants
have no terminal proof bodies. The first unavailable forward leaf is
`M1041-F-CLOSED`, generator closedness for the exact `IsGenerator` graph. The
independent converse blocker begins at `M1041-C-YOSIDA-APPROX`; pinned mathlib
has no strongly continuous semigroup generator or Hille--Yosida API from which
to construct it.

All frozen proof inputs and dependency pins are byte-identical to their last
target change at `ec3b52a2`. Repository history, duplicate target
`THM-M-0330`, and legacy `S1_M_234.lean` provide only definitions, abstract
interfaces, transports, or conditional composition. A source search across
all 9676 Lean files in the pinned package cache found no terminal declaration
for this theorem family.

The audited external heads are unchanged. `mrdouglasny/hille-yosida` and its
`jagg-ix/HilleYosida` fork remain at
`680e9499ee866763e737c8d888c1248684ced667`; TauCeti remains at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`. They remain outside the pinned
closure and do not contain both exact direction packages. No dependency was
cloned, fetched, built, integrated, or credited.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; accepted receipt IDs stay empty; and `audit_complete` and
`theorem_complete` stay false. This pair is blocker evidence, not a proof
receipt. Because the assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The owned path was clean before this
evidence pair was added. The only pre-existing untracked entry was the
automation-provided `Formalizations/Lean/.lake` symlink to canonical pinned
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation ran. Direct Lean output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression fingerprint `e6e5f0...f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e...39c42`; root and both direction packages remain `M4`. |
| Direct pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match among 9676 Lean files: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet ec3b52a2 HEAD -- <proof-relevant inputs>` | 0 | Statement, architecture, audit input, manifest, and toolchain are unchanged. |
| `git ls-remote` for the three audited external branches | 0 | Heads remain `680e9499...d667`, `680e9499...d667`, and `c7e69c3c...94fa`; none entered the pinned closure. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-15-head-48fb6596-slot29.json` | 0 | Structured blocker artifact is valid JSON; no separately published schema validation is claimed. |
| Scoped whitespace checks | 0 | `git diff --check` passed; both untracked files also passed added-file no-index checks with expected exit 1 and no diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-slot29-current.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for d in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  lean_path="$lean_path:$d"
done
cd "$mathlib"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground 600 lake env lean --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
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
