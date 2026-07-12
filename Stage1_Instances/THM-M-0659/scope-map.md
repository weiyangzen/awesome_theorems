# Scope map

## Preserved repository scope

- The assigned identity is `THM-M-0659`, named `谢拉赫分类定理` (Shelah classification
  theorem), attributed without citation to Saharon Shelah and dated 1990.
- The entire supplied mathematical gloss is `超稳定理论的分类` (classification of superstable
  theories).
- First-order theories and models, superstability, types, elementary maps, decompositions, and
  cardinal spectra are legitimate discovery surfaces because they are native to the named field.

This is a family-level boundary, not an exact theorem. The phrase does not specify whether the
intended result is a structure/decomposition theorem, a main-gap or spectrum theorem, a dividing
line inside superstable theories, or a result specific to extra hypotheses.

## Decisions required at the statement gate

An immutable primary or critical source must fix:

- the exact theorem identifier, edition, page, and incorporated definitions;
- whether the theory is complete, the language size, and all model cardinalities;
- the definition of superstable used by the source;
- every extra dividing-line hypothesis, including any DOP/NDOP, OTOP/NOTOP, depth, or shallowness
  condition if present;
- the objects being classified, the equivalence or isomorphism notion, the invariants or
  decomposition data, and the exact conclusion;
- all ambient cardinal-arithmetic or set-theoretic assumptions and all excluded boundary cases.

Only after those choices are reviewed may a Lean target choose universes, binders, language and
theory structures, model cardinalities, or encodings of stability and classification. Any
soundness, completeness, saturation, prime-model, independence, decomposition, or cardinal bridge
used by the result must later be visible as an obligation rather than hidden in prose.

## Explicit exclusions

- Morley's categoricity theorem or any transfer-of-categoricity statement.
- The definition or general development of stability/superstability without the claimed
  classification conclusion.
- The broad programme called classification theory, presented as though it were one proposition.
- A main-gap dichotomy, decomposition theorem, or spectrum-counting result selected merely because
  it is familiar or easier to formalize.
- A theorem with extra NDOP, NOTOP, shallow, countability, or cardinal hypotheses unless the
  accepted source contains them.
- Treating the year 1990, the author label, or `已验证` as a primary-source locator or proof evidence.
