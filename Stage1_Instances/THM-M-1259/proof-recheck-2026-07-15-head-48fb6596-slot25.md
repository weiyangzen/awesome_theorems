# THM-M-1259 proof-phase blocker reaffirmation at base 48fb6596

Item: `S56-M-1259-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T14:53:14+08:00`

Base revision: `48fb6596b1844f4183c411142415d872ff21e842`

Base tree: `eb8dfff0e90b5ce5b11ac2096777060d62874064`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen target. The existing
owned, placeholder-free declaration

```text
Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget :
  Not Stage1Instances.THM_M_1259.hormanderTarget
```

freshly kernel-checks at trust level zero against the pinned Lean and mathlib artifacts.

The target permits `n = r = 0` and quantifies over every measure. At the zero measure,
`IsSmoothDistribution` characterizes only the zero distribution. In zero-dimensional Euclidean
space, bracket generation and coefficient smoothness are automatic, the bundled zero operator maps
the nonzero evaluation distribution to zero, and that zero image is smooth. The target would
therefore make the nonzero evaluation distribution smooth relative to the zero measure, a
contradiction.

This refutes only the overbroad frozen Lean encoding, not Hormander's mathematical theorem. No
positive proof body or proof receipt was added, no obligation was closed, and the item remains
`[ ]`. Lifecycle remains `planned`; predecessor records remain `[H2, M4, R3]`. The negative
evidence warrants fail-closed `[H5, M5, R3]`, but this proof worker does not mutate predecessor or
authoritative state. Audit and theorem completion are false. `.stage1-worker-selftest.json` is
deliberately absent because the assigned proof phase is not complete.

## Failed gate and retry

The first failed gate is exact-target consistency. Rev-5.6 section 3.1 makes `H5` a terminal
classification and blocks ordinary theorem-proof execution. Repair requires reopening
`S56-M-1259-STATEMENT`, binding a source-audited reference measure and every source-required
nondegenerate condition, and accepting a new exact-expression fingerprint and obligation-registry
version. The anchor audit, obligation tree, and proof phase must then be rerun against that repaired
target.

The current statement receipt is also stale: it records SHA-256 `50c18b67...28d5`, while the actual
statement source hashes to `8258728f...c0c7`, and its prose says Lebesgue measure although the Lean
root accepts arbitrary `Measure`. The source crosswalk does not contain the primary-source
transcription and assumption audit needed to guess a repair safely.

Even after repair, the localized commutator estimate and regularity bootstrap need real Lean proof
bodies or an eligible immutable pinned proof. The checked
`expandedCore_composes_hormanderTarget` is only a conditional wrapper from the unproved
`ExpandedHypoellipticCore` premise.

Thirty-four earlier proof-attempt, recheck, or blocker JSON packets were tracked before this run,
well beyond the five-tick split threshold. Splitting a positive proof of a refuted proposition
cannot help; scheduling must redirect to the statement dependency rather than issue the unchanged
proof task again. The sole predecessor `S56-M-1259-OBLIGATION_TREE` also remains provisional `[_]`,
not master-accepted `[x]`.

## Narrow validation

Commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network discovery, or dependency
mutation was run. The smallest real recheck invoked the existing `lake env lean` toolchain at trust
level zero, with `LEAN_PATH` obtained from the pinned project and a temporary `Statement.olean`.
This is narrow kernel evidence, not a hermetic, release, or completion receipt.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| isolated `lake env lean --trust=0 -t0` replay | 0 | `Statement.lean` and `Counterexample.lean` both elaborated; exits were `0,0`; the latter printed `[propext, Classical.choice, Quot.sound]` for `not_hormanderTarget`. |
| prohibited-construct scan over `Statement.lean` and `Counterexample.lean` | 1 | Expected no-match exit; no prohibited construct occurs. |
| `git diff --quiet c45f3c70..HEAD --` the five frozen proof inputs | 0 | Statement, counterexample, registry, graphs, and anchor audit are unchanged since the counterexample was integrated. |
| JSON parse, packet-invariant, and whitespace checks | 0 | The companion parses and its blocker boundary is internally consistent; both new artifacts are clean. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is correctly absent because the proof phase is blocked. |

The successful trust-zero replay ran from `2026-07-15T14:50:55+08:00` through
`2026-07-15T14:51:30+08:00`. Its statement and counterexample output SHA-256 values were,
respectively, `a65df923b3d080172ecece147795744282d5c908b6100d82cd24647762cabac6`
and `aa64bb5770bb5af2aee91a37c8eefca3ae90581899ef29779a8986b5110d1dd2`.
The counterexample axiom report includes:

```text
'Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

The replay recipe was:

```bash
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1259-proof-48fb6596.XXXXXX)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env which lean)

LEAN_NUM_THREADS=1 LEAN_PATH="$LP" "$LEAN" --trust=0 -t0 \
  -R "$repo/Stage1_Instances/THM-M-1259" \
  -o "$tmp/Statement.olean" \
  "$repo/Stage1_Instances/THM-M-1259/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$LP" "$LEAN" --trust=0 -t0 \
  -R "$repo/Stage1_Instances/THM-M-1259" \
  "$repo/Stage1_Instances/THM-M-1259/Counterexample.lean"
rm -rf "$tmp"
```

Only the prior slot25 blocker pair changed under this target between base `ec3b52a2` and current
base `48fb6596`; every semantic invalidation input is byte-identical. This packet is therefore a
current-base reaffirmation, not new mathematical evidence.

The structured JSON companion binds the exact blocker, input hashes, environment, commands, retry
condition, ownership, freshness, invalidation policy, and changed paths. It is not a proof receipt,
does not satisfy `S56-M-1259-PROOF`, and claims no scheduler transition or master acceptance.
