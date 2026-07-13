# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `下推自动机`, attributes it to "many
mathematicians", dates it only to the twentieth century, and gives the gloss
`上下文无关语言的识别` ("recognition of context-free languages"). Stage0 repeats that wording and
leaves exact definitions, assumptions, proof path, axioms, and formal artifacts open. The rev-5.6
manifest preserves `已验证` only as explicitly untrusted source metadata.

This record neither asserts a direction nor defines a pushdown automaton. It is secondary inventory
metadata, not a theorem/page-level source.

## Neighbor record and source leads

The separate computer-science catalog record `THM-C-0141` says "context-free grammars and pushdown
automata are equivalent," attributes the result to Chomsky and Schuetzenberger, and gives 1962. It
is outside the closed 1546-target Stage1 set. It supports the interpretation of the topic family,
but provides no citation, definitions, exact proposition, accepted alias, or transferable evidence.

Crossref and DBLP metadata identify M. P. Schuetzenberger, *On Context-Free Languages and Push-Down
Automata*, *Information and Control* 6(3), September 1963, pages 246-264, DOI
`10.1016/S0019-9958(63)90306-1`. Crossref's reference metadata also names Chomsky's 1962
"Context-free grammars and push-down storage." These are bibliographic leads only. No article text,
theorem locator, incorporated definitions, complete premise/conclusion map, proof boundary,
correction or errata audit, or independent review was admitted. In particular, a historically
related paper title is not by itself evidence for the modern blanket biconditional.

The generic bibliography in `Docs/researches/cs_theorems.md` names Sipser (2012) and
Hopcroft-Motwani-Ullman (2006), but supplies no edition-specific theorem, chapter, or page mapping.
It is E5 discovery material, not H0 evidence.

## Phrase crosswalk

| Repository phrase | Material mathematical choice | Required Lean component | Intake status |
|---|---|---|---|
| "language" | sets of finite terminal words and extensional equality | `Language T` and word encoding | pinned interface available; exact source domain open |
| "context-free" | existence of a finite-rule CFG generating exactly the language | `ContextFreeGrammar`, derivation, `.language`, `Language.IsContextFree` | pinned CFG-side interface elaborated |
| "pushdown automaton" | finite control plus one stack and an input-consuming nondeterministic transition relation | source-specific PDA structure and configuration semantics | absent from the catalog and not identified by bounded pinned search |
| "recognition" | one accepted direction, acceptance predicate, and end-of-input convention | runs/reachability and final-state or empty-stack acceptance | direction and semantics absent |
| possible equivalence | both class inclusions or a checked `Iff` | CFG-to-PDA and PDA-to-CFG constructions plus root composition | neighboring record only; not accepted here |
| `已验证` | untrusted inventory label | no proposition or proof credit | explicitly rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.ContextFreeGrammar` defines finite-rule context-free grammars, one-step and
reflexive-transitive derivation, generated languages, and `Language.IsContextFree`. Its advertised
main theorem is closure under reversal, not CFG/PDA equivalence.

`Mathlib.Computability.TuringMachine.StackTuringMachine` defines deterministic machines with an
arbitrary collection of stacks and internal memory. Although it supplies push/pop/peek operations,
its own documentation says the models are deterministic by construction. It is not automatically
the source's nondeterministic one-stack PDA model and receives no target or proof credit.

The bounded case-insensitive exact-topic search of repo-local and pinned mathlib Lean sources found
no explicitly named `PushdownAutomaton`, `PDA`, or CFG/PDA-equivalence declaration. This is an
intake observation, not a global absence claim or the later immutable anchor audit.

## Source-fidelity gate

Before `H0`, an approved exact source proposition must be preserved and pinpointed; every definition,
premise, direction, transition and acceptance convention, conclusion, dependency, correction, and
erratum must be crosswalked and independently reviewed. Before statement credit, that proposition
must map to one elaborated Lean expression and checked transports without importing the neighboring
catalog statement or completing missing clauses from memory.
