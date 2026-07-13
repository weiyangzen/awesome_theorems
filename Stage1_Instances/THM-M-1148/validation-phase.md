# THM-M-1148 validation-phase evidence

Item: `S56-M-1148-VALIDATION`. Base revision:
`2d334dfd1443fdb9dbdf08b9d53d6c67399ec7af`.

This phase rechecks the proof proposal without changing its mathematics. The structured recipe
copies `Statement.lean`, `PoissonUnitDisk.lean`, `Proof.lean`, and a separately composed
`Validation.lean` into a temporary directory. Bubblewrap denies network access for every Lean
subrecipe, exposes the repository and pinned dependencies read-only, and runs Lean with `--trust=0`
through the pinned `lake env lean` adapter. The validation module
does not import `Proof.lean`; it reconstructs the final implication from `generalDiskConstruction`
to the exact frozen `PoissonIntegralFormula` target.

## Commands and results

All commands ran in this worker clone on 2026-07-14. No `lake update`, build, clone, fetch, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered manifest has 1546 unique targets. |
| `python3 scripts/stage1_target.py show THM-M-1148` | 0 | Rank 353; planned; theorem completion false. |
| `bash Stage1_Instances/THM-M-1148/check_proof.sh` | 1 | Its Lean phase passed all 28 declarations; its old structural checker then correctly failed because it is bound to the superseded proof-worker base revision. |
| `python3 -B Stage1_Instances/THM-M-1148/check_validation.py` | 0 | Network-isolated trust-zero replay, axiom checks, local provenance, fail-closed decisions, and packet checks passed. |
| `env PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-1148/check_validation.py` | 1 | Negative fixture rejected disabled Python assertions. |
| `python3 Stage1_Instances/THM-M-1148/check_statement.py` | 0 | Exact expression hash and all five mutation distinctions passed. |
| `python3 Stage1_Instances/THM-M-1148/check_anchor_audit.py` | 0 | Pinned mathlib anchor boundary and installed revision agreed. |
| `python3 Stage1_Instances/THM-M-1148/check_obligation_tree.py` | 0 | Frozen 26-obligation denominator and 51 typed edges passed. |
| `git diff --check -- Stage1_Instances/THM-M-1148 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The fresh replay reported exactly `[propext, Classical.choice, Quot.sound]` for all 21 selected
unit-disk declarations, seven proof declarations, and the separately composed validation root.
It found no `sorryAx` and the comment-aware source scan rejected `sorry`, `admit`, custom axioms,
bodyless constants, unsafe declarations, native-oracle shortcuts, or external implementations.

## Gate decisions

The narrow kernel and direct local provenance observations pass, but the validation verdict is
`blocked`. The proof prerequisite has only provisional `[_]` worker state, its receipt is bound to
an earlier base revision, the local task DAG and frozen typed graphs still have no accepted proof or
closed obligation, and the implemented Mobius-transform route has not been reconciled with the
frozen near/far-arc architecture.

Release-grade provenance also fails closed. The adapted ATLAS upstream source is not vendored for
offline comparison, and the vendored CC BY-NC 4.0 license plus no-training/no-evaluation rider has
not received a compatibility decision. The replay uses the canonical pinned but warm shared
dependency cache, not a new checkout with an empty cache and offline archive restoration. The
separately written validation proof still shares this worker identity, checkout, Lean binary, and
cache, so it is differential evidence rather than the required distinct signed independent runner.

The accepted vector remains conservatively `H2/M4/R4`, with no accepted closed obligations.
`audit_complete` and `theorem_complete` remain false. This packet is provisional worker self-test
evidence only; it is not E0/E1, release evidence, master acceptance, or theorem completion.

The outer Python checker is not itself network-sandboxed; it performs local file, process, Git, and
hash checks only. Accordingly, the structured network claim is limited to the Lean subrecipes.
