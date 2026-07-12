# Scope map

## Included topic boundary

- Infinite cardinals and a source-specified definition of weak compactness.
- The exact combinatorial property, characterization, or implication selected by the source.
- All necessary inaccessibility, regularity, strong-limit, coloring, tree, or logical hypotheses.
- Explicit universe and cardinal-representation conventions for the Lean target.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different claims commonly associated with
weak compactness:

1. A partition relation such as a two-color relation on unordered pairs, with precisely specified
   cardinal, coloring domain, and homogeneous subset size.
2. A characterization using strong inaccessibility and the tree property.
3. A compactness theorem for an infinitary language, requiring exact syntax, theory cardinality,
   and satisfiability semantics.
4. An indescribability, extension, filter, or elementary-embedding characterization.
5. One direction of an equivalence, the full equivalence, or merely a consequence of weak
   compactness.

The statement phase must inspect an immutable source and freeze one proposition, ordered binders,
hypotheses, definitions, conclusion, and boundary cases. In particular it must not silently treat
a conventional definition as the requested unspecified "combinatorial properties" theorem.

## Explicit exclusions

- Strong compactness, measurable cardinality, Ramsey cardinality, or ordinary topological weak
  compactness as substitutes.
- Replacing an equivalence with an easier implication, or assuming the desired combinatorial
  property and projecting it back as the conclusion.
- Treating mathlib's universe cardinal `Cardinal.univ` or `Cardinal.IsInaccessible.univ` as an
  ordinary ZFC existence theorem for a weakly compact cardinal.
- Any convenient fact about inaccessible cardinals absent a checked source-statement crosswalk.
- The repository label `已验证` as human-source or kernel-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.
