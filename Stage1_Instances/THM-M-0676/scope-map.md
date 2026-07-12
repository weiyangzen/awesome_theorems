# Scope map

## Preserved source scope

- Subject: prime models in first-order model theory.
- Requested result family: an existence assertion and a uniqueness assertion.
- Repository provenance: a twentieth-century result attributed only to multiple mathematicians.
- Formal status: the repository's `已验证` label is untrusted metadata and grants no proof credit.

This is all the mathematical scope fixed by the repository source. In particular, the intake does
not assert that every first-order theory has a prime model.

## Decisions required before statement freeze

The statement phase must select an exact source theorem and freeze:

- whether the object is a theory `T`, a complete theory, or a completion of a theory;
- the language cardinality and whether `T` is consistent, complete, countable, or atomic;
- the definition of a prime model: elementary embeddability into every model of `T`, or an
  explicitly proved equivalent formulation;
- the existence hypothesis or criterion, such as density of isolated complete types, and every
  finiteness/countability premise used in constructing a model;
- whether uniqueness means isomorphism, unique isomorphism, or uniqueness up to an elementary map;
- universe levels, model nonemptiness, model cardinalities, and the treatment of an inconsistent
  theory or a theory with no models;
- the ordered quantifiers connecting the existence and uniqueness conclusions.

## Explicit exclusions

- The unconditional claim that every theory or every complete theory has a prime model.
- Uniqueness of a prime model without fixing the language and theory shared by both models.
- Substituting prime substructures, minimal models, atomic formulas, or algebraic prime fields.
- Encoding existence or the universal elementary embedding as a field of an assumed structure.
- Treating a definition, an abstract implication from the desired conclusion, or the metadata
  label `已验证` as proof of the theorem.

A later formal target must expose concrete first-order languages, structures, theory satisfaction,
elementary embeddings, and structure isomorphisms. Any isolated-type or atomic-model condition must
appear as an explicit hypothesis or as a separately checked equivalent criterion.
