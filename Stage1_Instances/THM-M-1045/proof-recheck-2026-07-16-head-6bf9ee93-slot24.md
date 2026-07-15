# THM-M-1045 proof phase: current-base exact-target blocker

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision/tree: `6bf9ee93a322e7d25cf9249226222095f95d1cff` /
`24acf86e69ab2e6fca9480c6269b6429874ba295`

Rechecked: `2026-07-16T04:46:11+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible nonvacuous proof body establishes the exact frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`, and no root
`.stage1-worker-selftest.json` is written.

The required v2 dependency audit is complete. THM-M-1045 has no direct hard parent, transitive hard
ancestor, hard edge, reuse hint, or shared lemma group. The empty closure is recorded in
`dependency-reuse-ledger.json` using schema `stage1-dependency-reuse-ledger/1.1`, graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, and context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`. Absence of an admitted
dependency remains `unknown_not_independent_proof_claim`; it supplies no proof credit.

The root quantifies over every `WienerData`, but `WienerData.paleyWienerIntegral` is constrained
only by measurability. `ProofBlockerCurrent.lean` preserves every Wiener-law field, changes only
that pairing to the measurable constant-one map, and kernel-checks:

```text
no_target_of_wienerData (W : WienerData) : Not CameronMartinTarget
```

At `h = 0` and `g = 0`, the density branch makes the self Radon-Nikodym derivative equal
`ENNReal.ofReal (Real.exp 1)` almost everywhere; `Measure.rnDeriv_self` makes it equal one. The
checked exact characterization is:

```text
target_iff_isEmpty_wienerData : CameronMartinTarget iff IsEmpty WienerData
```

This does not construct `WienerData`, so it is not an unconditional refutation of the root.
Conversely, empty elimination would be a vacuous interface-emptiness proof rather than the
mathematical Cameron-Martin theorem and is ineligible under the exact-target and no-substitution
gates. Three read-only analyses in this run found no exact positive body, pinned terminal import,
or construction of `WienerData`. Pinned mathlib contains no known Cameron-Martin or Paley-Wiener
terminal body; the legacy slot contains a one-dimensional Gaussian shift and conditional
interfaces only.

## Failed Gate

Rev-5.6 section 5.1 exact-target consistency fails first at `M1045-S-DEFINITIONS`. The defective
pairing interface invalidates `M1045-L-PALEY-WIENER` and blocks `M1045-B-DENSITY`,
`M1045-T-ASSEMBLE`, and `M1045-ROOT`. The fail-closed vector proposed for master reconciliation is
`[H1, M3, R3] -> [H1, M5, R3]`. Predecessor `S56-M-1045-OBLIGATION_TREE` is also only
worker-provisional `[_]`, not master-accepted `[x]`, so proof acceptance is independently not
dependency-legal.

Two further statement risks require statement-phase review. The path measurable-space definition
comaps `top` rather than establishing the advertised cylinder/Borel sigma-algebra. The selected
`timeMeasure` pushes all real volume through `Real.toNNReal`, collapsing the negative half-line at
zero. The mutation suite also lacks explicit changed-domain and changed-binder-scope cases required
by section 5.1.

Positive proof work can resume only after a source-justified statement repair constructs or
constrains the Paley-Wiener integral without assuming quasi-invariance or the desired density,
corrects or justifies both measure encodings, adds the missing mutations, publishes a fresh target
fingerprint, and obtains fresh accepted statement, anchor-audit, version-2 registry, and typed-graph
evidence.

Thirty-one tracked blocker/recheck JSON packets predate this run. The authoritative DAG still
records zero proof attempts and no children. The five-tick split threshold has therefore been
crossed repeatedly, but the first failed node is the predecessor statement, not a divisible proof
leaf. The master should reopen `S56-M-1045-STATEMENT` and stop scheduling unchanged proof-root
retries.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation ran. Lean object output was isolated under `/tmp`
and removed.

The structured JSON packet records the exact commands, exit codes, and result summaries. The narrow
Lean recipe was:

```bash
set -u
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-6bf9ee93-slot24.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && timeout --foreground --kill-after=5s 120 lake env which lean)
base_path=$(cd "$lean_root" && timeout --foreground --kill-after=5s 120 \
  env -u LEAN_PATH lake env printenv LEAN_PATH)
cd "$target"
for source in Statement ProofBlockerCurrent \
  ProofBlockerCharacterizationHead443b8bbcSlot38 ObligationTree; do
  output=${source/ProofBlockerCharacterizationHead443b8bbcSlot38/ProofBlockerCharacterization}
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
    timeout --foreground --kill-after=10s 600 "$lean" \
    --trust=0 -t0 -R "$target" -o "$tmp/$output.olean" "$source.lean" \
    >"$tmp/$output.log" 2>&1
done
```

All four modules elaborated. The blocker, characterization, and conditional composer use exactly
`[propext, Classical.choice, Quot.sound]`. Their log SHA-256 values are respectively
`55dcd476292f394eca6e28e17cf180ad4d1773f6601d84fed4adcc8284a58964`,
`38cd8fdac134d193c3293524684a66c80023fb7d9ab84740f0ad23aeb7bfde95`, and
`8f9246d00cd8e9461675b69ca071323c2818448bedf026cdf27fbaaac2b43737`.

The global standard, v2 DAG, and cron aggregate validators fail only because fresh discovery sees
the new target-owned ledger and blocker packet while the checked-in theorem-DAG inventory remains
immutable in the worker clone. This is an expected integration boundary, not proof success: the
integration lane regenerates the v2 DAG after merging owned artifacts. No authority file was
edited. Target membership, ledger schema/context/base binding, statement fingerprint checks,
anchor audit, 15-obligation/30-edge structure, trust-zero blocker elaboration, and placeholder scan
all passed at their stated boundaries.

This is a current-base, target-scoped, nonrelease blocker handoff. It supplies no positive root
proof credit and makes no provisional-state, audit-completion, validation, release,
theorem-completion, or master-acceptance claim.
