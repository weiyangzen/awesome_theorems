# Scope map

## Included subject

- A homology theory whose objects are topological pairs and whose values are graded abelian groups
  or modules, with covariant maps induced by maps of pairs.
- Natural connecting homomorphisms for pairs.
- The classical homotopy, exactness, excision, and dimension axioms.
- Additivity or a disjoint-union axiom only after its status in the selected source/profile is
  fixed explicitly.
- The distinction between a data-and-laws structure and a theorem proving that a concrete homology
  construction instantiates that structure.

This freezes the mathematical topic meant by the Chinese phrase "同调理论的公理系统" (an axiom
system for homology theory), but it deliberately does not invent a theorem absent from that phrase.

## Statement-phase fork

The exact source inspection must select exactly one root:

1. a Lean structure or predicate defining an Eilenberg-Steenrod homology theory;
2. a theorem that a named concrete theory, most naturally singular homology with fixed
   coefficients, satisfies every field of that structure;
3. a source-backed characterization or uniqueness theorem, with its actual hypotheses and
   conclusion.

Option 1 is principally a definition/package and must not be presented as a proved mathematical
theorem. Option 2 carries substantive construction and proof obligations. Option 3 is stronger and
cannot be inferred merely from the name of the axioms.

Whichever root is chosen must also freeze: reduced versus unreduced homology; coefficient ring or
group; grading by natural numbers or integers; the precise category of spaces/pairs and maps;
universe levels; the exact sequence and degree shift; excision hypotheses; the dimension value on
a point; additivity/wedge conventions; naturality strength; and empty-space, degree-zero, and
negative-degree behavior.

## Explicit exclusions

- Assuming an `EilenbergSteenrod` structure and then claiming its fields prove that a concrete
  homology theory satisfies the axioms.
- Proving just one axiom, or a list of unrelated facts, as the complete target.
- Substituting the uniqueness theorem for ordinary homology without a source statement that asks
  for it.
- Replacing homology with cohomology, generalized homology, or a spectrum-valued theory.
- Treating the repository's untrusted `已验证` label as a citation or kernel result.
- Reusing the adjacent `THM-M-0537` "homology axioms" record as proof credit; the records are
  semantically overlapping but independently scheduled.

No obligation denominator or proof architecture is frozen during intake. Those belong after the
exact statement and formal-candidate audit.
