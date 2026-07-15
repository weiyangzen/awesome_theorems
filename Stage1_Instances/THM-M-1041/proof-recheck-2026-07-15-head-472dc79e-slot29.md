# THM-M-1041 proof recheck at `472dc79e`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Base revision: `472dc79eb4d406a6707691193fbe3ab58d0f0cc4`

Base tree: `881d873727dc80435119839b8e60e9e9c2cfb208`

Recorded: 2026-07-15 15:10:13 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target is the real Banach-space contraction Hille--Yosida
equivalence in `Statement.lean`. A proof must implement both
`ForwardPackage` and `ConversePackage` from `ObligationTree.lean`. The existing
`root_of_directionPackages` theorem is only conditional composition: it takes
those complete packages as premises and constructs neither one.

The minimal open root cut remains
`{M1041-F-ASSEMBLE, M1041-C-ASSEMBLE}`. Its fourteen substantive descendants
have no terminal proof bodies. The first unavailable forward leaf is
`M1041-F-CLOSED`, generator closedness for the exact `IsGenerator` graph. The
independent converse blocker starts at `M1041-C-YOSIDA-APPROX`; pinned mathlib
has no strongly continuous semigroup generator or Hille--Yosida API from which
to build it.

The proof inputs and dependency pins are unchanged since `76c08cb5`.
Repository history, duplicate target `THM-M-0330`, and legacy module
`S1_M_234.lean` contain definitions, abstract interfaces, transports, or
conditional composition, not either direction package. A fresh search of all
9676 Lean sources in the pinned package cache found no terminal declaration
for this theorem family.

The audited external candidates remain outside the pinned closure and do not
provide both exact directions. `mrdouglasny/hille-yosida` and its fork at
`680e9499ee866763e737c8d888c1248684ced667` contain only an incomplete
prospective forward resolvent development; the source marks the range/right
inverse work and converse as unfinished. TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` uses incompatible pins and is
also incomplete. Nothing was cloned, fetched, built, integrated, or credited.

Closing the target requires new proofs of generator closedness and density,
the Laplace/Bochner resolvent with both inverse laws and its norm bound, and
the converse Yosida-approximation semigroup construction with exact generator
identification. Assuming either direction, weakening the equivalence, or
replacing the analytic predicates with abstract fields would prove a different
theorem and was rejected.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; receipt IDs stay empty; and `audit_complete` and
`theorem_complete` stay false. This pair is blocker evidence, not a proof
receipt. Since the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The owned path was initially clean; the
only pre-existing untracked path was the automation-provided
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.
Direct Lean output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both directions remain `M4`. |
| Direct pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. Temporary `Statement.olean` SHA-256: `e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`. |
| Pinned-package topical search below | 1 | Expected no-match among 9676 Lean files: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 76c08cb5 HEAD -- <proof-relevant inputs>` | 0 | Frozen statement, architecture, audit input, manifest, and toolchain are unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |
| `python3 -m json.tool <this-json>` | 0 | The structured blocker artifact is syntactically valid JSON; no separate schema-validator claim is made. |
| Added-file whitespace checks | 0 | Both new evidence files passed `git diff --no-index --check` with the expected added-file status and no diagnostics. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-472dc79e-slot29.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for d in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  lean_path="$lean_path:$d"
done
cd "$mathlib"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
    "$target/ObligationTree.lean"
```

The replay ran from `2026-07-15T15:08:43+08:00` through
`2026-07-15T15:08:55+08:00`.

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
