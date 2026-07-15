# THM-M-0406 proof-phase recheck at `9d50d838`

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `9d50d838c8132b2aaf005a4863baeb5385e52a97`

Base tree: `ef268baf236c1fe55806a57847c7f78ed6587b9d`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the pinned Lean and mathlib closure. Its model sets
`boundaryDivisor := Fin 4`, selects all four divisors, uses unit weights and
intersection numbers, makes every geometric and boundary premise true, and
sets `curve := Empty`. A proof of the root would therefore produce an
inhabitant of `Empty`.

A separately implemented temporary countermodel also kernel-checks. It uses
the inhabited curve type `Bool` but sets `isProperCurve := False`; the root
would then produce a proof of `False`. This also establishes that merely
adding `Nonempty X.curve` cannot repair the encoding.

These models refute the frozen abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically connect its
scheme, point, divisor, curve, or predicate fields. Changing `SurfaceData`,
adding output-producing premises, or proving a realizable specialization
would change the assigned target. `SurfaceDegeneracyEngine` is definitionally
the same refutable proposition, so its conditional adapters provide no
positive proof credit.

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The frozen vector remains `[H1, M4, R3]`; the countermodels
support a fail-closed `[H1, M5, R3]` classification for master reconciliation,
but this worker does not promote state. Audit and theorem completion are both
false. `.stage1-worker-selftest.json` is deliberately absent.

The authoritative DAG projects the obligation-tree predecessor as worker-
provisional `[_]`, while target-owned `task-dag.json` still records it `open`.
Only the integration lane may resolve that predecessor-state mismatch.

There were already 68 `proof-recheck-*` artifacts, including 33 JSON records,
before this packet. That exceeds the five-unresolved-tick split trigger.
Master/integration must stop identical proof retries and reopen the failed
definition/statement gate.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency.
The remaining root cut set is `M0406-S-DEFINITIONS` and `M0406-ROOT`.

Retry only after master/integration authorizes an intrinsic, source-faithful
geometric encoding that rules out both checked countermodels, accepts a new
statement fingerprint and obligation registry, and reruns the statement,
anchor-audit, and obligation-tree gates. Assuming `Nonempty X.curve` or the
desired conclusion is not a source-faithful repair.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, checkout change, or intentional `.lake` mutation was
performed. Temporary Lean sources, objects, and logs were created under
`/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` link makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| Read the rev-5.6 blueprint, execution skill, blueprint guidelines, target manifest, execution DAG, and target artifacts with `sed`, `rg`, `jq`, and structured JSON reads | 0 | Prove, ownership, dependency, exact-target, blocker, five-tick split, evidence, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| Pre-write `git status --short`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `9d50d838...2a97`, tree `ef268baf...b9d`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | 14 obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; root open. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...6740`, Release. |
| Isolated `lake env` Lean `--trust=0 -t0` replay of temporary `Statement.lean` and `Proof.lean` copies | 0 | From `2026-07-15T15:17:48+08:00` to `15:18:07+08:00`, both exits were 0. Both countermodel declarations reported exactly `[propext, Classical.choice, Quot.sound]`; output/olean hashes were `0f59d348...385b`, `942b7cc7...a1f8`, and `deafda33...a27`. |
| Independent temporary countermodel with `curve := Bool` and `isProperCurve := False`, using the same pinned trust-0 closure | 0 | It elaborated and both declarations reported `[propext, Classical.choice, Quot.sound]`; source/output hashes were `547ab52a...c1e0` and `3493046c...04c9`. |
| `git -C Formalizations/Lean/.lake/packages/{mathlib,flt-regular} rev-parse HEAD HEAD^{tree}` (run separately) | 0 | Mathlib is `8a178386...ea95` / `bdc39a31...e5c2b`; flt-regular is `56161b6e...1a27` / `32c9eace...c893`. |
| Broad prohibited-construct `rg` scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless declaration, unsafe escape, `implemented_by`, or `native_decide` occurs. |
| `python3 -m json.tool`, `jq -e` blocker-invariant checks, and Markdown marker scan | 0 | The record parsed; item, theorem, base, blocked/incomplete/no-selftest fields passed; the target ID and literal `blocked` marker were present. |
| `git diff --no-index --check /dev/null` for each new artifact | expected 1 each | Both statuses represented new content and both diagnostic streams were empty. |
| `git diff --check -- Stage1_Instances/THM-M-0406 .stage1-worker-selftest.json` | 0 | No whitespace errors; explicit no-index checks covered the untracked artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists because the proof phase is incomplete. |

## Exact kernel replay

Run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head-9d50d838-slot32.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 --root="$tmp" -o Statement.olean Statement.lean \
  >statement.log 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 --root="$tmp" Proof.lean >proof.log 2>&1
sed -n '1,240p' statement.log
sed -n '1,240p' proof.log
sha256sum statement.log proof.log Statement.olean
```

## Input and output hashes

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
| independent countermodel source | `547ab52a8ba749d17915b57618eef7cbb7bc76c4a5fabae9835b2ba8af7ec1e0` |
| independent countermodel output | `3493046c0b34fa54cd81496f0a61ddb4eb1540249c3e8723ba2734c3d44304c9` |

The companion JSON binds the exact current base, target inputs, environment,
commands, results, failed gate, retry condition, and changed paths. This is
durable blocker evidence only, not a proof or completion receipt.
