# Scope map

## Included claim

- An arbitrary type `P` equipped with a partial order `≤`.
- A chain represented as a subset `c : Set P` whose distinct elements are comparable under `≤`.
- Existence of a chain `c` that is maximal under set inclusion: every chain containing `c` equals
  `c`.
- Empty and singleton underlying types. For the empty type, the empty subset is the maximal chain;
  no unnecessary `Nonempty P` hypothesis is introduced.

This is an existence theorem. It does not select a unique maximal chain and makes no finite,
countable, cardinality, well-foundedness, or completeness assumption on the partial order.

## Statement-phase decisions

The canonical Lean target uses the direct existential form
`∀ (P : Type u) [PartialOrder P], ∃ c : Set P, IsMaxChain (· ≤ ·) c`. It does not mention
mathlib's constructed witness and does not import its defining module. A checked iff expands
`IsMaxChain` at the statement boundary. The common extension form and mathlib's arbitrary-relation
strengthening remain noncanonical alternates requiring separate source and proof transports.

## Explicit exclusions

- Zorn's lemma: existence of a maximal element when every chain has an upper bound.
- The well-ordering theorem, axiom of choice, Tukey's lemma, or Kuratowski-Zorn as a substituted root.
- A maximum/greatest chain by cardinality, a longest finite chain, or a maximal element of `P`.
- A linearly ordered subset assumed as input without proving its inclusion-maximality.
- A structure carrying the desired maximal chain as a field.
- The arbitrary-relation mathlib theorem as exact source credit before statement specialization and
  source review.

## Degenerate and mutation boundaries

Later statement tests must cover the empty type, a singleton type, an antichain with at least two
elements, and a total order. They must reject mutations replacing inclusion-maximality by mere
chainhood, replacing equality of containing chains by only one inclusion, or asserting that the
maximal chain contains every element of the poset.
