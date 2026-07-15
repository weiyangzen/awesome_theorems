# THM-M-1067 proof-phase recheck at `e57cfb09` (slot47)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T20:05:45+08:00`

Base: `e57cfb0904e8a827b17320aba51bd41b96109c7c` / tree
`79ab3544eee575a45c51d85923144ed20f607f9e`

## Verdict: blocked

The assigned proof phase cannot truthfully close on this base. The frozen definition

```lean
def nonnegativeLebesgue : Measure NNReal := Measure.map Real.toNNReal volume
```

is not Lebesgue measure on nonnegative time. `Real.toNNReal` maps every nonpositive real to zero,
so this pushforward gives `{0}` infinite mass. At `t = 0`, the time integral of the indicator of
zero is therefore infinite, while its spatial integral is zero for every proposed `NNReal`-valued
local-time field.

The existing placeholder-free certificate in `Proof.lean` was re-elaborated with pinned Lean
4.29.0 at trust zero. It proves:

- `nonnegativeLebesgue_singleton_zero`: the frozen time measure gives `{0}` infinite mass;
- `occupation_at_zero_false`: the occupation identity fails at time zero for every path and field;
- `no_local_time_of_wiener`: no field satisfies the frozen predicate under a Wiener measure;
- `target_iff_no_wiener_measure`: the frozen target is equivalent to nonexistence of its own
  Wiener measures.

These declarations are negative kernel certificates for an exact-statement defect. They do not
construct Brownian local time or prove the canonical human theorem. Proving the malformed target
through nonexistence of its Wiener measures would be a vacuous theorem substitution and receives no
proof credit.

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

These inputs are byte-identical to the preceding integrated `b366bdd9` recheck. The pinned mathlib
revision/tree is `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. It has no Brownian-motion module or exact stochastic
local-time terminal theorem, and the recorded external audit found no exact compatible
placeholder-free body.

## Validation

All checks reused the automation-provided symlink to existing pinned artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Lean outputs were written only to a fresh temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check && python3 scripts/stage1_target.py show THM-M-1067` | 0 | 1,546 unique targets passed; rank 509 is planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 typed edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement, four defect declarations, and obligation interfaces elaborated. Each defect theorem reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal bodies. |
| Prohibited-construct `rg` scan | expected no-match exit 1 | No prohibited proof construct occurs in owned Lean sources. |
| Frozen-input comparison from `b366bdd9` | 0 | Statement, proof certificate, obligation artifacts, anchor audit, and Lean locks are unchanged. |
| Pinned mathlib identity, Brownian-module test, and source search | expected module-test success for absence; search 0 | Revision/tree matched; Brownian module absent; the only search match was an unrelated Wiener-Ikehara comment. |
| `test ! -e .stage1-worker-selftest.json` and generated-output check | 0 | Completion self-test manifest and stray owned Lean outputs are absent. |

The exact isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-heade57cfb09-slot47.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
cp "$repo/Stage1_Instances/THM-M-1067/ObligationTree.lean" "$tmp/ObligationTree.lean"
lean=$(cd "$repo/Formalizations/Lean" && timeout 120 lake env which lean)
lean_path=$(cd "$repo/Formalizations/Lean" && timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" "$tmp/ObligationTree.olean"
```

The object hashes were `be965b25bd779d55ff6000d2fc721c1cef439ba3e2070e0b5218ca6f898b5164`
for `Statement.olean`, `1ac94b10534b168fe7f4df222b5e8797388021cfb942f6ee486c222eb4b04bae`
for `Proof.olean`, and `052930aeb6659bc098c0c1ad69807d3e3dc80ce4e644f01314f2c34b81d763f5`
for `ObligationTree.olean`.

## Retry boundary

Reopen `S56-M-1067-STATEMENT` and replace the malformed pushforward with a faithfully characterized
Lebesgue measure on nonnegative time. Then rerun and accept the statement identity, mutation,
anchor-audit, and versioned obligation-freeze phases in dependency order. After that repair, the
Brownian construction, estimates, convergence, continuity, measurability, and simultaneous
occupation identity still need actual placeholder-free proof bodies or an exact compatible audited
import.

No `.stage1-worker-selftest.json` is written. This packet is blocker evidence only: it does not
satisfy `S56-M-1067-PROOF`, close an obligation or root, change scheduler state, or support audit or
theorem completion.
