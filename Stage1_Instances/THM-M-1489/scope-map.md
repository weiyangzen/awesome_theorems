# THM-M-1489 scope map

## Preserved catalog scope

- Target identity: `THM-M-1489`, named `Transformer`.
- Literal gloss: `注意力机制的神经网络` (an attention-mechanism neural network).
- Catalog attribution and time: Vaswani et al., 2017.
- Recognizable boundary: attention-based neural architectures in the Transformer family.

This identifies a model family, not one proposition. Intake preserves that ambiguity rather than
silently turning a familiar equation, implementation property, complexity claim, or benchmark into
the requested theorem.

## Proposition-changing decisions

An accountable source correction must select one immutable proposition and freeze:

1. The claim kind: definition well-formedness, forward-evaluation identity, normalization,
   masking or causality correctness, equivariance, expressivity or approximation, numerical
   stability, complexity, optimization, generalization, or an empirical result.
2. The architecture: encoder only, decoder only, encoder-decoder, layer count, sublayer order,
   residual and normalization convention, feed-forward blocks, embeddings, readout, and parameter
   sharing.
3. Tensor shapes and index types: batch, sequence, query, key, value, model, head, vocabulary, and
   feed-forward dimensions; finite versus variable sequence lengths; and every shape constraint.
4. Attention semantics: dot-product compatibility, the `sqrt(d_k)` scaling, row or column
   normalization, softmax definition and temperature, masks and sentinel values, head projections,
   concatenation order, output projection, and dropout.
5. Positional and autoregressive semantics: sinusoidal or learned encodings, offset convention,
   padding, causal mask orientation, allowed dependency relation, decoding order, and stopping.
6. Scalar and computation model: real, rational, floating-point, quantized, or symbolic values;
   exact versus approximate exponential, square root, division, normalization, overflow,
   underflow, infinities, rounding, randomness, kernels, and oracle policy.
7. Input, output, data, and training models when relevant: tokens and vocabulary, loss, optimizer,
   initialization, batching, distribution, sample independence, evaluation metric, and hardware or
   cost model.
8. The exact conclusion: equality, implication, positivity or sum-to-one property, dependency
   restriction, approximation bound, rate, probability, operation or path-length bound, or an
   experimentally measured claim, including every constant and dependency.
9. Ordered binders, universes, typeclasses, hypotheses, strictness, alternate encodings and
   transport directions, degenerate cases, foundation, TCB, computation, freshness, and revocation
   profiles.
10. An immutable primary or approved authoritative source with exact section/equation/theorem or
    dataset locator, incorporated definitions, proof versus experimental boundary, corrections,
    edition drift, translation policy, and independent source and scope review.

Each choice changes truth conditions and proof obligations.

## Boundary and degenerate cases

The selected source must decide empty query, key, value, token, vocabulary, batch, sequence, and
head index types; zero heads or layers; `d_k = 0`; empty normalization rows; all-masked rows; zero or
negative temperature; zero, repeated, or identical queries and keys; zero values and parameters;
padding-only inputs; length-one sequences; mask sentinels; dimension divisibility; and malformed
matrix shapes.

It must also decide numerical overflow and underflow, division by zero, ties, NaN or infinity,
finite versus exact-real arithmetic, zero dropout probability, randomized dropout, train versus
inference behavior, positional collisions, maximum length, and deterministic versus stochastic
decoding. No case is silently excluded at intake.

## Candidate propositions not credited

- The paper equation `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V` as a definition or a
  coordinatewise matrix identity.
- Positivity and row-sum normalization of a selected exact softmax attention matrix.
- Correctness of a selected causal mask: output position `i` depends only on permitted input and
  prior output positions.
- Shape preservation or equivalence between matrix, finite-function, and multi-head encodings.
- Permutation equivariance of an attention block under a precisely selected action and positional
  encoding policy.
- One source-defined operation-count, sequential-depth, or maximum-path-length comparison.
- An expressivity, approximation, optimization, robustness, or generalization theorem for a
  source-defined Transformer class.
- The paper's measured BLEU scores, training time, or hardware-dependent performance.

These are planning candidates, not accepted statements or alternate encodings.

## Neighbor ownership and exclusions

- `THM-M-1484` separately owns generic neural networks.
- `THM-M-1485` separately owns backpropagation algorithms.
- `THM-M-1486` separately owns deep learning.
- `THM-M-1487` separately owns convolutional neural networks.
- `THM-M-1488` separately owns recurrent neural networks.

None contributes a statement, source, or proof receipt to this target. Generic matrix
multiplication, dot products, exponential or square-root facts, a hand-written softmax definition,
an architecture diagram, trained weights, a finite execution trace, or a benchmark cannot be
substituted. A structure field or hypothesis that assumes the desired result, the untrusted
`已验证` label, and the discovery probe likewise receive no credit.

## Execution boundary

Intake may record the ambiguity, source-family lead, candidate clauses, formal substrate, profiles,
and open downstream DAG. It must not select a canonical root, freeze an obligation registry, credit
a proof body, or perform the statement, anchor, obligation, proof, validation, or release phase.
The first downstream gate is an independently reviewed source-statement decision.
