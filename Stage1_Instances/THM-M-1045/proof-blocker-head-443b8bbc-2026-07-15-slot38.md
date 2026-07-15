# THM-M-1045 proof phase: model-emptiness blocker

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

Rechecked: `2026-07-15T11:44:48+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible positive proof body establishes the exact frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`; no root
`.stage1-worker-selftest.json` was written.

The frozen `WienerData.paleyWienerIntegral` has only a measurability law, while the target quantifies
over every `WienerData` and demands the exact Radon-Nikodym density formed from that field. The
existing placeholder-free `ProofBlockerCurrent.lean` replaces only this field by the constant-one
map and kernel-checks

```text
no_target_of_wienerData (W : WienerData) : Not CameronMartinTarget.
```

The new `ProofBlockerCharacterizationHead443b8bbcSlot38.lean` strengthens the obstruction to

```text
target_iff_isEmpty_wienerData : CameronMartinTarget <-> IsEmpty WienerData.
```

Thus the frozen root has no nonvacuous model: for any supplied Wiener datum, zero translation and
zero direction make the requested density `exp 1`, whereas `Measure.rnDeriv_self` makes the same
derivative one almost everywhere. Conversely, the root holds when `WienerData` is empty only by
empty elimination. That reverse implication is a vacuous encoding artifact, not a proof of the
mathematical Cameron-Martin theorem, and rev-5.6 prohibits claiming it as proof completion.

The checked result refutes only the frozen Lean interface, not the mathematical theorem. The
fail-closed machine classification proposed for master reconciliation remains `M5`; no predecessor
authority, registry, typed graph, or checklist state was edited.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`. The unconstrained pairing invalidates
`M1045-L-PALEY-WIENER`, blocking `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
Separately, `S56-M-1045-OBLIGATION_TREE` remains worker-provisional `[_]`, so dependency-ordered
master acceptance is outstanding.

Positive proof execution can resume only after the statement constructs the Paley-Wiener integral
or adds source-justified, noncircular linearity, isometry, Gaussian-law, and compatibility laws that
rule out the constant-one replacement. The path measurable-space and `NNReal` time-measure
encodings also require review. Any repair changes the canonical fingerprint, so statement,
anchor-audit, and obligation-tree acceptance must be repeated before proof work resumes.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`, dependency fetch/clone, or
dependency mutation was performed by this worker. The automation-provided `.lake` symlink points to
canonical pinned artifacts, but its unrelated `flt-regular` checkout currently has an invalid HEAD;
therefore `lake env` discovery and `check_statement.py` fail before Lean starts. The narrow kernel
replay used the exact pinned Lean binary and already materialized mathlib/package oleans directly,
with all generated output isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at L0/rework-required passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238; planned hard-mathlib anchor/wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground 600 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 1 | Environment blocker: `lake env` could not resolve `Formalizations/Lean/.lake/packages/flt-regular` HEAD; no fetch or repair was attempted. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Target fingerprint, ten support probes, candidate inventory, and pinned mathlib revision agree. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains open at M3 in predecessor data. |
| Direct isolated pinned Lean recipe below | 0 | Statement, existing blocker, and new characterization elaborated with `--trust=0 -t0`; both blocker theorems report exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in either checked blocker source. |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No tracked-diff whitespace errors. |
| `git diff --no-index --check /dev/null <each new artifact>` | 1 expected | Each new file differs from `/dev/null`; empty diagnostics mean no whitespace errors. |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/proof-blocker-head-443b8bbc-2026-07-15-slot38.json` | 0 | Structured blocker packet parsed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
tmp=$(mktemp -d /tmp/thm-m-1045-characterization-head443b8bbc-slot38.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for package in Cli LeanSearchClient Qq aesop batteries checkdecls importGraph mathlib plausible proofwidgets; do
  package_path="$lean_root/.lake/packages/$package/.lake/build/lib/lean"
  if test -d "$package_path"; then lean_path="$lean_path:$package_path"; fi
done
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/ProofBlockerCurrent.olean" ProofBlockerCurrent.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 ProofBlockerCharacterizationHead443b8bbcSlot38.lean
```

Exact prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean \
  Stage1_Instances/THM-M-1045/ProofBlockerCharacterizationHead443b8bbcSlot38.lean
```

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The statement, existing-blocker, and characterization log SHA-256 values are respectively
`4adb258a91317991276961bad1d03712638888a5a2af84a12240a92e12a8b110`,
`55dcd476292f394eca6e28e17cf180ad4d1773f6601d84fed4adcc8284a58964`, and
`38cd8fdac134d193c3293524684a66c80023fb7d9ab84740f0ad23aeb7bfde95`.

This is target-scoped nonrelease blocker evidence. It supplies no positive root proof credit and
makes no provisional-state, validation, release, audit-completion, theorem-completion, or
master-acceptance claim.
