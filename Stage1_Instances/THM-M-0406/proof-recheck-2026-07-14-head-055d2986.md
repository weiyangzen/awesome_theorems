# THM-M-0406 proof-phase recheck at current base

Item: `S56-M-0406-PROOF`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `055d2986f15165228f00094a7de24a77795055a2`  
Base tree: `0fced52df7813bdc38ea71f4d649a788bb895512`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the current pinned closure. Its model sets
`boundaryDivisor := Fin 4`, uses all four divisors with unit weights and unit
intersection numbers, makes every geometric and boundary premise true, and
sets `curve := Empty`. The requested conclusion would therefore produce an
element of `Empty`.

This is a countermodel to the frozen abstract encoding, not to the mathematical
Corvaja--Zannier theorem. The encoding does not intrinsically connect its
scheme, point, divisor, curve, or predicate fields. Adding a curve-existence
premise, changing `SurfaceData`, or proving only a realizable specialization
would change or substitute the assigned target. `SurfaceDegeneracyEngine` in
`ObligationTree.lean` is definitionally the same refutable proposition, so its
conditional adapters cannot provide positive proof credit.

No proof body or receipt was added, no frozen obligation was closed, and the
proof item remains `[ ]`. The checked countermodel supports the existing M5
exact-target-mismatch classification, but it does not satisfy this proof
deliverable, audit completion, validation, release, theorem completion, or
master acceptance. `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency. The
remaining root cut set is `M0406-S-DEFINITIONS` and `M0406-ROOT`.

Retry only after reopening the statement and obligation-tree gates, replacing
the disconnected abstract interface with a source-faithful proposition whose
intrinsic, noncircular semantics rule out this model, and freezing a new exact
expression fingerprint and obligation registry. Merely assuming
`Nonempty X.curve` or the desired output is not a source-faithful repair.

## Validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. No Lake update/build, dependency clone/fetch, or `.lake` mutation
was performed. Temporary Lean objects and logs were created under `/tmp` and
removed. The automation-provided untracked `Formalizations/Lean/.lake` symlink
makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | 14 obligations and 26 typed edges passed; denominator `46deb9e278a5e0383923334b032877af6743372ba6cafa2fd0d03a569d1d90a7`; predecessor graph still reports root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; no proof-bearing root candidate exists. |
| Isolated `lake env lean` recipe below | 0 | The exact statement and countermodel elaborated. Both countermodel declarations reported exactly `[propext, Classical.choice, Quot.sound]`. Statement-output SHA-256: `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b`; proof-output SHA-256: `942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `rg -n '\\b(sorry|admit|sorryAx)\\b|^[[:space:]]*axiom\\b|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-0406 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited declaration or proof escape occurs in the owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/proof-blocker.json >/dev/null` | 0 | The structured blocker record parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0406` | 0 | No whitespace errors in the owned-path delta. |
| `git status --short` | 0 | Only the automation-provided `Formalizations/Lean/.lake` symlink and this uniquely named owned blocker report are untracked. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" -t 0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" -t 0 Proof.lean
```

The current input SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `9d6e2a94131455eedcee2ae75765746958988f23f6398cc5c4ea3fbc193258ec` |
| `ObligationTree.lean` | `bbcd4865cc660a210b104c50e19d5ca66055dacdab07182f6d4693c096f3f02c` |
| `obligation-registry.json` | `90d988ef727c9f1cbe99cfffb73c21b05f32f6d0b61a2177b624217cfb4612b6` |
| `typed-graphs.json` | `f4da55995c5413f92314904e9687721153b52e7d1d1e1e27fe551f0d7333da17` |
| `anchor-audit.json` | `8e0f84a533e183b8b70ef48955d9fa2dc8dbf39274f4345c600c8f2c143cfd21` |
| `Proof.lean` | `afeb346ab8f1ff9e41b87395744faa7a352509d28ef842f10f18a3ec00874aaf` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This uniquely named report records the current-base retry without overwriting
the integrated historical blocker. It is durable blocker evidence only.
