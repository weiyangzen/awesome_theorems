# Scope map

## Included theorem family

The source-supported candidate family has these components, none yet adopted as the canonical
Lean expression:

- a real topological vector space with continuous addition and scalar multiplication;
- a locally convex topology, with the source's separation convention made explicit;
- a nonempty compact convex subset `K`;
- a continuous map of `K` into itself, encoded either as an ambient map preserving `K` or as a
  subtype self-map; and
- existence of a point of `K` fixed by that map, without a uniqueness claim.

The inspected 1935 theorem says that every continuous self-map of a convex compact subset of a
locally convex topological linear space has at least one fixed point. The source definitions and
the translation from its terminology still require an independent row-by-row review before this
family may become the exact target for `THM-M-0638`.

## Proposition-changing decisions

The statement phase must resolve these choices from accepted source evidence and the duplicate-ID
policy, not from convenience:

| Decision | Open alternatives | Why it matters |
|---|---|---|
| target identity | duplicate/alias of `THM-M-0317`, corrected split, or separately retained instance | determines whether one claim is duplicated and how evidence ownership is handled |
| scalar field | the source's real scalars versus a proved generalization | changes typeclass assumptions and source fidelity |
| separation | source-conventional Hausdorff/regular space versus a weaker modern formulation | changes the mathematical statement and compactness behavior |
| domain encoding | ambient subset plus `Set.MapsTo` versus a continuous subtype self-map | requires a checked transport, not prose equivalence |
| continuity | global ambient continuity versus continuity only on the domain | neither form may silently replace the other |
| compactness/nonemptiness | compact in the source's convention versus mathlib `IsCompact` plus explicit nonemptiness | mathlib permits the empty compact set, where the conclusion is false |

The exact universes, ordered binders, hypotheses, conclusion, minimal imports, alternate-encoding
relationship, and foundation profile remain statement-phase outputs.

## Boundary cases and later mutations

- Remove nonemptiness: the empty compact convex set has no in-set fixed point.
- Remove domain preservation: a continuous translation can send a compact interval out of itself
  and have no fixed point in it.
- Move the existential witness outside the domain or before the map binder: this changes the claim.
- Replace local convexity, compactness, convexity, or continuity with a weaker condition: accept
  only if a checked source-faithful transport establishes the relationship.
- Compare the ambient-map and subtype-map conclusions with a kernel-checked equivalence.
- Exercise singleton and zero-dimensional cases without using them as substitutes for the general
  theorem.

## Explicit exclusions

- Tychonoff's compact-product theorem, separately cataloged as `THM-M-0620`.
- Schauder, Brouwer, Kakutani, Markov-Kakutani, or Banach fixed-point theorems as terminal claims.
- A finite-dimensional, normed-space, contraction, affine-map, or set-valued-map specialization.
- An approximate fixed point, an ambient fixed point not shown to lie in `K`, or uniqueness.
- Any hypothesis, structure field, axiom, or opaque declaration that already supplies the fixed
  point or the theorem.
- Transfer of acceptance, proof credit, receipts, or lifecycle state from `THM-M-0317`.

No canonical statement is frozen by this intake. The first downstream gate is exact source and
duplicate-scope reconciliation followed by statement elaboration and mutation tests.
