# Scope map

## Included topic boundary

- A source-selected formulation of Goedel's first incompleteness theorem or Rosser's strengthening.
- A precisely represented formal theory and derivability relation.
- Exact arithmetic-strength, effective-axiomatizability, and consistency assumptions.
- The coding, diagonalization, representability, and metatheoretic conditions used by that source.
- A conclusion identifying a sentence and the exact senses in which it and/or its negation are not
  derivable.

## Decisions required at statement freeze

1. **Theorem version:** Goedel 1931 with omega-consistency, a modern semantic/syntactic variant,
   or Rosser's consistency-only strengthening.
2. **Theory domain:** recursively enumerable or computably axiomatized extensions of a named base
   such as Robinson arithmetic, rather than unrestricted "systems containing arithmetic".
3. **Arithmetic inclusion:** literal extension in one language, definitional extension, or an
   interpretation capable of representing the needed recursive functions.
4. **Consistency condition:** ordinary consistency, omega-consistency, 1-consistency, or soundness.
5. **Conclusion:** syntactic incompleteness, an explicit undecidable sentence, or semantic
   incompleteness, with every negation and derivability predicate scoped explicitly.
6. **Metatheory:** which coding and computability results are internalized in Lean and which source
   theorem is being reconstructed.

## Counterexample and exclusion boundary

The unrestricted gloss cannot be frozen as the canonical claim. A complete consistent extension
of arithmetic exists semantically as the set of all first-order arithmetic sentences true in the
standard natural numbers; its failure of effective axiomatizability is precisely why an
effectivity assumption matters.

Explicitly excluded as substitutions are:

- Goedel's second incompleteness theorem about proving consistency.
- The semantic incompleteness of second-order logic or incompleteness of a particular decision
  procedure.
- Only Goedel's beta-function lemma, diagonal lemma, or an encoding theorem presented as if it were
  the root incompleteness theorem.
- A theorem made tautological by defining "incomplete" as an assumed field.
- Any formulation that silently replaces consistency with soundness or omega-consistency.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake. The next phase must first select an immutable exact
source proposition that resolves all six decisions.
