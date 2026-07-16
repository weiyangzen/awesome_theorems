# Statement validation

`Stage1Instances.THM_M_0105.RiemannRochTarget` elaborates the intake-selected
curve/divisor formula under the pinned Lean and mathlib environment. The source
uses exactly three deletion-essential direct imports for geometric
integrality, properness, and relative smoothness.

The validator serializes the fully explicit target, binds its SHA-256 and the
complete Lean stdout, checks the definitional expansion and its axiom report,
and verifies four distinct exact-type mutations: removed hypothesis, changed
domain, changed binder scope, and boundary case. It also binds the selected
statement record, Lean source, and source crosswalk by SHA-256 and Git blob.

This is worker-local M3 statement evidence only. The typed divisor and
cohomology interfaces still require concrete downstream transports, the source
review remains open, and no theorem proof or terminal decision is claimed.
