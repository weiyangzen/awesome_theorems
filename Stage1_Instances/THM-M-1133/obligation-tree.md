# THM-M-1133 frozen obligation tree

Registry v1 freezes the standard strict-perturbation architecture. Open debt is intentional; this is not a proof-completion claim.

## M1133-ROOT

**Claim:** The exact classical weak heat-equation maximum principle frozen in Statement.lean.

**Role:** supplies `A boundary maximizer for every classical caloric function on the closed cylinder.` through the typed graph.

**Formal target:** `Stage1Instances.THM_M_1133.HeatEquationWeakMaximumPrinciple`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `A boundary maximizer for every classical caloric function on the closed cylinder.`; budget `40` substantive steps.

**Boundary and status:** `[H2, M3, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-S-INTERFACE

**Claim:** Preserve the closed cylinder, parabolic boundary, coordinate Laplacian, regularity, and forward heat sign convention.

**Role:** supplies `The exact elaborated vocabulary of the root.` through the typed graph.

**Formal target:** `Stage1Instances.THM_M_1133.{ClosedCylinder,ParabolicBoundary,spatialLaplacian,IsClassicalCaloricOn}`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `The exact elaborated vocabulary of the root.`; budget `40` substantive steps.

**Boundary and status:** `[H2, M0-L, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-S-BOUNDARY

**Claim:** Prove compactness and nonemptiness of the closed cylinder and characterize points outside the parabolic boundary, including the terminal-time interior case.

**Role:** supplies `A compact nonempty domain and an exhaustive boundary/interior split.` through the typed graph.

**Formal target:** `planned cylinder compactness/nonemptiness and boundary-membership declarations`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `A compact nonempty domain and an exhaustive boundary/interior split.`; budget `80` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-S-FOUNDATION

**Claim:** Audit classical extrema, choice, imports, transitive axioms, TCB, and the no-oracle boundary.

**Role:** supplies `An accepted trust boundary for every terminal body.` through the typed graph.

**Formal target:** `planned transitive axiom and TCB certificate`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `An accepted trust boundary for every terminal body.`; budget `40` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-N-SUBSOLUTION

**Claim:** Generalize the equality-form heat equation to the forward subsolution inequality without changing domain, regularity, or boundary.

**Role:** supplies `The exact subsolution proposition used by the analytic proof.` through the typed graph.

**Formal target:** `Stage1Instances.THM_M_1133.{IsClassicalSubcaloricOn,WeakSubsolutionMaximumPrinciple}`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `The exact subsolution proposition used by the analytic proof.`; budget `40` substantive steps.

**Boundary and status:** `[H2, M0-L, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-N-PERTURB

**Claim:** For epsilon > 0 form v(x,t)=u(x,t)-epsilon*t and prove strict forward subcaloricity, continuity, and unchanged spatial regularity.

**Role:** supplies `A strict subsolution converging uniformly back to u.` through the typed graph.

**Formal target:** `planned strict perturbation construction and invariant package`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `A strict subsolution converging uniformly back to u.`; budget `100` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-L-EXTREMUM

**Claim:** Use compactness and continuity to obtain a global maximizer of the perturbed function on the closed cylinder.

**Role:** supplies `A selected cylinder maximizer with global comparison.` through the typed graph.

**Formal target:** `planned IsCompact.exists_isMaxOn bridge`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `A selected cylinder maximizer with global comparison.`; budget `60` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-B-LOCATION

**Claim:** Split the selected maximizer into parabolic-boundary membership or a spatial-interior point at positive time, and prove exhaustiveness.

**Role:** supplies `Either the desired boundary witness or the forbidden interior branch.` through the typed graph.

**Formal target:** `planned parabolic-boundary/interior dichotomy`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `Either the desired boundary witness or the forbidden interior branch.`; budget `80` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-L-SPATIAL

**Claim:** At a spatial interior maximum prove vanishing first spatial derivative and nonpositive coordinate second derivatives, hence nonpositive Laplacian.

**Role:** supplies `Delta_x v is nonpositive at the selected interior point.` through the typed graph.

**Formal target:** `planned local-maximum Hessian/Laplacian sign package`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `Delta_x v is nonpositive at the selected interior point.`; budget `100` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-B-TIME

**Claim:** Split positive time into t<T and t=T, preserving the one-sided cylinder maximum information in both cases.

**Role:** supplies `An exhaustive interior-time or terminal-time branch.` through the typed graph.

**Formal target:** `planned time endpoint dichotomy`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `An exhaustive interior-time or terminal-time branch.`; budget `60` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-L-TIME

**Claim:** At the cylinder maximizer prove the time derivative is zero for 0<t<T and nonnegative for t=T using the left-hand maximum inequality.

**Role:** supplies `partial_t v is nonnegative at every nonboundary maximizer.` through the typed graph.

**Formal target:** `planned temporal derivative sign package`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `partial_t v is nonnegative at every nonboundary maximizer.`; budget `100` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-T-STRICT

**Claim:** Combine the temporal and spatial derivative signs to contradict the strict subsolution inequality at a nonboundary maximizer.

**Role:** supplies `Every perturbed strict subsolution has a boundary maximizer.` through the typed graph.

**Formal target:** `planned strict-subsolution maximum-on-boundary theorem`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `Every perturbed strict subsolution has a boundary maximizer.`; budget `80` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-T-LIMIT

**Claim:** Let epsilon decrease to zero and transfer the perturbed boundary estimate to the original subsolution without assuming a convergent choice of maximizers.

**Role:** supplies `The full weak subsolution maximum principle.` through the typed graph.

**Formal target:** `planned epsilon inequality limit theorem`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `The full weak subsolution maximum principle.`; budget `100` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-T-ASSEMBLE

**Claim:** Specialize the subsolution principle to heat-operator equality and compose it into the exact root.

**Role:** supplies `The exact canonical target, conditional only on the open subsolution package.` through the typed graph.

**Formal target:** `Stage1Instances.THM_M_1133.root_of_subsolutionMaximumPrinciple`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `The exact canonical target, conditional only on the open subsolution package.`; budget `30` substantive steps.

**Boundary and status:** `[H2, M0-L, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-X-SOURCE

**Claim:** Pinpoint every proof transition in a primary PDE source, map assumptions, check errata, and obtain independent source review.

**Role:** supplies `Accepted human-source coverage.` through the typed graph.

**Formal target:** `human-source ledger and independent review`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `Accepted human-source coverage.`; budget `100` substantive steps.

**Boundary and status:** `[H2, M5, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.

## M1133-X-PROVENANCE

**Claim:** Inventory terminal proof bodies, wrappers, imports, axioms, automation, and replay boundaries.

**Role:** supplies `Release provenance coverage without proof credit.` through the typed graph.

**Formal target:** `planned proof-body provenance and trust closure`

**Step ledger:** premises are exactly the proof-graph children; the inference is the claim above; output is `Release provenance coverage without proof credit.`; budget `60` substantive steps.

**Boundary and status:** `[H2, M4, R3]`. Frozen architecture or conditional interface only; M0-L marks checked local structure, not the open analytic package or root.
