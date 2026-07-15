# THM-M-1259 proof-phase current-base recheck

Item: `S56-M-1259-PROOF`

Base revision: `255c85c9e88403358cd081cd624f3b90eb808654`

Base tree: `5165028b1b2e17baadaf6a4936b14b7b5fd8c9ed`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen target. The existing
placeholder-free declaration

```text
Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget :
  Not Stage1Instances.THM_M_1259.hormanderTarget
```

freshly kernel-checks at trust level zero against the pinned Lean and mathlib artifacts.

The counterexample instantiates the target with `n = r = 0`, the top open set, zero coefficients,
the zero-dimensional zero operator, and the zero measure. Bracket generation holds because the
tangent space is a subsingleton. The nonzero evaluation distribution has zero image, and that image
is smooth relative to the zero measure, while every distribution represented by a density relative
to the zero measure is zero. The asserted hypoellipticity conclusion is therefore contradictory.

This refutes only the broadened frozen Lean encoding, not Hormander's mathematical theorem. The
proof worker did not weaken or replace the target and did not modify predecessor-phase artifacts.
The assigned item stays `[ ]`; lifecycle stays `planned`; proof-phase completion, root closure,
audit completion, theorem completion, release, and master acceptance are all false. No
`.stage1-worker-selftest.json` was written because the assigned proof phase is not complete.

## First Failed Gate

The first failed gate is exact-target consistency. Under rev-5.6, a refuted target is negative
evidence rather than a positive proof candidate. Repair requires reopening
`S56-M-1259-STATEMENT`, binding the source-intended reference measure and every source-required
nondegenerate condition, and accepting a new exact-expression fingerprint and obligation-registry
version. The anchor audit, obligation tree, and proof phase must then be rerun against the repaired
target.

The predecessor `S56-M-1259-OBLIGATION_TREE` is only provisional `[_]`, not master-accepted `[x]`.
That independently blocks proof acceptance. Even after a statement repair, the frozen architecture
identifies the localized commutator estimate and regularity bootstrap as substantial open
formalization work. Those obligations need real proof bodies or an eligible immutable pinned proof;
the existing conditional composition wrapper does not close them.

The statement receipt is also stale. It records statement SHA-256 `50c18b67...a28d5`, while the
actual statement source hashes to `8258728f...c0c7`, and its prose calls the measure Lebesgue while
the elaborated root universally quantifies an arbitrary `Measure`. The source crosswalk lacks an
immutable primary-source transcription and full assumption audit from which this proof worker could
truthfully infer a repaired statement.

Forty-seven earlier proof-attempt, recheck, or blocker JSON packets were present before this run,
well beyond the five-tick split threshold. Splitting a positive proof of a refuted proposition
cannot help; scheduling must redirect to the statement dependency rather than issue another
unchanged proof task.

## Validation

All commands ran from this worker automation clone. The automation-provided canonical `.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, network
discovery, or dependency mutation was run. This is narrow current-clone kernel evidence, not a
hermetic release receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete |
| isolated trust-zero recipe below | 0 | `statement_exit=0`; `counterexample_exit=0`; `not_hormanderTarget` axioms `[propext, Classical.choice, Quot.sound]` |
| scoped prohibited-construct scan below | 1 | expected no-match exit; neither Lean file contains a prohibited construct |
| predecessor JSON parse and DAG query | 0 | registry/graphs parse; obligation-tree `[_]`; proof `[ ]` |
| frozen-input diff from `c45f3c70` | 0 | `Statement.lean`, `Counterexample.lean`, registry, graphs, and anchor audit are unchanged |

The isolated Lean recipe was:

```bash
repo=$PWD
tmp=$(mktemp -d)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 600 "$LEAN" --trust=0 -t0 \
  -R "$repo/Stage1_Instances/THM-M-1259" -o "$tmp/Statement.olean" \
  "$repo/Stage1_Instances/THM-M-1259/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$LP" timeout 600 "$LEAN" --trust=0 -t0 \
  -R "$repo/Stage1_Instances/THM-M-1259" \
  "$repo/Stage1_Instances/THM-M-1259/Counterexample.lean"
rm -rf "$tmp"
```

It ran from `2026-07-15T18:39:22+08:00` through `2026-07-15T18:39:37+08:00`.
The statement output digest was
`a65df923b3d080172ecece147795744282d5c908b6100d82cd24647762cabac6`; the counterexample
output digest was `aa64bb5770bb5af2aee91a37c8eefca3ae90581899ef29779a8986b5110d1dd2`.

The scoped prohibited-construct scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|\bexternal\b' \
  Stage1_Instances/THM-M-1259/Statement.lean \
  Stage1_Instances/THM-M-1259/Counterexample.lean
```

## Evidence Identity

- Lean toolchain: `leanprover/lean4:v4.29.0`
- Lean commit: `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- `Statement.lean`: `8258728ff71980a4431fb47213487c8d7655c64d0dd0f3ab2e9b058f8a95c0c7`
- `Counterexample.lean`: `91e1610bf3fab308b7d8025415eae1db9e2d284a7e06c415baf3be47bfa74ad1`
- `obligation_registry.json`: `2eb6b3db5d79dbed5b9f22dd467cfb964b15a3441927919e635670715342d1a0`
- `typed_graphs.json`: `d48d5c6724a1716e82685ad535cfc8dcc1df6f3f75fc5fe691d6e13fcab7259b`

This packet is current-base nonrelease blocker evidence and an actionable retry record. It is not a
proof receipt and does not satisfy `S56-M-1259-PROOF`.
