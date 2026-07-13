# THM-M-0405 proof-phase attempt

Item: `S56-M-0405-PROOF`  
Date: `2026-07-14T00:04:29+08:00`  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Verdict

`blocked`: no eligible proof body for the exact Bilu-Hanrot-Voutier target
exists in the repository or pinned dependency closure. No proof body was added,
no proof credit is claimed, and the root remains `[H1, M4, R3]`.

The first unavailable frozen package is `M0405-X-BHV-BRIDGE`. It requires the
pair normalization, homogeneous cyclotomic factor, nonprimitive upper bound,
large-index exclusion, and exhaustive defective-pair classification packages.
After that common theorem, the exact Lucas and Lehmer adapters must still
recover every discriminant, parity-sensitive denominator, and earlier-term
exclusion in the canonical predicates. None of these terminal bodies is in the
pinned Lean closure.

`ObligationTree.lean` contains the checked term `statement_of_branches`, but it
accepts the complete `LucasBranch` and `LehmerBranch` as premises and constructs
neither. Its projections likewise start from an already supplied root. Treating
any of them as the proof would replace the canonical premise-free statement
with a conditional theorem. The legacy `S1_M_018.lean` file contains only object
models, transports, and an index-3 Fibonacci toy proof; it explicitly records
that the `n > 30` BHV existence theorem is absent.

The prerequisite anchor audit found no exact repo-local, pinned mathlib, or
eligible immutable external proof to integrate. Pinned `LucasLehmer` and
`LucasPrimality` declarations are primality tests for different targets, while
the recurrence and cyclotomic APIs are only substrate. Introducing the bridge
or either branch as an axiom, premise, bodyless declaration, or other assumed
result would violate the placeholder and exact-target gates.

The proof deliverable is therefore incomplete. `.stage1-worker-selftest.json`
is deliberately absent, `root_closed=false`, and `theorem_complete=false`.

## Narrow validation evidence

All commands ran in this worker clone using the existing canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0405` | 0 | Rank 18; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0405/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; denominator `cd9daee4...da793`; root remained open `M4`. |
| Run the isolated elaboration recipe below | 0 | The exact `Statement` and conditional composition elaborated. Each `#print axioms` report contained only `propext`, `Classical.choice`, and `Quot.sound`; no branch proof was produced. |
| `rg -n -i --glob '*.lean' '\\bBilu\\b|\\bHanrot\\b|\\bVoutier\\b|\\bZsigmondy\\b|primitive[ _-]?divisor' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | All relevant hits were the owned dossier or legacy `S1_M_018`; pinned mathlib supplied no terminal BHV declaration. |
| `rg -n '\\b(sorry|admit|sorryAx|axiom|unsafe)\\b' Stage1_Instances/THM-M-0405 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited token occurs in the owned Lean sources. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `sha256sum` on statement, obligation tree, registry, anchor audit, Lake manifest, and toolchain | 0 | `db2edf61...8da1`; `d43df06f...c9b`; `85019c33...12d`; `d23923ab...cd3`; `321626c8...2d81`; `651c8acc...b1d2`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0405/proof-blocker.json >/dev/null` | 0 | The structured blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0405 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker completion manifest. |

Exact isolated elaboration recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0405
tmp=$(mktemp -d /tmp/thm-m-0405-proof-attempt.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" ObligationTree.lean
```

The pre-existing untracked `Formalizations/Lean/.lake` entry is the
automation-provided link to the canonical pinned artifacts and was not modified.
This is scoped nonrelease blocker evidence, not theorem validation or release
evidence.

## Reopen condition

Resume after placeholder-free implementations of the frozen BHV bridge and
both exact adapters, or discovery of an immutable compatible Lean 4 proof that
can be pinned, exact-type transported, and checked without changing the
dependency lock.
