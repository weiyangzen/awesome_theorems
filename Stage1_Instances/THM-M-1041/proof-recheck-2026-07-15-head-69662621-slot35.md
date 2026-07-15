# THM-M-1041 proof recheck at `69662621`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Base revision: `69662621a19907de342801b09124e8dfe3495e40`

Base tree: `fbfbc07e2045accdd0144baf892481a9bb6717f8`

Recorded: 2026-07-15 18:53:01 +08:00

## Verdict

`blocked`; no state change.

The frozen target is the real Banach-space contraction Hille--Yosida
equivalence in `Statement.lean`, with expression SHA-256
`e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`.
A premise-free proof must inhabit both `ForwardPackage` and `ConversePackage`
from `ObligationTree.lean`. The existing theorem
`root_of_directionPackages` only composes those packages after receiving both
as premises; it constructs neither direction and is not root proof evidence.

No placeholder-free body for either package exists in the repository or the
pinned Lake dependency closure. The minimal root cut remains
`{M1041-F-ASSEMBLE, M1041-C-ASSEMBLE}`. The first unavailable forward leaf is
`M1041-F-CLOSED`, generator closedness for the frozen `IsGenerator`
definition. Independently, the first unavailable converse construction is
`M1041-C-YOSIDA-APPROX`. All fourteen substantive direction obligations
remain without terminal bodies.

The frozen proof inputs and dependency pins are byte-identical to their last
target-changing revision, `76c08cb569093ff0ea02564e80dced5284ebd59d`.
Repository history, duplicate target `THM-M-0330`, and legacy module
`S1_M_234.lean` contain definitions, abstract interfaces, transports, or
conditional composition only. A source search over the existing pinned
package cache found no Hille--Yosida theorem or strongly continuous-semigroup
generator API. No hidden inconsistency or vacuity was found in the frozen
statement: the right-neighborhood filter on `NNReal` is nontrivial, limits in
the norm topology are unique, and the identity semigroup with the zero
generator is a consistent special case rather than a proof of the universal
claim.

The external candidate `mrdouglasny/hille-yosida` remains at immutable main
revision `680e9499ee866763e737c8d888c1248684ced667`. Its other visible branches
also contain partial forward Laplace-resolvent work, while generator density
and the generation theorem remain absent; none supplies the converse. A
fresh TauCeti remote query failed after the first remote query because GitHub
became unreachable, so this run makes no fresh TauCeti revision claim. The
previously audited immutable TauCeti revision remains outside the pinned
closure and cannot receive proof credit. No external dependency was cloned,
fetched, built, integrated, or credited.

Closing the exact root requires new formal analysis: generator closedness and
density; the Laplace/Bochner resolvent with both inverse laws and its
contraction estimate; and the real-Banach Yosida approximation, limiting
semigroup, laws, continuity, contraction, and exact generator identification.
Alternatively, an immutable compatible exact proof must enter the pinned
closure. Assuming a direction package, weakening the equivalence, or replacing
the analytic definitions with abstract fields would add an unproved premise
or prove a substituted theorem and was rejected.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; accepted receipt IDs stay empty; and `audit_complete` and
`theorem_complete` stay false. This pair is blocker evidence, not a proof
receipt. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The owned path was initially clean; the
only pre-existing untracked path was the automation-provided
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.
Direct Lean output was isolated under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Direct pinned `lean --trust=0 -t0` replay below | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` SHA-256 `e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`. |
| Pinned-package topical search below | 1 | Expected no-match over 9042 Lean source files: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 76c08cb5 HEAD -- <proof-relevant inputs>` | 0 | Statement, composition, registry, typed graphs, anchor audit, validation specs, Lake manifest, and toolchain are unchanged. |
| `git ls-remote https://github.com/mrdouglasny/hille-yosida.git refs/heads/main` | 0 | Main remains `680e9499ee866763e737c8d888c1248684ced667`; it was not fetched or integrated. |
| `git ls-remote https://github.com/TauCetiProject/TauCeti.git refs/heads/main` | 128 | GitHub became unreachable after the first query; no fresh remote-state claim is made. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-69662621-slot35.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && env -u LEAN_PATH lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    ObligationTree.lean
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
