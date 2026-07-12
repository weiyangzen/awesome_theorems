# Scope map

## Included topic boundary

- Decision languages and an exact computational encoding.
- A source-specified definition of polynomial time and nondeterministic or oracle computation.
- The finite levels conventionally denoted by `Sigma_k^P`, `Pi_k^P`, and `Delta_k^P`, if selected.
- The exact definition, characterization, containment, or collapse proposition named by the source.
- Every needed convention about reductions, completeness, uniformity, complements, and level zero.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these non-interchangeable readings:

1. A definition of the polynomial hierarchy as the union of its finite alternating levels.
2. A quantified-predicate characterization of a fixed level.
3. Standard containments between levels or the containment of the hierarchy in PSPACE.
4. A conditional collapse theorem, such as collapse following equality of adjacent levels.
5. Existence of complete problems for a level under a specified reduction.
6. Strictness of levels, which must not be presented as a proved unconditional theorem.

The statement phase must select a pinpoint source and freeze one proposition, ordered binders,
machine/cost model, encodings, polynomial-bound convention, oracle or alternation semantics, class
indexing, hypotheses, and conclusion. It must separately decide complements, empty instances,
index zero, encoding invariance, and whether reductions are many-one or Turing reductions.

## Explicit exclusions

- The polynomial hierarchy as a topic or definition substituted for a theorem about it.
- The exponential hierarchy, arithmetical hierarchy, or projective hierarchy.
- `P = NP`, strictness of PH, or noncollapse as if currently proved.
- A conditional collapse statement with its premise removed.
- A containment theorem with a different machine, oracle, uniformity, or reduction convention.
- A finite toy hierarchy packaged as assumed predicates and tautological set inclusions.
- The repository label `已验证` as evidence of a human or machine proof.

No canonical Lean target is frozen at intake because the source record does not identify one.
