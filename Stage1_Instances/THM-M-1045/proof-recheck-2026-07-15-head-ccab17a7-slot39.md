# THM-M-1045 proof phase: unchanged exact-target blocker

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision: `ccab17a70dd799a6c34193b21d360a8f94611417`

Base tree: `257b40436bffe8f314152da5ab3be907d3a33363`

Rechecked: `2026-07-15T18:35:38+08:00` (`Asia/Shanghai`)

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

Empty elimination is a vacuous interface-emptiness result, not a proof of the mathematical
Cameron-Martin theorem, and is ineligible under the exact-target and no-substitution gates. Three
independent bounded inspections found no exact positive body or pinned terminal import. The
repo-local legacy slot contains a one-dimensional Gaussian shift and conditional wrappers, but
not the required infinite-dimensional equivalence, density, or singularity branches. No material
closure input has changed since the exact negative characterization was integrated.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`, invalidating
`M1045-L-PALEY-WIENER` and blocking `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
The fail-closed vector proposed for master reconciliation is `[H1, M3, R3] -> [H1, M5, R3]`.
Separately, predecessor `S56-M-1045-OBLIGATION_TREE` remains worker-provisional `[_]`, not
master-accepted `[x]`.

Two other statement risks remain. The path measurable-space encoding comaps `top`, producing the
top measurable space rather than establishing the advertised cylinder/Borel sigma-algebra. The
selected `timeMeasure` pushes all real volume through `Real.toNNReal`, collapsing the negative
half-line at zero rather than selecting ordinary volume on `NNReal`. The statement mutation suite
also lacks visibly explicit changed-domain and changed-binder-scope cases required by section 5.1.

Positive proof work can resume only after a source-justified statement revision constructs or
constrains the Paley-Wiener integral without assuming quasi-invariance or the desired density,
corrects or justifies both measure encodings, publishes a fresh target fingerprint, and refreezes
the dependent anchor audit and a version-2 obligation registry and typed graphs.

Nineteen prior target-local blocker/recheck JSON packets predate this run. The authoritative DAG
nevertheless records zero proof attempts and no children, so packet count alone does not establish
five scheduler execution ticks. This worker did not edit scheduler authority. Because the first
failed node is the predecessor statement rather than a divisible proof leaf, the master should
reopen that dependency and stop scheduling unchanged proof-root retries.

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
| `timeout --foreground --kill-after=10s 600 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 0 | Exact target fingerprint `e1b35bb7...5cea` agreed and all four recorded mutations were distinguished. |
| `timeout --foreground --kill-after=10s 600 python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Fingerprint, ten Lean probes, candidate inventory, and mathlib pin agreed. |
| `timeout --foreground --kill-after=10s 600 python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | Fifteen obligations and 30 typed edges passed; root remains open at M3. |
| Narrow pinned `lake env lean` replay below | 0 | Statement, blocker, characterization, and conditional composer elaborated with `--trust=0 -t0`; all three theorem bodies report exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in the three checked proof-related sources. |
| Pinned terminal-candidate text search | 0 | Matches were confined to the legacy local scaffold; pinned mathlib contains no terminal match. |
| `git diff --quiet c74f595e9..HEAD -- <material target paths and Lean pins>` | 0 | No statement, blocker, composer, registry, graph, validation-spec, legacy anchor, toolchain, or lockfile delta since the exact characterization first appeared. |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No tracked-diff whitespace diagnostics before this packet was written. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-ccab17a7-slot39.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground --kill-after=10s 600 \
  "$lean_bin" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean \
  >"$tmp/Statement.log" 2>&1
for source in ProofBlockerCurrent ProofBlockerCharacterizationHead443b8bbcSlot38 ObligationTree; do
  output=${source/ProofBlockerCharacterizationHead443b8bbcSlot38/ProofBlockerCharacterization}
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground --kill-after=10s 600 \
    "$lean_bin" --trust=0 -t0 -o "$tmp/$output.olean" "$source.lean" \
    >"$tmp/$output.log" 2>&1
done
sha256sum "$tmp"/{Statement,ProofBlockerCurrent,ProofBlockerCharacterization,ObligationTree}.log
sha256sum "$tmp"/{Statement,ProofBlockerCurrent,ProofBlockerCharacterization,ObligationTree}.olean
```

Exact prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean \
  Stage1_Instances/THM-M-1045/ProofBlockerCharacterizationHead443b8bbcSlot38.lean \
  Stage1_Instances/THM-M-1045/ObligationTree.lean
```

The statement, blocker, characterization, and conditional-composer log SHA-256 values are
respectively `4adb258a91317991276961bad1d03712638888a5a2af84a12240a92e12a8b110`,
`55dcd476292f394eca6e28e17cf180ad4d1773f6601d84fed4adcc8284a58964`,
`38cd8fdac134d193c3293524684a66c80023fb7d9ab84740f0ad23aeb7bfde95`, and
`8f9246d00cd8e9461675b69ca071323c2818448bedf026cdf27fbaaac2b43737`.

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This is fresh target-scoped nonrelease blocker evidence. It supplies no positive root proof credit,
does not satisfy `S56-M-1045-PROOF`, and makes no provisional-state, audit-completion, validation,
release, theorem-completion, or master-acceptance claim.
