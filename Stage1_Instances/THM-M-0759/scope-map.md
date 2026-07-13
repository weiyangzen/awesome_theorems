# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0759`, the label "automata theory," collective twentieth-
century attribution, and the gloss "the theory of finite automata." Importance "high" and status
`verified` are inventory metadata, not source or kernel evidence. Intake preserves only the broad
finite-automata subject boundary; it does not select word acceptors, another automaton family, or a
theorem within that subject.

## Proposition-changing decisions

An approved source correction must select one exact, truth-valued result and freeze:

- the automaton family: finite-word acceptor, transducer, tree automaton, infinite-word automaton,
  probabilistic or weighted finite-state model, or another explicitly sourced family;
- for a word acceptor, whether it is deterministic, nondeterministic, or epsilon-nondeterministic,
  plus the alphabet, state type, words, transition relation or function, start state or set,
  accepting states, accepted language, and equality or language-equivalence convention;
- which carriers the word `finite` qualifies, including whether the alphabet, state space,
  transition data, tree, or another object must be finite, plus decidable-equality or effectiveness
  assumptions;
- whether transitions are total or partial and how epsilon transitions, unreachable states, and
  completion by a sink state are treated;
- the exact result: semantic correctness, a model equivalence, a regular-language
  characterization, a closure theorem, pumping, minimization, or a decision procedure;
- every construction, complexity or computability claim, including its resource model when one is
  part of the conclusion; and
- all universes, ordered binders, dependent hypotheses, conclusion clauses, and alternate
  encodings with their checked relationship.

These choices define inequivalent propositions. They are an open resolution ledger, not a
canonical statement.

## Boundary cases

Source review must explicitly resolve empty and singleton alphabets; empty words and languages;
empty accepting sets; whether a state type can be empty despite a required start state; empty or
unreachable start sets for nondeterministic machines; automata with no reachable accepting state;
zero, one, or infinitely many states; epsilon cycles; incomplete transition tables; duplicate or
unreachable states; and equality of machines versus equality of accepted languages.

## Neighboring target boundaries

`THM-M-0760` separately names the Myhill-Nerode theorem, `THM-M-0761` the pumping lemma,
`THM-M-0762` context-free-language properties, `THM-M-0763` the Chomsky hierarchy,
`THM-M-0764` pushdown automata, `THM-M-0765` Turing-machine-recognizable languages, and
`THM-M-0766` linear-bounded automata. This target may eventually depend on a checked neighboring
result, but it cannot absorb its root or inherit its source or proof credit.

## Prohibited substitutions

- silently choosing DFA/NFA equivalence, pumping, Myhill-Nerode, Kleene equivalence,
  regular-language closure, minimization, or decidability as the target;
- selecting word acceptors, transducers, tree, Buchi, Rabin, probabilistic, weighted, alternating,
  or timed finite-state models without source approval;
- replacing the finite-automata topic with unbounded-memory pushdown, Turing, or linear-bounded
  machines;
- calling a `DFA`, `NFA`, or `epsilon-NFA` value finite without an explicit finite state-space
  condition;
- projecting a desired theorem from a structure or hypothesis that already assumes it;
- treating an API check, survey row, bibliography entry, theorem name, or the catalog's untrusted
  `verified` label as source or proof evidence; and
- claiming that no relevant formalization exists globally from a bounded local search.

## Formal boundary

Pinned mathlib provides word languages, DFA/NFA/epsilon-NFA structures, regular-language
predicates and closure results, subset constructions, pumping, a Myhill-Nerode characterization,
and regular-expression semantics. Its automaton structures allow infinite state types; a
`Fintype` instance is needed for a genuine finite automaton. The regular-expression module also
states that equivalence with DFA/NFA is not yet shown there. These facts make the adjacent API
surface real but prevent it from selecting or closing the catalog's absent root.

A bounded search found no target-specific automata artifact in repo-local Lean. This is intake
discovery only, not the downstream immutable anchor audit or a global absence claim.
