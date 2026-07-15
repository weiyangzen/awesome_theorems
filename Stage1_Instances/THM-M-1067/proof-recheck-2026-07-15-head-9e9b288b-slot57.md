# THM-M-1067 proof-phase recheck at `9e9b288b` (slot57)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T12:24:40+08:00`

Base: `9e9b288bc68d49399b5213338febc717e7624b76` / tree
`4af7553f47b9d96ae14915b2a728e9f0298be5cc`

## Verdict: blocked

The assigned proof phase cannot truthfully close on this base. The frozen definition

```lean
def nonnegativeLebesgue : Measure NNReal := Measure.map Real.toNNReal volume
```

is not Lebesgue measure on nonnegative time. `Real.toNNReal` collapses the whole nonpositive
half-line to zero, so this pushforward gives the singleton `{0}` infinite mass. At time zero, the
time integral of the indicator of zero is therefore infinite, whereas its spatial integral is zero
for every proposed `NNReal`-valued local-time field.

The existing placeholder-free certificate in `Proof.lean` was re-elaborated at kernel trust zero:

- `nonnegativeLebesgue_singleton_zero` proves `nonnegativeLebesgue {0} = infinity`;
- `occupation_at_zero_false` proves the frozen occupation identity fails at `t = 0` for every path
  and proposed field;
- `no_local_time_of_wiener` proves that no proposed field satisfies the frozen predicate under an
  `IsWienerMeasure` hypothesis;
- `target_iff_no_wiener_measure` proves that the frozen target is equivalent to nonexistence of its
  own Wiener measures.

This is negative kernel evidence for an exact-statement defect. It does not construct Brownian
local time and does not prove the canonical human theorem. Closing the formal target by asserting
that no Wiener measure exists would be a vacuous substituted theorem, which rev-5.6 forbids.

## Frozen proof surface

The proof inputs and Lean locks are unchanged since the current target packet was last integrated:

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

The obligation checker reports 17 obligations and 71 typed edges with an open `M4` root. All 15
machine-required obligations still have `terminal_proof_body_id: null`. The composition theorems
in `ObligationTree.lean` only consume assumed children and receive no existence-proof credit.

The pinned mathlib search found no Brownian-motion, Wiener-measure construction, local-time, or
occupation-density theorem. The only text match for the combined Brownian/Wiener/local-time search
was an unrelated Wiener-Ikehara comment. The external candidate already recorded in
`anchor-audit.md` has no local-time theorem, uses a different Lean version, and has admitted
dependencies. It cannot supply a terminal body.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. All Lean
outputs were created in fresh `/tmp` directories and removed. The automation-provided untracked
`.lake` symlink was reused read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 typed edges passed; denominator `7a96f4bf...`; root open `M4`. |
| Trust-zero isolated Lean recipe below | 0 | Statement, defect certificate, and composition interfaces elaborated. Each defect declaration reported exactly `[propext, Classical.choice, Quot.sound]`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal bodies. |
| Prohibited-construct `rg` scan | 1, expected | No prohibited proof construct occurs in owned Lean sources. |
| Pinned mathlib source search | 0 | One unrelated Wiener-Ikehara comment; no Brownian/local-time candidate. |
| Frozen-input comparison from `443b8bbc` to this base | 0 | Target proof inputs and Lean locks are unchanged. |
| Corrected-measure boundary probe | 0 | A restricted pushforward candidate gives `{0}` mass zero at trust zero; this is repair guidance, not an owned statement edit or proof receipt. |

The reproducible Lean recipe used Lake only in the pinned mathlib package, whose own manifest is
valid, then rewrote its nested package-cache paths to the canonical shared package paths:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-slot57-lakeenv.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
cp "$repo/Stage1_Instances/THM-M-1067/ObligationTree.lean" "$tmp/ObligationTree.lean"
cd "$repo/Formalizations/Lean/.lake/packages/mathlib"
lean_bin=$(lake env which lean)
lake_path=$(lake env printenv LEAN_PATH)
base_lean_path=${lake_path//\/Formalizations\/Lean\/.lake\/packages\/mathlib\/.lake\/packages/\/Formalizations\/Lean\/.lake\/packages}
LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" "$tmp/ObligationTree.olean"
```

Object hashes were:

- `Statement.olean`: `be965b25bd779d55ff6000d2fc721c1cef439ba3e2070e0b5218ca6f898b5164`;
- `Proof.olean`: `1ac94b10534b168fe7f4df222b5e8797388021cfb942f6ee486c222eb4b04bae`;
- `ObligationTree.olean`: `052930aeb6659bc098c0c1ad69807d3e3dc80ce4e644f01314f2c34b81d763f5`.

The repository-root `lake env lean` route is presently unavailable because the shared
`Formalizations/Lean/.lake/packages/flt-regular` artifact has `HEAD` pointing to
`refs/heads/.invalid`; this worker did not repair, fetch, or otherwise mutate it. The package-local
Lake route above still supplies a real pinned Lean 4.29 kernel replay using the existing mathlib
objects.

## Retry boundary

Reopen `S56-M-1067-STATEMENT` and replace the malformed time measure with a faithful nonnegative-time
measure. A checked concrete boundary repair candidate is

```lean
Measure.map Real.toNNReal ((volume : Measure Real).restrict (Set.Ici 0))
```

for which an ephemeral trust-zero probe proves singleton-zero mass is zero. After the repair, rerun
statement identity and mutation checks, the anchor audit, and a versioned obligation/graph freeze
in dependency order. The corrected theorem will still need the Brownian construction, estimates,
convergence, continuity, measurability, and simultaneous occupation-identity bodies, or an exact
compatible placeholder-free imported theorem.

This packet leaves `S56-M-1067-PROOF` at `[ ]`. It proposes no closed obligation, proof receipt,
audit completion, theorem completion, or master acceptance. Because the assigned proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.
