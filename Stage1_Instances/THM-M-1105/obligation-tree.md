# THM-M-1105 obligation tree

Registry version 1 freezes a bounded-entry moment-method route before proof implementation. Every semantic node below is open.

## M1105-ROOT

Exact bounded-entry Wigner semicircle law

Formal target: `Stage1.THM_M_1105.WignerSemicircleLaw`

Output: The exact canonical proposition in Statement.lean.

Semantic ledger:
1. Inputs: M1105-T-COMPOSE.
2. Inference: Exact bounded-entry Wigner semicircle law.
3. Output and use: The exact canonical proposition in Statement.lean.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-S-DEFINITIONS

Freeze the random-matrix, eigenvalue, empirical-average, and semicircle-integral objects

Formal target: `planned signature v1 for M1105-S-DEFINITIONS`

Output: Exact objects used by all analytic nodes.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Freeze the random-matrix, eigenvalue, empirical-average, and semicircle-integral objects.
3. Output and use: Exact objects used by all analytic nodes.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-S-BOUNDARY

Preserve n+1 dimensions, off-diagonal variance one, diagonal freedom, bounded entries, and one common almost-everywhere set

Formal target: `planned signature v1 for M1105-S-BOUNDARY`

Output: No GOE, expected-only, moment-only, or pointwise-null-set substitute.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Preserve n+1 dimensions, off-diagonal variance one, diagonal freedom, bounded entries, and one common almost-everywhere set.
3. Output and use: No GOE, expected-only, moment-only, or pointwise-null-set substitute.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-S-FOUNDATION

Freeze the classical measure-theory, Hermitian-spectrum, choice, and kernel trust boundary

Formal target: `planned signature v1 for M1105-S-FOUNDATION`

Output: A foundation profile for every eventual body.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Freeze the classical measure-theory, Hermitian-spectrum, choice, and kernel trust boundary.
3. Output and use: A foundation profile for every eventual body.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-N-TRACE

Rewrite empirical monomial averages as normalized traces of scaled matrix powers

Formal target: `planned signature v1 for M1105-N-TRACE`

Output: An exact trace-moment identity with scaling and eigenvalue multiplicity.

Semantic ledger:
1. Inputs: M1105-S-DEFINITIONS, M1105-S-BOUNDARY, M1105-S-FOUNDATION.
2. Inference: Rewrite empirical monomial averages as normalized traces of scaled matrix powers.
3. Output and use: An exact trace-moment identity with scaling and eigenvalue multiplicity.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-B-PARITY

Split trace moments into odd and even exponents and prove exhaustiveness

Formal target: `planned signature v1 for M1105-B-PARITY`

Output: Odd moments vanish asymptotically; even moments enter the pairing count.

Semantic ledger:
1. Inputs: M1105-N-TRACE.
2. Inference: Split trace moments into odd and even exponents and prove exhaustiveness.
3. Output and use: Odd moments vanish asymptotically; even moments enter the pairing count.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-C-WALKS

Expand normalized traces into closed index walks and associate entry products and multigraphs

Formal target: `planned signature v1 for M1105-C-WALKS`

Output: A finite walk sum with all multiplicities and normalization factors.

Semantic ledger:
1. Inputs: M1105-B-PARITY.
2. Inference: Expand normalized traces into closed index walks and associate entry products and multigraphs.
3. Output and use: A finite walk sum with all multiplicities and normalization factors.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-INDEPENDENCE

Use upper-triangular independence and centering to eliminate singly occurring edges

Formal target: `planned signature v1 for M1105-L-INDEPENDENCE`

Output: Only walk patterns with every edge repeated can contribute.

Semantic ledger:
1. Inputs: M1105-C-WALKS.
2. Inference: Use upper-triangular independence and centering to eliminate singly occurring edges.
3. Output and use: Only walk patterns with every edge repeated can contribute.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-NONPAIR

Bound all surviving non-pairing and diagonal-containing walk patterns using the common entry bound

Formal target: `planned signature v1 for M1105-L-NONPAIR`

Output: Every non-leading pattern is o(1) after normalization.

Semantic ledger:
1. Inputs: M1105-L-INDEPENDENCE.
2. Inference: Bound all surviving non-pairing and diagonal-containing walk patterns using the common entry bound.
3. Output and use: Every non-leading pattern is o(1) after normalization.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-PAIRING

Identify leading even closed walks with genus-zero pairings

Formal target: `planned signature v1 for M1105-L-PAIRING`

Output: The leading expectation is the number of noncrossing pairings.

Semantic ledger:
1. Inputs: M1105-L-INDEPENDENCE.
2. Inference: Identify leading even closed walks with genus-zero pairings.
3. Output and use: The leading expectation is the number of noncrossing pairings.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-CATALAN

Count noncrossing pairings by Catalan numbers

Formal target: `planned signature v1 for M1105-L-CATALAN`

Output: The limiting even moment is the corresponding Catalan number.

