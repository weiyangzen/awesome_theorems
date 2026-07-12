# Scope map

## Included topic boundary

- Cohen's forcing construction as used for the continuum-hypothesis result.
- An exact, source-selected relative-consistency, model-existence, or non-provability theorem.
- The selected formal encoding of ZF/ZFC, CH, consistency, and semantic or syntactic consequence.
- Ground-model hypotheses, the forcing poset, names and valuation, genericity, the extension, and
  all preservation and truth results needed by that theorem.

## Ambiguities to resolve at statement freeze

The repository phrase does not distinguish these materially different targets:

1. If ZFC is consistent, then ZFC plus `not CH` is consistent.
2. ZFC proves neither CH nor `not CH`, normally combining Cohen's direction with a separate
   constructibility result and requiring consistency qualifications.
3. From a specified suitable model, construct a generic extension satisfying `not CH` while
   preserving the required axioms and ordinals/cardinals.
4. A forcing theorem or truth lemma that is an ingredient of the construction rather than the CH
   independence conclusion.

The statement phase must select an immutable source passage and freeze one proposition. It must
also decide whether consistency is syntactic or model-theoretic, whether a countable transitive
ground model is assumed externally, which fragment of set theory is encoded, and how CH and
cardinal preservation are represented.

## Explicit exclusions

- Treating the method name as a theorem without a quantified conclusion.
- Substituting the adjacent `THM-M-0781` claim about independence of CH and AC from ZF.
- Crediting Goedel's constructible-universe direction as Cohen's forcing direction.
- Assuming a forcing extension already satisfies `not CH` and projecting that field.
- Proving a generic order-theory fact about dense sets or filters with no source crosswalk.
- Treating first-order syntax APIs or bibliography in mathlib as a formalization of forcing.
- Using the repository label `已验证` as human-source or kernel evidence.

No canonical Lean target is frozen at intake because the source record identifies a historical
method and purpose, not an exact theorem.
