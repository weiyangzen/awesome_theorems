# THM-M-1067 proof-phase recheck at `5bb51543` (slot53)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T07:59:56+08:00`

Base revision: `5bb515438bd0e1d53584e5243c5d434dfde7158e`

Base tree: `8055b8d863f0978f110a628ab3ccc7ab1e146b12`

## Verdict

`blocked`. No legal positive proof body can close the intended Brownian-local-time claim from the
current frozen statement. The tracked, placeholder-free declarations in `Proof.lean` instead give
a trust-zero checked certificate that the statement's time measure is malformed:

```text
Stage1Instances.THM_M_1067.nonnegativeLebesgue_singleton_zero :
  nonnegativeLebesgue {0} = top

Stage1Instances.THM_M_1067.no_local_time_of_wiener :
  IsWienerMeasure W -> Not (IsBrownianLocalTime W L)

Stage1Instances.THM_M_1067.target_iff_no_wiener_measure :
  BrownianLocalTimeTarget <-> Not (Exists W, IsWienerMeasure W)
```

`nonnegativeLebesgue` was defined as `Measure.map Real.toNNReal volume`. Since `Real.toNNReal`
maps the entire nonpositive half-line to zero, this measure assigns infinite mass to `{0}`. At
`t = 0`, the time integral of the indicator of `{0}` is therefore infinite, while its spatial
Lebesgue integral against any finite `NNReal`-valued proposed field is zero. Thus every proposed
field fails the frozen occupation identity under a Wiener measure.

This is a checked refutation of the frozen encoding's intended meaning, not a refutation of the
mathematical Brownian-local-time theorem and not a positive proof of the canonical human claim.
Using the reverse implication of `target_iff_no_wiener_measure` would require proving that no
Wiener measure exists, a mathematically false premise and a forbidden vacuity substitution.

The item remains `[ ]`. No positive root body, terminal body, composition receipt, state change,
audit completion, theorem completion, validation, release, or master acceptance is claimed.
`.stage1-worker-selftest.json` is deliberately absent because the requested proof phase is not
genuinely complete.

## Failed Gate And Retry

The first failed gate is the rev-5.6 exact-statement and boundary-normalization gate at
`M1067-S-BOUNDARY`: the purported nonnegative-time Lebesgue measure is not Lebesgue measure on
`NNReal`. Under section 3.2 this is an effective `M5` statement mismatch. The accepted instance
surface remains provisionally `[H2, M3, R4]`, and the frozen typed graph still records an open
`M4` root; this worker proposes the fail-closed diagnosis without rewriting either predecessor.

The prerequisite `S56-M-1067-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`, so proof acceptance would also be dependency-blocked. Its registry contains 17 obligations,
15 machine-required; every required obligation has `terminal_proof_body_id: null`. The checked
composition interfaces in `ObligationTree.lean` assume their mathematical children and earn no
proof credit.

Positive execution must reopen `S56-M-1067-STATEMENT`, replace the full-real pushforward with a
faithful nonnegative-time Lebesgue measure (for example, push forward real volume restricted to
`Ici 0`), rerun boundary and mutation checks, re-audit candidates, and publish a versioned re-freeze
of the registry and typed graphs. Proof work would then still need the Wiener
interface, mollified-density construction, moment and Cauchy estimates, limiting field, joint
continuity, measurability, and simultaneous occupation-identity packages, or an exact compatible
placeholder-free external theorem. The pinned mathlib audit found no Brownian-motion or local-time
terminal theorem; the recorded external project has no local-time theorem, targets Lean 4.31
rather than 4.29, and has admitted dependencies.

The authoritative DAG records `attempts: 0` and no children. The master or scheduler must
reconcile this checked statement blocker and redirect to statement repair rather than repeat
proof-only search against the unchanged encoding. This worker did not edit the DAG or checklist.

## Validation

All checks reused the automation-provided symlink to existing canonical pinned artifacts. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Lean outputs were confined to a fresh directory under `/tmp` and removed. The untracked
dependency-cache symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; planned; `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 typed edges passed; denominator `7a96f4bf...`; root open M4. |
| Isolated pinned Lean trust-zero recipe below | 0 | Statement, defect proof, and obligation interfaces elaborated. The four public defect declarations report exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal proof-body IDs. |
| Prohibited-token `rg` scan below | 1 | Expected no-match: no prohibited construct occurs in the owned Lean sources. |
| Pinned environment identity checks | 0 | Lean 4.29.0 commit `98dc76e3...`; mathlib revision/tree `8a178386...` / `bdc39a31...`; toolchain and manifest hashes matched. |
| Structured evidence validation | 0 | JSON parsed and current-base identities, hashes, blocker flags, open arrays, and absent completion manifest agreed. |
| Explicit new-file whitespace checks | 0 | No whitespace errors in either new blocker artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The exact isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-slot53-head-5bb51543.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-1067/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1067/Proof.lean" "$tmp/Proof.lean"
cp "$repo/Stage1_Instances/THM-M-1067/ObligationTree.lean" "$tmp/ObligationTree.lean"
lean=$(cd "$repo/Formalizations/Lean" && timeout 120 lake env which lean)
lean_path=$(cd "$repo/Formalizations/Lean" && timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean" \
  >"$tmp/proof.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" >"$tmp/obligation.log" 2>&1
cat "$tmp/statement.log" "$tmp/proof.log" "$tmp/obligation.log"
```

The generated object hashes were `be965b25bd779d55ff6000d2fc721c1cef439ba3e2070e0b5218ca6f898b5164`
for `Statement.olean`, `1ac94b10534b168fe7f4df222b5e8797388021cfb942f6ee486c222eb4b04bae`
for `Proof.olean`, and `052930aeb6659bc098c0c1ad69807d3e3dc80ce4e644f01314f2c34b81d763f5`
for `ObligationTree.olean`. The combined kernel-output SHA-256 was
`33616edc9fb3843ec874f14cd32bc77fb0bc2d3c415c8b761c296d02535d3e16`.

The exact prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern|external)(?:[[:space:]]|$)' \
  Stage1_Instances/THM-M-1067 --glob '*.lean'
```

## Status Boundary

This is current-base, nonrelease proof-blocker evidence. It does not satisfy
`S56-M-1067-PROOF`, propose `[_]` or `[x]`, close an obligation or the root, or support audit or
theorem completion. The retry begins with authorized statement correction and dependency-ordered
re-freezing, not another proof attempt against this target.
