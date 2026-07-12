# Frozen obligation tree

Item: `S56-M-1286-OBLIGATION_TREE`  
Freeze date: 2026-07-12

The registry freezes 18 semantic obligations before proof status is credited. Every obligation is
root-relevant. Sixteen require machine evidence; the source boundary is human-only and the
provenance boundary is an informational release overlay. Eligibility cannot change without a new
registry version and append-only delta.

## M1286-ROOT

The exact root is `Stage1Instances.THM_M_1286.PolyaSzegoTarget`. Its proof graph requires the
conditional terminal composition `M1286-T-ASSEMBLE`, which in turn requires two open packages:

1. `M1286-C-REARRANGE`: construct a measurable, `MemLp`, symmetric decreasing function that is
   equimeasurable with the input. Its children expose the distribution function, centered-ball
   radius construction, and the proof of all construction invariants.
2. `M1286-L-GRADIENT`: construct a weak gradient of the rearrangement and bound its `eLpNorm`.
   Its children expose the smooth estimate, coarea, isoperimetry, Sobolev approximation, and weak
   lower-semicontinuity passage.

The statement, boundary, foundation, and normalization nodes refine the root without pretending to
be independent proof premises. Source, trust, documentation, provenance, and workflow relations
live in separate typed graphs and receive no machine proof credit.

## Composition certificate

`ObligationTree.lean` defines exact planned signatures for `RearrangementConstruction` and
`GradientEstimate`. The theorem `exactTarget_of_packages` consumes both and elaborates to the exact
frozen root. This checks architecture only: neither analytic package is proved here.

## Status boundary

The root remains `M4`. No exact anchor exists in the audited pinned sources, and no obligation-tree
artifact proves the rearrangement construction, coarea formula, isoperimetric inequality,
approximation theorem, lower semicontinuity, or the Polya-Szego theorem. The remaining root cut set
is exactly `M1286-C-REARRANGE` and `M1286-L-GRADIENT`.
