# THM-M-0406 proof-phase recheck at `5b35bc15`

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `5b35bc151522d93c7f54966ef64f1fc630371537`

Base tree: `fe77824631ab2573a4596bddc1a2534c06cd23f8`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the pinned Lean dependency closure. Its model sets
`boundaryDivisor := Fin 4`, selects all four divisors, uses unit weights and
intersection numbers, makes every required premise true, and sets
`curve := Empty`. Every frozen premise is satisfied, but the root conclusion
would produce an inhabitant of `Empty`.

This countermodel refutes the frozen abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically connect its
scheme, point, divisor, curve, or predicate fields. Changing that structure,
adding output-producing premises, or proving a realizable specialization
would change the assigned target. `SurfaceDegeneracyEngine` in
`ObligationTree.lean` is definitionally the same refutable proposition, so
its conditional adapters provide no positive proof credit.

There is also an independent source-fidelity failure. The immutable
`math/0206100` source archive, whose SHA-256 is the dossier-pinned
`cea7fd97f089fb2d33a771dce9399a30d869e24b06fd319cb62fba26f20139de`,
states at source lines 124-133 that
`p_i p_j (D_i . D_j) = c` holds for all pairs `i,j`. Its proof at lines
1038-1051 explicitly uses the diagonal identity `D_i^2 = c / p_i^2`.
`HasTheoremOneBoundary` instead guards the equation by `D1 != D2`, omitting
every diagonal case and materially weakening the purported transcription.
The source concludes that there is a curve on `X`; the Lean target separately
requires an arbitrary, disconnected `isProperCurve` predicate.

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The frozen obligation-tree vector remains
`[H1, M4, R3]`; the negative evidence supports a fail-closed
`[H1, M5, R3]` classification, but this worker does not promote it or modify
authoritative state. Audit and theorem completion are both false.
`.stage1-worker-selftest.json` is deliberately absent.

The generated checklist projects the obligation-tree predecessor as `[_]`,
but target-owned `task-dag.json` still records it `open`. Only integration may
reconcile that mismatch. There were already 74 `proof-recheck-*` artifacts,
including 36 JSON records, before this packet. This exceeds the five-tick
split trigger; identical proof retries cannot progress without upstream
repair.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency and
source fidelity. The remaining root cut set is `M0406-S-DEFINITIONS` and
`M0406-ROOT`.

Master/integration must stop identical proof retries, reopen and split at
`M0406-S-DEFINITIONS`, and replace the disconnected encoding with a
source-faithful proposition whose intrinsic, noncircular geometric semantics
rule out the countermodel and include every source-required intersection
case. It must then freeze a new exact expression and obligation registry and
rerun statement, anchor-audit, and obligation-tree gates. Adding
`Nonempty X.curve` or assuming the desired output is not a source-faithful
repair.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or intentional `.lake` mutation was
performed. Temporary Lean sources, objects, and logs were created under
`/tmp`; they were removed after recording hashes. The automation-provided
untracked `Formalizations/Lean/.lake` link makes this nonrelease blocker
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| Read the rev-5.6 blueprint, execution skill, blueprint guidelines, target manifest, execution DAG, and target artifacts via `sed`, `rg`, and structured JSON reads | 0 | Prove, ownership, dependency, exact-target, blocker, split-trigger, evidence, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| Pre-write `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `5b35bc15...1537`, tree `fe778246...23f8`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; predecessor root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; root open. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Isolated pinned Lean `--trust=0 -t0` replay below | 0 | From `2026-07-15T15:55:35+08:00` to `15:55:53+08:00`, statement and proof exits were both 0. Both countermodel declarations reported exactly `[propext, Classical.choice, Quot.sound]`; statement/proof output and temporary olean hashes were `0f59d348...385b`, `942b7cc7...a1f8`, and `deafda33...a27`. |
| Lean binary, toolchain/manifest, and dependency identity checks | 0 | Binary `3e0d0d3d...28bbf`; toolchain `651c8acc...b1d2`; manifest `321626c8...2d81`; mathlib `8a178386...ea95` / `bdc39a31...e5c2b`; flt-regular `56161b6e...1a27` / `32c9eace...c893`. |
| Exact topic search over pinned mathlib | 1 | Expected no-match result; no Corvaja--Zannier, arithmetic Subspace Theorem, or surface-integral-point terminal theorem was found. |
| Inspect pinned primary-source archive and its theorem/proof lines | 0 | Archive hash matched `cea7fd97...139de`; source requires all pairs including diagonal cases, which the Lean statement omits. |
| Broad prohibited-construct `rg` scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless declaration, unsafe escape, `implemented_by`, or `native_decide` occurs. |
| Count pre-existing `proof-recheck-*` artifacts | 0 | `total=74 json=36 md=38`; the five-tick escalation rule has already fired. |
| Final companion JSON parsing, invariants, and whitespace checks | not embedded | No self-referential final-byte claim is recorded; integration must independently check this two-file blocker packet. |

Exact isolated replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head-5b35bc15-slot53.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/
cd "$tmp"
start=$(TZ=Asia/Shanghai date --iso-8601=seconds)
set +e
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 --root="$tmp" -o Statement.olean Statement.lean \
  >statement.log 2>&1
statement_exit=$?
if test "$statement_exit" -eq 0; then
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
    --trust=0 -t0 --root="$tmp" Proof.lean >proof.log 2>&1
  proof_exit=$?
else
  proof_exit=125
  : >proof.log
fi
set -e
end=$(TZ=Asia/Shanghai date --iso-8601=seconds)
sed -n '1,240p' statement.log
sed -n '1,240p' proof.log
printf 'started_at=%s\nended_at=%s\nstatement_exit=%s\nproof_exit=%s\n' \
  "$start" "$end" "$statement_exit" "$proof_exit"
sha256sum statement.log proof.log Statement.olean
test "$statement_exit" -eq 0
test "$proof_exit" -eq 0
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

The companion JSON binds the exact base, target inputs, environment, source
mismatch, commands, results, failed gate, retry condition, and changed paths.
This is durable blocker evidence only, not a proof or completion receipt.
