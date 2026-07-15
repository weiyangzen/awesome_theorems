# THM-M-0406 proof-phase recheck at `9bce865a`

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the available pinned Lean/mathlib closure. Its model
sets `boundaryDivisor := Fin 4`, selects all four divisors, uses unit weights
and intersection numbers, makes every geometric and boundary premise true,
and sets `curve := Empty`. A proof of the root would therefore produce an
inhabitant of `Empty`.

This refutes the frozen abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically connect its
scheme, point, divisor, curve, or predicate fields. Adding a curve-existence
premise, changing `SurfaceData`, or proving a realizable specialization would
change the assigned target. `SurfaceDegeneracyEngine` in
`ObligationTree.lean` is definitionally the same refutable proposition, so its
conditional adapters provide no positive proof credit.

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

There were already 58 `proof-recheck-*` artifacts, including 28 structured
recheck records, before this two-file packet. This exceeds the rev-5.6
five-unresolved-tick split trigger. Further identical proof scheduling cannot
progress until the upstream encoding is repaired.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency. The
remaining root cut set is `M0406-S-DEFINITIONS` and `M0406-ROOT`.

Master/integration must stop identical proof retries, reopen and split at
`M0406-S-DEFINITIONS`, replace the disconnected abstract interface with a
source-faithful proposition whose intrinsic, noncircular semantics rule out
the checked model, and freeze a new exact expression fingerprint and
obligation registry. The exact pinned `flt-regular` checkout must also be
restored without moving revisions. Anchor-audit and obligation-tree gates
must then be rerun before proof execution. Merely assuming
`Nonempty X.curve` or the desired output is not a source-faithful repair.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, checkout repair, or intentional `.lake` mutation was
performed. Temporary Lean sources, objects, and logs were created under
`/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease blocker evidence.

The shared pinned artifacts were incomplete during this run:
`Formalizations/Lean/.lake/packages/flt-regular` had `HEAD` pointing to
`refs/heads/.invalid`, with no resolvable checkout. Consequently
`check_anchor_audit.py` failed and the bounded root `lake env` probe timed
out. Per worker policy, no fetch, clone, checkout, or repair was attempted.
The narrow countermodel check used the installed pinned Lean 4.29.0 binary
and existing compiled mathlib artifacts directly. This is real negative
kernel evidence, but not a substitute for the unavailable root Lake gate.

| Command | Exit | Exact result |
|---|---:|---|
| Read the rev-5.6 blueprint, execution skill, blueprint guidelines, target manifest, execution DAG, and target artifacts via `sed`, `rg`, and structured JSON reads | 0 | Normative prove, ownership, dependency, exact-target, blocker, escalation, evidence, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| Pre-write `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `9bce865a...1c2`, tree `523a9471...5b4`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 1 | Failed because the shared `flt-regular` checkout had no resolvable `HEAD`; no dependency provisioning was attempted. |
| `cd Formalizations/Lean && timeout --foreground 120 lake env lean --version` | 124 | The bounded root probe did not complete while `flt-regular` had no resolvable `HEAD`; the process was terminated and no `lake env` success is claimed. |
| Isolated direct pinned Lean 4.29.0 `--trust=0 -t0` replay below | 0 | From `2026-07-15T13:47:55+08:00` to `2026-07-15T13:48:03+08:00`, statement and proof exits were both 0. Both countermodel declarations reported exactly `[propext, Classical.choice, Quot.sound]`; statement/proof output and temporary olean hashes were `0f59d348...385b`, `942b7cc7...a1f8`, and `deafda33...a27`. |
| `cd Formalizations/Lean/.lake/packages/mathlib && timeout --foreground 30 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Direct Lean binary identity and hash | 0 | Lean 4.29.0, commit `98dc76e3...6740`, Release; binary SHA-256 `3e0d0d3d...28bbf`. |
| Pinned dependency `rev-parse HEAD HEAD^{tree}` checks | mixed | Mathlib passed at `8a178386...ea95` / `bdc39a31...e5c2b`; `flt-regular` failed with exit 128 because `HEAD` was unresolvable. |
| Broad prohibited-construct `rg` scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless declaration, unsafe escape, `implemented_by`, or `native_decide` occurs. |
| `python3 -m json.tool` plus `jq -e` blocker-invariant checks on the companion record | 0 | Record parsed; item, theorem, base, blocked state, refutation, incomplete phase, two changed paths, empty accepted receipts, and no-selftest fields passed. |
| `git diff --no-index --check /dev/null` for each new artifact | expected 1 each | Each status denotes new content; both diagnostic streams were empty, so neither artifact has a whitespace error. |
| `git diff --check -- Stage1_Instances/THM-M-0406 .stage1-worker-selftest.json` | 0 | No whitespace errors reported; explicit no-index checks covered both untracked evidence artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists because the positive proof phase is blocked. |

Exact isolated replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head-9bce865a-slot8-direct.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  test -d "$p" && paths+=("$p")
done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/
cd "$tmp"
start=$(TZ=Asia/Shanghai date --iso-8601=seconds)
set +e
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" Statement.lean \
  >statement.log 2>&1
statement_exit=$?
if test "$statement_exit" -eq 0; then
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" \
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
| statement output | `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b` |
| proof output | `942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8` |
| temporary `Statement.olean` | `deafda332045568236e3354ba2870233cfdfd906e0105c9eb67b8fc575004a27` |

The structured companion record binds source hashes, exact results,
environment pins and missing artifacts, the countermodel, the blocker, the
retry condition, and changed paths. This uniquely named current-base report
is durable blocker evidence only.
