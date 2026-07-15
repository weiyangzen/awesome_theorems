# THM-M-1067 proof-phase recheck at `40af576c` (slot39)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T21:14:02+08:00`

Base: `40af576c997f512b8937d4c32a8b459dbb3c18a1` / tree
`9cf2d30df293b11ef79f6e4d662549b26a7bdf95`

## Verdict: blocked

The assigned proof phase cannot truthfully close on this base. The frozen definition

```lean
def nonnegativeLebesgue : Measure NNReal := Measure.map Real.toNNReal volume
```

does not give Lebesgue measure on nonnegative time. `Real.toNNReal` sends every nonpositive real
to zero, so this pushforward assigns infinite mass to `{0}`. At `t = 0`, the time integral of the
measurable indicator of zero is consequently infinite, while its spatial integral is zero for
every proposed `NNReal`-valued local-time field.

The existing placeholder-free certificate in `Proof.lean` was re-elaborated with pinned Lean
4.29.0 at trust zero. It proves:

- `nonnegativeLebesgue_singleton_zero`: the frozen time measure gives `{0}` infinite mass;
- `occupation_at_zero_false`: the occupation identity fails at time zero for every path and field;
- `no_local_time_of_wiener`: no field satisfies the frozen predicate under a Wiener measure;
- `target_iff_no_wiener_measure`: the frozen target is equivalent to nonexistence of its own
  Wiener measures.

These declarations are negative kernel certificates for an exact-statement defect. They do not
construct Brownian local time or prove the canonical human theorem. Using the malformed target's
vacuous equivalence as a positive proof would substitute a different theorem and receives no proof
credit.

The first failed gate is exact-statement fidelity at `M1067-S-BOUNDARY`, an effective `M5`
statement mismatch. The accepted instance snapshot remains `[H2, M3, R4]`; the provisional frozen
typed graph remains `[H2, M4, R4]`. This proof worker changes neither predecessor authority.

The prerequisite `S56-M-1067-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`; this independently prevents dependency-legal proof promotion. Its registry contains 17
obligations and 71 typed edges. All 15 machine-required obligations still have
`terminal_proof_body_id: null`, and the root remains open `M4`.

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

This surface is unchanged from the preceding integrated `b73dae2e` recheck. The pinned mathlib
revision/tree is `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The scoped source check found no Brownian-motion
module or stochastic local-time, occupation-density, or Tanaka terminal theorem. The recorded
external audit likewise found no exact compatible placeholder-free body.

## Validation

All checks reused the automation-provided symlink to the existing pinned `.lake` artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake`
mutation was performed. Lean outputs were written only to a fresh temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509 is planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 typed edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement, four defect declarations, and obligation interfaces elaborated. Each defect theorem reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal bodies. |
| Prohibited-construct `rg` scan | expected no-match exit 1 | No prohibited proof construct occurs in owned Lean sources. |
| Pinned environment identity and scoped mathlib source check | 0 | Lean/Lake and mathlib identities matched; Brownian module absent; source search had no match. |
| Frozen-input comparison from `b73dae2e` | 0 | Statement, negative certificate, obligation artifacts, anchor audit, and Lean locks are unchanged. |
| JSON parse, packet-state, and live source-hash assertions | 0 | Identity, current base, blocked/open flags, changed paths, and frozen hashes passed. |
| `git diff --no-index --check /dev/null` over both new artifacts | expected new-file exit 1 | Neither artifact produced a whitespace diagnostic. |
| Completion-manifest and generated-output absence assertion | 0 | No `.stage1-worker-selftest.json` or owned Lean output exists. |

The exact isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-head40af576c-slot39.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
cp "$repo/Stage1_Instances/THM-M-1067/ObligationTree.lean" "$tmp/ObligationTree.lean"
lean_bin=$(cd "$repo/Formalizations/Lean" && timeout 120 lake env which lean)
lean_path=$(cd "$repo/Formalizations/Lean" && timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" "$tmp/ObligationTree.olean"
```

The object hashes were `be965b25bd779d55ff6000d2fc721c1cef439ba3e2070e0b5218ca6f898b5164`
for `Statement.olean`, `1ac94b10534b168fe7f4df222b5e8797388021cfb942f6ee486c222eb4b04bae`
for `Proof.olean`, and `052930aeb6659bc098c0c1ad69807d3e3dc80ce4e644f01314f2c34b81d763f5`
for `ObligationTree.olean`.

## Retry boundary

Reopen `S56-M-1067-STATEMENT` and replace the malformed unrestricted pushforward with a faithfully
characterized Lebesgue measure on nonnegative time. Then rerun and master-accept statement identity,
mutation, anchor-audit, and versioned obligation-freeze phases in dependency order. After that
repair, the Brownian construction, estimates, convergence, continuity, measurability, and
simultaneous occupation identity still need actual placeholder-free bodies or an exact compatible
audited import.

No `.stage1-worker-selftest.json` is written. This packet is blocker evidence only: it does not
satisfy `S56-M-1067-PROOF`, close an obligation or root, change scheduler state, or support audit or
theorem completion.
