# THM-M-1080 obligation tree

Registry v1 freezes the direct exponential-moment route for the exact arbitrary-space statement. Every mathematical proof leaf remains open; only final conditional recomposition is kernel checked.

## M1080-ROOT

The exact arbitrary-measurable-space upper-tail proposition in Statement.lean.

Formal target: `Stage1Instances.THM_M_1080.Statement`

Output: The canonical Azuma upper-tail inequality.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: The exact arbitrary-measurable-space upper-tail proposition in Statement.lean.
3. Output: The canonical Azuma upper-tail inequality.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-S-DEFINITIONS

Freeze squaredBoundSum, event probability via Measure.real, martingale, filtration, and a.e. increment bounds.

Formal target: `Stage1Instances.THM_M_1080.{squaredBoundSum,Statement}`

Output: The exact objects and coercions used by every proof node.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Freeze squaredBoundSum, event probability via Measure.real, martingale, filtration, and a.e. increment bounds.
3. Output: The exact objects and coercions used by every proof node.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-S-SCOPE

Preserve the ordered universe, probability, filtration, process, varying NNReal bounds, horizon, and nonnegative-threshold binders.

Formal target: `binder package of Stage1Instances.THM_M_1080.Statement`

Output: No StandardBorelSpace or stronger conditional-sub-Gaussian premise is inserted.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Preserve the ordered universe, probability, filtration, process, varying NNReal bounds, horizon, and nonnegative-threshold binders.
3. Output: No StandardBorelSpace or stronger conditional-sub-Gaussian premise is inserted.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-S-BOUNDARY

Account for n=0, t=0, and squaredBoundSum=0 under Lean total division.

Formal target: `planned boundary lemmas for the frozen expression`

Output: All degenerate inputs remain inside the root theorem.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Account for n=0, t=0, and squaredBoundSum=0 under Lean total division.
3. Output: All degenerate inputs remain inside the root theorem.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-S-FOUNDATION

Fix classical measure theory, Lean/mathlib trust, axiom inspection, and no-oracle policy.

Formal target: `planned transitive trust and axiom report`

Output: An explicit foundation boundary for eventual terminal bodies.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Fix classical measure theory, Lean/mathlib trust, axiom inspection, and no-oracle policy.
3. Output: An explicit foundation boundary for eventual terminal bodies.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-N-INCREMENTS

Define Y k = X (k+1)-X k and establish measurability, integrability, adaptation, and conditional mean zero from Martingale X G mu.

Formal target: `planned martingale-difference interface`

Output: A bounded centered increment family without strengthening the space.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Define Y k = X (k+1)-X k and establish measurability, integrability, adaptation, and conditional mean zero from Martingale X G mu.
3. Output: A bounded centered increment family without strengthening the space.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-N-TELESCOPE

Prove the finite telescoping identity sum_{k<n} Y k = X n-X 0 and align c(k+1) indexing.

Formal target: `planned finite-sum telescoping transport`

Output: The sum-tail event is exactly the canonical event.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Prove the finite telescoping identity sum_{k<n} Y k = X n-X 0 and align c(k+1) indexing.
3. Output: The sum-tail event is exactly the canonical event.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-C-EXPONENTIAL

Construct the exponential process from partial sums and deterministic squared-bound sums and prove measurability/integrability needed for iteration.

Formal target: `planned exponential-supermartingale package`

Output: A valid exponential-moment object for every lambda >= 0.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Construct the exponential process from partial sums and deterministic squared-bound sums and prove measurability/integrability needed for iteration.
3. Output: A valid exponential-moment object for every lambda >= 0.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-L-COND-HOEFFDING

Derive the conditional Hoeffding bound for each a.e. centered increment in [-c(k+1),c(k+1)] on the frozen arbitrary measurable space.

Formal target: `planned conditional exponential-moment inequality`

Output: The one-step factor exp(lambda^2*c(k+1)^2/2).

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Derive the conditional Hoeffding bound for each a.e. centered increment in [-c(k+1),c(k+1)] on the frozen arbitrary measurable space.
3. Output: The one-step factor exp(lambda^2*c(k+1)^2/2).
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-L-MGF-ITERATE

