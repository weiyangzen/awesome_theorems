# THM-M-1486 scope map

## Catalog scope preserved

- Target identity: `THM-M-1486`, named `深度学习` (deep learning).
- Catalog attribution and date: many mathematicians, twenty-first century.
- Literal gloss: `深层神经网络` (deep neural networks).
- Recognizable subject boundary: mathematical models or results involving neural networks with
  multiple composed representation layers.

This identifies a research field and model family, not one mathematical proposition. The word
`deep` does not determine a numerical threshold, architecture, function class, learning problem,
or result.

## Decisions required before statement freeze

An accountable source correction must select one immutable proposition and freeze:

1. The result kind: a proposition about a source-frozen definition, expressiveness or
   approximation, depth/width separation, training or optimization convergence, statistical
   generalization, stability or robustness, verification, or an algorithmic complexity theorem.
2. The network architecture and graph semantics: feedforward, convolutional, recurrent,
   transformer, arithmetic circuit, residual, or another source-specific family; layer order,
   depth, widths, connectivity, parameter sharing, pooling, biases, and output interpretation.
3. The scalar, input, output, parameter, label, and data domains; finite-dimensional coordinates or
   function spaces; norms, topology, measure, probability, universes, and typeclass context.
4. Every activation, aggregation, normalization, loss, regularizer, initializer, optimizer,
   update recurrence, stopping rule, and exact-versus-floating-point convention used by the claim.
5. The target function or distribution, sample model, independence assumptions, noise, hypothesis
   class, realizability or regularity assumptions, and whether the claim is deterministic,
   almost-everywhere, in probability, or in expectation.
6. The observable and comparator: approximation error, tensor or matrix rank, network size,
   training loss, population risk, convergence rate, sample complexity, Lipschitz bound,
   robustness radius, or verified input-output property.
7. The exact conclusion, constants and rates, uniformity, asymptotic regime, strict or weak
   inequalities, existence versus construction, quantifier order, and probability or measure-zero
   exceptional set.
8. Every boundary and degenerate case, minimal Lean imports, expression fingerprint, foundation,
   TCB and computation profiles, checked alternate encoding, and required statement mutation.

These choices change truth conditions and proof obligations. They are a resolution checklist, not
a canonical claim.

## Candidate theorem families not credited

- A source-selected universal approximation theorem for a fixed activation, compact domain,
  function class, norm, and depth/width regime.
- A source-selected depth-separation or network-capacity theorem comparing deep and shallow
  architectures under exact size and approximation conventions.
- Cohen, Sharir, and Shashua's tensor-rank theorem or its deep-versus-shallow corollary for
  convolutional arithmetic circuits.
- Bentkamp's Isabelle/HOL `fundamental_theorem_network_capacity_v3`, which characterizes a
  measure-zero set of deep weights representable by a too-small shallow model in its exact locale.
- Convergence of gradient descent, stochastic gradient descent, backpropagation, or another
  optimizer on a selected network and loss landscape.
- A generalization, consistency, robustness, fairness, privacy, interpretability, or verified
  architecture result.

These are inequivalent or differently scoped propositions. Intake admits none without a source
identity decision and independent review.

## Boundary and degenerate cases

The statement phase must decide zero, one, and multiple hidden layers; empty layers and zero width;
zero-dimensional inputs and outputs; constant, linear, discontinuous, saturated, or unbounded
activations; absent or shared biases; zero and duplicate parameters; disconnected graphs; empty or
inconsistent training sets; constant labels; zero or infinite loss; nonunique optima; divergent or
stationary optimization; singular covariance or rank-deficient tensors; measure-zero parameter
sets; equality cases in size bounds; exact real arithmetic versus floating point; randomized
initialization; and whether architecture size counts parameters, units, channels, edges, depth, or
operations.

No case is excluded at intake. Assuming the desired approximation, separation, convergence, or
generalization property as a structure field would be circular if the selected root is meant to
establish it.

## Neighbor and substitution exclusions

- `THM-M-1484` separately names neural networks in general.
- `THM-M-1485` separately owns the backpropagation algorithm; its chain-rule correctness or
  complexity cannot silently become this target.
- `THM-M-1487` and `THM-M-1488` separately name convolutional and recurrent neural networks.
- `THM-M-1489` separately names transformers. One of these architectures cannot be silently made
  the generic deep-learning root.
- Generic matrix multiplication, tensor/holor CP-rank, continuity, polynomial density, derivative,
  probability, or optimization infrastructure is substrate only.
- A trained numerical model, benchmark score, finite experiment, sampled countercheck, floating-
  point loss trace, or unchecked certificate cannot establish an unidentified theorem.
- The untrusted `已验证` label, title match, AFP page, and discovery probe supply no H or M credit.

## Formal and execution boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Data.Holor` provides multidimensional arrays, tensor products, CP-rank predicates, and
rank upper bounds. It cites the AFP Deep Learning tensor library, but it contains no network,
activation, training, deep-versus-shallow, or network-capacity declaration. The pinned
Stone-Weierstrass module provides general polynomial-density theorems, not a neural-network
universal-approximation theorem.

A bounded exact-topic search, excluding this owned discovery probe, found only the neural-network
wording in the `Holor` module and no pre-existing source-identical repo-local Lean declaration. This
is intake discovery, not an exhaustive anchor audit or global
absence proof. Later phases own exact source selection, Lean statement identity, external-candidate
provenance, obligation freezing, typed graphs, proof bodies, composition, trust, readable
reconstruction, and release evidence.
