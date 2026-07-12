# Scope map

## Included theorem boundary

- A single fixed finite group presentation, not an input presentation varying uniformly.
- A finite generator alphabet and finite relator collection with an effective finite encoding.
- Words over generators and formal inverses, with equality to the identity interpreted in the
  quotient group determined by the presentation.
- Nonexistence of an algorithm/computable predicate deciding that identity relation for every word
  in the chosen fixed presentation.

This is the standard existential reading of the Novikov-Boone theorem. It is provisional until an
immutable source passage and independent source review fix the exact formulation.

## Statement-freeze decisions

1. The canonical repository target uses the fixed-presentation existential reading; whether an
   accepted primary source states this exact strength remains an open source-audit question.
2. Generators are `Fin n` and relators are `Finset (FreeGroup (Fin n))`.
3. Words are effectively coded by `List (Fin n × Bool)` and evaluated by `evalWord`.
4. The root uses the one-word identity predicate. No two-word equality transport is yet credited.
5. Undecidability is `¬ ComputablePred`; proof reductions and their foundation profile remain open.

## Explicit exclusions

- The false universal assertion that all groups or all finitely presented groups have undecidable
  word problem.
- The mere existence of groups for which a particular algorithm is slow or unknown.
- Post's correspondence problem, the halting problem, or another undecidable problem as a
  substitute; it may occur only as an explicit checked reduction dependency.
- Word problems for semigroups, monoids, rings, rewriting systems, or formal languages as the root.
- An arbitrary relation named `wordProblem` together with assumed noncomputability.
- A quotient-equality proposition without an effective word coding and computability semantics.
- The repository label `\u5df2\u9a8c\u8bc1` as human-proof or machine-proof evidence.

The statement phase freezes the canonical Lean expression. The obligation registry and discovery
result remain open.
