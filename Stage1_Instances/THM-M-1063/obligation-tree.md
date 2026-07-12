# THM-M-1063 obligation tree

This registry freezes the classical finite-second-moment Donsker route before proof closure is observed. Every mathematical node is open.

## M1063-ROOT

The normalized polygonal partial-sum processes converge in distribution in C([0,1], Real) to the specified standard Brownian path variable.

Formal target: `AwesomeTheorems.Stage1.THM_M_1063.DonskerInvariancePrinciple`

Output: The exact frozen Donsker target.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: The normalized polygonal partial-sum processes converge in distribution in C([0,1], Real) to the specified standard Brownian path variable.
3. Derive: The exact frozen Donsker target.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-S-DEFS

Freeze UnitInterval, polygonalValue, IsPolygonalWalk, IsStandardBrownian, and TendstoInDistribution with the exact binder order.

Formal target: `Definitions in DonskerTarget.lean`

Output: The exact objects and conclusion used by every proof node.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Freeze UnitInterval, polygonalValue, IsPolygonalWalk, IsStandardBrownian, and TendstoInDistribution with the exact binder order.
3. Derive: The exact objects and conclusion used by every proof node.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-S-DOMAINS

Fix both probability spaces, the Borel uniform topology on continuous paths, and all measurable structures and instances.

Formal target: `Measurable-space and BorelSpace context of DonskerInvariancePrinciple`

Output: No silent change of path topology, law, or probability space.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Fix both probability spaces, the Borel uniform topology on continuous paths, and all measurable structures and instances.
3. Derive: No silent change of path topology, law, or probability space.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-S-BOUNDARY

Account for n=0 totalization, t=0, t=1, positive sigma, and the clipped final interpolation segment.

Formal target: `Boundary package for polygonalValue`

Output: The total definition agrees with n normalized increments at t=1 and has the intended asymptotic domain.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Account for n=0 totalization, t=0, t=1, positive sigma, and the clipped final interpolation segment.
3. Derive: The total definition agrees with n normalized increments at t=1 and has the intended asymptotic domain.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-S-FOUNDATION

Freeze classical noncomputable measure theory, accepted Lean foundations, and the no-placeholder/no-oracle policy.

Formal target: `Foundation and trust certificate`

Output: An audited foundation profile for every admitted body.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Freeze classical noncomputable measure theory, accepted Lean foundations, and the no-placeholder/no-oracle policy.
3. Derive: An audited foundation profile for every admitted body.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-N-STANDARDIZE

Reduce the increments to centered variance-one variables by division by positive sigma.

Formal target: `X i / sigma with mean 0 and variance 1`

Output: A standardized iid sequence without changing the polygonal target.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Reduce the increments to centered variance-one variables by division by positive sigma.
3. Derive: A standardized iid sequence without changing the polygonal target.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-N-FIDI

Rewrite every finite linear combination of path evaluations as a triangular weighted sum of standardized increments plus a vanishing interpolation remainder.

Formal target: `Finite evaluation linear-combination identity`

Output: A scalar triangular-array expression suitable for Cramer-Wold.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Rewrite every finite linear combination of path evaluations as a triangular weighted sum of standardized increments plus a vanishing interpolation remainder.
3. Derive: A scalar triangular-array expression suitable for Cramer-Wold.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-B-FIDI

Prove convergence of every finite vector of polygonal evaluations to the Brownian evaluation vector.

Formal target: `Finite-dimensional distribution convergence for W n`

Output: All finite-dimensional marginals converge with covariance min(s,t).

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Prove convergence of every finite vector of polygonal evaluations to the Brownian evaluation vector.
3. Derive: All finite-dimensional marginals converge with covariance min(s,t).
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-B-TIGHT

Prove tightness of the complete sequence of polygonal path laws in the uniform topology.

Formal target: `Tight (fun n => Measure.map (W n) P)`

Output: Uniform path-space tightness under only a finite second moment.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Prove tightness of the complete sequence of polygonal path laws in the uniform topology.
3. Derive: Uniform path-space tightness under only a finite second moment.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-B-RECOMPOSE

