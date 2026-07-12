# Scope map

## Included topic boundary

- A source-specified, effectively presented formal theory and proof relation.
- A precise interpretation or representation of a sufficient fragment of arithmetic.
- The source's exact consistency or soundness hypothesis.
- A syntactic incompleteness conclusion for a sentence in the theory's language.
- The metatheoretic coding, diagonalization, representability, and derivability machinery required
  by the selected formulation.

## Decisions required at statement freeze

1. Choose the source theorem: Godel's original 1931 formulation, a Rosser strengthening, or another
   precisely cited standard formulation. These are related theorems, not interchangeable wordings.
2. Fix the theory class: recursively axiomatized/recursively enumerable or decidable axioms, the
   language, deductive calculus, and how the theory extends or interprets arithmetic.
3. Fix the strength threshold, such as a specified arithmetic base theory, rather than the phrase
   "contains arithmetic".
4. Fix ordinary consistency, omega-consistency, 1-consistency, or soundness exactly as required by
   the chosen source and direction of the conclusion.
5. Define `Provable T phi`, sentence negation, completeness, and the precise existential conclusion.
6. State whether the undecidable sentence is the constructed fixed point and what extra assumptions
   are used for each of its two unprovability directions.

## Explicit exclusions

- Godel's second incompleteness theorem (the neighboring `THM-M-0778`).
- Semantic incompleteness of a logic or failure of categoricity as substitutes for syntactic
  incompleteness of an effective arithmetic theory.
- Tarski's undefinability theorem, Church's theorem, or undecidability of the halting problem as the
  target, though they may later be related dependencies or consequences.
- An inconsistent theory, an arbitrary non-effective set of axioms, or a theory too weak to encode
  the required syntax and diagonal argument.
- Treating a generic assumed `Provable` predicate plus an assumed undecidable sentence as a proof.
- Treating the beta-function lemma, a theorem name, or the repository's `已验证` label as closure.

No canonical Lean target is frozen at intake. Selecting convenient definitions before the exact
source variant is fixed could strengthen the hypotheses or weaken the conclusion.
