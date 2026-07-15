# THM-M-1045 proof phase: frozen-target blocker

Item: `S56-M-1045-PROOF`

Base revision/tree: `cf0d919f2dfc00f3f777e9319188dec0f644d159` /
`993e3e180c52396b1dd8c970410284d8c3e5bf8d`

Rechecked: `2026-07-15T22:05:06+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible nonvacuous proof body establishes the frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`, and no root
`.stage1-worker-selftest.json` is written.

`WienerData.paleyWienerIntegral` is constrained only by measurability, while the root quantifies
over every `WienerData` and requires the exact exponential density for that field.
`ProofBlockerCurrent.lean` preserves every Wiener-law field, replaces only the pairing with the
measurable constant-one map, and kernel-checks:

```text
no_target_of_wienerData (W : WienerData) : Not CameronMartinTarget
```

At `h = 0` and `g = 0`, the target says that the self Radon-Nikodym derivative is
`ENNReal.ofReal (Real.exp 1)` almost everywhere; `Measure.rnDeriv_self` says it is one. The exact
checked characterization is:

```text
target_iff_isEmpty_wienerData : CameronMartinTarget iff IsEmpty WienerData
```

This does not construct `WienerData`, so it is not an unconditional proof of
`Not CameronMartinTarget`. Conversely, empty elimination would be a vacuous interface-emptiness
proof, not the Cameron-Martin theorem, and is ineligible under the exact-target and no-substitution
gates. Three independent read-only inspections found no exact positive body, pinned terminal
import, or construction of `WienerData`. Pinned mathlib has only lower-level Gaussian and
Radon-Nikodym APIs; the legacy slot supplies a one-dimensional Gaussian shift and conditional
interfaces.

## Failed Gate

The rev-5.6 section 5.1 exact-target consistency gate fails at `M1045-S-DEFINITIONS`. This
invalidates `M1045-L-PALEY-WIENER` and blocks `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and
`M1045-ROOT`. The fail-closed vector proposed for master reconciliation is
`[H1, M3, R3] -> [H1, M5, R3]`. Predecessor `S56-M-1045-OBLIGATION_TREE` is also only
worker-provisional `[_]`, not master-accepted `[x]`.

Positive proof work requires a source-justified statement revision that constructs or constrains
the Paley-Wiener integral without assuming the desired conclusion. That revision must also correct
or justify the path measurable space (`comap ... top`) and time measure
(`volume.map Real.toNNReal`), add explicit changed-domain and changed-binder-scope mutations,
publish a fresh target fingerprint, and refreeze the anchor audit, obligation registry, and typed
graphs.

Twenty-seven tracked blocker/recheck JSON packets predate this run, while the authoritative DAG
still records zero proof attempts and no children. The five-tick split threshold has therefore
been exceeded repeatedly, but the first failed node is the predecessor statement, not a divisible
proof leaf. The master should reopen that dependency and stop scheduling unchanged proof-root
retries.

## Validation

All commands ran in the worker clone. The automation-provided untracked `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation ran. Temporary Lean outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238; planned; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=10s 600 env LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 0 | Fingerprint `e1b35bb7...5cea` agreed; all four recorded mutations were distinguished. |
| `timeout --foreground --kill-after=10s 600 env LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Fingerprint, ten Lean probes, candidate inventory, and mathlib pin agreed. |
| `timeout --foreground --kill-after=10s 600 env LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains M3. |
| Narrow pinned `lake env lean` replay below | 0 | Four sources elaborated with `--trust=0 -t0`; blocker, characterization, and composer each use exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in the three proof-related sources. |
| Material-source freshness diff from `6ac589f0d` | 0 | No target-source, registry, graph, validation-spec, toolchain, or lockfile delta. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-cf0d919f-slot18.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
base_path=$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)
cd "$target"
for source in Statement ProofBlockerCurrent ProofBlockerCharacterizationHead443b8bbcSlot38 ObligationTree; do
  output=${source/ProofBlockerCharacterizationHead443b8bbcSlot38/ProofBlockerCharacterization}
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
    timeout --foreground --kill-after=10s 600 "$lean" \
    --trust=0 -t0 -R "$target" -o "$tmp/$output.olean" "$source.lean" \
    >"$tmp/$output.log" 2>&1
done
```

Exact prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean \
  Stage1_Instances/THM-M-1045/ProofBlockerCharacterizationHead443b8bbcSlot38.lean \
  Stage1_Instances/THM-M-1045/ObligationTree.lean
```

Statement, blocker, characterization, and composer log SHA-256 values are respectively
`4adb258a91317991276961bad1d03712638888a5a2af84a12240a92e12a8b110`,
`55dcd476292f394eca6e28e17cf180ad4d1773f6601d84fed4adcc8284a58964`,
`38cd8fdac134d193c3293524684a66c80023fb7d9ab84740f0ad23aeb7bfde95`, and
`8f9246d00cd8e9461675b69ca071323c2818448bedf026cdf27fbaaac2b43737`.

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This is current-base target-scoped nonrelease blocker evidence. It supplies no positive root proof
credit and makes no proof completion, validation, release, theorem completion, or master acceptance
claim.
