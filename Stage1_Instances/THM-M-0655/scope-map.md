# Scope map

## Preserved repository scope

- Subject: consistency or semantic satisfiability of the union of two first-order theories.
- Leading identification: the Robinson joint consistency theorem for theories whose signatures
  overlap in a common language.
- Expected substantive condition: the theories have no opposed consequences in that common
  language, rather than merely being consistent in isolation.
- Expected conclusion: models of the theories can be made jointly compatible in a suitable union
  signature, equivalently their translated union is satisfiable, subject to the selected source.

These bullets delimit a candidate theorem family. They do not freeze an exact proposition because
the repository supplies neither the compatibility hypothesis nor language and consistency
conventions.

## Required statement decisions

The source and statement phases must identify whether the theorem is Robinson joint consistency,
and whether `THM-M-0654` is an alias, a different formulation, or an accidental duplicate. They
must then fix semantic satisfiability versus syntactic consistency, first-order calculus and
nonempty-domain convention, the common and union signatures, embeddings or inclusions between
languages, translation of sentences and theories, and the exact separation condition. Any use of
Craig interpolation, compactness, or completeness must appear as a checked dependency rather than
being folded silently into the statement.

Boundary cases include identical signatures, disjoint signatures, empty theories, an empty common
signature, and inconsistent input theories. The source decides whether separate consistency is an
explicit hypothesis or follows from the no-separator condition under its conventions.

## Explicit exclusions

- The false unrestricted implication `Consistent T1 -> Consistent T2 -> Consistent (T1 union T2)`.
- The tautology that a union already assumed consistent is consistent.
- Directed-union compactness or satisfiability, which concerns a compatible chain of theories.
- Combining models over disjoint signatures without addressing overlapping-symbol agreement.
- Replacing first-order theories by propositional sets, complete theories, or finite theories just
  because the encoding is easier.
- Treating the adjacent Robinson entry, the metadata label `已验证`, or an upstream theorem name as
  proof or source-fidelity evidence.
