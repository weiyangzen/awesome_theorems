# THM-M-1045 proof phase: current-base blocker

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision: `3b741f76df83670ba151a8f6ad6257bb8b6f6ead`

Base tree: `021c27ee3fae960d30f31e7f932f29401412edb0`

Rechecked: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body was implemented for the exact frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`, and the proof item remains
`[ ]`. A root `.stage1-worker-selftest.json` is deliberately absent.

The frozen `WienerData.paleyWienerIntegral` field is constrained only by
measurability, but the target quantifies over every `WienerData` and demands
the exact Radon-Nikodym density for that field. The placeholder-free
`ProofBlockerCurrent.lean` preserves every Wiener-law field while replacing
the pairing by the measurable constant-one map. At the zero direction, the
target then forces the self Radon-Nikodym derivative to equal
`ENNReal.ofReal (Real.exp 1)` almost everywhere. `Measure.rnDeriv_self` makes
the same derivative equal one, and the probability-measure instance makes the
almost-everywhere filter nontrivial. Lean therefore checks:

```text
Stage1Instances.THM_M_1045.no_target_of_wienerData
  (W : WienerData) : Not CameronMartinTarget
```

This is conditional on a supplied `W : WienerData`; this phase does not claim
an independently constructed inhabitant. It nevertheless proves that the
frozen interface cannot state the intended theorem for any advertised Wiener
datum. It refutes only this overbroad Lean encoding, not the mathematical
Cameron-Martin theorem.

The fail-closed classification proposed for the frozen formal candidate is
`[H1, M3, R3] -> [H1, M5, R3]`, subject to master reconciliation. No
predecessor authority was edited, so the structured registry still truthfully
records the pre-proof vector and the root remains open.

## First Failed Gate

Exact-target consistency fails at the statement-level
`M1045-S-DEFINITIONS` boundary: the target requires a density formula for a
Paley-Wiener field constrained only by measurability. This invalidates the
planned `M1045-L-PALEY-WIENER` construction and blocks `M1045-B-DENSITY` and
`M1045-ROOT`. Separately, `S56-M-1045-OBLIGATION_TREE` remains
worker-provisional `[_]`, so dependency-ordered master acceptance also remains
outstanding; rev-5.6 concurrency still permits this provisional proof audit.

Positive proof work can resume only after the statement phase either
constructs the Paley-Wiener integral from the pinned Wiener model or adds
source-justified, noncircular isometry, Gaussian-law, linearity, and
compatibility laws that rule out the constant-one replacement. That repair
changes the canonical fingerprint, so the statement, anchor audit, obligation
registry, and typed graphs must be rerun and accepted in dependency order.

## Scoped Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was
reused read-only. No Lake update/build, dependency fetch/clone, or `.lake`
mutation was performed. Temporary Lean output was written under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at L0/rework-required passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238; planned hard-mathlib anchor/wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 0 | Exact expression fingerprint `e1b35bb7...5cea`; all four recorded mutations were distinguished. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Target fingerprint, ten support probes, candidate inventory, and mathlib pin agree. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; denominator `4f4276a1...a08e3`; root remains open at M3. |
| Isolated pinned Lean recipe below | 0 | `Statement.lean` and `ProofBlockerCurrent.lean` elaborated with `--trust=0 -t0`; `no_target_of_wienerData` reports exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in the checked Lean source. |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No tracked-diff whitespace error. |
| `git diff --no-index --check /dev/null <each new artifact>` | 1 expected | Each file differs from `/dev/null`; empty diagnostic output means no whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/proof-blocker-head-3b741f76-2026-07-15.json` | 0 | The structured blocker packet parsed successfully. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-slot41.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean_bin" \
  --trust=0 -t0 ProofBlockerCurrent.lean
```

Exact prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean
```

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This packet is fresh current-base negative kernel evidence only. It supplies
no positive root proof credit and makes no provisional-state, audit-completion,
validation, release, theorem-completion, or master-acceptance claim.
