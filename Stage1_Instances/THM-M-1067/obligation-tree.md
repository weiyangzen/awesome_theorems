# THM-M-1067 obligation tree

Registry v1 freezes the mollified-occupation-density route before proof closure is observed. Every semantic node below remains open.

## M1067-ROOT

Construct jointly continuous Brownian local time with the simultaneous occupation-density identity.

Formal target: `Stage1Instances.THM_M_1067.BrownianLocalTimeTarget`

Output: The exact canonical target.

Semantic ledger:
1. Consume every incoming child at its exact registered interface.
2. Derive: The exact canonical target.
3. Discharge the parent composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-S-DEFINITIONS

Freeze BrownianPath, Wiener measure, nonnegative Lebesgue measure, and local-time field types.

Formal target: `Statement.lean definitions used by BrownianLocalTimeTarget`

Output: Exact objects and binder order for every node.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Freeze BrownianPath, Wiener measure, nonnegative Lebesgue measure, and local-time field types.
3. Derive: Exact objects and binder order for every node.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-S-BOUNDARY

Preserve one common null set, all nonnegative times, all measurable ENNReal tests, and occupation normalization.

Formal target: `Boundary package for IsBrownianLocalTime`

Output: No fixed-level, fixed-test, Tanaka-only, or assumed-field substitution.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Preserve one common null set, all nonnegative times, all measurable ENNReal tests, and occupation normalization.
3. Derive: No fixed-level, fixed-test, Tanaka-only, or assumed-field substitution.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-S-FOUNDATION

Freeze classical noncomputable measure theory and the kernel trust policy.

Formal target: `Foundation and trust certificate`

Output: Auditable foundation profile for eventual bodies.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Freeze classical noncomputable measure theory and the kernel trust policy.
3. Derive: Auditable foundation profile for eventual bodies.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-N-WIENER

Derive usable increment, covariance, Gaussian-density, and path-law facts from IsWienerMeasure.

Formal target: `IsWienerMeasure W -> Wiener finite-dimensional interface`

Output: Brownian estimates without assuming local time.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Derive usable increment, covariance, Gaussian-density, and path-law facts from IsWienerMeasure.
3. Derive: Brownian estimates without assuming local time.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-C-APPROX

Define nonnegative mollified occupation densities from time spent near each level.

Formal target: `approxLocalTime epsilon w t x`

Output: A measurable nonnegative approximate field.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Define nonnegative mollified occupation densities from time spent near each level.
3. Derive: A measurable nonnegative approximate field.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-L-MOMENTS

Prove spatial and temporal moment bounds for increments of the approximate fields.

Formal target: `Uniform moment estimates for approxLocalTime`

Output: Bounds strong enough for convergence and continuity.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Prove spatial and temporal moment bounds for increments of the approximate fields.
3. Derive: Bounds strong enough for convergence and continuity.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-L-CAUCHY

Prove the approximations are Cauchy on compact time-space rectangles.

Formal target: `Cauchy approxLocalTime in a compact-field norm`

Output: A coherent limiting occupation-density field.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Prove the approximations are Cauchy on compact time-space rectangles.
3. Derive: A coherent limiting occupation-density field.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-C-LIMIT

Choose the limiting nonnegative field without changing versions between downstream properties.

Formal target: `limitLocalTime : BrownianPath -> NNReal -> Real -> NNReal`

Output: One common candidate L for all obligations.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Choose the limiting nonnegative field without changing versions between downstream properties.
3. Derive: One common candidate L for all obligations.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-L-JOINT-CONT

Use the moment bounds and a two-parameter continuity theorem to obtain a jointly continuous version.

Formal target: `forall_aᵐ w ∂W, Continuous (Function.uncurry (L w))`

Output: Joint continuity on a single full-measure event.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Use the moment bounds and a two-parameter continuity theorem to obtain a jointly continuous version.
3. Derive: Joint continuity on a single full-measure event.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-L-MEAS

Prove measurability of every time-level evaluation of the selected version.

Formal target: `forall t x, AEMeasurable (fun w => L w t x) W`

Output: The pointwise measurability conjunct.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Prove measurability of every time-level evaluation of the selected version.
3. Derive: The pointwise measurability conjunct.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-L-OCC-CORE

Pass the mollifier identity to the limit for a countable determining class of tests and times.

Formal target: `Occupation identity on a countable continuous/simple determining class`

Output: A common full-measure event for the core identity.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Pass the mollifier identity to the limit for a countable determining class of tests and times.
3. Derive: A common full-measure event for the core identity.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-L-OCC-EXTEND

Extend the core identity pathwise to every time and every measurable ENNReal-valued test.

Formal target: `OccupationIdentityAE W L`

Output: The exact simultaneous occupation identity.

Semantic ledger:
1. Freeze the exact hypotheses and named interfaces.
2. Establish: Extend the core identity pathwise to every time and every measurable ENNReal-valued test.
3. Derive: The exact simultaneous occupation identity.
4. Pass the output through its typed edge without weakening the target.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-T-FIELD

Combine evaluation measurability, joint continuity, and occupation identity for the same selected field.

Formal target: `IsBrownianLocalTime W L`

Output: The exact witness property for a fixed Wiener measure.

Semantic ledger:
1. Consume every incoming child at its exact registered interface.
2. Derive: The exact witness property for a fixed Wiener measure.
3. Discharge the parent composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-T-COMPOSE

Construct the field for each Wiener measure and package the exact existential conclusion.

Formal target: `BrownianLocalTimeTarget from the registered field components`

Output: The canonical root proposition.

Semantic ledger:
1. Consume every incoming child at its exact registered interface.
2. Derive: The canonical root proposition.
3. Discharge the parent composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-X-SOURCE

Map every mathematical node to exact source pinpoints, assumptions, normalization, and errata.

Formal target: `Human-source crosswalk overlay`

Output: Source classification only; no machine credit.

Semantic ledger:
1. Consume every incoming child at its exact registered interface.
2. Derive: Source classification only; no machine credit.
3. Discharge the parent composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or closure evidence.

## M1067-X-PROVENANCE

Record proof-body, wrapper, transitive dependency, axiom, unsafe, and computation provenance.

Formal target: `Formal provenance overlay`

Output: Provenance only; no proof credit without checked bodies.

Semantic ledger:
1. Consume every incoming child at its exact registered interface.
2. Derive: Provenance only; no proof credit without checked bodies.
3. Discharge the parent composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or closure evidence.
