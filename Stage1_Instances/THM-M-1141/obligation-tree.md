# THM-M-1141 obligation tree

The registry is frozen at v1. All nodes below are obligations, not proof claims.

## m1141-root

**root.** The exact compact-subset Harnack inequality.

Formal target: `Stage1Instances.THM_M_1141.HarnackInequality`. Machine debt: `M3`. Step budget: 40.
## m1141-l-local

**core_lemma.** Prove a dimension-uniform local Harnack estimate on a ball whose closure lies in the domain.

Formal target: `planned local-ball Harnack lemma for HarmonicOnNhd`. Machine debt: `M4`. Step budget: 100.
## m1141-l-positive

**lemma.** Preserve strict positivity and justify every division and comparison multiplication.

Formal target: `planned positivity/nonzero denominator package`. Machine debt: `M4`. Step budget: 40.
## m1141-c-cover

**construction.** Extract a finite interior ball cover of the compact set, with quantitative room inside the domain.

Formal target: `planned compact finite subcover package`. Machine debt: `M4`. Step budget: 80.
## m1141-c-chain

**construction.** Use connectedness of the open domain to build finite overlapping-ball chains between cover centers.

Formal target: `planned connected-domain Harnack-chain package`. Machine debt: `M4`. Step budget: 100.
## m1141-l-propagate

**core_lemma.** Propagate local comparisons along each finite chain and control the product constant.

Formal target: `planned finite-chain comparison lemma`. Machine debt: `M4`. Step budget: 80.
## m1141-t-uniform

**assembly.** Take a finite maximum/product to obtain one A independent of u, x, and y.

Formal target: `Stage1Instances.THM_M_1141.UniformValueComparison`. Machine debt: `M4`. Step budget: 80.
## m1141-t-ratio

**transport.** Convert symmetric value comparison into the exact two-sided ratio bound with C > 1.

Formal target: `Stage1Instances.THM_M_1141.harnackInequality_of_uniformValueComparison`. Machine debt: `M0-L`. Step budget: 40.
## m1141-x-source

**source_boundary.** Map every analytic and topological leaf to inspected human proof passages.

Formal target: `human source crosswalk; no Lean proposition`. Machine debt: `not_applicable`. Step budget: 40.
## m1141-x-trust

**certificate.** Audit axioms, imports, TCB, and absence of oracle or placeholder proof credit.

Formal target: `planned transitive trust report`. Machine debt: `M4`. Step budget: 40.
## m1141-x-provenance

**certificate.** Bind terminal proof bodies and validation evidence to immutable revisions and hashes.

Formal target: `planned provenance receipt`. Machine debt: `informational`. Step budget: 40.

The root remains M3 and theorem completion is false.
