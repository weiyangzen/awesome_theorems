# THM-M-1065 obligation tree

Registry version 1 freezes 18 obligations before proof work. Every node below is open architecture unless explicitly described as a kernel-checked composition interface.

## M1065-ROOT

Prove the exact normalized KMT strong-approximation target.

Formal target: `Stage1Instances.THM_M_1065.KMTStrongApproximationTarget`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Prove the exact normalized KMT strong-approximation target.
3. Produce: the exact canonical target.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-S-LAW

Preserve the probability, integrability, centering, variance-one, and two-sided exponential-moment assumptions.

Formal target: `AdmissibleLaw mu`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Preserve the probability, integrability, centering, variance-one, and two-sided exponential-moment assumptions.
3. Produce: the unchanged input-law package.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-S-EVENT

Preserve the running maximum over every 1 <= k <= n and the strict C log n + x threshold.

Formal target: `DiscrepancyEvent X Y C x n`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Preserve the running maximum over every 1 <= k <= n and the strict C log n + x threshold.
3. Produce: the exact measurable-event target.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-S-BOUNDARY

Handle n >= 1, x >= 0, positive constants, and ENNReal probability comparison without changing inequalities.

Formal target: `KMT boundary and coercion package`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Handle n >= 1, x >= 0, positive constants, and ENNReal probability comparison without changing inequalities.
3. Produce: the exact boundary conventions.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-S-FOUNDATION

Audit classical choice, noncomputable measure constructions, measurability, and the transitive trust closure.

Formal target: `foundation/trust certificate`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Audit classical choice, noncomputable measure constructions, measurability, and the transitive trust closure.
3. Produce: an admissible trust profile.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-C-SPACE

Construct one probability space carrying both infinite sequences.

Formal target: `exists Omega, MeasurableSpace Omega, P, X, Y`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Construct one probability space carrying both infinite sequences.
3. Produce: a common-space coupling carrier.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-L-X-LAWS

Prove every X increment has law mu on the constructed probability space.

Formal target: `forall i, HasLaw (X i) mu P`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Prove every X increment has law mu on the constructed probability space.
3. Produce: the prescribed marginal laws.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-L-X-INDEP

Prove the X increments are mutually independent.

Formal target: `ProbabilityTheory.iIndepFun X P`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Prove the X increments are mutually independent.
3. Produce: iid independence for X.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-L-Y-LAWS

Prove every Y increment has the standard real Gaussian law.

Formal target: `forall i, HasLaw (Y i) (gaussianReal 0 1) P`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Prove every Y increment has the standard real Gaussian law.
3. Produce: the Gaussian marginal laws.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-L-Y-INDEP

Prove the Y increments are mutually independent.

Formal target: `ProbabilityTheory.iIndepFun Y P`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Prove the Y increments are mutually independent.
3. Produce: iid independence for Y.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-L-EVENT-MEAS

Establish measurability of every finite-horizon discrepancy event used by the measure bound.

Formal target: `MeasurableSet (DiscrepancyEvent X Y C x n)`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Establish measurability of every finite-horizon discrepancy event used by the measure bound.
3. Produce: well-formed probability events.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-C-CONSTANTS

Construct law-dependent C, K, lambda that are strictly positive and uniform in n and x.

Formal target: `exists C K lambda, 0 < C and 0 < K and 0 < lambda`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Construct law-dependent C, K, lambda that are strictly positive and uniform in n and x.
3. Produce: uniform positive constants.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-L-BLOCK-COUPLING

Establish the quantitative finite-block coupling estimate from the exponential-moment law assumptions.

Formal target: `finite-block KMT coupling interface`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Establish the quantitative finite-block coupling estimate from the exponential-moment law assumptions.
3. Produce: the quantitative coupling input.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-L-MAXIMAL-TAIL

Upgrade the coupling estimate to the maximum of all partial-sum discrepancies through n.

Formal target: `P (DiscrepancyEvent X Y C x n) <= ofReal (K * exp (-lambda*x))`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Upgrade the coupling estimate to the maximum of all partial-sum discrepancies through n.
3. Produce: the uniform exponential maximal tail.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-T-WITNESS

Assemble the probability-space, law, independence, constant, and tail fields into one exact witness package.

Formal target: `CouplingData mu with TailGuarantee`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Assemble the probability-space, law, independence, constant, and tail fields into one exact witness package.
3. Produce: an exact root witness for each admissible mu.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-T-COMPOSE

Eliminate the witness package into the ordered existential and conjunction shape of the canonical target.

Formal target: `kmtTarget_of_couplingData`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Eliminate the witness package into the ordered existential and conjunction shape of the canonical target.
3. Produce: KMTStrongApproximationTarget.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-X-SOURCE

Pinpoint primary theorem, assumptions, constants, and errata for every human-required node.

Formal target: `node source crosswalk`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Pinpoint primary theorem, assumptions, constants, and errata for every human-required node.
3. Produce: human provenance only.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.

## M1065-X-PROVENANCE

Record terminal proof bodies, imports, axioms, and duplicate-body identities.

Formal target: `proof provenance ledger`

Semantic ledger:
1. Consume only the registered incoming premises at their frozen interfaces.
2. Establish: Record terminal proof bodies, imports, axioms, and duplicate-body identities.
3. Produce: machine provenance only.
4. Pass the result through the registered typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence is attached.
