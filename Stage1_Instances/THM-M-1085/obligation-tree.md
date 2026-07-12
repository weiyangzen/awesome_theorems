# THM-M-1085 obligation tree

This freezes the covariance-interpolation route before proof closure is observed. Every semantic node is open.

## M1085-ROOT

The exact finite-dimensional SlepianTarget.

Formal target: `Stage1Instances.THM_M_1085.SlepianTarget`

Output: The canonical lower-orthant comparison.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: The canonical lower-orthant comparison.
3. Use the registered composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-S-DEFINITIONS

Freeze BelowAll, coordinate means, covariances, and lower-orthant probabilities.

Formal target: `Definitions and binders of Statement.lean`

Output: The exact objects used by all later nodes.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Freeze BelowAll, coordinate means, covariances, and lower-orthant probabilities.
3. Derive: The exact objects used by all later nodes.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-S-DOMAINS

Audit finite nonempty indexing, two sample spaces, measurability, integrability, and extended-real measure values.

Formal target: `Domain package for SlepianTarget`

Output: No common-space, density, or positive-definiteness premise is introduced.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Audit finite nonempty indexing, two sample spaces, measurability, integrability, and extended-real measure values.
3. Derive: No common-space, density, or positive-definiteness premise is introduced.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-S-BOUNDARY

Cover singleton indices and singular or repeated-coordinate Gaussian laws.

Formal target: `Boundary package including singleton_boundary`

Output: The proof route includes every degenerate case admitted by the target.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Cover singleton indices and singular or repeated-coordinate Gaussian laws.
3. Derive: The proof route includes every degenerate case admitted by the target.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-S-FOUNDATION

Freeze classical choice, integration, measure, and trust assumptions.

Formal target: `Foundation and TCB certificate`

Output: An auditable foundation profile for eventual proof bodies.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Freeze classical choice, integration, measure, and trust assumptions.
3. Derive: An auditable foundation profile for eventual proof bodies.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-N-LAWS

Push both random vectors to their finite coordinate laws and recover means and covariance entries.

Formal target: `HasGaussianLaw pushforward reduction on a finite coordinate type`

Output: Two centered finite Gaussian laws with the frozen covariance data.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Push both random vectors to their finite coordinate laws and recover means and covariance entries.
3. Derive: Two centered finite Gaussian laws with the frozen covariance data.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-N-MATRIX

Encode covariance as symmetric positive-semidefinite matrices with equal diagonals and ordered off-diagonals.

Formal target: `Finite covariance-matrix interface`

Output: Matrix data equivalent in the required direction to the target hypotheses.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Encode covariance as symmetric positive-semidefinite matrices with equal diagonals and ordered off-diagonals.
3. Derive: Matrix data equivalent in the required direction to the target hypotheses.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-C-INTERPOLATION

Construct C(s) = (1-s) C_X + s C_Y and its centered Gaussian law for s in [0,1].

Formal target: `Interpolated centered Gaussian law with covariance C(s)`

Output: A Gaussian path joining the endpoint laws, including singular matrices.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Construct C(s) = (1-s) C_X + s C_Y and its centered Gaussian law for s in [0,1].
3. Derive: A Gaussian path joining the endpoint laws, including singular matrices.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-C-SMOOTHER

Construct bounded smooth decreasing coordinate cutoffs converging to 1_{x <= t}.

Formal target: `Smooth lower-orthant approximants F_epsilon,t`

Output: Integrable C2 test functions with controlled mixed derivatives.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Construct bounded smooth decreasing coordinate cutoffs converging to 1_{x <= t}.
3. Derive: Integrable C2 test functions with controlled mixed derivatives.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-L-INTERPOLATION-ID

Prove the Gaussian covariance interpolation derivative identity for bounded C2 tests.

Formal target: `d/ds E[F(Z_s)] = (1/2) sum_ij (C_Y-C_X)_ij E[partial_ij F(Z_s)]`

Output: An exact derivative formula valid at singular endpoints by approximation.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Prove the Gaussian covariance interpolation derivative identity for bounded C2 tests.
3. Derive: An exact derivative formula valid at singular endpoints by approximation.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-L-MIXED-SIGN

Show every off-diagonal mixed derivative of the product cutoff is nonnegative.

Formal target: `i != j -> 0 <= partial_i partial_j F_epsilon,t`

Output: The covariance-order terms have the comparison sign.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Show every off-diagonal mixed derivative of the product cutoff is nonnegative.
3. Derive: The covariance-order terms have the comparison sign.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-L-MONOTONE

Use equal diagonals and ordered off-diagonals in the derivative identity and integrate over s.

Formal target: `E[F_epsilon,t(X)] <= E[F_epsilon,t(Y)]`

Output: The smoothed lower-orthant comparison for every epsilon > 0.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Use equal diagonals and ordered off-diagonals in the derivative identity and integrate over s.
3. Derive: The smoothed lower-orthant comparison for every epsilon > 0.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-L-LIMIT

Pass the smooth inequality to lower-orthant indicators using bounded convergence and endpoint-law transport.

Formal target: `P(forall i, X_i <= t) <= P(forall i, Y_i <= t)`

Output: The exact event-probability inequality for every threshold.

Semantic ledger:
1. Fix the exact context and named premises from the frozen target.
2. Establish: Pass the smooth inequality to lower-orthant indicators using bounded convergence and endpoint-law transport.
3. Derive: The exact event-probability inequality for every threshold.
4. Pass the output through its typed edge without changing the target.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-T-COMPARISON

Package the comparison uniformly over every binder and hypothesis of SlepianTarget.

Formal target: `Stage1Instances.THM_M_1085.ObligationTree.PointwiseComparison`

Output: A proposition definitionally equal to the canonical target.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: A proposition definitionally equal to the canonical target.
3. Use the registered composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-T-COMPOSE

Transport the terminal comparison to the exact canonical declaration without changing binders.

Formal target: `Stage1Instances.THM_M_1085.ObligationTree.slepianTarget_of_pointwise`

Output: Stage1Instances.THM_M_1085.SlepianTarget.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: Stage1Instances.THM_M_1085.SlepianTarget.
3. Use the registered composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-X-SOURCE

Map mathematical nodes to exact primary-source proof locations and errata review.

Formal target: `Human-source overlay`

Output: Source classification only; no machine proof credit.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: Source classification only; no machine proof credit.
3. Use the registered composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or root closure is claimed.

## M1085-X-PROVENANCE

Record wrapper, terminal-body, dependency, axiom, and unsafe/oracle provenance.

Formal target: `Formal provenance overlay`

Output: Provenance classification only; no proof credit.

Semantic ledger:
1. Consume every incoming proof premise at its exact planned signature.
2. Derive: Provenance classification only; no proof credit.
3. Use the registered composition edge without an undeclared premise.

Boundary: Architecture only; no accepted proof body or root closure is claimed.
