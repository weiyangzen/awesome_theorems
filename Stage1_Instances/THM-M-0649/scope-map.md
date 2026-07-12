# Scope map

## Included claim

- All structures use one first-order language and have nonempty carriers.
- The index is a nonempty linear order; an ordinal or natural-number chain is a special case, not
  the canonical restriction.
- For every `i <= j`, the transition from `M_i` to `M_j` is a compatible elementary inclusion.
- The union is equipped with the unique induced language structure compatible with the chain.
- Every chain member, not merely the first one, embeds elementarily into the union.
- Singleton chains and chains with a greatest element are included.

## Formal encoding boundary

There are two faithful-looking encodings. A common-ambient encoding represents every `M_i` as an
elementary substructure of one structure and uses the supremum of the underlying substructures. A
typed encoding represents distinct carriers with compatible elementary embeddings and constructs a
direct limit. The statement phase must select a canonical form and provide checked transports for
the other; it may not quietly assume a common ambient model merely because that is easier in Lean.

Pinned mathlib exposes `Language.ElementaryEmbedding`, `Language.ElementarySubstructure`,
`Substructure.IsElementary`, `Substructure.isElementary_of_exists`, directed membership in
`Substructure.iSup`, and first-order direct limits. These are ingredients, not the root theorem.

## Statement-phase decisions

Freeze universe levels and binder order; the exact compatibility law for transition maps; whether
linear order is stated directly or generalized to a nonempty directed preorder; construction and
nonemptiness of the union/direct limit; and the exact meaning of "elementary extension" (an
elementary inclusion into the union rather than mere elementary equivalence). Mutation tests must
cover removal of elementarity, removal of compatibility, an empty index, changed binder scope, and
replacement of linear/directed order by an arbitrary relation.

## Explicit exclusions

- A union of arbitrary elementary substructures without directedness.
- Mere closure of a union under language operations without elementarity.
- Elementary equivalence of the members as a substitute for elementary inclusion into the union.
- The compactness theorem, Lowenheim-Skolem theorem, or Tarski-Vaught test alone.
- A structure that assumes the required elementary union map as a field.
- The repository label `已验证` or the intake probe as proof evidence.
