# THM-M-0764 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `下推自动机`
(pushdown automata). The repository supplies only the gloss `上下文无关语言的识别`
("recognition of context-free languages"), a collective attribution, and the period "20th
century." Those fields identify the familiar pushdown-automaton/context-free-language theorem
family, but not a binder-complete proposition.

Materially different claims fit the gloss: every context-free language is recognized by a
nondeterministic pushdown automaton, every language recognized by such an automaton is
context-free, the biconditional, or word-level correctness of one grammar-to-automaton
construction. The catalog also leaves the automaton model, epsilon moves, stack-bottom convention,
and acceptance by final state versus empty stack unresolved. The separate outside-Stage1 record
`THM-C-0141` explicitly names CFG/PDA equivalence, but cannot silently supply this target's
statement or proof credit.

Pinned mathlib defines formal languages, finite-rule context-free grammars, derivation, generated
languages, and `Language.IsContextFree`. It also contains a deterministic multi-stack Turing model.
`IntakeProbe.lean` authenticates those interfaces. Pinned mathlib has no explicitly named pushdown
automaton or CFG/PDA-equivalence declaration in the bounded search performed here; the general
multi-stack model is not a standard nondeterministic one-stack PDA substitute.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
root vector is `[H1, M3, R4]`: a standard published theorem family and bibliographic leads are
known, but no exact source proposition is accepted; pinned interfaces cover only adjacent
definition/statement substrate, not the root; and no reviewed source-faithful proof reconstruction
can attach to an unfrozen target. All six downstream tasks remain open. No H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
