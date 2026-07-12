# Scope map

## Provisional included claim

- A first-order structure expanding a dense linear order and satisfying o-minimality: every unary
  definable set, with the source's parameter convention, is a finite union of points and intervals.
- A unary partial function with definable graph and interval domain.
- The monotonicity conclusion: a finite partition into points and intervals on which the function
  is continuous and either constant, strictly increasing, or strictly decreasing.
- Only the one-variable structural theorem selected by primary-source review. The separate
  cell-decomposition result remains owned by `THM-M-0664`.

This family is provisional because the repository says only "properties of o-minimal structures".
It supplies a concrete boundary for source review, not an exact statement or proof target.

## Statement-phase decisions

The statement phase must inspect and select an exact primary theorem before elaboration. It must
freeze whether parameters are allowed, whether the order has endpoints, the domain's endpoint
convention, partial versus total functions, the representation of finite partitions, continuity in
the order topology, strict monotonicity directions, and the treatment of empty, singleton, and
unbounded pieces. It must also freeze the language-map evidence showing that the first-order
structure really expands the order structure rather than merely placing unrelated structures on one
carrier.

Required mutations include removing o-minimality, weakening definability of the graph, changing the
function domain, moving the finite partition existential under a point quantifier, and replacing
strict monotonicity with an unjustified global conclusion.

## Explicit exclusions

- O-minimality's defining unary-set condition by itself; that is a premise/definition, not the
  provisional theorem conclusion.
- Full cell decomposition, cylindrical decomposition, definable triangulation, dimension theory,
  definable choice, or uniform finiteness as an interchangeable root.
- The Pila-Wilkie counting theorem or any arithmetic consequence of o-minimality.
- A finite partition or monotonicity proof supplied as a field of an abstract package.
- A theorem about ordinary continuous real functions with no definability or o-minimal hypothesis.
- The repository label `已验证`, adjacent API checks, or the intake probe as proof evidence.
