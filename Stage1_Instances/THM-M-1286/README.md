# THM-M-1286 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Polya-Szego inequality. The Stage0 phrase
"symmetrization lowers the Dirichlet integral" is resolved here to the finite-`p`, whole-space
Sobolev inequality for Schwarz symmetric decreasing rearrangement. That choice prevents later work
from silently substituting an elementary finite rearrangement inequality or only the `p = 2` case.

The structured claim is in `intake.json`, the inclusions and exclusions are in `scope_map.md`, and
the source-to-statement mapping is in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: the repository search found no candidate rearrangement declaration,
and neither an elaborated expression nor an environment fingerprint exists. The primary-source
pinpoint and errata audit also remain open. This intake is not theorem completion.

## Open task DAG

`STATEMENT` must select or define the exact Sobolev, weak-gradient, equimeasurability, and symmetric
decreasing rearrangement interfaces and elaborate the root. `ANCHOR_AUDIT` must then search pinned
mathlib and external Lean projects and finish the source audit. Only afterward may the obligation
registry separate rearrangement construction, equimeasurability, coarea/isoperimetric estimates,
approximation/lower-semicontinuity, and the root composition.

## Validation

The exact intake-only checks and their results are recorded in `validation.md`. They validate target
membership, repository structure, JSON syntax, scoped references, and the absence of forbidden proof
devices. They provide no kernel-proof evidence.
