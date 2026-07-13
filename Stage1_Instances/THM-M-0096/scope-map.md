# Scope map

## Preserved theorem family

The intake preserves the classical Chevalley-basis family: for a finite-dimensional semisimple Lie
algebra in a suitable characteristic-zero setting, one chooses compatible Cartan and root data and
normalizes a basis so that its Lie-bracket structure constants are integers. Equivalently in common
formulations, the integer span is a Lie ring whose scalar extension recovers the original Lie
algebra. This paragraph is a conventional scope description, not the frozen canonical proposition.

The catalog's phrase `半单李代数的整基` could denote the basis-with-integral-structure-constants
form, existence of a `Z`-form, or a more specific normalized Chevalley basis. These encodings may be
related, but rev-5.6 requires checked transports before proof credit can cross between them.

## Decisions required at statement freeze

1. Preserve and review an exact source edition, theorem, definitions, proof boundary, corrections,
   and historical attribution rather than treating the catalog gloss as a quotation.
2. Fix the scalar field: `Complex`, an algebraically closed characteristic-zero field, or another
   source-selected domain, with all finite-dimensionality and splitting assumptions.
3. Fix the Lie algebra hypothesis: semisimple versus simple or reductive, and the precise radical,
   Killing-form, decomposition, or other checked encoding of semisimplicity.
4. Define "integral basis": a field basis with integer bracket coefficients, a distinguished
   Chevalley basis with root-vector normalizations, a bracket-closed free `Z`-lattice, a `Z`-form
   whose scalar extension is the original algebra, or an explicitly sourced conjunction.
5. Fix the Cartan subalgebra, root system, simple roots, coroots, positive roots, index types, and
   sign or ordering choices, including how changes of choices transport the result.
6. State the exact relations required among the Cartan elements and root vectors, including the
   `alpha + beta` and opposite-root cases and the scope of all integrality assertions.
7. Decide whether the conclusion asserts existence only, a classification, uniqueness up to signs
   or automorphism, compatibility with a chosen root datum, or functorial base change.
8. Freeze ordered binders, universes, typeclasses, foundation and TCB profiles, every boundary case,
   and checked transports for alternate encodings.

## Degenerate and boundary cases

Source review must address the zero Lie algebra; the empty root system; rank zero and rank one;
simple versus nonsimple semisimple direct sums; repeated isomorphic simple factors; zero and
nonzero root spaces; nonreduced or noncrystallographic input data; reducible root systems; fields
that are not algebraically closed or have positive characteristic; reductive algebras with center;
and whether base change preserves and reflects the selected integral form.

No case is excluded at intake. In particular, an arbitrary module basis is not "integral" merely
because its index type is finite, and an integral Cartan matrix alone does not make every bracket
coefficient integral.

## Excluded substitutions

- Root-space decomposition or existence of a Cartan subalgebra supplies ingredients only.
- A crystallographic root system, integral Cartan matrix, or Cartan classification does not itself
  construct a basis of the received semisimple Lie algebra.
- A partial Chevalley-Serre generating structure that leaves root-vector bracket constants
  unconstrained is weaker than a Chevalley basis.
- Constructing a Lie algebra from a Cartan matrix or root system is not automatically an existence
  theorem for an arbitrary supplied semisimple Lie algebra; an exact classification/equivalence
  bridge would be required.
- A basis over `Complex` without integer bracket structure, or a `Z`-spanning family without
  freeness, bracket closure, and scalar-extension recovery, is not a substitute.
- Jordan-Chevalley decomposition, Jordan bases, Chevalley-Warning, Chevalley restriction, Chevalley
  groups, and classification of simple Lie algebras are distinct theorem families.
- A structure or hypothesis storing the desired integral basis supplies no proof of existence.
- The catalog's `verified` label, a theorem name, module TODO, citation, or successful `#check`
  supplies no H or M closure.

## Neighbor boundaries

`THM-M-0095` owns the catalog's Cartan root-space decomposition theorem; it is upstream structure,
not the integral-basis result. `THM-M-0092` owns the Cartan-Weyl theorem family, `THM-M-0093` the
highest-weight classification theorem, and `THM-M-0097` the Harish-Chandra character theorem. No
status, definitions, or proof credit transfer by proximity.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`LieAlgebra.Basis` stores an integer matrix, Cartan generators, positive and negative generators,
spanning and independence fields, `sl2` triples, and several Chevalley-Serre relations. The module
explicitly says the unconstrained brackets among like-signed root generators need further axioms
for a Weyl/Chevalley basis and lists `Define Weyl, Chevalley bases` and existence for every
semisimple Lie algebra as TODOs.

`RootPairing.GeckConstruction.basis` constructs the weaker `LieAlgebra.Basis` for a particular Lie
algebra built from reduced irreducible crystallographic root data. `Matrix.ToLieAlgebra` constructs
a quotient of a free Lie algebra from a Cartan matrix. These are genuine adjacent artifacts, but
neither supplies a Chevalley-basis predicate or an exact theorem about every semisimple Lie algebra.
This bounded intake inspection is not the downstream immutable anchor audit and not a global
absence theorem.
