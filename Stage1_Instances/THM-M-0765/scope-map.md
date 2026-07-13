# Scope map

## Preserved source boundary

The repository fixes only the title `图灵机可识别语言`, the gloss `递归可枚举语言`, Alan Turing,
and 1936. This locates a standard computability/formal-language family. It does not determine
whether the target is a definition, an equality of language classes, one direction of a
characterization, or a package of properties.

A later source and statement freeze must retain the connection among:

- a source-selected alphabet and finite-word representation;
- a source-selected effective Turing-machine model and valid encoding;
- a language represented extensionally as a set or predicate on words;
- acceptance or recognition semantics, including required behavior outside the language; and
- a source-selected meaning of recursive enumerability and the exact claimed relationship.

This boundary is a topic-family map, not a canonical mathematical statement.

## Decisions required at statement freeze

1. Preserve and independently review one immutable primary or approved authoritative source
   passage, including incorporated definitions, assumptions, conclusion, proof boundary,
   translation, correction, and errata disposition.
2. Decide whether the root asserts an equivalence between Turing-recognizable and recursively
   enumerable languages, only one implication, a definition, or another explicitly sourced
   characterization.
3. Fix the alphabet, word encoding, empty-word convention, language representation, universes,
   ordered binders, and any finiteness, encodability, or nonemptiness hypotheses.
4. Fix the machine model: deterministic or nondeterministic, tape and alphabet conventions,
   initial configuration, accepting states, rejection, halting, and divergence.
5. Fix recursive enumerability as the domain of a partial computable function, the range of a
   total or partial enumeration, a semidecision procedure, or another accepted formulation.
6. For an enumerator reading, decide duplicates, output order, empty languages, finite languages,
   delimiter/decoding rules, and whether every emitted value must be a valid word.
7. Compile checked transports among every credited encoding rather than identifying them by name,
   and perform the required domain, hypothesis, binder-scope, and boundary mutations.

## Explicit exclusions

- Treating the predicate-level definition `REPred` as automatically identical to the catalog's
  language-level wording.
- Crediting only the simulation `Turing.PartrecToTM2.tr_eval` as the full language-class
  characterization; the reverse machine-to-partial-recursive direction and language transports
  would still require exact source and formal mapping.
- The halting language or another single recursively enumerable language in place of a theorem
  about the entire class.
- Closure properties, undecidability properties, or the separate catalog topic
  `递归可枚举语言性质` as a substitute for this target.
- Recursive/decidable languages, co-recursively-enumerable languages, context-sensitive languages,
  or unrestricted classical `Decidable` predicates.
- A recognizer or enumeration witness supplied as a hypothesis or structure field and then merely
  projected as the desired conclusion.
- The catalog label `已验证`, an API name, a bounded search, or a successful probe as source or
  machine-proof evidence.

No canonical human proposition, Lean expression, alternate transport, obligation registry,
discovery protocol, proof body, or completion claim is frozen at intake.
