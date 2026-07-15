# THM-M-1045 proof phase: frozen-target blocker

Item: `S56-M-1045-PROOF`

Base revision/tree: `f7b3c872ab727ab689486d74020c11dc5d99869f` /
`6c3dc9661349dd7774b23660eb9bde0212918c51`

Rechecked: `2026-07-15T19:32:57+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible nonvacuous proof body establishes the frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`, and no root
`.stage1-worker-selftest.json` is written.

`WienerData.paleyWienerIntegral` is constrained only by measurability, although the root quantifies
over every `WienerData` and requires its exact exponential density. `ProofBlockerCurrent.lean`
preserves every Wiener-law field, changes only this pairing to the measurable constant-one map, and
kernel-checks:

```text
no_target_of_wienerData (W : WienerData) : Not CameronMartinTarget
```

At `h = 0` and `g = 0`, the density branch says that the self Radon-Nikodym derivative is
`ENNReal.ofReal (Real.exp 1)` almost everywhere; `Measure.rnDeriv_self` says it is one. The exact
checked characterization is:

```text
target_iff_isEmpty_wienerData : CameronMartinTarget iff IsEmpty WienerData
```

This characterization does not construct `WienerData` and therefore is not an unconditional proof
of `Not CameronMartinTarget`. Conversely, empty elimination would be a vacuous interface-emptiness
proof, not Cameron-Martin, so it is ineligible under the exact-target and no-substitution gates.
Three independent bounded inspections found no exact positive body or pinned terminal import.
Pinned mathlib has no terminal match, and the legacy slot has only a one-dimensional Gaussian shift
plus conditional interfaces.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`. It invalidates
`M1045-L-PALEY-WIENER` and blocks `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
The fail-closed vector proposed for master reconciliation is `[H1, M3, R3] -> [H1, M5, R3]`.
Predecessor `S56-M-1045-OBLIGATION_TREE` also remains worker-provisional `[_]`, rather than
master-accepted `[x]`.

Positive proof work requires a source-justified statement revision that constructs or constrains
the Paley-Wiener integral without assuming the desired conclusion. The revision must also correct
or justify the path measurable space (`comap ... top`) and the time measure
(`volume.map Real.toNNReal`), add changed-domain and changed-binder-scope mutations, publish a fresh
target fingerprint, and refreeze the anchor audit, obligation registry, and typed graphs.

Twenty-two blocker/recheck JSON packets predate this run, while the authoritative DAG still records
zero proof attempts and no children. The failed dependency is the statement, not a divisible proof
leaf. The master should reopen that dependency and stop scheduling unchanged proof-root retries.

## Validation

All commands ran in the worker clone. The automation-provided untracked `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation ran. Temporary Lean outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238; planned; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=10s 600 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 0 | The frozen fingerprint remains `e1b35bb7...5cea`; direct replay independently elaborated the exact target. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Fingerprint, ten Lean probes, candidate inventory, and mathlib pin agreed. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains M3. |
| Narrow pinned `lake env lean` replay below | 0 | Four sources elaborated with `--trust=0 -t0`; blocker, characterization, and composer each use exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in the three proof-related sources. |
| Material-source freshness diff from `647eb08e6` | 0 | No target-source, graph, validation-spec, toolchain, or lockfile delta. |

Artifact-only checks, run after writing this handoff, also passed: `python3 -m json.tool` exited 0;
`git diff --check` emitted no diagnostics; each `git diff --no-index --check /dev/null <new-file>`
emitted no diagnostics and exited 1 only because the new file differs from `/dev/null`; and
`test ! -e .stage1-worker-selftest.json` exited 0.

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-f7b3c872-slot28.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
  timeout --foreground --kill-after=10s 600 lake --dir "$lean_root" env lean \
  --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean \
  >"$tmp/Statement.log" 2>&1
for source in ProofBlockerCurrent ProofBlockerCharacterizationHead443b8bbcSlot38 ObligationTree; do
  output=${source/ProofBlockerCharacterizationHead443b8bbcSlot38/ProofBlockerCharacterization}
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
    timeout --foreground --kill-after=10s 600 lake --dir "$lean_root" env lean \
    --trust=0 -t0 -o "$tmp/$output.olean" "$source.lean" \
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

The statement, blocker, characterization, and composer log SHA-256 values are respectively
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
