# Scope map

## Included theorem family

- A first-order language and a theory `T` in that language.
- Model completeness as the property that every embedding between models of `T` is elementary.
- A necessary-and-sufficient criterion for that property, if an exact criterion is selected from
  the primary source. Plausible candidates include preservation or existential-formula criteria,
  but no candidate is promoted at intake.
- The semantic and syntactic notions needed by the selected source: models, theory satisfaction,
  embeddings, elementary embeddings, formulas, parameters, and equivalence modulo `T`.

## Decisions required at statement freeze

The statement phase must select an immutable primary-source edition and exact theorem. It must then
freeze whether the result is a definition, an iff criterion, or an application to a particular
theory; whether `T` is assumed consistent, complete, or inductive; the language cardinality and
finitary conventions; treatment of free variables and parameters; whether existential formulas are
quantifier-free after their leading quantifiers; the direction and type of structure embeddings;
and every use of compactness, diagrams, or preservation theorems. Empty theories, theories with no
models, empty structures, and inconsistent theories require explicit boundary decisions.

## Explicit exclusions

- Godel completeness, completeness of a theory, quantifier elimination, model completion, or
  elimination of imaginaries as substitutes for model completeness.
- The assertion that a named theory is model complete unless that is the exact selected source
  theorem.
- A Lean structure carrying elementarity of every embedding as assumed data and then projecting it.
- Treating the repository label `已验证`, the attribution, or the year as proof or source-fidelity
  evidence.

No Lean target is frozen at intake. A later target must expose the actual first-order semantic and
syntactic objects and may not assume the desired criterion or conclusion as a field or hypothesis.
