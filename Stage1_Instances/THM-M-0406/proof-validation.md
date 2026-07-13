# THM-M-0406 proof-phase attempt

Item: `S56-M-0406-PROOF`  
Date: `2026-07-14T01:01:35+08:00`  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

## Verdict

`blocked`: the exact frozen Lean proposition is refutable. `Proof.lean` gives a
placeholder-free countermodel and proves
`not_corvajaZannierTheoremOne :
  not (CorvajaZannierTheoremOne.{0, 0} (k := Rat))`.

The countermodel takes `boundaryDivisor := Fin 4`, all four divisors as the
boundary, unit weights and intersection numbers, `point := Unit`, and
`curve := Empty`. Every canonical premise holds, including the finite-place
and boundary conditions, but the conclusion would produce an element of
`Empty`. The kernel reports only `propext`, `Classical.choice`, and
`Quot.sound` for both the boundary witness and refutation.

This identifies an earlier exact-target consistency failure at
`M0406-S-DEFINITIONS`: the abstract fields in `SurfaceData` do not enforce that
the curve type and predicates describe the algebraic curves of the supplied
scheme. Consequently no proof body for the frozen root can exist in a
consistent Lean environment. Adding a curve-existence hypothesis or proving a
different realizable model would broaden or substitute the target.
`SurfaceDegeneracyEngine` is definitionally this same proposition, so its
current conditional adapters cannot provide consistent positive closure. This
countermodel refutes the overbroad Lean encoding, not the mathematical
Corvaja--Zannier theorem.

The proof deliverable is incomplete. The existing frozen predecessor graph
still records open `M4`; this attempt proposes the fail-closed `M5`
classification supported by the countermodel for upstream reconciliation. No
obligation is closed, no proof credit or execution-item state change is
proposed, and `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

Commands ran in this worker clone using the existing canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | `ok: 14 obligations, 26 typed edges, denominator 46deb9e2...d90a7; root open M4`. |
| Run the isolated elaboration recipe below | 0 | The statement and countermodel elaborated; both `#print axioms` reports were exactly `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\\b(sorry\\|admit\\|sorryAx)\\b\\|^[[:space:]]*axiom\\b\\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-0406 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited declaration or placeholder occurs in the owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/proof-blocker.json >/dev/null` | 0 | The structured blocker record parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0406 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker completion manifest. |

Exact isolated elaboration recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-countermodel.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" -t 0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" -t 0 Proof.lean
```

The pre-existing untracked `Formalizations/Lean/.lake` entry is the
automation-provided link to canonical pinned artifacts. This is scoped
nonrelease blocker evidence, not theorem validation or release evidence.

## Reopen condition

Reopen the statement and obligation-tree gates, replace the refuted abstract
encoding with a source-faithful target whose intrinsic, noncircular semantics
rule out this model (rather than merely assuming `Nonempty X.curve` or the
desired output), then re-freeze the exact expression and obligation registry
before scheduling another proof attempt.
