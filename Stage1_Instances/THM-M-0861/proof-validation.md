# THM-M-0861 proof-phase validation

## Scope

`Proof.lean` closes the exact `LowerBoundTarget`: at each actual vertex it restricts a proper edge
coloring to the subtype of incident edge identities, proves that restriction injective, compares
its finite cardinality with `Fin k`, and lifts the pointwise bounds through `Finset.sup`. It also
proves `DegreeBound G (maxDegree G vertexFinite)`, constructs a proper coloring whenever the whole
edge-set cardinality is at most the palette size, and checks conditional upper/root composition
from an explicit `BoundedSatzCTarget` premise.

The premise is not hidden or credited. No inhabitant of `BoundedSatzCTarget`, `UpperBoundTarget`, or
the canonical root is declared.

## Pinned replay

From the repository root:

```bash
python3 -B Stage1_Instances/THM-M-0861/check_proof.py
```

The checker derives `lean` and `LEAN_PATH` with `lake env`, compiles `Statement.lean` and
`ObligationTree.lean` into a temporary directory, then elaborates `Proof.lean` with `--trust=0`.
It also verifies the pinned mathlib revision, receipt hashes and boundaries, exact declaration
markers, and a comment-aware prohibited-construct scan. The expected result is exit 0,
`check_proof: ok`, and exactly nine axiom reports containing only `propext`, `Classical.choice`, and
`Quot.sound`.

No `lake update`, `lake build`, clone, fetch, or dependency-cache mutation is part of the recipe.
The automation-provided canonical `.lake` symlink is reused read-only, so this is warm-cache worker
evidence rather than release evidence.

## Commands and results

Executed from worker-clone revision `51c2828e82ffb19860830f78b771f80e13ad7dff`:

| command | exit | result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard OK: 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest OK: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0861` | 0 | rank 1415, planned, L0/rework required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0861/check_proof.py` | 0 | nine declarations elaborated with `--trust=0`; each axiom report was exactly `propext`, `Classical.choice`, `Quot.sound`; prohibited-construct scan passed |
| `python3 -m json.tool .stage1-worker-selftest.json >/dev/null` and both owned proof JSON files | 0 | all worker packet, receipt, and blocker JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0861-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0861/check_proof.py` | 0 | checker syntax passed without owned-path cache output |
| `git diff --check -- Stage1_Instances/THM-M-0861 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The historical predecessor command
`python3 -B Stage1_Instances/THM-M-0861/check_obligation_tree.py` exited 1 before Lean replay because
that old receipt checker hard-codes its own earlier base revision. This is a freshness limitation of
the predecessor receipt, not evidence for this proof packet; the proof checker independently
recompiles the exact current `Statement.lean` and `ObligationTree.lean` inputs.

## Open gate

The first failed gate is `M0861-T-SATZ-C`. Pinned mathlib has Hall/matching and simple-graph
coloring substrate, but no exact finite bipartite multigraph edge-coloring theorem. The frozen
edge-deletion, missing-color, alternating-trail, bipartite endpoint, swap, and insertion packages
therefore remain open. The remaining root cut is `M0861-T-UPPER`. Partial closure proposes
H1/M2/R4 under the rev-5.6 debt definition; accepted authority stays H1/M4/R4 until master review.
Source/readability, validation, independent replay, release, and master acceptance do not change.
