# THM-M-0510 rev-5.6 dossier

This directory is the fail-closed `planned` dossier for the Hardy-Ramanujan asymptotic formula for
the ordinary integer partition function. The conventional mathematical target is

`p(n) ~ exp(pi * sqrt(2*n/3)) / (4*n*sqrt(3))` as `n -> infinity`,

where `p(n)` counts unordered partitions of the nonnegative integer `n` into positive integers.
The statement phase freezes this conventional claim as
`Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget`. Its full constant-factor target,
definitional expansion, boundary convention, and four structural mutations elaborate in the pinned
Lean environment with two minimal direct imports. This is pending master acceptance and is not a
proof or a claim that the primary-source audit is complete.

The root remains `[H2, M3, R4]`: exact source pinpointing and independent review are open, and only
the statement rather than a proof has been elaborated. Statement commands and results are in
`statement-validation.md`; the earlier intake evidence remains in `validation.md`.

## Frozen proof architecture

The obligation-tree phase freezes a 17-obligation circle-method architecture in
`obligation-registry.json`, with separate typed proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs in `typed-graphs.json`. This is a coverage denominator and proof
plan, not proof evidence. The Euler-product, contour, modular-transformation, major-arc, minor-arc,
source, and foundation obligations remain open; the root remains `M3` and theorem completion is not
claimed. See `obligation-tree.md` for the exact phase boundary.
