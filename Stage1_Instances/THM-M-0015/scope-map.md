# Scope map

## Preserved source scope

The repository fixes the title `阿廷互反律` (Artin reciprocity), Emil Artin, 1927, and the gloss
`类域论的核心定理` ("the central theorem of class field theory"). This identifies a classical
reciprocity theorem family but does not itself form a truth-valued proposition.

The strongest inspected discriminator is J. S. Milne, *Class Field Theory* v4.03, Chapter V,
Theorem 5.3. In the chapter's number-field setup, its global idelic form constructs a global Artin
map from the idele group, says that principal ideles lie in its kernel, and gives a quotient
isomorphism for every finite abelian extension. That theorem family is the leading candidate for a
later exact target. It is not frozen as the canonical statement here because the repository does
not cite it or resolve the alternatives below.

## Proposition-changing decisions

An approved statement run must resolve all of the following from an immutable source:

- number fields only versus arbitrary global fields;
- the ideal/ray-class formulation versus the idelic formulation and a checked transport between
  them;
- the base field, fixed algebraic closure or maximal abelian extension, finite abelian extension,
  idele and idele-class objects, norm subgroup, and topology;
- whether the root asserts existence and uniqueness of the global map, triviality on principal
  ideles, the finite-level kernel/quotient isomorphism, compatibility with local maps and norms, or
  a source-authorized conjunction of these clauses;
- arithmetic Frobenius versus geometric Frobenius, including inverses and the sign/direction of
  every local and global Artin map;
- ramified places, archimedean places, modulus and positivity conventions in an ideal encoding;
- trivial extensions, function-field degree behavior, connected-component issues, and other
  boundary cases; and
- the complete order and scope of universes, binders, typeclass assumptions, and conclusions.

These choices affect the statement or its normalization. They are a resolution checklist, not an
asserted theorem.

## Candidate clauses not credited

- Milne v4.03, Chapter V, Theorem 5.3(a): the global Artin map kills principal ideles.
- Milne v4.03, Chapter V, Theorem 5.3(b): for each finite abelian extension `L/K`, it induces
  `C_K / Nm(C_L) ≃ Gal(L/K)`.
- Artin's 1927 ideal-theoretic reciprocity theorem, with an appropriate modulus and ray group.
- The inverse-limit or maximal-abelian-extension formulation after all connected-component and
  topology conventions are fixed.

No clause, conjunction, or equivalence is selected or credited at intake.

## Explicit exclusions

The separate existence theorem for class fields is not silently added to this target. Milne states
it separately as Chapter V, Theorem 5.5, and repository target `THM-M-0422` covers global class
field theory as a broader reciprocity-plus-existence package. Local class field theory alone,
Kronecker-Weber, one Hilbert or ray class field, a single base field, Artin L-function reciprocity,
Shimura reciprocity, and nonabelian or Langlands reciprocity are also not substitutes for the root.

Legacy `S1_M_077.lean` supplies discovery-only global-class-field interfaces. Its candidate idele
class group and abstract reciprocity data neither construct the source Artin map nor prove its
kernel or quotient theorem, and the uniform L0 rule grants it no proof credit for this target.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies number fields, the additive adele
ring, an injective diagonal algebra map, ideal class groups, abelian Galois extensions, and quotient
group primitives. The intake probe checks only those substrates. It does not define a restricted
multiplicative idele group, the source-faithful idele class group, norm maps between them, a global
Artin map, Frobenius compatibility, or the reciprocity isomorphism. A full formal-candidate audit is
downstream.
