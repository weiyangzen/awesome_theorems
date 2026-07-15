# THM-M-1259 proof-phase current-base recheck

Item: `S56-M-1259-PROOF`

Base revision: `d1933ff69a2dc943cd3203497ab9cf9fe79f4e58`

Base tree: `8eca89518ce485e51886ee61d92b6251d0df7dc7`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen target. The
placeholder-free declaration
`Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget` has type
`Not Stage1Instances.THM_M_1259.hormanderTarget`, and the current-base trust-zero replay elaborated
it successfully.

The counterexample instantiates the target with `n = r = 0`, the top open set, zero coefficients,
the zero-dimensional zero operator, and the zero measure. Bracket generation holds because the
tangent space is a subsingleton. The nonzero evaluation distribution has zero image, and that image
is smooth relative to the zero measure, while any distribution represented by a density relative
to the zero measure must be zero. The target's asserted hypoellipticity therefore contradicts the
nonzero evaluation distribution.

This refutes only the broadened frozen Lean encoding, not Hormander's mathematical theorem. The
proof worker did not weaken or replace the target and did not modify predecessor-phase artifacts.
The assigned item stays `[ ]`; lifecycle stays `planned`; proof-phase completion, root closure,
audit completion, theorem completion, release, and master acceptance are all false. No
`.stage1-worker-selftest.json` was written.

## First Failed Gate

The first failed gate is exact-target consistency. Under rev-5.6, a refuted target is negative
evidence, not a proof candidate. Repair requires reopening `S56-M-1259-STATEMENT`, binding the
source-intended reference measure and source-required nondegenerate conditions, and accepting a new
statement fingerprint and obligation-registry version. Anchor audit, obligation-tree construction,
and proof execution must then be repeated against the repaired target.

The predecessor `S56-M-1259-OBLIGATION_TREE` is only provisional `[_]`, not master-accepted `[x]`.
That independently blocks proof acceptance. Even after a statement repair, the frozen architecture
identifies the localized commutator estimate and regularity bootstrap as substantial open
formalization work. Those obligations need real local proof bodies or an eligible immutable pinned
proof; the existing conditional composition wrapper does not close them.

## Validation

All commands ran from the worker automation clone. The automation-provided canonical `.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, network
discovery, or other dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete |
| isolated trust-zero recipe below | 0 | `statement_exit=0`; `counterexample_exit=0`; `not_hormanderTarget` axioms `[propext, Classical.choice, Quot.sound]` |
| scoped prohibited-construct scan below | 1 | expected no-match exit; neither Lean file contains a prohibited construct |
| predecessor JSON parse and DAG query | 0 | registry/graphs parse; obligation-tree `[_]`; proof `[ ]` |
| frozen-input diff from `c45f3c70` | 0 | `Statement.lean`, `Counterexample.lean`, registry, graphs, and anchor audit are unchanged |
| packet JSON, invariants, whitespace, and self-test absence | 0 | packet is valid; no whitespace diagnostic; self-test manifest remains absent |

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

It ran from `2026-07-15T15:45:58+08:00` through `2026-07-15T15:46:13+08:00`.
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

The statement receipt is also stale: it records statement hash `50c18b67...` while the actual hash
is `8258728f...`, and its Lebesgue-measure prose disagrees with the universal `Measure` binder in
the elaborated root. The source crosswalk does not supply an immutable primary-source transcription
and full assumption audit for a replacement target.

This packet is current-base nonrelease blocker evidence and an actionable retry record. It is not a
proof receipt and does not satisfy `S56-M-1259-PROOF`.
