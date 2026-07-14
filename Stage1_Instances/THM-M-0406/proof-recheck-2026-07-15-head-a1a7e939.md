# THM-M-0406 proof-phase recheck at current base

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the current pinned closure. Its model sets
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

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The frozen obligation-tree vector remains
`[H1, M4, R3]`; the countermodel supports a fail-closed `[H1, M5, R3]`
classification, but this recheck does not promote it or modify authoritative
state. Audit and theorem completion are both false.
`.stage1-worker-selftest.json` is deliberately absent.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency. The
remaining root cut set is `M0406-S-DEFINITIONS` and `M0406-ROOT`.

Retry only after reopening statement and obligation-tree gates, replacing the
disconnected abstract interface with a source-faithful proposition whose
intrinsic, noncircular semantics rule out this model, and freezing a new exact
expression fingerprint and obligation registry. Merely assuming
`Nonempty X.curve` or the desired output is not a source-faithful repair.

## Validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. Temporary Lean sources, objects,
and logs were created under `/tmp` and removed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink makes this nonrelease blocker
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | 14 obligations and 26 typed edges passed; denominator `46deb9e278a5e0383923334b032877af6743372ba6cafa2fd0d03a569d1d90a7`; predecessor root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; root open. |
| Isolated pinned `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and countermodel elaborated. Both countermodel declarations reported exactly `[propext, Classical.choice, Quot.sound]`; statement/proof output SHA-256 values were `0f59d348...385b` and `942b7cc7...a1f8`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Pinned dependency `rev-parse HEAD HEAD^{tree}` checks | 0 | mathlib `8a178386...ea95` / `bdc39a31...e5c2b`; flt-regular `56161b6e...1a27` / `32c9eace...893`. |
| Prohibited-construct `rg` scan over owned Lean files | 1 | Expected no-match exit; no prohibited proof escape occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/proof-recheck-2026-07-15-head-a1a7e939.json >/dev/null` | 0 | The fresh structured blocker record parsed. |
| `git diff --no-index --check /dev/null <each new owned artifact>` | 1 each | Expected content-difference status with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists because the proof phase is incomplete. |

Exact isolated replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head-a1a7e939.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" Statement.lean \
  >statement.log 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
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
| statement output | `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b` |
| proof output | `942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8` |
| temporary `Statement.olean` | `deafda332045568236e3354ba2870233cfdfd906e0105c9eb67b8fc575004a27` |

The structured companion record binds source hashes, exact results,
environment pins, the blocker, the retry condition, and changed paths. This
uniquely named current-base report is durable blocker evidence only.
