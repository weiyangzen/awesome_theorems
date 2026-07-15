# THM-M-1067 proof-phase recheck at `443b8bbc` (slot57)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T11:57:04+08:00`

Base: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b` / tree
`c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict: blocked

The exact proof phase cannot truthfully proceed on this base. The frozen definition

```lean
def nonnegativeLebesgue : Measure ℝ≥0 := Measure.map Real.toNNReal volume
```

does not give Lebesgue time on the nonnegative reals. `Real.toNNReal` collapses the entire
nonpositive half-line to zero, so the resulting measure assigns infinite mass to `{0}`. The
placeholder-free certificate already present in `Proof.lean` was re-elaborated at trust zero and
checks the resulting boundary contradiction:

- `nonnegativeLebesgue_singleton_zero` proves `nonnegativeLebesgue {0} = ∞`;
- `occupation_at_zero_false` proves that the frozen occupation identity is impossible at `t = 0`
  for every path and proposed field;
- `no_local_time_of_wiener` proves that no proposed field satisfies the frozen local-time predicate
  for a Wiener measure;
- `target_iff_no_wiener_measure` proves that the frozen target is equivalent to nonexistence of its
  own Wiener measures.

This is negative kernel evidence for a statement mismatch, not a construction of Brownian local
time and not a positive proof of the canonical human claim. Proving the formal target by separately
asserting nonexistence of Wiener measure would be a vacuous substituted theorem. The checked
certificate therefore supports a fail-closed `M5` diagnosis pending master reconciliation, but it
does not support proof, audit, or theorem completion.

## Frozen proof surface

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `00c33bd06b1930a28b92706f9f2064d039bc5280078103814dfe02e1eb437480` |
| `Proof.lean` | `efdee3a7b28e682e5a4a929bb95cd52cb7632962bf2bb3bcce903c28ef3d2eca` |
| `ObligationTree.lean` | `45257cb9285ffbe723ac4128161124471a3591168dc79ac1dbd2aaf8e435074e` |
| `obligation-registry.json` | `4e7a564ce1b2be77de5115245c0ba484a8f4bc2ed0ee8fa7739218756aa1e92b` |
| `typed-graphs.json` | `2593501c7c1404feb2a559521d161adebaf7b8e97e77564f91db04612f108c62` |
| `anchor-audit.md` | `09a4f1e1d0c9641a60ec1d1b79527a7791426cf5993803dab708a3f946d258d6` |

The registry checker still reports 17 obligations and 71 typed edges with an open `M4` root. All
15 machine-required obligations still have null terminal proof-body IDs. Pinned mathlib contains no
Brownian-motion or local-time terminal theorem. The audited external project has no local-time
result, targets a different Lean version, and has admitted dependencies. The prerequisite
`S56-M-1067-OBLIGATION_TREE` also remains worker-provisional `[_]`, so dependency-ordered proof
acceptance is illegal even apart from the statement defect.

## Validation

All successful Lean checks reused the existing dependency sources and build artifacts and placed
Lean outputs only in a fresh temporary directory, which was removed. Lake may inspect repository
metadata while resolving the environment; no dependency source, revision, or build content was
changed. No Lake update/build, dependency clone/fetch, or network operation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement elaborated; each of the four defect declarations reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal bodies. |
| Prohibited-construct `rg` scan | 1, expected | No prohibited proof construct occurs in the owned Lean sources. |
| Brownian-module existence check | 1, expected | `Mathlib/Probability/BrownianMotion/Basic.lean` is absent. |
| Local-time/Tanaka/occupation search in pinned mathlib | 1, expected | No stochastic local-time candidate was found. |
| Frozen-input comparison from `a23d86cd` to this base | 0 | Statement, proof certificate, obligation artifacts, anchor audit, and Lean locks are unchanged. |
| Direct project-root `lake env lean` attempt | 1 | The shared `flt-regular` checkout has `.git/HEAD` equal to `ref: refs/heads/.invalid`; no repair or fetch was attempted. |
| Pinned mathlib `lake env lean` with the existing dependency build paths | 0 | Narrow elaboration succeeded without requiring or mutating the unrelated broken checkout. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is deliberately absent. |

The successful narrow Lean command, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
dep_paths=$(find "$repo/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
cd "$repo/Formalizations/Lean/.lake/packages/mathlib"
LEAN_NUM_THREADS=1 LEAN_PATH="$dep_paths" timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$dep_paths" timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

The object hashes were `be965b25bd779d55ff6000d2fc721c1cef439ba3e2070e0b5218ca6f898b5164`
for `Statement.olean` and `1ac94b10534b168fe7f4df222b5e8797388021cfb942f6ee486c222eb4b04bae`
for `Proof.olean`.

## Retry boundary

Reopen and repair `S56-M-1067-STATEMENT` with a faithful nonnegative-time Lebesgue measure, then
rerun statement identity and boundary mutations, the anchor audit, and a versioned obligation-tree
freeze in dependency order. Positive proof execution can resume only after those predecessors are
accepted and a placeholder-free construction or exact compatible audited theorem is available.

This current-base nonrelease blocker record leaves `S56-M-1067-PROOF` at `[ ]`. Because the
assigned proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.
