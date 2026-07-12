# Statement validation

Item: `S56-M-1268-STATEMENT`. Base revision:
`8da22023e24f307fb21f41ed93f69f2b8fa82879`.

The canonical target uses mathlib's `WeakSpace Real E`, `EReal`, and topological
`LowerSemicontinuous`. The Lean file contains only definitions, a checked definitional transport,
and separately elaborated mutations. It contains no proof of the target.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1268` | exit 0; rank 444, planned, L0/rework_required, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1268/Statement.lean` | exit 0; exact target, checked transport, and four mutations elaborated; explicit target printed |
| `python3 -m json.tool Stage1_Instances/THM-M-1268/statement.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1268 .stage1-worker-selftest.json` | exit 0; no output |

The direct imports were selected by narrow API probing: `WeakSpace` and its closure bridge come
from `WeakSpace`, the topological predicate comes from `Semicontinuity.Basic`, and the functional
codomain comes from `EReal.Basic`. Validation reused the canonical pinned `.lake` symlink and did
not update or mutate dependencies.

Known downstream failures: the primary-source edition/theorem/page crosswalk is not H0, no anchor
audit or obligation registry has been accepted, and no proof or release validation exists. These
do not invalidate statement elaboration but prevent audit and theorem completion.
