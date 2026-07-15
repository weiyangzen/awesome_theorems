# THM-M-1067 proof-phase recheck at `3f5b3108` (slot53)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T15:00:08+08:00`

Base: `3f5b310884eb802487a4c901cb0d76752e368da0` / tree
`a1bb0a117c463908411f55d51fdb5ed25c457ab0`

## Verdict: blocked

The assigned proof phase cannot truthfully close on this base. The frozen definition

```lean
def nonnegativeLebesgue : Measure NNReal := Measure.map Real.toNNReal volume
```

is not Lebesgue measure on nonnegative time. `Real.toNNReal` maps every nonpositive real to zero,
so this pushforward assigns infinite mass to `{0}`. At `t = 0`, the time integral of the indicator
of zero is therefore infinite, while its spatial integral is zero for every proposed
`NNReal`-valued local-time field.

The existing placeholder-free certificate in `Proof.lean` was re-elaborated with the pinned Lean
4.29 kernel at trust zero:

- `nonnegativeLebesgue_singleton_zero` proves `nonnegativeLebesgue {0} = infinity`;
- `occupation_at_zero_false` proves that the frozen occupation identity fails at `t = 0` for every
  path and proposed field;
- `no_local_time_of_wiener` proves that no proposed field satisfies the frozen predicate under an
  `IsWienerMeasure` hypothesis;
- `target_iff_no_wiener_measure` proves that the frozen target is equivalent to nonexistence of its
  own Wiener measures.

This is negative kernel evidence for an exact-statement defect. It neither constructs Brownian
local time nor proves the canonical human theorem. Closing the formal target by asserting that no
Wiener measure exists would be a vacuous substituted theorem, which rev-5.6 forbids.

## Frozen proof surface

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `00c33bd06b1930a28b92706f9f2064d039bc5280078103814dfe02e1eb437480` |
| `Proof.lean` | `efdee3a7b28e682e5a4a929bb95cd52cb7632962bf2bb3bcce903c28ef3d2eca` |
| `ObligationTree.lean` | `45257cb9285ffbe723ac4128161124471a3591168dc79ac1dbd2aaf8e435074e` |
| `obligation-registry.json` | `4e7a564ce1b2be77de5115245c0ba484a8f4bc2ed0ee8fa7739218756aa1e92b` |
| `typed-graphs.json` | `2593501c7c1404feb2a559521d161adebaf7b8e97e77564f91db04612f108c62` |
| `anchor-audit.md` | `09a4f1e1d0c9641a60ec1d1b79527a7791426cf5993803dab708a3f946d258d6` |
| `lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

These inputs are unchanged since the prior `ec3b52a2` trust-zero recheck. The obligation checker
reports 17 obligations and 71 typed edges with an open `M4` root. All 15 machine-required
obligations still have `terminal_proof_body_id: null`. The composition theorems in
`ObligationTree.lean` consume assumed children and earn no existence-proof credit. The prerequisite
obligation-tree item remains worker-provisional `[_]`, so proof acceptance is also dependency-
illegal apart from the statement defect.

The pinned mathlib source search found no Brownian-motion, Wiener-measure construction,
local-time, occupation-density, or Tanaka theorem. The external candidate recorded in
`anchor-audit.md` contains no local-time theorem, uses a different Lean version, and has admitted
dependencies, so it cannot supply a terminal body.

## Validation

All checks reused existing pinned artifacts. No `lake update`, `lake build`, dependency clone,
dependency fetch, network operation, or other `.lake` mutation was run. The Lean recipe used
`lake env` only to locate the existing pinned binary and `LEAN_PATH`, then compiled isolated copies
into a fresh temporary directory that was removed afterward.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 typed edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement, defect certificate, and composition interfaces elaborated. Each defect theorem reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal bodies. |
| Prohibited-construct `rg` scan | expected no-match exit 1 | No prohibited proof construct occurs in owned Lean sources. |
| Pinned mathlib source search | 0 | Only an unrelated Wiener-Ikehara comment matched; no Brownian or stochastic local-time candidate occurs. |
| Pinned identity and frozen-input checks | 0 | Lean 4.29.0 at `98dc76e3...`; mathlib revision/tree `8a178386...` / `bdc39a31...`; input hashes match and are unchanged since `ec3b52a2`. |
| Structured JSON/hash assertions plus `git diff --check` | 0 | Packet invariants, current base, open state, hashes, and whitespace checks passed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The exact isolated kernel recipe was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-head3f5b3108-slot53.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
cp "$repo/Stage1_Instances/THM-M-1067/ObligationTree.lean" "$tmp/ObligationTree.lean"
lean_bin=$(cd "$repo/Formalizations/Lean" && lake env which lean)
lean_path=$(cd "$repo/Formalizations/Lean" && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" "$tmp/ObligationTree.olean"
```

The object hashes were `be965b25...` (`Statement.olean`), `1ac94b10...` (`Proof.olean`), and
`052930ae...` (`ObligationTree.olean`). Lean was version 4.29.0 at commit `98dc76e3...`; pinned
mathlib was revision/tree `8a178386...` / `bdc39a31...`.

## Retry boundary

Reopen `S56-M-1067-STATEMENT` and replace the malformed time measure with a faithful nonnegative-
time Lebesgue measure, such as a pushforward of real volume restricted to `Ici 0`. Then rerun
statement identity and mutation checks, the anchor audit, and a versioned obligation freeze in
dependency order. After that repair, the Brownian construction, estimates, convergence,
continuity, measurability, and simultaneous occupation identity still require actual
placeholder-free proof bodies or an exact compatible audited import.

No `.stage1-worker-selftest.json` is written. This packet is blocker evidence only: it does not
satisfy `S56-M-1067-PROOF`, close any obligation, change scheduler state, or support audit or
theorem completion.
