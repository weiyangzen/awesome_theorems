# Scope map

## Repository boundary

- Target: `THM-M-0843`, "Szemerédi regularity lemma", graph-theory category.
- Literal gloss: a regular partition of a dense graph.
- Attribution/year: Endre Szemerédi, 1975.
- Lifecycle: `planned` from the uniform `L0 / rework_required` baseline.
- The catalog label `已验证` is untrusted metadata and receives no human or machine proof credit.

## Included theorem family

The intended family concerns a finite simple graph and a decomposition of its entire vertex set
into finitely many nonempty parts. For a positive real tolerance, all but a controlled proportion
of the off-diagonal pairs of parts must be regular/uniform: sufficiently large subsets of a pair
have edge density close to that of the original pair. The number of parts is bounded independently
of the graph.

This scope includes the conventional existential regularity lemma and the equitable effective
version exposed by pinned mathlib as candidates. It does not yet choose between them.

## Candidate binders and conclusion

The pinned candidate has the following ordered mathematical data:

1. a finite vertex type `alpha`, decidable equality, and its finite enumeration;
2. a finite simple graph `G` with decidable adjacency;
3. a real tolerance `epsilon`;
4. a natural lower bound `l`;
5. hypotheses `0 < epsilon` and `l <= card alpha`.

It concludes that there is a finite partition `P` of the full vertex finset such that:

- `P` is equitable, so any two part sizes differ by at most one;
- `l <= card P.parts`;
- `card P.parts <= bound epsilon l`, for mathlib's explicit graph-independent bound;
- `P` is `epsilon`-uniform under mathlib's off-diagonal ordered-pair convention.

These are candidate fields only. The statement phase must freeze the canonical human proposition,
the precise ordered Lean binders and universes, minimal import, normalized expression and
environment fingerprint, and checked source-to-candidate relationship.

## Decisions deferred to statement freeze

- Whether the root requires an equipartition or only a partition plus an exceptional class.
- Whether the upper bound is existential or the particular effective `bound epsilon l`.
- Whether the graph-size hypothesis is `l <= |V|` or a separate threshold depending on the
  tolerance and requested number of parts.
- Whether uniformity counts ordered or unordered off-diagonal pairs, whether the diagonal is
  ignored, and whether the exceptional-pair bound is strict or non-strict.
- Whether the tolerance is restricted to `epsilon <= 1`; the pinned theorem's type accepts every
  positive tolerance, but the behavior and source relationship for `epsilon > 1` remain to be
  audited.
- The treatment of `l = 0`, the empty vertex type, singleton graphs, empty/complete graphs,
  empty parts, and a zero-part partition.
- The exact relationship between "dense graph" in the repository gloss and the pinned theorem,
  which applies to every finite simple graph and does not assume positive global edge density.

## Explicit exclusions

- Szemerédi's theorem on arithmetic progressions (`THM-M-0948`), the triangle-removal lemma, or an
  application of regularity as a substitute for this root.
- Hypergraph, sparse, directed, weighted, degree, diagonal, or algorithmic regularity variants.
- A partition predicate assumed as input, a tautological projection of an assumed witness, or a
  theorem only asserting that regularity definitions are available.
- The neighboring Alon-Fischer-Newman testing result (`THM-M-0844`).
- The ITP paper's display snippets with omitted proofs as proof evidence; only the actual pinned
  mathlib terminal object can receive later kernel credit.
- The untrusted catalog status or theorem-name match as H0, M0, audit, or theorem completion.

## Current cut set

Source-variant selection and independent review, exact Lean statement elaboration and mutation
tests, formal-candidate/provenance audit, obligation and discovery freezes, proof/composition
credit, readable reconstruction, trust closure, hermetic replay, independent validation, and
master acceptance remain open.
