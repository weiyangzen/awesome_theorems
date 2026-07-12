# Scope map

## Source-preserving scope

| Surface | Source supplies | Intake result |
|---|---|---|
| Subject | homogeneous models | retained as the topic name only |
| Language/signature | nothing | unresolved |
| Structure/model | nothing | unresolved |
| Cardinal parameter | nothing | unresolved |
| Homogeneity convention | nothing | unresolved |
| Hypotheses | nothing | unresolved |
| Conclusion/property | "properties" | not proposition-level; unresolved |
| Boundary cases | nothing | cannot be frozen |

## Interpretations that must not be silently merged

1. A relational structure is **ultrahomogeneous** when every isomorphism
   between finite substructures extends to an automorphism. This may itself be
   a definition rather than the target theorem.
2. Model-theoretic **cardinal homogeneity** is formulated using partial
   elementary maps, elementary embeddings, or realization of types over small
   sets. Definitions vary in their size bounds and in whether extensions are
   one-point, full, or strongly homogeneous.
3. Existence and uniqueness results for homogeneous or homogeneous-universal
   models need substantial extra assumptions on a theory, class of models,
   cardinal, and sometimes cardinal arithmetic.
4. Saturation can imply forms of homogeneity, but saturation and homogeneity
   are not interchangeable names. Adopting that implication would select a new
   theorem absent from the source record.

None of these candidates is canonicalized here. In particular, the dossier
does not turn a definition into a theorem or use a trivial self-implication to
manufacture a Lean proposition.

## Resolution contract

Before the dependent statement phase, a source owner must provide:

- an immutable bibliographic source with theorem/definition number and page;
- the exact language, theory/model, cardinal parameters, and size relations;
- the precise notion of homogeneity and whether maps are partial elementary
  maps or finite-substructure isomorphisms;
- every hypothesis and the exact conclusion;
- intended treatment of finite, empty, and singular cardinal cases;
- whether the target is a definition, characterization, existence theorem,
  uniqueness theorem, or implication from another model property.

Only then can the Lean module, expression, transports, mutations, foundation
profile, and obligation registry be frozen.
