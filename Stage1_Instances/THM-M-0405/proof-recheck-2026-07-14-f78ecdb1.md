# THM-M-0405 proof recheck at `f78ecdb1`

Item: `S56-M-0405-PROOF`

Date: `2026-07-14T02:07:23+08:00`

Base revision: `f78ecdb166de720e4af8d8859826b4a22a4c1733`

Base tree: `6d72b645f5722769d4ed5d9eea3559c9e4c69856`

## Verdict

`blocked`: this proof attempt found neither a placeholder-free body for the
exact Bilu-Hanrot-Voutier root nor an immutable compatible Lean 4 result that
can be imported from the pinned dependency closure. The first failed gate is
`M0405-X-BHV-BRIDGE`. The minimal mathematical open root cut remains
`[M0405-X-BHV-BRIDGE]`, all 15 machine-required obligations remain open, and
the root remains `[H1, M4, R3]`.

No `Proof.lean` or proof receipt was added. `root_closed=false` and
`theorem_complete=false`. The assigned proof deliverable is not complete.

The exact target requires both Lucas and Lehmer primitive-divisor branches for
every index above 30. The checked local declaration
`Stage1.THM_M_0405.statement_of_branches` consumes those two complete branches
as premises; it constructs neither branch. The two projection declarations
likewise start from an already closed root. Using any of these declarations as
the missing proof would introduce premises and replace the canonical theorem
with a conditional result.

The legacy `S1_M_018.lean` file still provides only models, adapters,
conditional wrappers, and a Fibonacci index-three toy result. The fresh
repo-local and pinned-mathlib scan found no BHV, Zsigmondy, or primitive-divisor
terminal theorem. Fresh Sourcegraph global Lean searches, including forks and
archived repositories, returned `matchCount: 0` and `skipped: []` for each of
`"Bilu-Hanrot-Voutier"`, `Zsigmondy`, and `"primitive divisor"`. This bounded
negative search is discovery evidence only, not a universal nonexistence claim
or proof credit.

## Validation evidence

All local checks reused the automation-provided canonical pinned `.lake`
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0405` | 0 | Rank 18, lifecycle `planned`, baseline `L0`, legacy artifacts unaccepted, and `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0405/check_obligation_tree.py` | 0 | `ok: 15 obligations, 30 typed edges, denominator cd9daee4...da793; root open M4` |
| Run the isolated Lean recipe below | 0 | The exact `Statement` and conditional composition module elaborated. Each `#print axioms` report listed only `propext`, `Classical.choice`, and `Quot.sound`; no branch proof was produced. |
| `rg -n -i --glob '*.lean' '\\bBilu\\b|\\bHanrot\\b|\\bVoutier\\b|\\bZsigmondy\\b|primitive[ _-]?divisor' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Relevant hits were confined to the owned dossier and legacy `S1_M_018.lean`; pinned mathlib supplied no terminal theorem. |
| Three Sourcegraph stream searches with `context:global fork:yes archived:yes count:1000 lang:Lean` and the terms above | 0 | Final records reported durations `5686ms`, `4591ms`, and `6732ms`, each with `done:true`, `matchCount:0`, and `skipped:[]`. |
| `rg -n '\\b(sorry|admit|sorryAx|axiom|unsafe)\\b' Stage1_Instances/THM-M-0405 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited token occurs in the owned Lean sources. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `sha256sum` on the statement, obligation interface, registry, typed graphs, anchor audit, Lake manifest, and toolchain | 0 | `db2edf61...8da1`, `d43df06f...c9b`, `85019c33...12d`, `a69a1ee0...889b`, `d23923ab...cd3`, `321626c8...2d81`, and `651c8acc...b1d2`. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0405/proof-recheck-2026-07-14-f78ecdb1.md; code=$?; test "$code" -eq 1` | 0 | The expected new-file diff produced no whitespace diagnostic. |
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
cd "$lean_root"
lake env lean -R "$target" -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean "$target/ObligationTree.lean"
```

The frozen inputs were unchanged: `Statement.lean`
`db2edf61...8da1`, `ObligationTree.lean` `d43df06f...c9b`, obligation
registry `85019c33...12d`, typed graphs `a69a1ee0...889b`, anchor audit
`d23923ab...cd3`, Lake manifest `321626c8...2d81`, and toolchain file
`651c8acc...b1d2`.

## Prerequisite observations

Two pre-existing obligation-tree metadata inconsistencies remain outside this
proof implementation attempt. `obligation-tree.md` reports 12 human-source
obligations, while the authoritative registry reports 11. Several
`typed-graphs.json` nodes name a nonexistent `obligation-graphs.json` in
`owned_sources`. The structural checker does not reject either inconsistency.
They provide no proof credit and must be reconciled by the appropriate
obligation-tree or master lane before any broad acceptance claim.

## Retry condition

Resume after placeholder-free implementations of the frozen pair
normalization, cyclotomic-factor, nonprimitive-bound, large-index-exclusion,
defective-pair classification, common BHV bridge, and both exact adapters, or
after discovery of an immutable compatible Lean 4 terminal proof that can be
pinned and exact-type checked without changing the dependency lock.

This is fresh nonrelease blocker evidence only. It does not satisfy
`S56-M-0405-PROOF`, proposes no state change, and cannot be promoted to proof,
validation, release, audit, master, or theorem completion. Because the assigned
proof phase is not genuinely self-tested, no `.stage1-worker-selftest.json` is
emitted.
