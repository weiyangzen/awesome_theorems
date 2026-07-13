# Scope map

## Preserved subject boundary

This intake preserves exactly the catalog wording: a Zassenhaus-named result "about classification
of group extensions." It does not choose a familiar theorem from that subject. A classification
claim is not exact until the classified objects, equivalence relation, fixed data, invariant, and
classification conclusion are all specified.

The provisional vector is `[H5, M4, R4]`. `H5` here records that the received target is not yet a
stable proposition, not that a corrected extension theorem is false. Source identification and
target correction must select a proposition before ordinary theorem-proof execution can begin.

## Decisions required at statement freeze

1. Preserve and independently review an authoritative source edition, exact theorem/page,
   incorporated definitions, proof boundary, translation, corrections, and errata.
2. Resolve the bibliographic conflict between the catalog's Hans Zassenhaus/1937 metadata, the
   1937 discrete-groups paper, and the 1971 Johnson-Zassenhaus finite-extension paper.
3. Fix whether the objects are all groups, finite groups, abelian groups, or extensions with an
   abelian kernel; and fix every universe and finiteness encoding.
4. Fix the extension convention: short exact sequence, normal subgroup with quotient, factor set,
   crossed product, or another source-defined representation.
5. Fix the kernel `N`, quotient `G`, middle group `E`, embeddings and quotient maps, an outer or
   actual action of `G` on `N`, and whether any of these vary.
6. Fix extension equivalence, congruence, weak equivalence, isomorphism of middle groups, or another
   relation, including whether endpoint maps are identities or allowed automorphisms.
7. Fix the classifying data and theorem direction: factor systems/cocycles, an `H^2` class, an
   obstruction in `H^3`, an action plus cohomology data, existence, injectivity, surjectivity, or a
   bijection of explicitly defined quotient types.
8. Fix split versus nonsplit extensions, normalization choices, changes of section, ordered binders,
   hypotheses, conclusion, foundations, computation policy, and checked alternate encodings.

## Boundary cases

Source and statement review must dispose of trivial kernel or quotient, trivial action, split and
direct-product extensions, empty or singleton classification types, finite versus infinite groups,
abelian versus nonabelian kernels, central extensions, changes of section, equivalent cocycles,
automorphisms of endpoint groups, and universe/coercion choices. No case is excluded at intake.

## Explicit substitutions excluded

- The Zassenhaus/butterfly lemma about subnormal subgroup chains is not extension classification.
- The Schreier refinement theorem or Jordan-Hoelder theorem is not the received subject.
- The Schur-Zassenhaus theorem supplies complements to normal Hall subgroups; it is not a
  classification of group extensions.
- The Zassenhaus lemma from homological algebra and any Lie-algebra, Lie-group, or matrix
  decomposition carrying the same surname are separate results.
- The classification of central extensions alone, split extensions alone, or extensions with one
  fixed special kernel cannot replace a source whose intended scope is unknown.
- A definition of extension equivalence, construction of a semidirect-product extension, or proof
  that a split extension is a semidirect product is infrastructure, not a general classification.
- An assumed bijection, classification structure, cohomology equivalence, or unproved theorem
  parameter would encode the desired conclusion rather than prove it.
- The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_078.lean` owns `THM-M-0424`
  (Brauer groups), not this theorem; its slot number supplies no statement or proof credit.
- The catalog's `已验证` label, a name match, a bibliography record, or the intake probe is not
  human-source or machine-proof evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.GroupTheory.GroupExtension.Defs` provides `GroupExtension`,
`GroupExtension.Equiv`, sections, splittings, and semidirect-product examples.
`Mathlib.GroupTheory.GroupExtension.Basic` provides selected basic and split-extension results.
The `Defs` documentation explicitly lists the equivalence-class/`H^2` classification for abelian
kernels as future work, and the low-degree cohomology module repeats that boundary. The canonical
Lean module, declaration, expression, and fingerprint therefore remain null. Exhaustive anchor
discovery, proposition matching, provenance, trust, and proof credit all belong downstream.
