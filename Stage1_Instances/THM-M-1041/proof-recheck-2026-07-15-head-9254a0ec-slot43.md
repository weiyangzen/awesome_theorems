# THM-M-1041 proof recheck at `9254a0ec`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Base revision: `9254a0ec0d0c71b346ae15a911721409e3ab3139`

Base tree: `a3de0086d55c8f209894b07409deeeed04c393a3`

Recorded: 2026-07-15 15:34:33 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target is the real Banach-space contraction Hille--Yosida
equivalence in `Statement.lean`. Its proof requires implementations of both
`ForwardPackage` and `ConversePackage` from `ObligationTree.lean`. The only
root-facing theorem currently present, `root_of_directionPackages`, is
conditional composition: it takes the two complete packages as premises and
constructs neither package.

The minimal open root cut remains
`{M1041-F-ASSEMBLE, M1041-C-ASSEMBLE}`. All fourteen substantive descendants
lack terminal proof bodies. The first unavailable forward leaf is
`M1041-F-CLOSED`, generator closedness for the frozen `IsGenerator` graph.
Independently, the converse is blocked first at `M1041-C-YOSIDA-APPROX`.

The proof-relevant target inputs and dependency pins are unchanged since
`76c08cb5`. Repository history, duplicate target `THM-M-0330`, and legacy
module `S1_M_234.lean` contain definitions, abstract interfaces, transports,
or conditional composition only. A current search across all 9676 Lean files
in the pinned package cache found no Hille--Yosida theorem or strongly
continuous-semigroup generator API.

The audited external candidates cannot close this target. The immutable
`mrdouglasny/hille-yosida` revision `680e9499...d667` contains partial forward
resolvent work, but lacks generator closedness and density, the left inverse,
and the converse. TauCeti revision `c7e69c3...94fa` proves density and some
forward resolvent facts, but uses incompatible Lean/mathlib pins, remains
outside the pinned closure, and lacks generator closedness, the left inverse,
and the Yosida converse. Neither project was cloned, fetched, built, integrated,
or credited.

Closing the exact root requires new formal analysis: generator closedness and
density; construction of the Laplace/Bochner resolvent with both inverse laws
and its bound; and the Yosida approximants, limiting semigroup, semigroup laws,
strong continuity, contraction, and exact generator identification. Assuming
either package, weakening the equivalence, or replacing the analytic facts by
abstract fields would add an unproved premise or substitute another theorem.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; accepted receipt IDs stay empty; and `audit_complete` and
`theorem_complete` stay false. This pair is blocker evidence, not a proof
receipt. Because the assigned proof phase is not genuinely complete,
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
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Direct pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` SHA-256 was `e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`. |
| Pinned-package topical search below | 1 | Expected no-match among 9676 Lean files: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 76c08cb5 HEAD -- <proof-relevant inputs>` | 0 | Frozen statement, architecture, audit input, graph, manifest, and toolchain are byte-for-byte unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-15-head-9254a0ec-slot43.json` | 0 | The structured blocker artifact is syntactically valid JSON; no separate schema-validator claim is made. |
| `git diff --no-index --check /dev/null <new-artifact>` for each evidence file | 1 | Expected added-file diff status with no whitespace diagnostics for either artifact. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-9254a0ec-slot43.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for d in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  lean_path="$lean_path:$d"
done
cd "$lean_root/.lake/packages/mathlib"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
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
