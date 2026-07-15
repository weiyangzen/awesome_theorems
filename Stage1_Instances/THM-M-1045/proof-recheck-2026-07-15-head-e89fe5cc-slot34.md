# THM-M-1045 proof phase: current-base blocker

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision: `e89fe5cc9f4b8de45e791d470b1e02e39ca0e734`

Base tree: `dc43d49d892d5f7eb05124c95f52f837b97734ba`

Rechecked: `2026-07-15T14:51:03+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible positive proof body can establish the exact frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`, and no root
`.stage1-worker-selftest.json` is written.

The root quantifies over every `WienerData`, but `WienerData.paleyWienerIntegral` is constrained
only by measurability. The checked `ProofBlockerCurrent.lean` preserves every Wiener-law field,
replaces only that field by the measurable constant-one pairing, and proves:

```text
no_target_of_wienerData (W : WienerData) : Not CameronMartinTarget
```

At `h = 0` and `g = 0`, the frozen density branch makes the self Radon-Nikodym derivative equal
`ENNReal.ofReal (Real.exp 1)` almost everywhere, while `Measure.rnDeriv_self` makes it equal one.
The checked exact characterization is:

```text
target_iff_isEmpty_wienerData : CameronMartinTarget iff IsEmpty WienerData
```

Empty elimination is a vacuous interface-emptiness result, not a proof of the Cameron-Martin
theorem, so it is ineligible under the exact-target and no-substitution gates. Repo-local and pinned
package searches found no exact positive proof or import. The legacy `S1_M_238.lean` has only
conditional/model-field projections and finite-dimensional Gaussian-shift wrappers.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`, invalidating
`M1045-L-PALEY-WIENER` and blocking `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
The fail-closed vector proposed for master reconciliation is `[H1, M3, R3] -> [H1, M5, R3]`.
Separately, predecessor `S56-M-1045-OBLIGATION_TREE` remains worker-provisional `[_]`, not
master-accepted `[x]`.

Two other statement risks remain. The path measurable-space encoding comaps `top`, producing the
discrete/top measurable space on `WienerPath` rather than the advertised cylinder/Borel
sigma-algebra. The selected `timeMeasure` pushes all real volume through `Real.toNNReal`, sending
the negative half-line to zero and giving the singleton zero infinite mass rather than ordinary
volume on `NNReal`.

Positive proof work can resume only after a source-justified statement revision constructs or
constrains the Paley-Wiener integral without assuming the desired conclusion, corrects or justifies
the measure encodings, publishes a fresh target fingerprint, and refreezes the dependent anchor
audit and a version-2 obligation registry and typed graphs.

Ten prior dated target-local blocker/recheck JSON-plus-Markdown packet pairs predate this run (not
counting the standalone `proof-blocker.md`), but the authoritative DAG still records zero proof
attempts and no children. Packet-pair count alone does not establish five scheduler execution ticks.
This worker did not edit that authority. Because the failed node is the predecessor statement rather
than a divisible proof leaf, the master should reopen the statement dependency and stop scheduling
unchanged proof-root retries.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation ran. Lean outputs were isolated under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at L0/rework-required passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238, planned, legacy artifacts unaccepted, theorem incomplete. |
| `timeout --foreground 600 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 0 | Exact target fingerprint `e1b35bb7...5cea` agreed and all four recorded mutations were distinguished. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Fingerprint, ten Lean probes, candidate inventory, and mathlib pin agreed. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains open at M3. |
| Narrow pinned `lake env lean` replay below | 0 | Statement, blocker, characterization, and conditional composer elaborated with `--trust=0 -t0`; all three theorem bodies report exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in the three checked proof-related sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-e89fe5cc-slot34.json` | 0 | Structured blocker packet parsed successfully. |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No tracked-diff whitespace diagnostics. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-e89fe5cc-slot34.json` | 1 expected | No whitespace diagnostics; exit 1 records that the new JSON file differs from `/dev/null`. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-e89fe5cc-slot34.md` | 1 expected | No whitespace diagnostics; exit 1 records that the new Markdown file differs from `/dev/null`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-e89fe5cc-slot34.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  timeout --foreground 600 lake --dir "$lean_root" env lean \
  --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean \
  >"$tmp/Statement.log" 2>&1
for source in ProofBlockerCurrent ProofBlockerCharacterizationHead443b8bbcSlot38 ObligationTree; do
  output=${source/ProofBlockerCharacterizationHead443b8bbcSlot38/ProofBlockerCharacterization}
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
    timeout --foreground 600 lake --dir "$lean_root" env lean \
    --trust=0 -t0 -o "$tmp/$output.olean" "$source.lean" \
    >"$tmp/$output.log" 2>&1
done
for log in Statement ProofBlockerCurrent ProofBlockerCharacterization ObligationTree; do
  sha256sum "$tmp/$log.log"
done
for obj in Statement ProofBlockerCurrent ProofBlockerCharacterization ObligationTree; do
  sha256sum "$tmp/$obj.olean"
done
sed -n '/depends on axioms:/,/^$/p' \
  "$tmp/ProofBlockerCurrent.log" \
  "$tmp/ProofBlockerCharacterization.log" \
  "$tmp/ObligationTree.log"
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

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This is fresh target-scoped nonrelease blocker evidence. It supplies no positive root proof credit,
does not satisfy `S56-M-1045-PROOF`, and makes no provisional-state, audit-completion, validation,
release, theorem-completion, or master-acceptance claim.
