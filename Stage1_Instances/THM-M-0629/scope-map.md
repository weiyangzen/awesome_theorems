# Scope map

## Preserved catalog scope

The intake preserves the named Alexandroff one-point compactification family for locally compact
Hausdorff spaces. A conventional full formulation starts with a topological space `X`, adjoins one
point, embeds `X` as the complement of that point, and establishes compactness and Hausdorffness;
under the classical compactification convention the image is also dense, normally requiring `X`
to be noncompact. This is a scope description, not a frozen statement.

## Proposition-changing decisions

An approved source and statement review must settle all of the following:

1. Whether the input is locally compact Hausdorff, weakly locally compact Hausdorff, or explicitly
   noncompact locally compact Hausdorff, with a checked relationship between conventions.
2. Whether "compactification" means a constructed carrier and topology, an existence theorem, a
   bundled embedding into a compact Hausdorff space, or a universal/uniqueness characterization.
3. Whether the root includes compactness, Hausdorffness or T4 separation, continuity and embedding,
   openness of the image, density, the singleton complement, or some exact conjunction.
4. Whether a compact input is permitted. Mathlib then adds an isolated infinity and the embedding
   is not dense; excluding this case changes the theorem's domain.
5. The topology at infinity, including whether neighborhoods are complements of compact sets or
   closed compact sets and which separation assumptions make these formulations agree.
6. The carrier, universes, ordered binders, implicit typeclass assumptions, witness data, equality
   orientations, exact conclusion, foundation profile, and every credited alternate encoding.
7. Whether uniqueness is literal equality, equivalence, or homeomorphism over the embedding, and
   whether it assumes an embedding with range exactly the complement of a designated point.
8. The exact source edition, theorem/page, incorporated definitions, proof boundary, translation,
   corrections and errata, plus independent source and Lean review.

## Boundary and mutation cases

Source and statement review must explicitly handle empty, singleton, finite discrete, infinite
discrete, compact, noncompact, connected, and non-Hausdorff inputs. Required mutations include
removing local compactness or Hausdorffness, removing noncompactness from a density claim, changing
the input domain, changing binder scope, replacing singleton complement by merely nonempty
complement, and confusing an open embedding with a dense embedding.

No case is silently excluded at intake. In particular, `OnePoint Empty` is a one-point compact
space, while a compact `X` receives a new isolated point; these construction facts do not by
themselves establish the source's intended meaning of compactification.

## Excluded substitutions and ownership

- `THM-M-0628` owns the broad local-compactness topic and transfers no statement or proof credit.
- `THM-M-0630` owns Stone-Cech compactification; its maximality/universal property is distinct.
- A sphere or projective-line model is a specialized example, not the general root.
- Compactness of `OnePoint X` alone, Hausdorffness alone, density alone, or the uniqueness
  homeomorphism alone cannot replace an unresolved bundled theorem.
- A structure or hypothesis storing the desired compactification, the catalog's verified label,
  or a successful API probe supplies no source or proof credit.

## Lean boundary

Pinned module `Mathlib.Topology.Compactification.OnePoint.Basic` constructs `OnePoint X` as
`Option X`. It provides the extra point, canonical open embedding, singleton complement,
unconditional compactness, density under `NoncompactSpace X`, T4 separation under weak local
compactness and Hausdorffness, and a uniqueness homeomorphism for an embedding into a compact
Hausdorff space whose range is exactly one-point-complementary. These are direct `M3` interfaces,
not an exact statement receipt. Minimal imports, canonical expression and environment fingerprints,
checked composition, mutation tests, proof-body provenance, and trust closure remain downstream.
