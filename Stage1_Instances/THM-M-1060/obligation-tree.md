# THM-M-1060 obligation tree

This registry freezes a polygonal-approximation proof route before proof closure is observed. All nodes are open architecture obligations.

## M1060-ROOT

SchilderTarget for every Wiener measure on BasedPath.

Formal target: `Stage1Instances.THM_M_1060.SchilderTarget`

Output: The exact canonical target.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: The exact canonical target.
3. Discharge the registered parent composition edge without an undeclared premise.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-S-DEFINITIONS

Fix BasedPath, scaling, Wiener finite-dimensional laws, the small-noise LDP, and the Cameron-Martin rate.

Formal target: `Statement.lean definitions used by SchilderTarget`

Output: Exact objects and binder order used by every later node.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Fix BasedPath, scaling, Wiener finite-dimensional laws, the small-noise LDP, and the Cameron-Martin rate.
3. Derive: Exact objects and binder order used by every later node.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-S-BOUNDARY

Retain the horizon [0,1], epsilon tending to zero from above, empty sets, and extended-real conventions.

Formal target: `Boundary package for SchilderTarget`

Output: No finite-dimensional, one-sided, or assumed-LDP substitution enters the proof.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Retain the horizon [0,1], epsilon tending to zero from above, empty sets, and extended-real conventions.
3. Derive: No finite-dimensional, one-sided, or assumed-LDP substitution enters the proof.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-S-FOUNDATION

Freeze classical noncomputable measure theory, choice, and kernel trust policy.

Formal target: `Foundation and trust certificate`

Output: An audited foundation profile for every eventual proof body.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Freeze classical noncomputable measure theory, choice, and kernel trust policy.
3. Derive: An audited foundation profile for every eventual proof body.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-N-WIENER

Derive the increment, covariance, and path-law facts needed from IsWienerMeasure.

Formal target: `IsWienerMeasure W -> Wiener increment and covariance interface`

Output: A usable Wiener-law interface without assuming any LDP conclusion.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Derive the increment, covariance, and path-law facts needed from IsWienerMeasure.
3. Derive: A usable Wiener-law interface without assuming any LDP conclusion.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-N-LDP

Translate the epsilon-log filter convention to the finite-dimensional and exponential-equivalence formulations used below.

Formal target: `Equivalence of SmallNoiseLDP bounds with the selected auxiliary normalizations`

Output: Correct signs, speed, filters, and empty-set behavior in both directions.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Translate the epsilon-log filter convention to the finite-dimensional and exponential-equivalence formulations used below.
3. Derive: Correct signs, speed, filters, and empty-set behavior in both directions.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-C-PROJECTION

Construct dyadic polygonal interpolation and its finite evaluation map on BasedPath.

Formal target: `Dyadic projection P_n : BasedPath -> BasedPath with measurable/continuous evaluation maps`

Output: A based piecewise-linear approximation with all measurability and compatibility invariants.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Construct dyadic polygonal interpolation and its finite evaluation map on BasedPath.
3. Derive: A based piecewise-linear approximation with all measurability and compatibility invariants.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-L-GAUSSIAN

Prove the small-noise LDP for each finite Gaussian increment vector.

Formal target: `Finite-dimensional centered Gaussian LDP with quadratic covariance rate`

Output: Open and closed finite-dimensional bounds at speed 1/epsilon.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Prove the small-noise LDP for each finite Gaussian increment vector.
3. Derive: Open and closed finite-dimensional bounds at speed 1/epsilon.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-L-PROJECTED

Transport the finite Gaussian LDP through dyadic polygonal interpolation.

Formal target: `Small-noise LDP for Measure.map P_n (Measure.map (scale (sqrt epsilon)) W)`

Output: An LDP for every fixed polygonal approximation with its discrete energy.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Transport the finite Gaussian LDP through dyadic polygonal interpolation.
3. Derive: An LDP for every fixed polygonal approximation with its discrete energy.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-L-MODULUS

Establish the Brownian modulus-of-continuity exponential tail bound uniformly at small noise.

Formal target: `lim n -> infinity, limsup epsilon -> 0+, epsilon * log P(||sqrt epsilon W-P_n(sqrt epsilon W)||>=delta)=-infinity`

Output: Exponential approximation of scaled paths by dyadic interpolants.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Establish the Brownian modulus-of-continuity exponential tail bound uniformly at small noise.
3. Derive: Exponential approximation of scaled paths by dyadic interpolants.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-L-EXP-EQUIV

