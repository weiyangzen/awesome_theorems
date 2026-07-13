# Scope map

## Preserved theorem family

The intake preserves the classical family in which finite-dimensional irreducible modules of a
finite-dimensional complex semisimple Lie algebra are classified, after choosing Cartan and
positive-root data, by dominant integral highest weights. This is a scope description, not the
frozen canonical proposition.

Etingof's inspected formulation combines three logically distinct surfaces: every
finite-dimensional irreducible module is highest-weight; an irreducible highest-weight module is
uniquely determined by its highest weight; and precisely the dominant integral weights produce
finite-dimensional simple modules. A future statement may combine them only if an approved source
and exact root contract do so. Otherwise they require separately checked composition or transport.

## Decisions required at statement freeze

1. Select and preserve the exact source edition, theorem and proof boundary; map every definition,
   assumption and conclusion; audit corrections and historical attribution; obtain independent
   review.
2. Fix the scalar field: `Complex`, an algebraically closed characteristic-zero field, or another
   source-selected domain, including all finite-dimensionality and splitting hypotheses.
3. Fix the Lie algebra assumptions: semisimple versus simple or reductive, finite-dimensionality,
   nonzero convention, and whether semisimplicity uses radical, Killing-form, or another checked
   equivalent encoding.
4. Fix a Cartan subalgebra and a choice of positive/simple roots or Borel subalgebra, and specify how
   changing that choice transports the parameterization.
5. Define the weight lattice, positive root lattice, fundamental weights, coroot pairing, and
   dominant-integral predicate in the selected conventions.
6. Fix the representation model: Lie module, Lie algebra homomorphism into endomorphisms, or a
   universal-enveloping-algebra module; define finite dimensionality, nonzero and irreducibility.
7. Define highest-weight vector and highest-weight module, including nonzero and generation
   conditions and the positive-root annihilation convention.
8. Fix the conclusion: existence of a highest weight, uniqueness of that weight, uniqueness of a
   simple module up to isomorphism, construction from a Verma module, a bijection of isomorphism
   classes, or an explicitly sourced conjunction.
9. Freeze ordered binders, universes, typeclasses, foundation/TCB profiles, all boundary cases, and
   kernel-checked transports for every credited alternate encoding.

## Degenerate and boundary cases

Source review must explicitly address the zero Lie algebra; the zero module; one-dimensional and
trivial modules; reducible modules; infinite-dimensional irreducible modules; nonsimple semisimple
direct sums; repeated isomorphic modules; zero highest weight; empty root systems; dependence on
Cartan/Borel/positive-root choices; fields that are not algebraically closed or have positive
characteristic; reductive algebras with center; and group-versus-Lie-algebra integration.

No case is excluded at intake. In particular, dropping finite dimensionality would make the common
classification gloss false: arbitrary irreducible modules need not be highest-weight modules.

## Excluded substitutions

- Classification of simple Lie algebras or root systems does not classify their representations.
- Complete reducibility, Lie's theorem, Engel's theorem, weight-space decomposition, or existence of
  Cartan subalgebras supplies ingredients only.
- The universal property of a Verma module or uniqueness of its simple quotient does not alone show
  that every finite-dimensional irreducible occurs or characterize finite-dimensional parameters.
- Weyl's character formula and Weyl's dimension formula are downstream formulas, not the
  highest-weight classification root.
- A result for compact Lie groups needs a checked group/algebra equivalence and cannot silently
  replace the Lie-algebra target.
- Kac-Moody, affine, category O, quantum-group, modular-characteristic, finite-group, or
  infinite-dimensional classification theorems are different targets.
- Abstract predicates or a structure that assumes highest-weight classification as a field supply
  no proof.
- A theorem name, `#check`, generic weight/root infrastructure, or the untrusted `verified` label
  supplies no H or M credit.

## Neighbor boundaries

`THM-M-0090` owns the Weyl character formula, `THM-M-0091` the Weyl dimension formula,
`THM-M-0092` the Cartan-Weyl theorem, and `THM-M-0094` the Borel-Weil-Bott theorem. Their future
definitions and artifacts remain separate. Legacy `S1_M_053.lean` records affine character-formula
predicate data, not this finite-dimensional semisimple classification.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, discovery found
`LieAlgebra.IsSemisimple`, `LieSubalgebra.IsCartanSubalgebra`, `LieModule.weightSpace`,
`LieModule.genWeightSpace`, `LieModule.Weight`, `LieAlgebra.rootSpace`,
`LieAlgebra.IsKilling.rootSystem`, and universal-enveloping-algebra infrastructure. These APIs do
not define the source's positive system, dominant-integral weights, Verma/simple modules, or terminal
classification. The bounded search is intake discovery only, not a global absence result or the
later immutable anchor audit.

The pinned `LieAlgebra.IsKilling.rootSystem` API assumes nondegeneracy of the Killing form. Pinned
mathlib supplies the implication from this condition to semisimplicity, but not the converse needed
to start from the catalog's semisimple hypothesis. Strengthening the root to `IsKilling` merely to
reuse this API would narrow the received theorem; a future exact statement must instead retain its
source domain and own any required bridge obligation.
