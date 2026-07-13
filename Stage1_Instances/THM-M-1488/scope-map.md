# Scope map

## Preserved scope

The repository supports only a recurrent-neural-network topic family for sequence processing. A
standard real-valued cell might update a hidden state by an affine map of the previous state and
current input followed by a coordinatewise activation, but even that recurrence is not present in
the source. It is an inventory aid, not the accepted target.

## Decisions required at statement freeze

1. Choose a truth-valued root: a recurrence/unrolling identity, expressivity or approximation
   theorem, state stability or contraction result, finite/infinite-memory result, gradient
   vanishing/explosion result, training convergence, generalization, or another source-selected
   conclusion.
2. Fix the architecture: Elman/Jordan cell, LSTM, GRU, bidirectional or stacked recurrence, other
   feedback graph, and whether parameters are shared across time. Fix every gate and update rule.
3. Fix time and sequence semantics: `Nat` or finite-index time, finite or infinite horizon, variable
   length and padding/masking convention, causal direction, state before or after the current input,
   and whether an output is produced at every step or only at the end.
4. Fix scalar field, finite or infinite dimensional state/input/output spaces, index types,
   universes, matrix or linear-map representation, weights, recurrent and output biases, parameter
   carrier, and evaluator semantics.
5. Fix activation and gate functions, coordinatewise lifting, regularity/Lipschitz/boundedness
   assumptions, initial state, input admissibility, and state or parameter constraints.
6. For approximation or memory claims, fix the sequence domain and topology, target causal
   functional or transducer class, norm/error metric, tolerance quantifiers, widths/state dimension,
   horizon dependence, and whether the result is uniform, pointwise, probabilistic, or in `Lp`.
7. For stability or gradient claims, fix norms, perturbation variables, Jacobian convention,
   spectral/operator bounds, constants, quantifier order, finite versus asymptotic horizon, and the
   exact conclusion. For learning claims, also fix data law, labels, loss, optimizer,
   initialization, stochastic assumptions, convergence mode, and rate.
8. Fix ordered binders, hypotheses, conclusion, alternate encodings and directions, logical and
   choice policy, computation boundary, and every source-required constant dependency.
9. Resolve empty and singleton sequences, horizon zero, empty input/state/output index types, zero
   state dimension, constant activations, zero parameters, missing initial state, unbounded states,
   zero tolerance, nonattained optima, and exact versus floating-point arithmetic.
10. Select an immutable primary or approved authoritative source with an exact theorem/definition
    locator, incorporated definitions, assumptions, proof boundary, corrections, translation
    policy, and independent source and scope review.

## Candidate families not credited

- Equivalence between a source-selected recurrence and an unrolled feed-forward computation.
- A universal approximation or expressivity theorem for a source-selected recurrent architecture.
- Contractive-state stability, fading-memory, or input perturbation bounds under exact hypotheses.
- Vanishing/exploding gradient bounds for a source-selected cell, loss, and Jacobian convention.
- Training, generalization, sequence-classification, language-modeling, or forecasting results.

No candidate is selected, combined, or credited at intake. A definition or evaluator identity alone
cannot silently become the unidentified theorem.

## Neighbor ownership and exclusions

- `THM-M-1484` owns generic neural networks; it donates no architecture, statement, or proof.
- `THM-M-1485` owns backpropagation; backpropagation through time does not identify this root.
- `THM-M-1486` owns deep learning, `THM-M-1487` convolutional networks, and `THM-M-1489`
  Transformers. Their architectures, tasks, and results are distinct.
- Generic `List.foldl`, matrix multiplication, scalar sigmoid facts, iteration lemmas, dynamical
  systems results, or sequence algorithms are substrate only.
- A structure or hypothesis storing the wanted recurrence property, a trained model, benchmark,
  sampled sequence, plot, floating-point experiment, or unchecked certificate is not a proof.
- The catalog label `已验证`, bibliographic metadata, an API probe, and a bounded search give no H
  or M credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, matrix-vector
multiplication, scalar sigmoid properties, and list folds can support some future RNN encodings.
`IntakeProbe.lean` checks representative declarations. They provide no recurrent cell, sequence
evaluator, source-selected proposition, or target proof. The bounded repository search is intake
discovery, not the downstream anchor audit or a global absence claim.

No canonical Lean target, checked transport, expression fingerprint, discovery-protocol hash,
obligation registry, or proof state is frozen in this phase.
