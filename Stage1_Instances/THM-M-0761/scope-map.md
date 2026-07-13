# Scope map

## Preserved collective theorem family

The repository claim contains two materially different pumping lemmas. A later source and statement
freeze must retain both components rather than selecting the easier branch.

### Regular-language component

- A source-selected alphabet and language of finite words.
- A regularity witness, either a finite-state recognizer or a checked transport from another
  definition of regular language.
- A pumping bound determined uniformly by the language or recognizer, before the pumped word is
  chosen.
- Every accepted word meeting the length threshold decomposes in source-specified order into three
  factors.
- The pumped factor is nonempty, its position is bounded near the start of the word, and replacing
  it by every permitted natural power preserves language membership.

### Context-free-language component

- A source-selected alphabet and context-free language, with a grammar, pushdown automaton, or
  checked equivalent witness.
- A uniform pumping bound chosen before the word.
- Every word in the language meeting the threshold decomposes into five source-ordered factors.
- Two factors are pumped simultaneously with one shared exponent; the selected middle region has
  the source-stated length bound, and the two pumped factors satisfy the exact joint nonemptiness
  condition.
- Every permitted exponent preserves membership in the original language.

This is a family boundary, not yet a canonical proposition, shared-binder decision, formal
expression, alternate encoding, or proof architecture.

## Decisions required at statement freeze

1. Acquire and independently review immutable primary or authoritative passages for both branches,
   recording edition, exact theorem/section/page, incorporated definitions, assumptions,
   conclusions, proof boundaries, corrections, errata, translations, and component mapping.
2. Decide whether the canonical root is an explicit conjunction, a two-field proposition, or an
   indexed family, while ensuring that closing one component cannot close the other.
3. Fix each branch's alphabet, language representation, universes, finiteness and decidable-
   equality assumptions, and whether the two branches use independent alphabets and languages.
4. Freeze pumping-length existence, positivity, and dependency order: the bound must not depend on
   the later chosen word or decomposition.
5. Freeze regular factors, concatenation association, nonempty factor, prefix bound, accepted word
   threshold, and the exponent domain including or excluding zero.
6. Freeze context-free factors, simultaneous-power notation, bounded-region formula, joint
   nonemptiness condition, threshold, and exponent domain.
7. Check transports among language-level, DFA-level, grammar-level, singleton/Kleene-star, and
   pointwise list-power encodings in precisely the required directions.
8. Resolve all empty, singleton, epsilon, boundary-length, zero-state, unproductive-grammar, and
   zero-exponent cases before elaborating and fingerprinting the canonical expression.
9. Perform the rev-5.6 removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
   mutations separately for each component and for their collective composition.

## Explicit exclusions

- Only `DFA.pumping_lemma`, only a regular-language corollary, or only a context-free pumping result.
- A necessary pumping condition presented as a characterization: the converse is false in both
  standard settings without additional restrictions.
- Ogden's lemma used as the root merely because it implies the CFL pumping lemma; a checked,
  source-approved implication would be an alternate route, not statement identity.
- Pumping lemmas for deterministic CFLs, indexed languages, context-sensitive languages, omega
  languages, tree languages, or other hierarchies.
- A loop decomposition without the universal membership-preservation conclusion, or a single
  successful pumping exponent instead of all required exponents.
- Sharing one alphabet, language, pumping length, or decomposition witness across the two branches
  unless an accepted source explicitly requires that stronger collective claim.
- Assuming the desired decomposition or pumping property through a typeclass, structure field,
  hypothesis, axiom, oracle, or unchecked computation.
- Transferring state or proof credit from separate catalog records `THM-C-0133` and `THM-C-0144`.
- Treating `已验证`, a theorem name, import success, or an API probe as source or proof evidence.

No canonical Lean target, statement fingerprint, checked alternate transport, obligation registry,
discovery protocol, accepted execution state, or completion claim is frozen at intake.
