# THM-M-1487 scope map

## Preserved catalog scope

- Target identity: `THM-M-1487`, named `卷积神经网络`.
- Literal gloss: `图像处理的神经网络` (neural networks for image processing).
- Catalog attribution and time: Yann LeCun, 1989.
- Recognizable boundary: convolutional neural-network models used with image-like inputs.

This is a model and application family, not one proposition. Intake preserves that ambiguity
rather than silently adopting a familiar architecture or theorem.

## Proposition-changing decisions

An accountable source correction must select one immutable proposition and freeze:

1. The claim kind: definition well-formedness, forward-evaluation identity, translation
   equivariance or invariance, expressivity or approximation, optimization, generalization,
   robustness, complexity, or another exact conclusion.
2. The architecture: number and order of layers, channel and spatial index types, filter support,
   parameter sharing, biases, nonlinearities, subsampling or pooling, normalization, and readout.
3. The convolution convention: discrete or continuous, convolution versus cross-correlation,
   index reversal, origin, padding, stride, dilation, boundary extension, groups, and shape rules.
4. The domain: finite arrays, holors, functions on a group or Euclidean space, pixel scalar and
   color space, spatial dimension and resolution, batch semantics, and finite or infinite width.
5. The image and task model: admissible inputs, labels and outputs, preprocessing, augmentation,
   translation or other transformation action, and classification or regression semantics.
6. The parameter and arithmetic model: real, rational, floating-point, quantized, or symbolic
   weights; exact versus approximate evaluation; overflow, rounding, and solver or oracle policy.
7. Training semantics, if relevant: loss, optimizer, update order, initialization, stochastic
   sampling, differentiability and subgradient conventions, stopping rule, and randomness.
8. Statistical hypotheses, if relevant: data distribution, independence, sample size, confidence,
   probability space, hypothesis class, norm or metric, and quantifier order.
9. The exact conclusion: equality, implication, bound, convergence, probability guarantee,
   approximation rate, robustness radius, complexity statement, or experimentally measured claim,
   with all constants and dependencies.
10. Ordered binders, strictness, alternate encodings, degenerate cases, foundation, TCB,
    computation, review, freshness, and revocation profiles.

Each choice changes truth conditions and proof obligations. This list is a resolution ledger, not
a candidate theorem statement.

## Candidate families not credited

- A checked finite-array identity for one discrete convolution or cross-correlation layer.
- Translation equivariance of a selected convolutional stack and invariance after selected pooling.
- Approximation or expressivity of one source-defined CNN class on a fixed function space.
- Correctness of reverse-mode differentiation for one selected convolutional architecture.
- A robustness, generalization, or sample-complexity theorem under explicit distributional norms.
- The empirical recognition performance reported for one trained 1989 network.

No candidate is selected, combined, or credited at intake.

## Neighbor ownership and exclusions

- `THM-M-1484` owns the generic neural-network topic.
- `THM-M-1485` owns backpropagation algorithms.
- `THM-M-1486` owns deep learning.
- `THM-M-1488` owns recurrent neural networks.
- `THM-M-1489` owns Transformers.

None contributes a statement, source, or proof receipt to this target. A generic neural network,
backpropagation lemma, multilayer model, recurrent model, attention model, ordinary analytic
convolution theorem, matrix multiplication fact, tensor-rank result, or scalar sigmoid theorem
cannot be substituted because it is convenient. A structure whose field assumes the desired CNN
property, a sampled image experiment, trained weights, benchmark accuracy, numerical trace, or the
catalog's `已验证` label supplies no theorem credit.

## Boundary cases

Source review must decide empty spatial axes or channel sets, zero-sized filters, zero layers,
zero stride, filters larger than the input, padding and cropping, boundary pixels, even versus odd
filter centers, dilation, singleton dimensions, constant and zero images, zero weights, bias-only
networks, activation nondifferentiability, ties in max pooling or classification, invalid shapes,
NaN and overflow behavior, and exact versus approximate arithmetic. For statistical claims it must
also decide empty samples, zero-probability events, adversarial versus random perturbations, and
finite versus asymptotic regimes. Intake silently excludes none of them.

No canonical Lean target, checked transport, expression fingerprint, discovery protocol,
obligation registry, or proof state is frozen in this phase.
