# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0763`, the title `乔姆斯基层次`, the attribution Noam Chomsky,
the year 1956, and the gloss `形式语言的分类`. Importance `高` and status `已验证` are inventory
metadata, not human-source or kernel evidence. Intake preserves only the formal-language
classification family identified by that wording.

The related Stage0-only computer-science record `THM-C-0151` says `形式语言的四层层级`, but it is
outside the 1546-target rev-5.6 manifest. It is a provenance and ambiguity boundary, not an accepted
duplicate, canonical statement, or evidence source.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from a pinpoint immutable source:

1. Whether the root asserts definitions of grammar types, weak inclusions, strict inclusions with
   witnesses, a completeness/classification statement, grammar-machine equivalences, or a precise
   conjunction of separately owned claims.
2. The alphabet, its finiteness and nonemptiness, words and the empty word, languages, terminal and
   nonterminal symbols, start symbols, productions, generated-language semantics, and universes.
3. Exact type-3 conventions: right- or left-linear grammars, mixed linearity, epsilon productions,
   the start-symbol exception, and the selected definition of regular language.
4. Exact type-2 conventions: context-free productions, finiteness of rules and used nonterminals,
   epsilon rules, useless symbols, derivation direction, and grammar equivalence.
5. Exact type-1 conventions: context-sensitive versus noncontracting rules, context form, monotone
   length, the start-symbol/epsilon exception, and the corresponding language class.
6. Exact type-0 conventions: unrestricted or phrase-structure grammars, effectiveness and finite
   presentation, derivations, and whether the conclusion identifies their languages with
   recursively enumerable or Turing-recognizable languages.
7. The machine models and encodings, if any: DFA/NFA, PDA, linear-bounded automata, Turing machines,
   acceptance convention, tape and input representation, and checked grammar-machine transports.
8. Inclusion directions and strictness strength, the exact witness language for every strict edge,
   ordered binders, hypotheses, coercions, conclusion, foundation/TCB policy, and all degenerate
   cases.

These choices produce materially different propositions. This ledger does not choose among them.

## Candidate readings not credited

- Definitions of the four conventional grammar types and the language classes they generate.
- The weak chain regular languages contained in context-free languages, contained in
  context-sensitive languages, contained in recursively enumerable languages.
- Strictness of all three inclusions, including explicit separating languages and all alphabet
  assumptions needed by those witnesses.
- Equivalences between the four grammar classes and finite automata, pushdown automata,
  linear-bounded automata, and Turing machines.
- Chomsky's 1956 Theorem (27), a different three-class comparison involving finite-state,
  derivable, and terminal languages.

No candidate is canonical, asserted, or credited at intake.

## Degenerate and representation cases

The eventual source must decide empty and singleton alphabets; empty languages; languages
containing only the empty word; empty production sets; absent, unreachable, or nullable start
symbols; epsilon productions; grammars with no terminal derivations; zero-symbol right-hand sides;
mixed left/right-linear rules; whether nonterminals form a finite type or only a finite used subset;
duplicate rules; reflexive versus positive derivation closure; and machine encodings of empty input,
nontermination, and rejection. No case is excluded here.

## Neighbor and substitution boundaries

- `THM-M-0759` automata theory is a broader topic and cannot replace the hierarchy root.
- `THM-M-0760` Myhill-Nerode is a regular-language characterization, while `THM-M-0761` owns
  regular- and context-free-language pumping results; neither is the whole classification.
  `THM-M-0762` separately owns properties of context-free languages.
- `THM-M-0764` pushdown automata, `THM-M-0765` Turing-recognizable languages, and `THM-M-0766`
  linear-bounded automata own machine/class-specific targets. Their definitions or recognition
  theorems cannot silently stand for the hierarchy.
- The Stage0-only `THM-C-0151` record cannot select, broaden, or close this rev-5.6 target.
- A definition packaged as a structure or predicate, an assumed inclusion, a single closure
  theorem, or the catalog label `已验证` is not a proof of an unidentified classification theorem.

## Formal boundary

Pinned mathlib supplies `Language`, `Language.IsRegular`, `ContextFreeGrammar`, its generated
language, `Language.IsContextFree`, and generic computability predicates. It does not expose a
complete source-selected type-0/type-1/type-2/type-3 hierarchy in the bounded intake search.
`ContextFreeGrammar` also uses a finite set of rules with a nonterminal type not itself required to
be finite, a representation choice that any source transport must address.

These APIs elaborate and make some candidate encodings plausible, but they do not select the root.
Statement identity, minimal imports, checked transports, mutations, formal candidate provenance,
the obligation registry, and all proof architecture belong to later phases.
