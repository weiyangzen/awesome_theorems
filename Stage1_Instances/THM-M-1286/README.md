# THM-M-1286 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Polya-Szego inequality. The Stage0 phrase
"symmetrization lowers the Dirichlet integral" is resolved here to the finite-`p`, whole-space
Sobolev inequality for Schwarz symmetric decreasing rearrangement. That choice prevents later work
from silently substituting an elementary finite rearrangement inequality or only the `p = 2` case.

The structured claim is in `intake.json`, the inclusions and exclusions are in `scope_map.md`, and
the source-to-statement mapping is in `source_statement_crosswalk.md`.

## Current verdict

Lifecycle is `planned`; the root remains `[H2, M4, R3]`. The exact Lean statement and environment
fingerprint now exist, and the anchor audit found no exact proof candidate at the recorded immutable
revisions. The first failed theorem gate is proof architecture and closure: the rearrangement,
equimeasurability, weak-gradient energy, and limiting arguments are not formalized. The
primary-source pinpoint and errata audit also remain open. This dossier is not theorem completion.

## Task DAG

`STATEMENT` has selected the exact Sobolev, weak-gradient, equimeasurability, and symmetric decreasing
rearrangement interfaces and elaborated the root. `ANCHOR_AUDIT` searched the pinned mathlib tree and
an identified external Lean project at immutable revisions; `anchor-audit.md` records why the nearby
declarations do not close the target. The next phase may now freeze obligations for rearrangement
construction, equimeasurability, coarea/isoperimetric estimates, approximation/lower-semicontinuity,
and root composition. The root remains open.

## Validation

The exact intake-only checks and their results are recorded in `validation.md`. They validate target
membership, repository structure, JSON syntax, scoped references, and the absence of forbidden proof
devices. They provide no kernel-proof evidence.