Combine tightness and finite-dimensional convergence, identify all subsequential limits, and recover convergence of the whole sequence.

Formal target: `TendstoInDistribution W atTop B (fun _ => P) PB`

Output: The exact path-space convergence conclusion.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Combine tightness and finite-dimensional convergence, identify all subsequential limits, and recover convergence of the whole sequence.
3. Derive: The exact path-space convergence conclusion.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-C-PATH

Construct the polygonal interpolation as a continuous map and prove equality with polygonalValue.

Formal target: `forall n omega, C(UnitInterval, Real)`

Output: Continuous based polygonal paths with the frozen pointwise formula.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Construct the polygonal interpolation as a continuous map and prove equality with polygonalValue.
3. Derive: Continuous based polygonal paths with the frozen pointwise formula.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-C-MEAS

Prove measurability of every polygonal path random variable into the Borel uniform path space.

Formal target: `forall n, AEMeasurable (W n) P`

Output: Well-defined pushforward laws and applicability of convergence-in-distribution APIs.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Prove measurability of every polygonal path random variable into the Borel uniform path space.
3. Derive: Well-defined pushforward laws and applicability of convergence-in-distribution APIs.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-C-TRUNC

Choose a deterministic truncation scale and split increments into bounded centered parts and a rare large-jump remainder.

Formal target: `Triangular truncation and recentering package`

Output: A bounded array plus a remainder controlled by finite second moments.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Choose a deterministic truncation scale and split increments into bounded centered parts and a rare large-jump remainder.
3. Derive: A bounded array plus a remainder controlled by finite second moments.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-TAIL

Use finite second moment to show the accumulated large-jump contribution is negligible at diffusive scale.

Formal target: `Large-jump maximum tends to zero in probability`

Output: Removal of the truncation remainder uniformly over time.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Use finite second moment to show the accumulated large-jump contribution is negligible at diffusive scale.
3. Derive: Removal of the truncation remainder uniformly over time.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-MAX

Establish the required maximal inequality for centered independent bounded block sums.

Formal target: `Maximal partial-sum probability estimate`

Output: Control of oscillations inside time blocks.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Establish the required maximal inequality for centered independent bounded block sums.
3. Derive: Control of oscillations inside time blocks.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-MODULUS

Combine truncation and maximal estimates to control the uniform modulus of continuity of polygonal paths.

Formal target: `lim delta->0, limsup n, P(modulus(W n,delta)>eta)=0`

Output: The equicontinuity-in-probability criterion for tightness.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Combine truncation and maximal estimates to control the uniform modulus of continuity of polygonal paths.
3. Derive: The equicontinuity-in-probability criterion for tightness.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-ORIGIN

Control W n at the origin and uniform path magnitude using the same maximal estimates.

Formal target: `Tightness at one time and uniform boundedness in probability`

Output: The pointwise component of the path compactness criterion.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Control W n at the origin and uniform path magnitude using the same maximal estimates.
3. Derive: The pointwise component of the path compactness criterion.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-ASCOLI

Apply Arzela-Ascoli to turn uniform bounds and modulus control into compact subsets of continuous path space.

Formal target: `Compact containment from bounded equicontinuous path sets`

Output: Compact sets capturing arbitrarily large path-law mass.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Apply Arzela-Ascoli to turn uniform bounds and modulus control into compact subsets of continuous path space.
3. Derive: Compact sets capturing arbitrarily large path-law mass.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-TIGHT

Derive tightness of polygonal laws from compact containment.

Formal target: `Tight (fun n => Measure.map (W n) P)`

Output: The complete tightness branch.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Derive tightness of polygonal laws from compact containment.
3. Derive: The complete tightness branch.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-CLT

Prove the scalar triangular-array central limit theorem needed for finite linear combinations, preserving the variance calculation.

Formal target: `Weighted triangular-array CLT`

Output: Gaussian limits for the Cramer-Wold scalar projections.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Prove the scalar triangular-array central limit theorem needed for finite linear combinations, preserving the variance calculation.
3. Derive: Gaussian limits for the Cramer-Wold scalar projections.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-COV

Compute limiting covariances of polygonal evaluations as min(s,t).

