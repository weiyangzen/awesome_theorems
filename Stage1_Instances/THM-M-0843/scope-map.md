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

Intake retained both the conventional existential regularity lemma and the equitable effective
version exposed by pinned mathlib as candidates. The statement phase has now selected the latter,
as displayed in Section 3 of the inspected ITP article.

## Frozen binders and conclusion

The canonical target has the following ordered mathematical data:

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

These fields are frozen in `Statement.lean` at arbitrary universe `u`. Its fully explicit
expression, minimal-import environment, and four structural mutations are bound in `statement.json`
and `statement-receipt.json`.

## Statement decisions

- The root requires an equipartition of all vertices, with no exceptional vertex class.
- The root uses the particular effective `bound epsilon l`; its implication to an existential-bound
  form using the same `Finpartition.IsUniform` predicate is kernel-checked.
- The size premise is exactly `l <= Fintype.card alpha`.
- Uniformity uses mathlib's ordered off-diagonal nonuniform-pair count, ignores the diagonal, and
  uses its existing strict pair-uniformity definition.
- The only tolerance premise is `0 < epsilon`; values at least one remain included.
- `l = 0`, empty and singleton types when the size premise permits them, and empty/complete graphs
  are included. `Finpartition` parts are nonempty; no extra boundary restriction is added.
- The target applies to every finite simple graph. The repository's "dense graph" phrase is treated
  as contextual wording, not a global positive-density hypothesis.

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

Independent source review, formal-candidate/provenance audit, obligation and discovery freezes,
proof/composition credit, readable reconstruction, trust closure, hermetic replay, independent
validation, and master acceptance remain open. Exact statement elaboration and the four mutation
classes are self-tested pending master acceptance; they supply no downstream proof credit.