Apply a proved exponential-approximation transfer theorem to the projected laws.

Formal target: `Exponential approximation transfer for open/closed LDP bounds`

Output: Path-space lower and upper bounds with the limiting candidate rate.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Apply a proved exponential-approximation transfer theorem to the projected laws.
3. Derive: Path-space lower and upper bounds with the limiting candidate rate.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-L-RATE-ID

Identify the supremum of dyadic discrete energies with cameronMartinRate.

Formal target: `sup_n discreteEnergy n f = cameronMartinRate f`

Output: The transferred LDP uses exactly the frozen Cameron-Martin rate.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Identify the supremum of dyadic discrete energies with cameronMartinRate.
3. Derive: The transferred LDP uses exactly the frozen Cameron-Martin rate.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-T-LOWER

Derive the open-set lower bound for every Wiener measure.

Formal target: `forall W, IsWienerMeasure W -> forall G, IsOpen G -> -(sInf (rate '' G)) <= liminf ...`

Output: The first conjunct of SmallNoiseLDP.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: The first conjunct of SmallNoiseLDP.
3. Discharge the registered parent composition edge without an undeclared premise.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-T-UPPER

Derive the closed-set upper bound for every Wiener measure.

Formal target: `forall W, IsWienerMeasure W -> forall F, IsClosed F -> limsup ... <= -(sInf (rate '' F))`

Output: The second conjunct of SmallNoiseLDP.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: The second conjunct of SmallNoiseLDP.
3. Discharge the registered parent composition edge without an undeclared premise.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-C-CM-WITNESS

Relate integral-representation witnesses to absolutely continuous based paths and their a.e. derivatives.

Formal target: `Cameron-Martin witness equivalence and energy uniqueness`

Output: A representation-independent energy characterization.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Relate integral-representation witnesses to absolutely continuous based paths and their a.e. derivatives.
3. Derive: A representation-independent energy characterization.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-L-RATE-LSC

Prove lower semicontinuity of cameronMartinRate in the uniform path topology.

Formal target: `LowerSemicontinuous cameronMartinRate`

Output: Closed real sublevel sets.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Prove lower semicontinuity of cameronMartinRate in the uniform path topology.
3. Derive: Closed real sublevel sets.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-L-SUBLEVEL-BOUND

Prove uniform boundedness and equicontinuity of every finite-energy sublevel using Cauchy-Schwarz.

Formal target: `Equicontinuity and uniform boundedness of {f | cameronMartinRate f <= a}`

Output: Relative compactness of each real sublevel.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Prove uniform boundedness and equicontinuity of every finite-energy sublevel using Cauchy-Schwarz.
3. Derive: Relative compactness of each real sublevel.
4. Pass the output through the registered typed edge without changing the target.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-T-GOOD

Combine closedness and relative compactness to prove compactness of every real rate sublevel.

Formal target: `forall a : Real, IsCompact {f | cameronMartinRate f <= a}`

Output: The third conjunct of SmallNoiseLDP.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: The third conjunct of SmallNoiseLDP.
3. Discharge the registered parent composition edge without an undeclared premise.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-T-COMPOSE

Conjoin the exact open lower, closed upper, and goodness conclusions for each Wiener measure.

Formal target: `SchilderTarget from the three exact conjunct packages`

Output: The complete SmallNoiseLDP conclusion with no undeclared premise.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: The complete SmallNoiseLDP conclusion with no undeclared premise.
3. Discharge the registered parent composition edge without an undeclared premise.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-X-SOURCE

Map every root-relevant proof node to exact primary and modern source pinpoints and errata review.

Formal target: `Human-source crosswalk overlay`

Output: Source-boundary classification only; no machine proof credit.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: Source-boundary classification only; no machine proof credit.
3. Discharge the registered parent composition edge without an undeclared premise.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.

## M1060-X-PROVENANCE

Record terminal proof-body, wrapper, dependency, axiom, and unsafe/oracle provenance.

Formal target: `Formal provenance overlay`

Output: Provenance classification only; no proof credit without checked bodies.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: Provenance classification only; no proof credit without checked bodies.
3. Discharge the registered parent composition edge without an undeclared premise.

Boundary: Architecture only; this node has no accepted proof body and does not close the root.
