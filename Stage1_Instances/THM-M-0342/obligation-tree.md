# THM-M-0342 frozen obligation tree

Registry version 1 freezes 15 root-relevant obligations before proof-phase closure is credited. The
exact root is the elaborated `PlancherelTarget`, including every dimension `n`, the zero-dimensional
case, complex-valued representatives, the volume measure, exponent 2, and the `MemLp.toLp` passage.

The machine route is frozen from the exact specialized norm anchor through
`MeasureTheory.Lp.norm_fourier_eq` and its `LinearIsometryEquiv.norm_map` projection. The underlying
isometry construction owns separate obligations for `extendOfIsometry`, its two dense-range inputs,
the Schwartz-space norm identity, and the Schwartz Fourier equivalence. This prevents the short
public theorem from hiding its analytic bridge and construction work. `M0342-T-ASSEMBLE` is the
only local composition theorem: Lean checks that the open exact anchor implies the exact root, but
the obligation-tree phase does not credit that anchor as an accepted proof body.

Source, foundation/trust, provenance/evidence, and readable documentation are independent nodes.
The graph bundle contains separate proof, refinement, provenance, evidence, trust, documentation,
workflow, and source graphs. Every node has a semantic ledger, stable validation recipe, and a step
budget no greater than 100. The pinned norm theorem and isometry construction share their terminal
bodies rather than receiving wrapper or alias duplication credit.

The current root cut set is `M0342-C-ANCHOR`, `M0342-X-SOURCE`, `M0342-X-FOUNDATION`,
`M0342-X-PROVENANCE`, and `M0342-X-DOCUMENTATION`. Root status remains M2 and theorem completion is
false pending proof-phase integration and all later rev-5.6 gates.
