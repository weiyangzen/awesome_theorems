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

The statement phase must freeze universe binders and choose between the direct existential form

`∃ c : Set P, IsMaxChain (· ≤ ·) c`

and an explicitly checked specialization of mathlib's constructed witness
`maxChain (· ≤ ·)`. It must inspect whether the primary edition states bare existence or the common
extension form saying that every chain is contained in a maximal chain. The latter must not silently
replace the repository's bare-existence wording. If the arbitrary-relation strengthening exposed by
mathlib is retained, a checked specialization/crosswalk must preserve the partial-order source
claim rather than broaden the canonical target without notice.

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
