# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `dd9bc71d70586d022d87833d780fbe15959b89b0`

Base tree: `d096d4ef8804532c9165b75d369f49b7b74945d8`

## Verdict

`blocked`. No placeholder-free proof body for the exact frozen contraction
Hille--Yosida equivalence exists in the repository or pinned dependency
closure. Neither `ForwardPackage` nor `ConversePackage` is inhabited. The
minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only the final composition after callers
supply both complete directions. It is not a proof body for either package or
the root.

Pinned mathlib contains the `LinearPMap`, bounded-operator, topology, and
integration substrate, but no strongly continuous semigroup generator API or
terminal Hille--Yosida theorem. The repository search found only the legacy
`S1_M_234.lean` abstract interface and the duplicate frozen target
`THM-M-0330`; neither contains the required proof bodies.

The previously audited external candidates do not close this item.
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667` supplies prospective forward
resolvent pieces only and remains outside the pinned Lake closure.
`TauCetiProject/TauCeti` at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` uses incompatible Lean/mathlib
pins and also lacks generator closedness, the left inverse, and the converse
generation construction. Neither candidate was fetched, integrated, or
credited during this recheck.

The root vector remains `[H2, M4, R4]`, accepted receipt IDs remain empty, and
the execution item remains `[ ]`. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

Checks ran in this worker clone against the automation-provided pinned
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or deliberate
`.lake` mutation was run. The shared canonical `.lake` became transiently
unavailable while another concurrent worker was creating its `flt-regular`
checkout. To avoid retrying a command that could fetch, the successful narrow
kernel replay used the same pinned Lean binary and assembled `LEAN_PATH`
directly from the existing pinned build directories. Its output object lived
under `/tmp` and was removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | The checked script passed before the shared-cache race; the frozen expression hash remains `e6e5f0cb...f7768d`. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | Recorded immutable candidate classifications and fail-closed root decision passed. |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e...b39c42`; root and both direction packages remain `M4`. |
| Direct pinned Lean `--trust=0 -t0` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reported `[propext, Classical.choice, Quot.sound]`. |
| Direct pinned mutation replay mirroring `check_statement.py` | 0 | The canonical target and all three structural mutations elaborated, and none had the canonical kernel expression. |
| Scoped repository and pinned-package source searches | 0 / 1 | Repository matches were only legacy/duplicate interfaces; the pinned-package search had the expected no-match result. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-14-head-dd9bc71d.json` | 0 | Current-base structured blocker record is valid JSON. |
| Scoped prohibited-token scan over owned `*.lean` files | 1 | Expected no-match result. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is correctly absent. |
| `git diff --check -- Stage1_Instances/THM-M-1041 .stage1-worker-selftest.json` | 0 | No whitespace errors in tracked differences. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1041
lake_root=$(readlink -f "$repo/Formalizations/Lean/.lake")
toolchain=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0
lean=$toolchain/bin/lean
pkg_paths=$(find -L "$lake_root/packages" -path '*/.lake/build/lib/lean' \
  -type d -print | LC_ALL=C sort | paste -sd: -)
lean_path="$pkg_paths:$lake_root/build/lib/lean:$toolchain/lib/lean"
tmp=$(mktemp -d /tmp/thm-m-1041-proof-dd9bc71d.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Current SHA-256 values are
recorded in the paired JSON artifact.

## Retry condition

Resume after placeholder-free implementations of both frozen direction
packages and their required children become available, or after an immutable
compatible exact Lean 4 proof is integrated into the pinned dependency closure
and passes exact-type, placeholder, axiom, provenance, composition, and trust
checks. This artifact is blocker evidence, not a proof receipt or state-change
request.
