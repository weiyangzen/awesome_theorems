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

## Decisions required at statement freeze

1. Whether the accepted source states existence of one finitely presented group or a uniform
   undecidability result about finite presentations, and which direction is canonical.
2. The concrete finite generator and relator types, including whether relators are a finite set or
   list and how finiteness is carried into computation.
3. The computable word code. Mathlib's abstract `FreeGroup` and `PresentedGroup` quotient express
   the algebra, but noncomputability requires a `Primcodable` or equivalent effective input type.
4. The exact word predicate: equality of two words or the equivalent identity problem for one
   word. Any equivalence used for credit needs a checked transport.
5. The computability notion and its foundation profile, plus every reduction theorem needed to
   connect the historical proof to that predicate.

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

The intake does not freeze a canonical Lean expression, obligation registry, or discovery result.
