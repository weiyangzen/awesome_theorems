# THM-M-1259 proof-phase blocker

Item: `S56-M-1259-PROOF`  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`  
Validation date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`: the exact frozen Lean target is false, so no placeholder-free positive proof body can
truthfully inhabit it. The assigned item remains `[ ]`; no proof, audit-completion,
theorem-completion, release, or master-acceptance claim is made.

The existing owned declaration
`Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget` kernel-checks

```text
Not Stage1Instances.THM_M_1259.hormanderTarget
```

The counterexample uses cases admitted by the frozen target. Set `n = 0`, `r = 0`, the domain to
`top`, all coefficients to zero, and `mu` to the zero measure. The tangent space is a subsingleton,
so the bracket-span premise holds, and the bundled formal adjoint is the zero operator. Evaluation
at the unique point is a nonzero scalar distribution whose image is the zero distribution. That
image has a smooth zero density relative to the zero measure, while every distribution represented
by any density relative to the zero measure is zero. The demanded hypoellipticity conclusion is
therefore contradictory.

This is stronger than the older missing-library diagnosis in `proof-validation.md`: the current
target is refutable, not merely unsupported by pinned mathlib. It refutes only the broadened Lean
encoding, not Hormander's mathematical theorem. Proving the conventional Lebesgue-measure theorem,
silently excluding the boundary case, or assuming the analytic core would substitute a different
target and earns no proof credit.

The predecessor graph remains unreconciled at `[H2, M4, R3]`. The checked refutation proposes
`[H5, M5, R3]` under rev-5.6 section 3: `H5` blocks ordinary proof execution and `M5` records the
statement mismatch. This worker does not rewrite predecessor or scheduler state. Because the
positive proof phase cannot be completed, `.stage1-worker-selftest.json` is deliberately absent.

## First Failed Gate

The first failed gate is exact-target consistency. Repair requires reopening the statement phase,
binding the intended Lebesgue measure and source-faithful nondegenerate domain conditions, then
freezing a new statement fingerprint and obligation-registry version. The anchor audit, obligation
tree, and proof execution must then be repeated against that repaired target.

## Scoped Validation

All checks ran in this worker clone against the existing pinned Lake closure. No `lake update`,
`lake build`, dependency clone/fetch, or other dependency mutation was performed. The Lean replay
used a temporary `Statement.olean` outside the repository and removed it afterward.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | rank 161; planned; hard-mathlib-anchor lane; theorem incomplete |
| isolated `lake env lean --trust=0` recipe below | 0 | exact statement and counterexample elaborated; the refutation's axiom report was `[propext, Classical.choice, Quot.sound]` |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1259/Statement.lean Stage1_Instances/THM-M-1259/Counterexample.lean` | 1 | no prohibited construct; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-1259/proof-blocker-2026-07-14.json` | 0 | blocker JSON syntax valid |
| `git diff --check -- Stage1_Instances/THM-M-1259` | 0 | no whitespace errors |

Exact Lean recipe, run from the repository root:

```bash
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH="$LP" "$LEAN" --trust=0 -R Stage1_Instances/THM-M-1259 \
  -o "$tmp/Statement.olean" Stage1_Instances/THM-M-1259/Statement.lean
LEAN_PATH="$tmp:$LP" "$LEAN" --trust=0 -R Stage1_Instances/THM-M-1259 \
  Stage1_Instances/THM-M-1259/Counterexample.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Final source SHA-256 values:

- `Statement.lean`: `8258728ff71980a4431fb47213487c8d7655c64d0dd0f3ab2e9b058f8a95c0c7`
- `Counterexample.lean`: `91e1610bf3fab308b7d8025415eae1db9e2d284a7e06c415baf3be47bfa74ad1`
- `obligation_registry.json`: `2eb6b3db5d79dbed5b9f22dd467cfb964b15a3441927919e635670715342d1a0`

This is real negative kernel evidence and an actionable blocker. It does not satisfy
`S56-M-1259-PROOF`, close the positive root, or support theorem completion.
