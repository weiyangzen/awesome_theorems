# Scope map

## Preserved source scope

The repository fixes only the topic label `上下文无关语言的性质`, the gloss `CFL的闭包性质`, a
collective attribution, and a twentieth-century date. This identifies the standard family of
closure and non-closure results for context-free languages. It does not identify a theorem-sized
member of that family or say whether the intended output is one closure result, a finite bundle,
or a complete classification table.

This intake preserves the family boundary without asserting any member. A later statement run must
admit an immutable source and freeze exactly which operations and directions are claimed.

## Proposition-changing decisions

An approved statement must fix all of the following:

- the alphabet carrier, universe and any finiteness, decidability, or nonemptiness assumptions;
- words as finite lists or another encoding, and languages as sets or recognized/generated objects;
- the definition of context-free language, including grammar finiteness and epsilon-production
  conventions, or a checked equivalence to a pushdown-automaton encoding;
- the exact operation list: finite or indexed union, concatenation, Kleene star or plus, reversal,
  substitution, homomorphic image, inverse image, quotient, or intersection with a specified class;
- for homomorphisms, whether erasing maps are allowed and how alphabet changes are represented;
- for intersection, whether the second language is regular rather than context-free;
- whether the conclusion is one proposition, an ordered conjunction, a classification record, or
  separate theorem branches, with every ordered binder and witness explicit; and
- empty alphabet, empty language, the language containing only the empty word, zero-fold star,
  empty operation families, and all other boundary cases.

These choices alter statement strength, proof architecture, foundation requirements, and sometimes
truth value. They are a resolution checklist, not a canonical statement.

## Candidate branches not credited

- Closure under finite union.
- Closure under language concatenation.
- Closure under Kleene star.
- Closure under word reversal.
- Closure under homomorphic image or inverse homomorphism.
- Closure under intersection with a regular language.
- Non-closure under arbitrary intersection or complement.

Pinned mathlib's reversal theorem is a formal candidate for one branch only. No branch, conjunction,
or classification is selected or credited at intake.

## Explicit exclusions

- Treating all operations on `Language` as preserving context-freeness merely because the type has
  Boolean, semiring, or Kleene-algebra operations.
- Claiming closure under arbitrary intersection or complement; those substitutions would make the
  ordinary CFL family statement false.
- Replacing intersection with a regular language by intersection of two context-free languages.
- Using the neighboring pumping-lemma, Chomsky-hierarchy, or pushdown-automaton targets as this
  target's root, even though a future proof may depend on them.
- Assuming closure as a field of a custom structure or as a hypothesis and projecting it.
- Treating `Language.IsContextFree.reverse` or any other convenient pinned theorem as the catalog
  statement without a checked source crosswalk.
- Crediting the repository label `已验证` as human-proof or Lean-kernel evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Computability.Language` supplies languages,
union, concatenation, Kleene star, maps and reversal; `Mathlib.Computability.ContextFreeGrammar`
supplies grammars, generated languages, `Language.IsContextFree`, and reversal closure. The intake
probe checks this substrate and direct reversal interface only. It is not the downstream exhaustive
anchor audit, does not establish the catalog's intended operation list, and supplies no root proof
credit.
