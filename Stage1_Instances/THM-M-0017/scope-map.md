# Scope map

## Preserved theorem family

The intake preserves the 1910 field-theory family selected by the catalog's author, date, category,
and gloss. Direct inspection of the primary paper exposes these candidate roots:

- Section 21, Satz 9 (page 287): every field has an algebraic algebraically closed extension,
  essentially unique;
- Section 21, Satz 8 (page 286): existence and essential uniqueness of an extension just sufficient
  to split a given polynomial family;
- Section 17, Satz 2 (page 261): the smallest algebraically closed subextension within an already
  algebraically closed extension; and
- the modern classification reading: algebraically closed fields are isomorphic exactly when they
  have the same characteristic and transcendence degree.

This sentence is a candidate interpretation, not the frozen canonical statement. A later statement
phase must select it or another reading from a directly inspected immutable source passage and map
every definition and assumption.

## Decisions required at statement freeze

1. Select the exact edition, `Satz`, page range, incorporated definitions, proof boundary,
   correction history, and independent reviewer for the 1910 source.
2. Decide whether the root is Satz 9 existence alone or existence plus essential uniqueness, the
   more general Satz 8, the relative Satz 2, the modern classification iff, only the construction of
   an isomorphism from matching invariants, or another explicitly sourced result.
3. For classification, fix two fields and their universes, algebraic-closedness assumptions, the
   representation of characteristic, the base prime field, and whether the output is a field
   equivalence, ring equivalence, or algebra equivalence.
4. Fix whether the invariant is `Algebra.trdeg`, the cardinality of explicitly chosen
   transcendence bases, or underlying field cardinality under an uncountability hypothesis.
5. If using explicit bases, fix their coefficient ring, algebra structures, index universes,
   algebraic independence, basis maximality, and cardinal equivalence including universe lifts.
6. If claiming an iff, separately encode and prove that an isomorphism preserves characteristic
   and transcendence degree; the pinned sufficient-direction construction alone is not the iff.
7. Freeze binder order, implicit versus explicit typeclass data, choice/classical requirements,
   minimal imports, boundary cases, and checked transports among every credited alternate form.
8. For an algebraic-closure root, fix existential versus chosen construction, algebraicity,
   algebraic closedness, base-field embedding, uniqueness up to which base-preserving equivalence,
   and whether "essentially" asserts mere existence or chosen uniqueness of an isomorphism.

## Boundary and degenerate cases

Source review must explicitly handle characteristic zero versus prime characteristic; finite and
countable algebraically closed fields; transcendence degree zero, finite, and infinite; empty
transcendence-basis index types; universe-lifted cardinal equality versus a type equivalence;
noncanonical choices of prime subfield and transcendence basis; and whether isomorphism is asserted
plainly, nonemptily, or by a chosen noncomputable equivalence.

For an algebraic-closure reading it must also handle the base field's universe, an extension in the
same or a larger universe, algebraicity and algebraic closedness as separate conditions, embeddings
over the base, nonunique automorphisms, the meaning of minimality, the polynomial family in Satz 8,
and the well-ordering/choice used by the primary construction.

The uncountable cardinality specialization cannot silently replace the arbitrary-field
classification. For example, algebraic closures of finite fields are countable, and cardinality
does not carry the same information as transcendence degree without the stated cardinal
hypotheses.

## Explicit substitutions excluded

- Pinned mathlib's explicitly named **Steinitz theorem**
  `Field.exists_primitive_element_iff_finite_intermediateField` concerns primitive elements of an
  algebraic extension, not classification of algebraically closed fields.
- Existence or uniqueness of an algebraic closure cannot replace classification unless an exact
  source selection shows that this is the catalog's intended 1910 result.
- The Steinitz theorem characterizing graphs of convex three-dimensional polytopes is outside the
  catalog's field-theory scope and 1910 date.
- The fundamental theorem of algebra, finite-field uniqueness, real-closed-field classification,
  and special results only about `Real` and `Complex` are neighboring theorems, not substitutes.
- `IsAlgClosed.equivOfTranscendenceBasis` is a promising sufficient-direction construction but is
  not automatically the arbitrary-field characteristic-and-transcendence-degree iff.
- `IsAlgClosed.ringEquiv_of_equiv_of_char_eq` assumes uncountability and equal underlying
  cardinality; it cannot be generalized by deleting those restrictions.
- A class field or structure that already contains the desired equivalence cannot be projected to
  manufacture the result.
- The catalog's untrusted `verified` label and the API probe supply no human-source or kernel-proof
  credit.

No canonical statement, Lean expression fingerprint, alternate encoding, mutation result,
obligation registry, discovery protocol, or proof state is frozen at intake.
