# THM-M-1067 proof-phase recheck at `72a35d5f` (slot58)

Item: `S56-M-1067-PROOF`

Recorded at: `2026-07-15T08:12:40+08:00`

Base revision: `72a35d5f64e32233c0bc77a57e47bd078475ad74`

Base tree: `a80eb91ed5629dee62d031e78bc87b509cf8e6eb`

## Verdict

`blocked`. A positive body for the intended Brownian-local-time theorem cannot truthfully be added
to the current frozen statement. Trust-zero replay confirms the pre-existing, placeholder-free
certificate in `Proof.lean`:

```text
Stage1Instances.THM_M_1067.nonnegativeLebesgue_singleton_zero :
  nonnegativeLebesgue {0} = top

Stage1Instances.THM_M_1067.no_local_time_of_wiener :
  IsWienerMeasure W -> Not (IsBrownianLocalTime W L)

Stage1Instances.THM_M_1067.target_iff_no_wiener_measure :
  BrownianLocalTimeTarget <-> Not (Exists W, IsWienerMeasure W)
```

`Statement.lean` defines `nonnegativeLebesgue` as `Measure.map Real.toNNReal volume`.
`Real.toNNReal` sends the whole nonpositive half-line to zero, so this pushforward assigns infinite
mass to `{0}`. At `t = 0`, the time integral of the zero indicator is therefore infinite, whereas
the corresponding spatial singleton integral is zero for every `NNReal`-valued field. Hence no
field satisfies the frozen occupation identity under a Wiener measure.

This refutes the frozen encoding's intended meaning, not the mathematical Brownian-local-time
theorem. The equivalence above offers no legal positive proof: it would require proving that no
Wiener measure exists, which is mathematically false and would be a vacuous substitution for the
requested theorem. The current environment also contains no such proof.

The item remains `[ ]`. No positive root body, terminal body, composition receipt, state change,
audit completion, theorem completion, validation, release, or master acceptance is claimed.
`.stage1-worker-selftest.json` is deliberately absent because the proof phase is not complete.

## Failed gate and retry

The first failed gate is exact-statement fidelity at `M1067-S-BOUNDARY`. This is an effective `M5`
statement mismatch under the rev-5.6 machine-debt rules. The accepted instance snapshot remains
`[H2, M3, R4]`, while the frozen typed graph still records an open `M4` root; this worker changes
neither predecessor authority.

The dependency `S56-M-1067-OBLIGATION_TREE` is only worker-provisional `[_]`, not master-accepted
`[x]`. Its registry has 17 obligations, of which 15 are machine-required, and all 15 have
`terminal_proof_body_id: null`. The checked composition declarations merely assume their open
mathematical children and receive no proof credit.

Positive work must first reopen `S56-M-1067-STATEMENT`, replace the malformed pushforward with a
faithful nonnegative-time Lebesgue measure, rerun statement identity and mutation gates, re-audit
anchors, and publish a versioned obligation/graph re-freeze. The corrected target would then still
need the Brownian interface, occupation-density approximation, estimates, convergence, limiting
field, continuity, measurability, and simultaneous occupation-identity bodies, or an exact
compatible placeholder-free external theorem. The pinned audit found neither a mathlib terminal
body nor an eligible external one.

## Validation

All checks reused the automation-provided symlink to canonical pinned artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Lean outputs were written only to a fresh `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | Rank 509; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations and 71 typed edges passed; denominator `7a96f4bf...`; root open `M4`. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1067/Proof.lean` | 1 | Direct invocation cannot resolve the sibling `import Statement` because no target-owned `Statement.olean` is on `LEAN_PATH`; no source error was inferred. |
| Isolated trust-zero Lean recipe below | 0 | Statement and all four defect declarations elaborated. Each defect declaration reports exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| Required-body `jq` assertion | 0 | All 15 machine-required obligations have null terminal proof-body IDs. |
| Prohibited-construct `rg` scan | 1, expected | No prohibited proof construct occurs in owned Lean sources. |
| Pinned environment identity checks | 0 | Lean 4.29.0 commit `98dc76e3...`; mathlib commit/tree `8a178386...` / `bdc39a31...`; lock hashes matched. |
| Frozen-input comparison from `5bb51543` to this base | 0 | Statement, proof certificate, obligation artifacts, anchor audit, and Lean locks are unchanged. |
| JSON packet invariant checks | 0 | Identity, hashes, open state, blocker flags, commands, and absent self-test agree. |
| `git diff --check -- Stage1_Instances/THM-M-1067` | 0 | No whitespace errors in the owned patch. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The exact isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1067-slot58-head-72a35d5f.XXXXXX)
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

The prohibited-construct scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern|external)(?:[[:space:]]|$)' \
  Stage1_Instances/THM-M-1067 --glob '*.lean'
```

## Status boundary

This is current-base, nonrelease proof-blocker evidence. It does not satisfy
`S56-M-1067-PROOF`, propose `[_]` or `[x]`, close an obligation or the root, or support audit or
theorem completion. Retry begins with authorized statement correction and dependency-ordered
re-freezing, not another proof search against the unchanged encoding.
