# THM-M-1485 scope map

## Preserved repository scope

The literal repository boundary is the label `反向传播算法`, glossed as
`神经网络的训练算法` and attributed to Rumelhart, Hinton, and Williams in 1986. This identifies
the backpropagation training-procedure family. It does not select one mathematical proposition.

The inspected 1986 source lead describes finite layered networks directed from lower to higher
layers, permits connections that skip intermediate layers, uses the logistic sigmoid in its
displayed formulas, sums squared output error over a fixed finite data set, propagates derivatives
backward, and then gives plain-gradient and momentum weight changes. A modern reverse-mode
derivative theorem, a program-correctness theorem, and a training-convergence theorem are different
claims. None is frozen at intake.

## Decisions required at statement freeze

1. Admit an immutable source and select one exact result: derivative-recurrence correctness,
   parameter-gradient correctness, update semantics, termination, complexity, convergence, or a
   source-approved conjunction.
2. Fix the network carrier: a strictly layered graph, an arbitrary finite acyclic graph, or another
   representation; also fix depth, finite layer/unit index types, edge orientation, skipped edges,
   and topological ordering.
3. Fix parameter and value types, weight/bias representation, shared or tied parameters, scalar
   field, exact equality notion, and every universe and typeclass assumption.
4. Fix forward semantics, including activation functions, the linear aggregation formula, bias
   nodes, input/output conventions, and whether activations are homogeneous or node-specific.
5. Fix the data and loss contract: finite cases, input/target types, squared-error factor and
   aggregation, batch versus per-case evaluation, regularization, and reduction order.
6. Fix the reverse semantics: output seed, derivative or adjoint convention, recurrence over all
   outgoing edges, accumulation order, parameter-gradient representation, and proof of equality to
   the derivative of the selected loss.
7. Decide whether training includes equation (8)'s plain gradient step, equation (9)'s momentum
   step, online updates, accumulated batch updates, a learning-rate range, termination, or merely
   computation of a gradient.
8. Decide whether any convergence, minimization, or complexity conclusion is included. The 1986
   article explicitly disclaims a global-minimum guarantee, so such a theorem cannot be inferred
   from the title or attribution.
9. Fix exact-real versus floating-point arithmetic and whether rounding, overflow, execution cost,
   memory, parallelism, and numerical error are within scope.
10. Freeze ordered binders, hypotheses, conclusion, alternate encodings and transport directions,
    then elaborate and mutation-test one exact Lean expression.

## Boundary and degenerate cases

The selected source must decide zero-depth and identity networks, no hidden layer, empty input,
output, unit, edge, or case index types, a singleton case, isolated units, zero outgoing edges,
skipped layers, zero weights, bias-only nodes, constant activations, vanishing derivatives, repeated
or shared weights, zero learning rate, empty gradient accumulation, and loss normalization.

It must also decide nondifferentiable activations, arbitrary differentiable activations versus the
source sigmoid, cyclic/recurrent graphs versus finite unrolling, invalid shapes, batch ordering,
and whether equality is extensional, coordinatewise, matrix-based, or expressed through continuous
linear maps. No case is silently excluded at intake.

## Candidate propositions not credited

- A source-faithful theorem that the backward recurrence in equations (4)-(7) computes each
  relevant partial derivative for a finite acyclic sigmoid network and squared loss.
- A theorem that reverse accumulation computes the Frechet derivative or gradient of a selected
  finite composition graph.
- Correctness and termination of one executable backpropagation implementation relative to a
  declarative forward-and-loss semantics.
- Equality between a matrix/layer encoding and an edge-indexed acyclic-graph encoding.
- Correctness of one plain-gradient or momentum update once its derivative is computed.
- A complexity result for one graph representation and cost model.

These are planning candidates, not alternate encodings or statements accepted for `THM-M-1485`.

## Explicit exclusions and neighboring ownership

- `THM-M-1484` neural networks and `THM-M-1486` deep learning are broader architecture/topic
  records, not substitutes for a backpropagation correctness proposition.
- `THM-M-1498` gradient descent and `THM-M-1499` stochastic gradient descent separately own generic
  optimizer claims; backpropagation computes or propagates derivative information and does not by
  itself establish their convergence.
- Modern ReLU/subgradient networks, convolutional or recurrent architectures, automatic
  differentiation systems, and stochastic training are excluded unless the accepted source root
  explicitly includes them.
- Generic chain rules, finite-sum derivatives, sigmoid derivatives, matrix operations, or a
  structure field storing the desired derivative equality are not the requested theorem.
- Successful training runs, numerical residuals, finite examples, benchmarks, plots, or empirical
  classification performance are not proof of exact gradient correctness or convergence.
- The untrusted `已验证` label, source title, and discovery-only Lean probe receive no source or
  proof credit.

## Execution boundary

Intake may record the ambiguity, source lead, candidate clauses, formal substrate, profiles, and
open downstream DAG. It must not choose an exact root, freeze an obligation registry, credit a proof
body, or perform later statement, anchor, proof, validation, or release work. The first downstream
gate is an independently reviewed source-statement decision.
