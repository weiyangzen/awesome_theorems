# THM-M-0405 proof recheck at `c8b8f4f8`

Item: `S56-M-0405-PROOF`

Date: `2026-07-14T01:48:36+08:00`

Base revision: `c8b8f4f857647bcc095dc48e8c30390991351ab3`

Base tree: `7a7e5a787c4d6e834f76a9787ee5e194074b1bc8`

## Verdict

`blocked`: this retry found no placeholder-free proof body for the exact
Bilu-Hanrot-Voutier root. The first failed gate remains
`M0405-X-BHV-BRIDGE`, the minimal open root cut remains
`[M0405-X-BHV-BRIDGE]`, and the root remains `[H1, M4, R3]`.
No `Proof.lean` or proof receipt was added, `root_closed=false`, and
`theorem_complete=false`.

The exact target requires both Lucas and Lehmer primitive-divisor branches for
every index above 30. The only owned composition declaration,
`Stage1.THM_M_0405.statement_of_branches`, takes those two complete branches as
premises. Its projection declarations likewise take an already closed root.
They are checked interfaces, not implementations of the BHV theorem. The
legacy `S1_M_018.lean` file still supplies only models, adapters, conditional
wrappers, and a Fibonacci index-three toy result.

A fresh repo/pinned-closure scan found no terminal BHV, Zsigmondy, or
primitive-divisor declaration. A fresh Sourcegraph global Lean search,
including forks and archived repositories, returned `matchCount: 0` for each
of `"Bilu-Hanrot-Voutier"`, `Zsigmondy`, and `"primitive divisor"`; each search
completed with `skipped: []`. This bounded search is new negative discovery
evidence, not a universal nonexistence claim and not proof credit.

## Validation evidence

All local checks reused the automation-provided canonical pinned `.lake`
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0405` | 0 | Rank 18, `planned`, `L0`, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0405/check_obligation_tree.py` | 0 | `15 obligations, 30 typed edges, denominator cd9daee4...da793; root open M4` |
| Run the isolated Lean recipe below | 0 | The exact `Statement` and conditional composition module elaborated; output included `Stage1.THM_M_0405.Statement : Prop`. |
| `rg -n -i --glob '*.lean' '\\bBilu\\b|\\bHanrot\\b|\\bVoutier\\b|\\bZsigmondy\\b|primitive[ _-]?divisor' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Relevant hits were confined to the owned dossier and legacy `S1_M_018.lean`; pinned mathlib supplied no terminal theorem. |
| Three Sourcegraph stream searches with `context:global fork:yes archived:yes count:1000 lang:Lean` and the terms above | 0 | Each final event had `done:true`, `matchCount:0`, and `skipped:[]`. |
| `rg -n '\\b(sorry|admit|sorryAx|axiom|unsafe)\\b' Stage1_Instances/THM-M-0405 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited token occurs in the owned Lean sources. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0405/proof-recheck-2026-07-14-c8b8f4f8.md; code=$?; test $code -eq 1` | 0 | The expected new-file diff produced no whitespace diagnostic. |
| `git diff --check -- Stage1_Instances/THM-M-0405/` | 0 | No tracked whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

Isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0405
tmp=$(mktemp -d /tmp/thm-m-0405-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" ObligationTree.lean
```

Exact Sourcegraph search recipe, run once for each listed query:

```bash
for query in \
  'context:global fork:yes archived:yes count:1000 lang:Lean "Bilu-Hanrot-Voutier"' \
  'context:global fork:yes archived:yes count:1000 lang:Lean Zsigmondy' \
  'context:global fork:yes archived:yes count:1000 lang:Lean "primitive divisor"'
do
  curl -L --max-time 45 -sS -G \
    'https://sourcegraph.com/.api/search/stream' \
    --data-urlencode "q=$query" --data 'v=V3' |
    rg '"done":true' | tail -1
done
```

The three final records respectively reported durations `2864ms`, `4800ms`,
and `9979ms`, with `matchCount:0` and `skipped:[]` in every record.

The frozen inputs remained unchanged: `Statement.lean`
`db2edf61...8da1`, `ObligationTree.lean` `d43df06f...c9b`, obligation
registry `85019c33...12d`, typed graphs `a69a1ee0...889b`, Lake manifest
`321626c8...2d81`, and toolchain file `651c8acc...b1d2`.

## Retry condition

Resume after placeholder-free implementations of the frozen normalization,
cyclotomic-factor, nonprimitive-bound, large-index-exclusion, defective-pair
classification, common BHV bridge, and both exact adapters, or after discovery
of an immutable compatible Lean 4 terminal proof that can be pinned and
exact-type checked without changing the dependency lock.

This is fresh nonrelease blocker evidence only. It does not satisfy
`S56-M-0405-PROOF`, proposes no checklist state change, and cannot be promoted
to proof, validation, release, audit, master, or theorem completion. Because
the assigned proof phase is not genuinely self-tested, no
`.stage1-worker-selftest.json` is emitted.
