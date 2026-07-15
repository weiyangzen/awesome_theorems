# THM-M-0406 proof blocker handoff at `4c391099`

Item: `S56-M-0406-PROOF`

Recorded: `2026-07-15T19:11:20+08:00` (Asia/Shanghai)

Base revision: `4c391099fc585eb02188ea57450990b3af042aab`

Base tree: `f96bc1a1b7c35e476a2e6191def82f8c33458e3c`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks under the pinned closure with `--trust=0`. Its model uses
`boundaryDivisor := Fin 4`, all four components, unit weights and intersection
numbers, true geometric premises, and `curve := Empty`. Every frozen premise
holds, but the conclusion would produce an inhabitant of `Empty`.

This refutes the disconnected abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData.curve` is an arbitrary type unrelated to
the supplied scheme and curve predicates, while the root quantifies over every
such structure and requires `Exists C : X.curve`. `SurfaceDegeneracyEngine` is
definitionally the same refutable proposition; its conditional adapters supply
no proof body.

The frozen statement also has an independent source-fidelity defect. The
pinned `math/0206100` source (SHA-256
`cea7fd97f089fb2d33a771dce9399a30d869e24b06fd319cb62fba26f20139de`)
states `p_i p_j (D_i . D_j) = c` for all pairs `i,j`, including diagonal
pairs, and its proof uses `D_i^2 = c / p_i^2`. The Lean definition instead
requires the equation only for distinct divisors. Its schemes, points,
divisors, curves, rationality, and integrality predicates are otherwise
independent fields rather than intrinsic geometric objects.

No proof body or receipt was added, no obligation was closed, and the item
remains `[ ]`. The authoritative vector remains `[H1, M4, R3]`; the checked
negative evidence supports only a fail-closed `[H1, M5, R3]` proposal. Audit
and theorem completion remain false, and `.stage1-worker-selftest.json` is
deliberately absent.

The blueprint projects the obligation-tree predecessor as worker-provisional
`[_]`, while target-owned `task-dag.json` still records it `open`. This proof
worker cannot accept or reconcile that dependency. There were already 94
`proof-recheck-*` artifacts before this handoff. The five-unresolved-tick split
trigger has long fired; this current-base record is durable blocker evidence,
not a claim that another identical retry made proof progress.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency and
source fidelity. The remaining root cut set is `M0406-S-DEFINITIONS` and
`M0406-ROOT`.

Master/integration must stop identical retries, reopen and split at
`M0406-S-DEFINITIONS`, and authorize a source-faithful proposition whose
intrinsic, noncircular geometric semantics rule out the checked model and
include every source-required intersection case. It must then freeze a new
exact expression and obligation registry and rerun statement, anchor-audit,
and obligation-tree gates. Adding only `Nonempty X.curve`, assuming the proof
engine, or proving a realizable specialization would substitute the theorem.

## Validation

All commands ran in this worker clone. The existing canonical pinned Lake
artifacts were reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout, network access, or intentional `.lake` mutation was
performed. Temporary Lean sources, objects, and logs were written under
`/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| Read the rev-5.6 blueprint, execution skill, blueprint guidelines, target manifest/DAG entries, and target artifacts | 0 | Ownership, dependency, exact-target, proof, blocker, split-trigger, evidence, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| Pre-write `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `4c391099...2aab`, tree `f96bc1a1...e3c`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; root open. |
| Isolated pinned `lake env lean --trust=0 -t0` replay below | 0 | From `2026-07-15T19:10:53+08:00` to `19:11:05+08:00`, statement and proof exited 0. Both countermodel declarations reported exactly `[propext, Classical.choice, Quot.sound]`; statement/proof output and temporary olean hashes were `0f59d348...385b`, `942b7cc7...a1f8`, and `deafda33...a27`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Pinned package `HEAD`/tree and toolchain/manifest checks | 0 | mathlib `8a178386...ea95` / `bdc39a31...e5c2b`; flt-regular `56161b6e...1a27` / `32c9eace...c893`; toolchain `651c8acc...b1d2`; manifest `321626c8...2d81`. |
| Broad prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no `sorry`, `admit`, bodyless declaration, unsafe escape, `implemented_by`, or `native_decide` occurs. |
| Structured record parse, invariant checks, `git diff --check`, and `test ! -e .stage1-worker-selftest.json` | recorded after write | Companion JSON parsed; blocker, incompleteness, ownership, and no-selftest invariants passed; no whitespace errors. |

Exact isolated replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head-4c391099-slot6.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" Statement.lean \
  >statement.log 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" \
  --trust=0 -t0 --root="$tmp" Proof.lean >proof.log 2>&1
```

Current input and output hashes:

| Input or output | SHA-256 |
|---|---|
| `Statement.lean` | `9d6e2a94131455eedcee2ae75765746958988f23f6398cc5c4ea3fbc193258ec` |
| `ObligationTree.lean` | `bbcd4865cc660a210b104c50e19d5ca66055dacdab07182f6d4693c096f3f02c` |
| `Proof.lean` | `afeb346ab8f1ff9e41b87395744faa7a352509d28ef842f10f18a3ec00874aaf` |
| `obligation-registry.json` | `90d988ef727c9f1cbe99cfffb73c21b05f32f6d0b61a2177b624217cfb4612b6` |
| `typed-graphs.json` | `f4da55995c5413f92314904e9687721153b52e7d1d1e1e27fe551f0d7333da17` |
| `anchor-audit.json` | `8e0f84a533e183b8b70ef48955d9fa2dc8dbf39274f4345c600c8f2c143cfd21` |
| `task-dag.json` | `e9888fdc413651364b476cea0d55cad197eddd433d1a2a818b23f1da3093c2f6` |
| statement output | `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b` |
| proof output | `942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8` |
| temporary `Statement.olean` | `deafda332045568236e3354ba2870233cfdfd906e0105c9eb67b8fc575004a27` |
| resolved Lean binary | `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf` |

The structured companion binds the current base, exact inputs, environment
pins, kernel result, blocker, retry condition, and status boundary. This
handoff is not a proof receipt, state transition, or completion claim.
