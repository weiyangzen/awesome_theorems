# THM-M-0406 proof-phase recheck at `c15c6495`

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `c15c649568664c4e58150dd755cb28f156d15ecb`

Base tree: `792c3ed97f9263da7e6a39abdce8d5e37a100368`

## Verdict

`blocked`. A consistent positive proof body cannot be implemented for the
exact frozen Lean proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the current pinned Lean closure. Its model uses
`boundaryDivisor := Fin 4`, all four components, unit weights and intersection
numbers, true geometric premises, and `curve := Empty`. Thus every frozen
premise holds while the conclusion would produce an inhabitant of `Empty`.

This refutes the disconnected abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically relate its
scheme, curve, point, divisor, or predicate fields. The
`SurfaceDegeneracyEngine` in `ObligationTree.lean` is definitionally the same
refutable proposition; its conditional adapters add no positive proof body.

There is also an independent source-fidelity failure. The dossier-pinned
`math/0206100` archive has SHA-256
`cea7fd97f089fb2d33a771dce9399a30d869e24b06fd319cb62fba26f20139de`.
Its Theorem 1 at source lines 124-133 requires
`p_i p_j (D_i . D_j) = c` for all pairs `i,j`. The proof at lines 1038-1051
uses the diagonal identity `D_i^2 = c / p_i^2`. The frozen
`HasTheoremOneBoundary` instead requires the equality only after `D1 != D2`,
so it omits every diagonal case and materially broadens the transcription.

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The frozen vector remains `[H1, M4, R3]`; the checked
negative evidence supports a fail-closed `[H1, M5, R3]` proposal, but this
worker does not modify authority or promote state. Audit and theorem
completion are false. `.stage1-worker-selftest.json` is deliberately absent.

The blueprint projects the obligation-tree predecessor as worker-provisional
`[_]`, while target-owned `task-dag.json` still records it `open`; this worker
cannot accept that dependency. There were already 76 `proof-recheck-*`
artifacts, including 37 JSON records, before this packet. The five-unresolved-
tick split trigger has long fired, so another identical proof retry cannot
progress without upstream repair.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency and
source fidelity. The remaining root cut set is `M0406-S-DEFINITIONS` and
`M0406-ROOT`.

Master/integration must stop identical proof retries, reopen and split at
`M0406-S-DEFINITIONS`, and authorize a source-faithful proposition whose
intrinsic, noncircular geometric semantics rule out the checked model and
include all source-required intersection cases. It must then freeze a new
exact expression and obligation registry and rerun statement, anchor-audit,
and obligation-tree gates. Adding only `Nonempty X.curve`, assuming the proof
engine, or proving a realizable specialization would substitute the target.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or intentional `.lake` mutation was
performed. Temporary Lean sources and objects were written under `/tmp`. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this
nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| Read `Docs/Stage1_Blueprint_rev-5.6.md`, `skills/execute-stage1-rev56/SKILL.md`, the manifest/DAG entry, and target artifacts | 0 | Ownership, dependency, exact-target, proof, blocker, split-trigger, validation, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| Pre-write `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `c15c6495...5ecb`, tree `792c3ed9...0368`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; root open. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | Statement/proof exits were both 0. Both countermodel theorems reported exactly `[propext, Classical.choice, Quot.sound]`; output/olean hashes were `0f59d348...385b`, `942b7cc7...a1f8`, and `deafda33...a27`. The same results were independently reproduced with the resolved binary from `2026-07-15T16:17:07+08:00` to `16:17:29+08:00`. |
| Lean binary, toolchain/manifest, and dependency identity checks | 0 | Lean 4.29.0 commit `98dc76e3...6740`; binary `3e0d0d3d...28bbf`; mathlib `8a178386...ea95` / `bdc39a31...e5c2b`; flt-regular `56161b6e...1a27` / `32c9eace...c893`. |
| `rg` exact Corvaja/Zannier/Subspace-Theorem and surface-integral-point terms in pinned Mathlib | 1 | Expected no-match exit; no applicable terminal theorem was found. |
| `sha256sum /tmp/math0206100.tar`; inspect source lines 124-133 and 1038-1051 | 0 | Archive matched `cea7fd97...139de`; source requires all pairs and explicitly uses diagonal self-intersections. |
| Broad prohibited-construct `rg` scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless declaration, unsafe escape, `implemented_by`, or `native_decide` occurs. |
| Count pre-existing `proof-recheck-*` artifacts | 0 | Before this packet: `total=76 json=37 md=39`; the five-tick escalation rule has fired. |
| Final JSON parsing, packet invariants, whitespace checks, and self-test absence | recorded after write | See the structured companion record for exact commands and results. |

Exact isolated replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head-c15c6495-slot2.XXXXXX)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/
cd "$lean_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean" \
  >"$tmp/proof.log" 2>&1
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

This current-base packet is durable blocker evidence only. It is not a proof,
completion receipt, scheduler transition, or theorem-completion claim.
