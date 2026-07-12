# Scope map

## Included claim

- A first-order language `L` and an infinite `L`-structure `M`.
- A target infinite cardinal `kappa` satisfying the language-size and source-model-size bounds.
- An `L`-structure `N` whose carrier has cardinality exactly `kappa`.
- An elementary embedding from `M` into `N`, which supplies the stated elementary equivalence.
- The universal cardinal reading of "arbitrarily large": every `kappa` above the required bounds,
  not only the existence of one larger model.

## Boundary decisions for the statement phase

The next phase must freeze the exact cardinal inequalities, universe lifts, binder order, and the
mathlib representation of the output model. It must also decide whether the canonical statement
names an elementary extension/embedding or only elementary equivalence. The stronger embedding
form matches the pinned upward theorem and implies the repository wording, but a checked bridge and
pinpoint source crosswalk are required before that strengthening is canonical.

Boundary cases requiring explicit tests are `kappa = #M`, a finite `M`, a finite `kappa`, a language
larger than `kappa`, an empty language, and mutation from elementary embedding to an arbitrary
function or plain structure embedding.

## Explicit exclusions

- The downward Loewenheim-Skolem theorem about small elementary substructures as a substitute.
- The assertion that an infinite theory merely has some larger model without relation to `M`.
- Isomorphism, rather than elementary equivalence, between models of different cardinality.
- A cardinality-only package lacking a concrete first-order structure and semantic relationship.
- The adjacent Loewenheim-Skolem-Tarski entry or the combined upward/downward entry as duplicate
  proof credit.

The later formal statement must preserve the exact repository claim while recording which modern
named variant it formalizes.
