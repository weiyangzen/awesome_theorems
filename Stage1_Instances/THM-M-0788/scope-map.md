# Scope map

## Included topic boundary

- Set-theoretic large-cardinal notions, explicitly including inaccessible and measurable cardinals.
- An exact source-selected proposition about one or more such notions.
- The object theory, metatheory, model encoding, consistency predicate, and all additional axioms
  required by that proposition.
- A checked separation between object-theoretic cardinals and Lean universe cardinals.

## Ambiguities to resolve at statement freeze

The repository record does not choose among materially different targets:

1. An **existence axiom**, such as `there exists a strongly inaccessible cardinal`.
2. A **conditional theorem** deriving a consequence from an assumed large cardinal.
3. A **relative consistency or independence theorem** relating an object theory plus a
   large-cardinal axiom to another theory.
4. A **definition/characterization theorem** for inaccessible, measurable, or another cardinal.
5. A hierarchy or consistency-strength comparison involving several non-equivalent notions.

The statement phase must select an immutable source and freeze one proposition. It must record the
object theory, universes, ordered binders, whether existence is assumed or concluded, the precise
large-cardinal definition, and all model/consistency assumptions.

## Explicit exclusions

- Treating the whole family of "large cardinal axioms" as one theorem.
- Substituting a convenient theorem about regular or strong-limit cardinals.
- Treating a definition, structure constructor, or field projection as an existence proof.
- Using `Cardinal.IsInaccessible.univ` as proof of an inaccessible cardinal inside ZFC; it concerns
  the cardinal of a higher Lean universe and carries a materially different foundation boundary.
- Substituting measurable, weakly compact, supercompact, Woodin, or another large-cardinal notion
  for an inaccessible-cardinal claim, or conversely.
- Crediting the repository label `已验证` as human-source or kernel evidence.

No canonical Lean target is frozen at intake because the source record does not state a theorem.
