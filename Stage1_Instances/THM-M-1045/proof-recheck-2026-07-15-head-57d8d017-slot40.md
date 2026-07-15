# THM-M-1045 proof phase: current-base recheck

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision: `57d8d01796f84ffc9de9adf1f5d0723555e7babb`

Base tree: `cdea5b3fad713816ee6c9ed6aae7a10f9009a18e`

Rechecked: `2026-07-15T13:20:49+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible positive proof body can establish the exact frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`, and no root
`.stage1-worker-selftest.json` is written.

`WienerData.paleyWienerIntegral` has only a measurability requirement, while the root quantifies
over every `WienerData` and requires the exact Radon-Nikodym density for that field. The checked
`ProofBlockerCurrent.lean` changes only this field to the measurable constant-one pairing. At
`h = 0` and `g = 0`, the target makes the self Radon-Nikodym derivative equal
`ENNReal.ofReal (Real.exp 1)` almost everywhere; `Measure.rnDeriv_self` makes it equal one.
Probability nontriviality and `1 < exp 1` give the contradiction.

The integrated characterization checks:

```text
Stage1Instances.THM_M_1045.target_iff_isEmpty_wienerData :
  CameronMartinTarget iff IsEmpty WienerData
```

The reverse implication is empty elimination. Using it as a positive root proof would be vacuous
and would substitute an interface-emptiness result for the mathematical Cameron-Martin theorem.
The fail-closed vector proposed for master reconciliation is `[H1, M3, R3] -> [H1, M5, R3]`.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`. The unconstrained pairing invalidates
`M1045-L-PALEY-WIENER`, blocking `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
Separately, `S56-M-1045-OBLIGATION_TREE` remains worker-provisional `[_]`, so dependency-ordered
master acceptance is outstanding.

Two further statement risks remain. The path measurable-space definition comaps `top` rather than
establishing the claimed cylinder or Borel sigma-algebra. Also, `timeMeasure` maps all real volume
through `Real.toNNReal`, collapsing the negative half-line to zero rather than selecting ordinary
volume on `NNReal`.

Positive proof work can resume only after a source-justified statement repair constrains or
constructs the Paley-Wiener integral without assuming the desired conclusion, corrects or justifies
the path and time measures, publishes a fresh target fingerprint, and refreezes the anchor audit and
version-2 obligation graphs.

Six prior blocker/recheck packets predate this run, but the authoritative DAG records zero attempts
and no children. Packet count alone does not establish five scheduler execution ticks, so this
worker makes no split-required claim and did not edit that authority. Because the first failed gate
is the predecessor statement rather than a divisible proof leaf, the master should reopen the
statement dependency instead of scheduling another unchanged proof-root attempt.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation ran. Lean object output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at L0/rework-required passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238, planned, legacy artifacts unaccepted, theorem incomplete. |
| `timeout --foreground 600 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 1 | `lake env` could not resolve the shared `flt-regular` checkout's `HEAD`; no repair or fetch was attempted. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Target fingerprint, ten Lean probes, candidate inventory, and mathlib pin agreed. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains open at M3. |
| Direct isolated pinned Lean recipe below | 0 | Statement, blocker, characterization, and conditional composer elaborated with `--trust=0 -t0`; all three printed theorem bodies depend exactly on `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in the three checked proof-related sources. |
| Exact material-delta command below from `dafb8b51` to current HEAD | 0 | No material target source, registry, graph, validation-spec, lockfile, or toolchain delta; only the previous blocker pair was added. |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-57d8d017-slot40.json` | 0 | Structured blocker packet parsed successfully. |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No tracked-diff whitespace errors. |
| Two exact `git diff --no-index --check` commands below | 1 expected each | Each file differs from `/dev/null`; empty diagnostics mean no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-57d8d017-slot40.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for package_path in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  lean_path="$lean_path:$package_path"
done
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean \
  >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/ProofBlockerCurrent.olean" ProofBlockerCurrent.lean \
  >"$tmp/blocker.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/ProofBlockerCharacterization.olean" \
  ProofBlockerCharacterizationHead443b8bbcSlot38.lean \
  >"$tmp/characterization.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean \
  >"$tmp/obligation.log" 2>&1
cat "$tmp/statement.log" "$tmp/blocker.log" \
  "$tmp/characterization.log" "$tmp/obligation.log"
sha256sum "$tmp/statement.log" "$tmp/blocker.log" \
  "$tmp/characterization.log" "$tmp/obligation.log" \
  "$tmp/Statement.olean" "$tmp/ProofBlockerCurrent.olean" \
  "$tmp/ProofBlockerCharacterization.olean" "$tmp/ObligationTree.olean"
```

The statement, blocker, characterization, and conditional-composer log SHA-256 values are
respectively `4adb258a91317991276961bad1d03712638888a5a2af84a12240a92e12a8b110`,
`55dcd476292f394eca6e28e17cf180ad4d1773f6601d84fed4adcc8284a58964`,
`38cd8fdac134d193c3293524684a66c80023fb7d9ab84740f0ad23aeb7bfde95`, and
`8f9246d00cd8e9461675b69ca071323c2818448bedf026cdf27fbaaac2b43737`.

Exact prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean \
  Stage1_Instances/THM-M-1045/ProofBlockerCharacterizationHead443b8bbcSlot38.lean \
  Stage1_Instances/THM-M-1045/ObligationTree.lean
```

Exact material-delta command:

```bash
git diff --quiet \
  dafb8b51c4561eee5fcf162a8d5ee49555584bdb..57d8d01796f84ffc9de9adf1f5d0723555e7babb -- \
  Stage1_Instances/THM-M-1045/Statement.lean \
  Stage1_Instances/THM-M-1045/ObligationTree.lean \
  Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean \
  Stage1_Instances/THM-M-1045/ProofBlockerCharacterizationHead443b8bbcSlot38.lean \
  Stage1_Instances/THM-M-1045/statement.json \
  Stage1_Instances/THM-M-1045/anchor-audit.json \
  Stage1_Instances/THM-M-1045/obligation-registry.json \
  Stage1_Instances/THM-M-1045/typed-graphs.json \
  Stage1_Instances/THM-M-1045/validation-specs.json \
  Formalizations/Lean/lake-manifest.json \
  Formalizations/Lean/lean-toolchain
```

Exact new-file whitespace commands:

```bash
git diff --no-index --check /dev/null \
  Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-57d8d017-slot40.json
git diff --no-index --check /dev/null \
  Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-57d8d017-slot40.md
```

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This is fresh target-scoped nonrelease blocker evidence. It supplies no positive root proof credit,
does not satisfy `S56-M-1045-PROOF`, and makes no provisional-state, audit-completion, validation,
release, theorem-completion, or master-acceptance claim.
