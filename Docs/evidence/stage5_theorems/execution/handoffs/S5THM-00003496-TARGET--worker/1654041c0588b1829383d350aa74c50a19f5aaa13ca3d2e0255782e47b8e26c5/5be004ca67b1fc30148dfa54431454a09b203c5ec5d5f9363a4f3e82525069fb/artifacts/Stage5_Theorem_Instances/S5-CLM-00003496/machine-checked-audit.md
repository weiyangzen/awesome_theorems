# Machine-checked audit — S5-CLM-00003496

The package contains five claim-owned theorem declarations. Each body is either
`Iff.rfl` or the direct return of an explicit proof premise. There are no local
definitions, abbreviations, parser extensions, instances, axioms, opaque
declarations, unsafe declarations, placeholders, or references to the
sorry-backed provider theorem body.

The exact root proposition states that, eventually in `n`, every finite tree
with `n` edges has a cyclic family of embeddings into `Fin (2*n+1)` whose mapped
edge sets are pairwise disjoint and whose supremum is the complete graph. The
statement audit uses reflexivity, and the forward and reverse transports expose
their proof argument in the theorem type. Thus the package proves the semantic
identity and transport obligations without concealing an oracle.

`machine-closure.json` is the structured declaration and dependency census.
The worker marks it as an M0-L candidate because its local declarations are
closed at trust zero conditional only on their explicit premises; Master must
independently compile the exact integrated bytes, recompute types, bodies,
dependencies and axioms, and decide whether the unconditional theorem root is
acceptable. The worker did not invoke Lean, Lake, or Elan.

Adversarial checks cover removal of the `Mathlib` import, mutation of the cyclic
shift clause, replacement of `Pairwise` by an unrestricted relation, removal of
the complete-graph equality, activation of the numeric provider import, local
shadowing of source symbols, and use of the provider proof body. Every mutation
must invalidate at least one statement, semantic, trust, or build predicate.
