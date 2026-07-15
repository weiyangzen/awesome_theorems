# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T13:53:50+08:00` (`Asia/Shanghai`)

Base revision: `21798c9c8a9ed9ea40e8df489d9c661b59026564`

Base tree: `9150bea4c07c5bc89526ce2540709f0e9e8fda24`

## Verdict

`blocked`. The frozen root is the full real contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof body for this equivalence exists in
the repository or the pinned Lake dependency closure. Neither
`ForwardPackage` nor `ConversePackage` is inhabited, so the minimal open root
cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only conditional final composition after a
caller supplies both complete directions. `target_iff_expanded` is only a
definitional transport. Neither is a proof body for the exact root.

The frozen statement, obligation architecture, audit input, and pins are
byte-identical to the most recent integrated recheck input. Repository
history, duplicate target `THM-M-0330`, and legacy module `S1_M_234` contain
definitions, abstract fields, transports, or the same conditional
architecture, not either direction package. A fresh source search across
every pinned package found no Hille--Yosida theorem or strongly continuous
semigroup generator API.

The audited external candidates still do not close the root. Both
`mrdouglasny/hille-yosida` and its `jagg-ix/HilleYosida` fork remain at
`680e9499ee866763e737c8d888c1248684ced667`. They provide prospective forward
resolvent pieces but no generator closedness or density, no resolvent left
inverse, and no converse. TauCeti remains at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`; it includes prospective dense
generator-domain and forward-resolvent pieces but still lacks generator
closedness, the left inverse, and the Yosida converse, and it uses incompatible
pins. A separately observed Yosida development proves Stone's theorem for
self-adjoint operators on complex Hilbert spaces, not the frozen theorem for
arbitrary real Banach-space contraction generators. None of these candidates
is in the pinned closure. No dependency was cloned, fetched, built,
integrated, or credited.

Closing the target requires new formal proofs of generator closedness and
density, the Laplace/Bochner resolvent with both inverse laws and its
contraction estimate, and the Yosida-approximation semigroup construction with
exact generator identification. Alternatively, an immutable compatible exact
proof must enter the pinned dependency closure. Assuming a direction package,
weakening the equivalence, or replacing the analytic predicates with abstract
fields would add an unproved premise or prove a different theorem.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; and accepted receipt IDs stay empty. This pair is blocker
evidence, not a proof receipt or state-change request. Because the proof phase
is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The initial owned path was clean; the
only untracked entry was the automation-provided `Formalizations/Lean/.lake`
symlink to the canonical pinned cache. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation ran. Direct Lean output was
isolated under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 1 | The helper could not resolve `HEAD` in the automation-provided incomplete `flt-regular` cache (`external command 'git' exited with code 128`). No repair or fetch was attempted. The direct replay below independently elaborated the unchanged statement. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Direct pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration in any pinned package source. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources. This lexical scan is supporting evidence only. |
| `git diff --quiet accbdd65 HEAD -- <proof-relevant inputs>` | 0 | Frozen statement, architecture, audit input, manifest, and toolchain are unchanged. |
| `git ls-remote` for the three audited external branches | 0 | Revisions remain `680e9499...d667`, `680e9499...d667`, and `c7e69c3c...94fa`; none entered the pinned closure. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-15-head-21798c9c-slot29.json` | 0 | The structured blocker artifact is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1041` | 0 | No whitespace errors in the owned-path changes. |
| Added-file `git diff --no-index --check` for both evidence files | 1 each | Expected added-file status with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is absent, as required for the incomplete phase. |

Exact narrow Lean replay, run from the repository root with `lake env lean`
from the pinned mathlib checkout (avoiding the incomplete unrelated package):

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-slot29.XXXXXX)
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

The JSON syntax check does not claim a separately published schema validator;
the structured record remains fail-closed blocker evidence only.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dea413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages are in the pinned closure, or after an immutable
compatible exact Lean 4 proof is pinned/imported and passes exact-type,
provenance, placeholder, axiom, composition, and trust checks.
