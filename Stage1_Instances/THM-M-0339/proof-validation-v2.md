# THM-M-0339 proof-phase validation (partial execution v2)

Item: `S56-M-0339-PROOF`. Base revision:
`443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`.

## Implemented Bodies

`Proof.lean` imports the exact `MSSPartitionStatement` frozen in `Statement.lean`. It rechecks the
existing `r = 1`, `d = 0`, and `m = 0` bodies and adds exact branches for `m <= r`, any frozen
right-hand side at least one, `delta >= 1`, and `delta = 0`. The `m <= r` proof assigns distinct
colors and reduces every fiber to a singleton or the empty sum. The large-bound proof assigns one
color and uses the identity-sum hypothesis.

`mssPartitionStatement_of_hardRegimeEngine` performs an exhaustive, exact-target case split. Its
remaining premise retains the original conclusion only for positive `d,m`, `1 < r < m`, and
`0 < delta < 1`. This is a materially narrower interface than the former circular
`PartitionEngine := Root`, but it is still an explicit premise. The mixed-characteristic-
polynomial, real-rootedness, interlacing, barrier, and Theorem 1.4 packages remain absent.

The registry gives these branches planned rather than exact formal fingerprints, so this packet
claims partial progress toward `M0339-S-BOUNDARY`, `M0339-B-RONE`, `M0339-B-RMANY`,
`M0339-T-COR15`, and `M0339-T-ASSEMBLE`; it claims zero whole frozen obligations closed. The root
stays `[H1, M4, R4]`, and `theorem_complete=false`.

## Commands And Results

Commands ran in the worker clone on 2026-07-15 (Asia/Shanghai). No update, build, dependency
clone/fetch, network validation, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0339` | 0 | rank 832, lifecycle `planned`, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0339/check_obligation_tree.py` | 0 | 19 obligations and 35 typed edges passed; root remains open M4 at `M0339-L-THEOREM14` |
| `bash Stage1_Instances/THM-M-0339/check_proof.sh` | 0 | isolated trust-zero replay elaborated the exact statement and all eight local declarations; each reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0339/Proof.lean)` | 1 | required recipe is blocked before Lean: shared pinned `flt-regular` checkout cannot resolve `HEAD`; no cache repair was attempted |
| prohibited-device scan over `Proof.lean` | 1 (expected) | no executable `sorry`, `admit`, `sorryAx`, axiom/constant/opaque/unsafe/extern declaration, `implemented_by`, or `native_decide` |
| `python3 Stage1_Instances/THM-M-0339/check_proof.py` | 0 | source, exact target, frozen hashes, pins, receipt/blocker boundary, changed paths, and worker packet passed |
| `git diff --check -- Stage1_Instances/THM-M-0339 .stage1-worker-selftest.json` | 0 | no whitespace errors |

`check_proof.sh` selects the pinned Lean 4.29.0 executable from `lean-toolchain`, constructs
`LEAN_PATH` only from the already-materialized pinned build directories, compiles a temporary
`Statement.olean`, and checks `Proof.lean` with `--trust=0 -t0`. Temporary output is removed. This
fallback is fresh kernel evidence for the covered declarations, but the broken mandated top-level
Lake recipe remains a known nonrelease failure rather than being hidden.

## Boundary

The first failed mathematical gate is `M0339-L-THEOREM14`. The exact root remains conditional on
`HardRegimeEngine`; no root closure, validation/release result, accepted state, source/readability
closure, hermetic replay, independent verification, audit completion, or theorem completion is
claimed. The worker packet proposes `[_]` only for this self-tested partial proof contribution;
master acceptance remains required.
