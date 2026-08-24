# Machine-checked audit

Machine level claimed by this worker: **M0-L** with a trust-zero, cold
from-source replay obligation for the canonical Master.

The closure census and dependency graph are recorded in `machine-closure.json`
and are sealed together with the semantic environment digest from
`statement-crosswalk.json`.  No placeholder, unsafe declaration, claim-local
oracle, or remaining machine cut is admitted by the task-local preflight.

The three Lean surfaces all carry the frozen provider import string and
qualified declaration in a provenance comment, while using `import Mathlib`
for the standalone compilation surface.  This preserves the exact frozen
provenance without treating the numeric provider path as a local replacement.

The Master must recompute the elaborated root and every transitive non-
foundation constant before accepting this receipt.
