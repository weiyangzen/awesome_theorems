# Scope map

## Preserved scope

The repository supports only a broad artificial-neural-network topic family. A standard
feed-forward real-valued network might compose affine maps with coordinatewise activations, but
that model is only a useful inventory of missing choices. It is not the accepted target.

## Decisions required at statement freeze

1. Choose a truth-valued root: a representation/expressivity theorem, universal approximation,
   an approximation rate, training convergence, optimization geometry, generalization, capacity,
   robustness, or another source-selected result.
2. Fix the architecture: feed-forward or another graph, layer count, widths, connectivity,
   parameter sharing, recurrence, convolution, residual connections, and input/output shapes.
3. Fix the scalar field, finite or infinite dimensional spaces, index types, universes, matrix or
   linear-map encoding, biases, parameter carrier, and evaluation semantics.
4. Fix every activation function and whether it is scalar or vector-valued, shared or per-neuron,
   continuous, measurable, differentiable, polynomial, bounded, monotone, or source-specifically
   constrained.
5. For approximation claims, fix the input domain, compactness and nonemptiness, target-function
   class, topology or norm, error metric, tolerance quantifiers, depth/width bounds, and whether
   approximation is uniform, pointwise, in measure, or in an `Lp` space.
6. For learning claims, fix the data/sample distribution, labels, loss, regularization, optimizer,
   initialization, stochastic assumptions, arithmetic model, convergence mode, and rate.
7. Fix ordered binders, hypotheses, conclusion, alternate encodings and directions, logical and
   choice policy, computation boundary, and every source-required constant dependency.
8. Resolve zero layers, zero-width or empty index types, constant activations, zero parameters,
   empty domains or samples, tolerance zero or negative, nonattained optima, and finite versus
   floating-point arithmetic.
9. Select an immutable primary or approved authoritative source with an exact theorem/definition
   locator, incorporated definitions, assumptions, proof boundary, corrections, translation
   policy, and independent source and scope review.

## Explicit exclusions

- Do not choose a universal-approximation theorem merely because it is a famous neural-network
  result, and do not replace the unidentified root with an easy evaluation identity.
- Do not substitute `THM-M-1485` backpropagation, `THM-M-1486` deep learning, `THM-M-1487`
  convolutional networks, `THM-M-1488` recurrent networks, or `THM-M-1489` Transformers.
- Do not treat a matrix composition, sigmoid property, generic optimization lemma, or
  Stone-Weierstrass theorem as the neural-network root without a checked source transport.
- Do not encode the wanted result as a structure field, hypothesis, certificate, axiom, opaque
  predicate, sampled experiment, trained model artifact, or floating-point benchmark.
- Do not credit the catalog label `已验证`, the API probe, or a bounded no-match search as source,
  statement, or proof evidence.

## Prospective proof-route boundary

After a source-approved proposition exists, a feed-forward representation result would normally
require an exact network datatype/evaluator and dimension-correct composition lemmas. A universal
approximation root would additionally require a density theorem and a source-faithful bridge from
its function algebra to the selected activation networks. Training or generalization roots require
different graphs. These are possible audit seeds only; no obligation registry or closure credit is
frozen at intake.
