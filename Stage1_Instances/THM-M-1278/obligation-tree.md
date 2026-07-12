# THM-M-1278 obligation tree

This registry freezes a direct normalized proof architecture. Every analytic node remains open; only the exact composition harness is kernel-checked.

## M1278-ROOT

The exact normalized Onofri inequality on the encoded unit two-sphere.

Formal target: `Stage1Instances.THM_M_1278.OnofriInequality`

Output: The exact canonical target.

Semantic ledger:
1. Consume every required incoming proof premise.
2. Derive exactly: The exact canonical target.
3. Validate the child-to-parent composition term and its target fingerprint.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-S-DEFINITIONS

Freeze the sphere, Hausdorff area, smooth ambient representative, tangential gradient, mean, and Dirichlet energy.

Formal target: `Definitions in Statement.lean and ObligationTree.lean`

Output: The objects occurring in the root have one fixed Lean meaning.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Freeze the sphere, Hausdorff area, smooth ambient representative, tangential gradient, mean, and Dirichlet energy.
3. Derive exactly: The objects occurring in the root have one fixed Lean meaning.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-S-AREA

Prove that the chosen two-dimensional Hausdorff measure of the unit sphere has total mass 4*pi.

Formal target: `sphereArea Set.univ = 4 * Real.pi`

Output: The normalization constants describe probability-normalized spherical area.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Prove that the chosen two-dimensional Hausdorff measure of the unit sphere has total mass 4*pi.
3. Derive exactly: The normalization constants describe probability-normalized spherical area.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-S-FINITE

Establish measurability, integrability, finiteness, and positivity needed for all root integrals and logarithms.

Formal target: `Integrable u sphereArea ∧ Integrable (fun x => Real.exp (u x)) sphereArea ∧ 0 < normalizedExpIntegral u`

Output: Every analytic expression used by the proof obeys its side conditions.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Establish measurability, integrability, finiteness, and positivity needed for all root integrals and logarithms.
3. Derive exactly: Every analytic expression used by the proof obeys its side conditions.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-S-FOUNDATION

Audit classical choice, quotient, extensionality, imported axioms, and the transitive Lean trust boundary.

Formal target: `Foundation and axiom-report certificate for the terminal declaration`

Output: A checked foundation and TCB profile for every proof body.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Audit classical choice, quotient, extensionality, imported axioms, and the transitive Lean trust boundary.
3. Derive exactly: A checked foundation and TCB profile for every proof body.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-N-SUBTRACT-MEAN

Construct the smooth representative v = u - mean(u) without changing the represented tangential derivatives.

Formal target: `forall u, exists v, forall x, v x = u x - mean u`

Output: A smooth mean-shifted representative.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Construct the smooth representative v = u - mean(u) without changing the represented tangential derivatives.
3. Derive exactly: A smooth mean-shifted representative.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-N-ZERO-MEAN

Using the area formula, prove that subtracting mean(u) produces spherical mean zero.

Formal target: `mean v = 0`

Output: The normalized function satisfies the sharp estimate's hypothesis.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Using the area formula, prove that subtracting mean(u) produces spherical mean zero.
3. Derive exactly: The normalized function satisfies the sharp estimate's hypothesis.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-N-ENERGY

Prove tangential gradients and Dirichlet energy are invariant under the constant mean shift.

Formal target: `dirichletEnergy v = dirichletEnergy u`

Output: The normalization introduces no energy error.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Prove tangential gradients and Dirichlet energy are invariant under the constant mean shift.
3. Derive exactly: The normalization introduces no energy error.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-N-EXP-SHIFT

Factor exp(mean u) from the integral and transport through log, discharging positivity and finiteness.

Formal target: `Real.log (normalizedExpIntegral u) = mean u + Real.log (normalizedExpIntegral v)`

Output: The left side decomposes into the mean plus the zero-mean left side.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Factor exp(mean u) from the integral and transport through log, discharging positivity and finiteness.
3. Derive exactly: The left side decomposes into the mean plus the zero-mean left side.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-T-SHIFT

Compose construction, zero-mean, energy, and exponential-shift facts into the exact mean-shift transport interface.

Formal target: `Stage1Instances.THM_M_1278_Obligations.MeanShiftTransport`

Output: A checked transport from arbitrary smooth input to normalized input.

Semantic ledger:
1. Consume every required incoming proof premise.
2. Derive exactly: A checked transport from arbitrary smooth input to normalized input.
3. Validate the child-to-parent composition term and its target fingerprint.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-L-SHARP-ONOFRI

Prove the sharp zero-mean Onofri estimate with coefficient 1/(16*pi) for every encoded smooth sphere function.

Formal target: `Stage1Instances.THM_M_1278_Obligations.SharpZeroMeanEstimate`

Output: The central sharp analytic inequality.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Prove the sharp zero-mean Onofri estimate with coefficient 1/(16*pi) for every encoded smooth sphere function.
3. Derive exactly: The central sharp analytic inequality.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-L-SOURCE-ROUTE

Expand the selected primary-source analytic route for the sharp estimate into independently checkable lemmas before proof credit.

Formal target: `A source-pinpointed derivation of SharpZeroMeanEstimate`

Output: A non-circular proof route for the central analytic inequality.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Expand the selected primary-source analytic route for the sharp estimate into independently checkable lemmas before proof credit.
3. Derive exactly: A non-circular proof route for the central analytic inequality.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-T-COMPOSE

Apply the sharp estimate to the shifted function and rewrite the energy and logarithmic integral.

Formal target: `Stage1Instances.THM_M_1278_Obligations.compose_root`

Output: The exact root proposition from both required semantic children.

Semantic ledger:
1. Consume every required incoming proof premise.
2. Derive exactly: The exact root proposition from both required semantic children.
3. Validate the child-to-parent composition term and its target fingerprint.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-X-SOURCE

Pinpoint and independently review the human source for every root-relevant analytic step.

Formal target: `Human-source crosswalk ledger`

Output: H-status evidence only; no machine proof credit.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Pinpoint and independently review the human source for every root-relevant analytic step.
3. Derive exactly: H-status evidence only; no machine proof credit.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.

## M1278-X-PROVENANCE

Trace every eventual wrapper to its terminal proof body, imports, revision, license, and axiom report.

Formal target: `Machine provenance ledger`

Output: Provenance evidence only; no duplicate semantic credit.

Semantic ledger:
1. Freeze the exact context and input interfaces.
2. Establish: Trace every eventual wrapper to its terminal proof body, imports, revision, license, and axiom report.
3. Derive exactly: Provenance evidence only; no duplicate semantic credit.
4. Pass the output along the declared typed edge without strengthening the target.

Boundary: Architecture interface only; no analytic proof body or closure is claimed.
