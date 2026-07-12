# Scope map

## Included claim

- An ambient locally convex real topological vector space `E`.
- A subset `K : Set E` that is nonempty, compact, and convex over `Real`.
- A family indexed by an arbitrary type, whose members are continuous affine self-maps of `K`
  (or ambient maps preserving `K`, with a checked transport between the encodings).
- Pairwise commutation under composition on `K`.
- One point of `K` fixed simultaneously by every member of the family.

The empty indexing family is included: its conclusion reduces to the stipulated nonemptiness of
`K`. Infinite families are included, not merely finite commuting families.

## Decisions deferred to the statement phase

The formal statement must decide whether maps are defined directly on the subtype `K` or on the
ambient space with an invariant-set hypothesis; whether the scalar field is exactly `Real` or a
supported ordered topological field; and the precise Lean formulation of pairwise commutation.
It must also inspect the selected primary theorem to determine its separation assumptions and
whether local convexity is stated on the ambient space or encoded through a separating family of
seminorms. Binder order, universes, imports, foundation profile, and degenerate cases must then be
frozen and mutation-tested.

## Explicit exclusions

- The Kakutani set-valued fixed-point theorem, the Riesz-Markov-Kakutani representation theorem,
  or a fixed-point theorem for Markov chains.
- A theorem for one map only, or for a finite family only, as a substitute for the full family.
- Arbitrary continuous self-maps: affinity and pairwise commutation are part of this target.
- A noncompact, nonconvex, or empty domain; a point fixed by only one family member; or a point in
  the ambient space not proved to belong to `K`.
- A structure that assumes a common fixed point as data, or an implication whose hypotheses already
  contain the desired conclusion.

The checked intake probe is vocabulary evidence only. It is not the canonical statement and gives
no machine-proof credit.
