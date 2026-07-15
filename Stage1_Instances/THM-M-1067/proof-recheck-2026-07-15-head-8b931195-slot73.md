# THM-M-1067 proof-phase recheck at `8b931195` (slot73)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T08:42:02+08:00`

Base revision: `8b9311952b6b4186c774d25758d16597a7c10a8b`

Base tree: `69a7cea0132f4b76e7324c2d5cc320dec94d2f10`

## Verdict

`blocked`. No positive proof body can truthfully close the intended Brownian-local-time theorem on
the current frozen statement. `Statement.lean` defines

```lean
def nonnegativeLebesgue : Measure NNReal := Measure.map Real.toNNReal volume
```

but `Real.toNNReal` maps the whole nonpositive half-line to zero. Consequently the frozen time
measure gives the singleton `{0}` infinite mass. At time zero, the time integral of the indicator
of zero is therefore infinite, while its spatial integral is zero for every proposed
`NNReal`-valued field.

The existing placeholder-free bodies in `Proof.lean` formally diagnose this mismatch:

```text
Stage1Instances.THM_M_1067.nonnegativeLebesgue_singleton_zero :
  nonnegativeLebesgue {0} = top

Stage1Instances.THM_M_1067.no_local_time_of_wiener :
  IsWienerMeasure W -> Not (IsBrownianLocalTime W L)

Stage1Instances.THM_M_1067.target_iff_no_wiener_measure :
  BrownianLocalTimeTarget <-> Not (Exists W, IsWienerMeasure W)
```

These declarations refute the malformed encoding, not the mathematical Brownian-local-time
theorem, and receive no positive proof credit. Proving the frozen target through nonexistence of a
Wiener measure would be a false, vacuous substitution and is prohibited by rev-5.6.

The item remains `[ ]`. No terminal body, closed obligation, composition receipt, state change,
audit completion, theorem completion, or master acceptance is claimed. The completion self-test
manifest remains absent.

## Failed gate and retry

The first failed gate is exact-statement fidelity at `M1067-S-BOUNDARY`. This supports an effective
fail-closed `M5` diagnosis; it does not alter the accepted instance vector `[H2, M3, R4]` or the
frozen graph's open `M4` root. The dependency `S56-M-1067-OBLIGATION_TREE` is also only
worker-provisional `[_]`, not master-accepted `[x]`.

The frozen registry has 17 obligations and 71 typed edges. All 15 machine-required obligations
have `terminal_proof_body_id: null`; `ObligationTree.lean` only checks assumption-parametric
composition interfaces. The pinned audit found no Brownian local-time terminal theorem in mathlib.
The recorded external Brownian project has no local-time theorem, uses a different Lean version,
and has admitted dependencies.

Positive work must first reopen `S56-M-1067-STATEMENT`, replace the malformed pushforward with a
faithful nonnegative-time Lebesgue measure, rerun the statement identity and mutation gates,
re-audit formal candidates, and version/refreeze the obligation registry and graphs. The corrected
theorem would then still require the Brownian interface, approximation, moment and convergence
estimates, limiting field, continuity, measurability, and simultaneous occupation-identity bodies,
or an exact compatible placeholder-free imported theorem.

## Validation

All Lean checks reused the automation-provided symlink to canonical pinned artifacts read-only.
No `lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary Lean outputs were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement and all four defect declarations elaborated; each declaration reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal proof-body IDs. |
| Prohibited-construct `rg` scan | 1, expected | No prohibited proof construct occurs in owned Lean sources. |
| Pinned environment identity checks | 0 | Lean 4.29.0 commit `98dc76e3...`; mathlib commit/tree `8a178386...` / `bdc39a31...`; lock hashes matched. |
| Frozen-input comparison from `d07d9d81` to this base | 0 | Statement, proof certificate, obligation artifacts, anchor audit, and Lean locks are unchanged. |
| `git diff --check -- Stage1_Instances/THM-M-1067` | 0 | No whitespace errors in the owned patch. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The isolated Lean command, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-slot73-head-8b931195.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
cd "$repo/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
base_lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

The object hashes were `be965b25bd779d55ff6000d2fc721c1cef439ba3e2070e0b5218ca6f898b5164`
for `Statement.olean` and `1ac94b10534b168fe7f4df222b5e8797388021cfb942f6ee486c222eb4b04bae`
for `Proof.olean`.

## Status boundary

This is current-base nonrelease blocker evidence. It does not satisfy `S56-M-1067-PROOF`, propose
`[_]` or `[x]`, close the exact root, or support audit or theorem completion. Retry begins with an
authorized statement correction and dependency-ordered re-freeze, not another proof search against
the unchanged encoding.