Formal target: `lim n, Cov(W n s,W n t)=min s t`

Output: The covariance matrix of every limiting finite Gaussian vector.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Compute limiting covariances of polygonal evaluations as min(s,t).
3. Derive: The covariance matrix of every limiting finite Gaussian vector.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-CRAMER

Apply Cramer-Wold to the scalar projection limits.

Formal target: `Finite-vector convergence in distribution`

Output: Joint Gaussian finite-dimensional limits with the Brownian covariance.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Apply Cramer-Wold to the scalar projection limits.
3. Derive: Joint Gaussian finite-dimensional limits with the Brownian covariance.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-BROWNIAN-FIDI

Use the specified Brownian process predicate to match the limiting Gaussian vectors, including their zero means and covariance.

Formal target: `FDD(W n) -> FDD(B)`

Output: The complete finite-dimensional convergence branch.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Use the specified Brownian process predicate to match the limiting Gaussian vectors, including their zero means and covariance.
3. Derive: The complete finite-dimensional convergence branch.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-PROKHOROV

Extract weakly convergent subsequences of path laws from tightness.

Formal target: `Every subsequence has a weakly convergent subsubsequence`

Output: Candidate probability laws on continuous path space.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Extract weakly convergent subsequences of path laws from tightness.
3. Derive: Candidate probability laws on continuous path space.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-EVAL

Transport subsequential weak convergence through every finite continuous evaluation map.

Formal target: `Candidate-law finite-dimensional marginals equal Brownian marginals`

Output: Every subsequential limit has the target finite-dimensional laws.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Transport subsequential weak convergence through every finite continuous evaluation map.
3. Derive: Every subsequential limit has the target finite-dimensional laws.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-L-LAW-UNIQUE

Prove that probability laws on continuous paths are determined by finite evaluations on a countable dense time set.

Formal target: `Equality of path laws from finite-dimensional marginals`

Output: Every subsequential limit equals the law of B.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Prove that probability laws on continuous paths are determined by finite evaluations on a countable dense time set.
3. Derive: Every subsequential limit equals the law of B.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-T-SEQUENCE

Use uniqueness of all subsequential limits to prove convergence of the full sequence of laws.

Formal target: `Tendsto (law(W n)) atTop (law B)`

Output: Full weak convergence, not merely subsequential convergence.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Use uniqueness of all subsequential limits to prove convergence of the full sequence of laws.
3. Derive: Full weak convergence, not merely subsequential convergence.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-T-API

Translate weak convergence of pushforward laws into the frozen TendstoInDistribution declaration with its varying source measures.

Formal target: `TendstoInDistribution W atTop B (fun _ => P) PB`

Output: The exact target API with no assumed convergence premise.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Translate weak convergence of pushforward laws into the frozen TendstoInDistribution declaration with its varying source measures.
3. Derive: The exact target API with no assumed convergence premise.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-X-SCALAR-CLT

Audit and use the pinned mathlib scalar CLT only at the exact scalar leaf it supports.

Formal target: `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum[_sub]`

Output: A checked scalar anchor; never path-space closure.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Audit and use the pinned mathlib scalar CLT only at the exact scalar leaf it supports.
3. Derive: A checked scalar anchor; never path-space closure.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-X-SOURCE

Map root-relevant mathematical nodes to pinpoint human sources and errata review.

Formal target: `Human-source crosswalk overlay`

Output: Source classification only; no machine proof credit.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Map root-relevant mathematical nodes to pinpoint human sources and errata review.
3. Derive: Source classification only; no machine proof credit.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.

## M1063-X-PROVENANCE

Record proof-body, dependency, axiom, unsafe, automation, and external-project provenance.

Formal target: `Formal provenance overlay`

Output: Provenance classification only; no proof credit.

Semantic ledger:
1. Consume each registered incoming premise at its exact planned signature.
2. Establish the named transition: Record proof-body, dependency, axiom, unsafe, automation, and external-project provenance.
3. Derive: Provenance classification only; no proof credit.
4. Pass that output through the typed parent edge without strengthening assumptions.

Boundary: Architecture only; no proof body or closure credit is assigned by this node.