Iterate the one-step conditional bound through the filtration.

Formal target: `planned finite-horizon MGF induction`

Output: E exp(lambda*(X n-X 0)) <= exp(lambda^2*squaredBoundSum c n/2).

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Iterate the one-step conditional bound through the filtration.
3. Output: E exp(lambda*(X n-X 0)) <= exp(lambda^2*squaredBoundSum c n/2).
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-L-MARKOV

Apply exponential Markov to the canonical upper-tail event.

Formal target: `planned exponential Markov inequality`

Output: For lambda >= 0, probability is bounded by exp(-lambda*t+lambda^2*S/2).

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Apply exponential Markov to the canonical upper-tail event.
3. Output: For lambda >= 0, probability is bounded by exp(-lambda*t+lambda^2*S/2).
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-L-OPTIMIZE

Choose and normalize the exponential parameter, with an explicit zero-sum branch, to obtain the frozen total-division exponent.

Formal target: `planned real arithmetic optimization`

Output: The exact exp(-t^2/(2*S)) bound for positive thresholds.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Choose and normalize the exponential parameter, with an explicit zero-sum branch, to obtain the frozen total-division exponent.
3. Output: The exact exp(-t^2/(2*S)) bound for positive thresholds.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-T-POSITIVE

Compose increments, telescoping, conditional Hoeffding, MGF iteration, Markov, and optimization for t>0.

Formal target: `Stage1Instances.THM_M_1080.ObligationTree.PositiveThresholdPackage`

Output: The canonical conclusion restricted only to the positive-threshold branch.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Compose increments, telescoping, conditional Hoeffding, MGF iteration, Markov, and optimization for t>0.
3. Output: The canonical conclusion restricted only to the positive-threshold branch.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-T-ZERO

Prove the t=0 conclusion from probability <= 1 and simplification of the frozen exponent.

Formal target: `Stage1Instances.THM_M_1080.ObligationTree.ZeroThresholdPackage`

Output: The canonical conclusion at the included threshold boundary.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Prove the t=0 conclusion from probability <= 1 and simplification of the frozen exponent.
3. Output: The canonical conclusion at the included threshold boundary.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-T-ASSEMBLE

Recombine t=0 and t>0 without changing any other binder or conclusion.

Formal target: `Stage1Instances.THM_M_1080.ObligationTree.azumaUpperTail_of_threshold_packages`

Output: The exact canonical root conditional on both open terminal packages.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Recombine t=0 and t>0 without changing any other binder or conclusion.
3. Output: The exact canonical root conditional on both open terminal packages.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-X-MATHLIB

Audit the pinned conditional-sub-Gaussian sum theorem as a semantic anchor only, including its StandardBorelSpace and hypothesis mismatches.

Formal target: `ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF`

Output: A provenance-aware optional bridge that earns no direct root credit.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Audit the pinned conditional-sub-Gaussian sum theorem as a semantic anchor only, including its StandardBorelSpace and hypothesis mismatches.
3. Output: A provenance-aware optional bridge that earns no direct root credit.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-X-SOURCE

Map every root-relevant mathematical node to fixed primary/modern source pinpoints and normalization review.

Formal target: `node-specific human-source crosswalk`

Output: Human-source coverage only; no machine proof credit.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Map every root-relevant mathematical node to fixed primary/modern source pinpoints and normalization review.
3. Output: Human-source coverage only; no machine proof credit.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.

## M1080-X-PROVENANCE

Inventory terminal bodies, wrappers, imports, axioms, placeholders, unsafe/oracle boundaries, and replay receipts.

Formal target: `planned machine-derived provenance closure`

Output: Release provenance only; no mathematical proof credit.

Semantic ledger:
1. Premises: Only the exact incoming proof_requires conclusions and the frozen formal context.
2. Inference: Inventory terminal bodies, wrappers, imports, axioms, placeholders, unsafe/oracle boundaries, and replay receipts.
3. Output: Release provenance only; no mathematical proof credit.
4. Outgoing use: Only declared typed proof, support, or workflow edges may consume this output.

Boundary: Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.
