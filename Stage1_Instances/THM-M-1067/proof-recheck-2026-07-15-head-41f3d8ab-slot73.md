# THM-M-1067 proof-phase recheck at `41f3d8ab` (slot73)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T08:51:30+08:00`

Base: `41f3d8abe3a5500190c3f5db50e05104ceeeeb8b` / tree
`3ddb4e8f36082a5a71e32c731390fef8207a6987`

## Verdict: blocked

The exact proof phase cannot truthfully proceed on this base. The frozen definition

```lean
def nonnegativeLebesgue : Measure ℝ≥0 := Measure.map Real.toNNReal volume
```

does not give Lebesgue time on the nonnegative reals: `Real.toNNReal` collapses the entire
nonpositive half-line to zero. Therefore `{0}` has infinite mass. The existing placeholder-free
certificate in `Proof.lean` checks the resulting boundary contradiction:

- `nonnegativeLebesgue_singleton_zero` proves `nonnegativeLebesgue {0} = ∞`;
- `occupation_at_zero_false` proves the frozen occupation identity is impossible at `t = 0` for
  every path and proposed field;
- `no_local_time_of_wiener` proves no proposed field satisfies the frozen local-time predicate for
  a Wiener measure;
- `target_iff_no_wiener_measure` proves that the frozen target is equivalent to nonexistence of its
  own Wiener measures.

This is negative kernel evidence for a statement mismatch, not a construction of Brownian local
time and not a positive proof of the canonical human claim. It supports a fail-closed `M5`
diagnosis pending master reconciliation. It does not support proof, audit, or theorem completion.

## Frozen proof surface

The current source hashes are unchanged since the preceding trust-zero recheck:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `00c33bd06b1930a28b92706f9f2064d039bc5280078103814dfe02e1eb437480` |
| `Proof.lean` | `efdee3a7b28e682e5a4a929bb95cd52cb7632962bf2bb3bcce903c28ef3d2eca` |
| `ObligationTree.lean` | `45257cb9285ffbe723ac4128161124471a3591168dc79ac1dbd2aaf8e435074e` |
| `obligation-registry.json` | `4e7a564ce1b2be77de5115245c0ba484a8f4bc2ed0ee8fa7739218756aa1e92b` |
| `typed-graphs.json` | `2593501c7c1404feb2a559521d161adebaf7b8e97e77564f91db04612f108c62` |
| `anchor-audit.md` | `09a4f1e1d0c9641a60ec1d1b79527a7791426cf5993803dab708a3f946d258d6` |

The registry checker still reports 17 obligations and 71 typed edges with open `M4` root. All 15
machine-required obligations still have null terminal proof-body IDs. The pinned mathlib closure
has no Brownian-motion or local-time terminal theorem, and the audited external project has no
local-time result, targets Lean 4.31 instead of 4.29, and has admitted dependencies. The
prerequisite `S56-M-1067-OBLIGATION_TREE` also remains worker-provisional `[_]`, so dependency-
ordered proof acceptance would be illegal even without the statement defect.

## Validation

All commands used the existing automation-provided pinned `.lake` symlink read-only. No Lake
update/build, dependency clone/fetch, network operation, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement and all four defect declarations elaborated; each declaration reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal bodies. |
| Prohibited-construct `rg` scan | 1, expected | No prohibited proof construct occurs in owned Lean sources. |
| Pinned environment identity checks | 0 | Lean 4.29.0 commit `98dc76e3...`; mathlib commit/tree `8a178386...` / `bdc39a31...`; lock hashes matched. |
| Frozen-input comparison from `8b931195` to this base | 0 | Statement, proof certificate, obligation artifacts, anchor audit, and Lean locks are unchanged. |

The isolated Lean command, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-slot73-head-41f3d8ab.XXXXXX)
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

## Retry boundary

Reopen and repair `S56-M-1067-STATEMENT` with a faithful nonnegative-time Lebesgue measure. Then
rerun statement identity and boundary mutations, the anchor audit, and a versioned obligation-tree
freeze in dependency order. Positive proof execution can resume only after those predecessors are
accepted and a placeholder-free construction or exact compatible audited theorem is available.

This current-base nonrelease blocker record leaves `S56-M-1067-PROOF` at `[ ]`. Because the assigned
proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.
