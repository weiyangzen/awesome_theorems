# Statement freeze

Item: `S56-M-0648-STATEMENT`

`Statement.lean` freezes one paired proposition parameterized by a first-order language. Its first
conjunct is the downward theorem: for every nonempty structure `M`, distinguished set `A`, and
infinite cardinal `kappa` bounding `#A` and `L.card` from above and `#M` from below, there is an
elementary substructure containing `A` whose lifted cardinal is exactly `kappa`. Its second conjunct
is the upward theorem: every infinite `M` elementarily embeds into an `L`-structure of exact
cardinality `kappa` whenever `kappa` bounds both `L.card` and `#M`.

## Encoding decisions

- The universes of language functions, relations, the ambient carrier, and `kappa` are explicit.
- Every cross-universe comparison uses the same `Cardinal.lift` orientation as the corresponding
  pinned mathlib declarations.
- The downward conclusion retains both subset containment and exact cardinality.
- The upward conclusion retains the given model through `Nonempty (M ↪ₑ[L] N)`; elementary
  equivalence without an embedding is not substituted.
- `kappa = #M`, `kappa = aleph0`, `A = empty`, and empty languages are included when the displayed
  hypotheses hold. Upward finite structures are excluded by `[Infinite M]`.
- `canonicalTarget_iff_expanded` checks the direct conjunction expansion by `Iff.rfl`.

The single direct import is `Mathlib.ModelTheory.Satisfiability` from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It is minimal among public modules that expose all
types needed by the statement, including the bundled elementary-extension conclusion. Three
separately elaborated mutations drop the upward half, remove the distinguished-set requirement, or
weaken the upward conclusion to elementary equivalence; their explicit expressions differ from the
canonical target.

This phase establishes exact target elaboration only. It gives no source acceptance, anchor audit,
proof credit, audit completion, or theorem completion.
