# THM-M-1067 proof-phase recheck at `3862149a` (slot54)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T16:59:32+08:00`

Base: `3862149a6bcf2a64e19fabdced9dd80a706f288e` / tree
`d3e57e661c2326a97c8b48580abe1f4a3797cd98`

## Verdict: blocked

The assigned proof phase cannot truthfully proceed on this base. The prerequisite
`S56-M-1067-OBLIGATION_TREE` is only worker-provisional `[_]` in the blueprint and remains open in
the generated target DAG, so dependency-ordered proof acceptance is already illegal. Independently,
the frozen definition

```lean
def nonnegativeLebesgue : Measure ℝ≥0 := Measure.map Real.toNNReal volume
```

does not define Lebesgue time on the nonnegative reals. `Real.toNNReal` collapses the entire
nonpositive half-line to zero, so this measure assigns infinite mass to `{0}`. The existing
placeholder-free certificate in `Proof.lean` kernel-checks the resulting contradiction:

- `nonnegativeLebesgue_singleton_zero` proves `nonnegativeLebesgue {0} = ∞`;
- `occupation_at_zero_false` proves the frozen occupation identity impossible at `t = 0` for every
  path and proposed field;
- `no_local_time_of_wiener` proves no proposed field satisfies the frozen local-time predicate for
  a Wiener measure;
- `target_iff_no_wiener_measure` proves the frozen target equivalent to nonexistence of its own
  Wiener measures.

This is negative kernel evidence for a statement defect, not a Brownian-local-time construction or
a proof of the canonical human claim. Proving the target by proving nonexistence of its own Wiener
measures would exploit the malformed encoding and substitute a different theorem, which rev-5.6
forbids. This evidence therefore receives no positive proof credit and supports only a fail-closed
`M5` diagnosis pending master reconciliation.

## Frozen proof surface

The proof inputs and Lean locks are byte-identical to the preceding trust-zero recheck at
`23d17225`:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `00c33bd06b1930a28b92706f9f2064d039bc5280078103814dfe02e1eb437480` |
| `Proof.lean` | `efdee3a7b28e682e5a4a929bb95cd52cb7632962bf2bb3bcce903c28ef3d2eca` |
| `ObligationTree.lean` | `45257cb9285ffbe723ac4128161124471a3591168dc79ac1dbd2aaf8e435074e` |
| `obligation-registry.json` | `4e7a564ce1b2be77de5115245c0ba484a8f4bc2ed0ee8fa7739218756aa1e92b` |
| `typed-graphs.json` | `2593501c7c1404feb2a559521d161adebaf7b8e97e77564f91db04612f108c62` |
| `anchor-audit.md` | `09a4f1e1d0c9641a60ec1d1b79527a7791426cf5993803dab708a3f946d258d6` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

The registry checker still reports 17 obligations and 71 typed edges with an open `M4` root. All
15 machine-required obligations still have null terminal proof-body IDs. A fresh scoped search
confirmed that the pinned mathlib closure has no Brownian-motion module or stochastic local-time,
Tanaka, or occupation-density declaration. The audited external candidate has no local-time result,
targets a different Lean version, and contains admitted dependencies, so it remains ineligible for
exact proof credit.

## Validation

All commands reused the automation-provided pinned `.lake` symlink read-only. No Lake update or
build, dependency clone or fetch, network operation, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 typed edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement, all four defect declarations, and the assumption-parametric composition interfaces elaborated; each defect declaration reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal proof-body IDs. |
| Prohibited-construct `rg` scan | 1, expected | No prohibited proof construct occurs in owned Lean sources. |
| Pinned environment identity checks | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake 5.0.0; mathlib commit/tree `8a178386...` / `bdc39a31...`; lock hashes matched. |
| Frozen-input comparison from `23d17225` to this base | 0 | Statement, proof certificate, obligation artifacts, anchor audit, and Lean locks are unchanged. |
| Scoped candidate search | 0 | Brownian module absent; no stochastic local-time, Tanaka, or occupation-density candidate found. |
| Structured packet and recorded-hash assertions | 0 | JSON identity/open-state invariants and all recorded input hashes agreed. |
| `git diff --check -- Stage1_Instances/THM-M-1067 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` plus generated-output check | 0 | Completion self-test manifest and stray Lean outputs are absent, as required for this blocked phase. |

The isolated Lean command, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-slot54-head-3862149a.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
cp "$repo/Stage1_Instances/THM-M-1067/ObligationTree.lean" "$tmp/ObligationTree.lean"
cd "$repo/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
base_lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" "$tmp/ObligationTree.olean"
```

The object hashes were `be965b25bd779d55ff6000d2fc721c1cef439ba3e2070e0b5218ca6f898b5164`
for `Statement.olean`, `1ac94b10534b168fe7f4df222b5e8797388021cfb942f6ee486c222eb4b04bae`
for `Proof.olean`, and `052930aeb6659bc098c0c1ad69807d3e3dc80ce4e644f01314f2c34b81d763f5`
for `ObligationTree.olean`.

## Retry boundary

Reopen and repair `S56-M-1067-STATEMENT` with a faithful nonnegative-time Lebesgue measure. Then
rerun statement identity and boundary mutations, the anchor audit, and a versioned obligation-tree
freeze in dependency order. Positive proof execution can resume only after those predecessors are
accepted and a placeholder-free construction or exact compatible audited theorem is available.

This current-base nonrelease blocker record leaves `S56-M-1067-PROOF` at `[ ]`. It adds no positive
proof body, closed obligation, composition certificate, content-addressed receipt, or accepted
state, and it does not claim audit or theorem completion. Because the assigned proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.
