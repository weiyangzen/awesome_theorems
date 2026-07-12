# Scope map

## Available source boundary

The repository supplies the name “Resolution principle,” attributes it to
John Alan Robinson in 1965, and glosses it as a method of automated theorem
proving. It supplies no mathematical binders or conclusion. Robinson's 1965
JACM paper is an appropriate primary-source candidate, but identifying the
paper does not choose one of its results as this target.

## Mutually distinct candidate roots

| Surface | Typical proposition | Why it is not adopted at intake |
|---|---|---|
| Local soundness | A resolvent is entailed by its parent clauses | Too weak to mean completeness of the method |
| Propositional completeness | Every unsatisfiable finite propositional clause set derives the empty clause | Adds a propositional domain and finiteness convention absent from the source |
| First-order completeness | Every unsatisfiable first-order clause set has a lifted resolution refutation | Requires choices about unification, factoring, variable hygiene, equality, and compactness |
| Lifting | A ground resolution derivation can be lifted to first-order clauses | Normally a bridge lemma, not necessarily the named root |

These are related results, not interchangeable encodings. No implication or
equivalence between them is credited here.

## Parameters that must be frozen

The source-resolution decision must specify:

- the term, literal, clause, substitution, and clause-set representations;
- propositional or first-order semantics and whether clause sets are finite;
- the exact resolution, factoring, and standardizing-apart rules;
- whether equality is absent, axiomatized, or handled by a stronger calculus;
- whether completeness means semantic entailment completeness or refutation completeness;
- the roles of Herbrand's theorem, unification, lifting, and compactness;
- boundary behavior for the empty clause, tautological clauses, empty clause sets,
  duplicate literals, and variable renaming.

Until those choices are source-backed, the Lean module, universes, ordered
binders, hypotheses, conclusion, foundation profile, and mutation fixtures
must remain open. This is an `M4` statement blocker, not permission to choose
the easiest formal theorem with a similar name.
