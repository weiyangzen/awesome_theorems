# THM-M-0406 proof-phase recheck at `471e4458`

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `471e4458269351ee096972776c478d019941b679`

Base tree: `e30e1cefce39148420ccc4525b726d57f58ee94b`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the current pinned Lean/mathlib closure. Its model sets
`boundaryDivisor := Fin 4`, selects all four divisors, uses unit weights and
intersection numbers, makes every geometric and boundary premise true, and
sets `curve := Empty`. A proof of the root would therefore produce an
inhabitant of `Empty`.

This refutes the frozen abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically connect its
scheme, point, divisor, curve, or predicate fields. Adding a curve-existence
premise, changing `SurfaceData`, or proving a realizable specialization would
change the assigned target. `SurfaceDegeneracyEngine` in
`ObligationTree.lean` is definitionally the same refutable proposition, so its
conditional adapters provide no positive proof credit.

There is also an independent source-fidelity failure. The dossier-pinned
`math/0206100` source archive has SHA-256
`cea7fd97f089fb2d33a771dce9399a30d869e24b06fd319cb62fba26f20139de`.
Theorem 1 requires `p_i p_j (D_i . D_j) = c` for all pairs `i,j`, including
diagonal pairs, and its proof uses `D_i^2 = c / p_i^2`. The frozen
`HasTheoremOneBoundary` instead guards the equation with `D1 != D2`, omitting
every diagonal case. The source place set also includes archimedean places,
whereas `IntegralPointData.S` contains only finite places.

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The frozen obligation-tree vector remains
`[H1, M4, R3]`; the countermodel supports a fail-closed `[H1, M5, R3]`
classification, but this recheck does not promote it or modify authoritative
state. Audit and theorem completion are both false.
`.stage1-worker-selftest.json` is deliberately absent.

The generated checklist projects the obligation-tree predecessor as `[_]`,
but target-owned `task-dag.json` still records it `open`. Only the integration
lane may reconcile that predecessor-state mismatch; this proof worker does
not treat it as accepted dependency evidence.

There were already 104 `proof-recheck-*` artifacts, including 51 structured
JSON records, before this two-file packet. This exceeds the rev-5.6
five-unresolved-tick split trigger. Further identical proof scheduling cannot
progress until the upstream encoding is repaired.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency and
source fidelity. The remaining root cut set is `M0406-S-DEFINITIONS` and
`M0406-ROOT`.

Master/integration must stop identical proof retries, reopen and split at
`M0406-S-DEFINITIONS`, replace the disconnected abstract interface with a
source-faithful proposition whose intrinsic, noncircular semantics rule out
this model and include every source-required intersection case, and freeze a
new exact expression fingerprint and obligation registry. Statement,
anchor-audit, and obligation-tree gates must then be rerun before proof
execution. Merely assuming `Nonempty X.curve`, assuming the engine, or proving
a specialization is not a source-faithful repair.

## Validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. Temporary Lean objects and logs
were removed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| Read the rev-5.6 blueprint, execution skill, blueprint guidelines, target manifest, execution DAG, and target artifacts via `sed`, `rg`, and structured JSON reads | 0 | Normative prove, ownership, dependency, exact-target, blocker, split-trigger, evidence, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| Pre-write `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `471e4458...b679`, tree `e30e1cef...e94b`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; predecessor root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; root open. |
| Isolated pinned `lake env lean --trust=0 -t0` replay below | 0 | From `2026-07-15T20:18:44+08:00` to `20:19:15+08:00`, statement and proof exited 0. Both countermodel declarations reported exactly `[propext, Classical.choice, Quot.sound]`; statement/proof output and temporary olean hashes were `0f59d348...385b`, `942b7cc7...a1f8`, and `deafda33...a27`. |
| Three parallel read-only reviews, including two independent Lean replays | 0 | All confirmed the exact root is refutable; no positive terminal candidate exists in the checked local or pinned surfaces. No reviewer changed the repository. |
| Direct Lean identity, binary hash, and pinned package `HEAD`/tree checks | 0 | Lean 4.29.0 commit `98dc76e3...6740`; binary `3e0d0d3d...28bbf`; mathlib `8a178386...ea95` / `bdc39a31...e5c2b`; flt-regular `56161b6e...1a27` / `32c9eace...c893`. |
| Broad prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no `sorry`, `admit`, bodyless declaration, unsafe escape, `implemented_by`, or `native_decide` occurs. |
| Count pre-existing `proof-recheck-*` artifacts | 0 | Before this packet: `total=104 json=51 md=53`; the five-tick escalation rule has already fired. |
| `python3 -m json.tool` plus `jq -e` blocker-invariant checks on the companion record | 0 | Recorded after write: item, theorem, base, blocked state, refutation, incomplete phase, two changed paths, empty receipts, and no-selftest fields passed. |
| `git diff --no-index --check /dev/null` for each new artifact | expected 1 each | Both files differed from `/dev/null` and produced no whitespace diagnostics. |
| `git diff --check -- Stage1_Instances/THM-M-0406 .stage1-worker-selftest.json` | 0 | No whitespace errors in the assigned owned path. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists because the proof phase is blocked. |

Exact isolated replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-lake-env-head-471e4458-slot12.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/
cd "$lean_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean" >"$tmp/proof.log" 2>&1
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

The structured companion record binds source hashes, exact results,
environment pins, independent review, the countermodel, source-fidelity
failures, blocker, retry condition, and changed paths. This uniquely named
current-base packet is durable blocker evidence only. It is not a proof,
completion receipt, scheduler transition, or theorem-completion claim.