Semantic ledger:
1. Inputs: M1105-L-PAIRING.
2. Inference: Count noncrossing pairings by Catalan numbers.
3. Output and use: The limiting even moment is the corresponding Catalan number.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-EXPECTATION

Combine the walk bounds and pairing count to prove convergence of expected trace moments

Formal target: `planned signature v1 for M1105-L-EXPECTATION`

Output: Expected odd/even empirical moments converge to semicircle moments.

Semantic ledger:
1. Inputs: M1105-L-NONPAIR, M1105-L-CATALAN, M1105-B-PARITY.
2. Inference: Combine the walk bounds and pairing count to prove convergence of expected trace moments.
3. Output and use: Expected odd/even empirical moments converge to semicircle moments.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-CONCENTRATION

Prove summable deviation bounds for every fixed normalized trace moment

Formal target: `planned signature v1 for M1105-L-CONCENTRATION`

Output: Borel-Cantelli applies without independence between matrix sizes.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Prove summable deviation bounds for every fixed normalized trace moment.
3. Output and use: Borel-Cantelli applies without independence between matrix sizes.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-T-MOMENTS-AS

Upgrade expected moment convergence to simultaneous almost-sure convergence for all natural powers

Formal target: `planned signature v1 for M1105-T-MOMENTS-AS`

Output: On one full-measure set, every empirical polynomial moment converges.

Semantic ledger:
1. Inputs: M1105-L-EXPECTATION, M1105-L-CONCENTRATION.
2. Inference: Upgrade expected moment convergence to simultaneous almost-sure convergence for all natural powers.
3. Output and use: On one full-measure set, every empirical polynomial moment converges.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-SEMICIRCLE-MOMENTS

Compute the moments of the stated density and verify it is a probability measure

Formal target: `planned signature v1 for M1105-L-SEMICIRCLE-MOMENTS`

Output: Odd moments are zero and even moments are Catalan.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Compute the moments of the stated density and verify it is a probability measure.
3. Output and use: Odd moments are zero and even moments are Catalan.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-TIGHTNESS

Derive almost-sure tightness of empirical spectral measures from high even moments

Formal target: `planned signature v1 for M1105-L-TIGHTNESS`

Output: Uniformly small tail mass on the common full-measure set.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Derive almost-sure tightness of empirical spectral measures from high even moments.
3. Output and use: Uniformly small tail mass on the common full-measure set.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-POLYNOMIAL

Extend monomial convergence to polynomial test functions

Formal target: `planned signature v1 for M1105-L-POLYNOMIAL`

Output: Every real polynomial integral converges on the common set.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Extend monomial convergence to polynomial test functions.
3. Output and use: Every real polynomial integral converges on the common set.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-L-BC-APPROX

Approximate bounded continuous tests on compact intervals and control both empirical and semicircle tails

Formal target: `planned signature v1 for M1105-L-BC-APPROX`

Output: Convergence holds for every bounded continuous real test function.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Approximate bounded continuous tests on compact intervals and control both empirical and semicircle tails.
3. Output and use: Convergence holds for every bounded continuous real test function.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-T-WEAK

Compose moment, determinacy, tightness, and approximation packages

Formal target: `planned signature v1 for M1105-T-WEAK`

Output: SampleWeakConvergence for almost every sample.

Semantic ledger:
1. Inputs: M1105-L-SEMICIRCLE-MOMENTS, M1105-T-MOMENTS-AS, M1105-L-TIGHTNESS, M1105-L-POLYNOMIAL, M1105-L-BC-APPROX.
2. Inference: Compose moment, determinacy, tightness, and approximation packages.
3. Output and use: SampleWeakConvergence for almost every sample.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-T-COMPOSE

Transport the terminal sample predicate to the exact frozen root

Formal target: `planned signature v1 for M1105-T-COMPOSE`

Output: The complete canonical conclusion, with every root hypothesis preserved.

Semantic ledger:
1. Inputs: M1105-T-WEAK.
2. Inference: Transport the terminal sample predicate to the exact frozen root.
3. Output and use: The complete canonical conclusion, with every root hypothesis preserved.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-X-SOURCE

Map every analytic obligation to pinpoint human sources

Formal target: `planned signature v1 for M1105-X-SOURCE`

Output: Source overlay only; no machine-proof credit.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Map every analytic obligation to pinpoint human sources.
3. Output and use: Source overlay only; no machine-proof credit.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.

## M1105-X-PROVENANCE

Track wrapper/body identities, axioms, and external boundaries

Formal target: `planned signature v1 for M1105-X-PROVENANCE`

Output: Provenance overlay only; no machine-proof credit.

Semantic ledger:
1. Inputs: frozen statement context.
2. Inference: Track wrapper/body identities, axioms, and external boundaries.
3. Output and use: Provenance overlay only; no machine-proof credit.

Boundary: Architecture only; no accepted proof body, source closure, or root closure.
