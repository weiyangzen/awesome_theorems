# Scope map

## Received claim

The repository supplies only the title "Wedderburn-Artin theorem" and the gloss "the structure
theorem for semisimple rings." It does not supply a truth-valued proposition. Intake therefore
freezes a theorem-family boundary, not an invented canonical theorem.

## Candidate classical boundary

A standard candidate existence reading has the following ingredients, all still requiring a
pinpoint source and checked Lean identity or transport:

- an associative unital ring `R`, with the zero-ring convention made explicit;
- a left or right semisimplicity predicate for the regular module;
- a finite indexing type for the simple factors;
- one division ring `D_i` and a positive matrix size `d_i` for each factor;
- a ring isomorphism from `R` to the finite product of the matrix rings `M_(d_i)(D_i)`.

A common stronger form is a biconditional between semisimplicity and existence of such data.
Uniqueness of the factors and sizes, classification up to permutation and division-ring
isomorphism, and equivalence with an Artinian semiprimitive condition are materially additional
claims unless the selected source includes them.

## Pinned formal-candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.RingTheory.SimpleModule.WedderburnArtin` provides:

1. `IsSemisimpleRing.exists_ringEquiv_pi_matrix_divisionRing`: under `[Ring R]` and
   `[IsSemisimpleRing R]`, there exist `n : Nat`, division rings `D i`, positive matrix sizes
   `d i`, and a nonempty ring equivalence from `R` to their `Fin n`-indexed product.
2. `isSemisimpleRing_iff_pi_matrix_divisionRing`: an existence biconditional. Its existential
   matrix sizes are not explicitly constrained by `NeZero`; empty matrix index types are allowed
   syntactically, which makes the exact relationship to source conventions a statement issue.
3. `IsSemisimpleRing.exists_ringEquiv_pi_matrix_end_mulOpposite`: a more canonical factor
   presentation using opposites of endomorphism rings of simple ideals.
4. Simple-Artinian and base-algebra variants, plus finite-module refinements. These are related
   theorem-family members, not automatic replacements for the general semisimple-ring claim.

The module contains downstream `proof_wanted` declarations about semiprimary/opposite-ring facts.
They are not used by the three candidate declarations probed here, but a later provenance audit
must still inspect terminal dependencies rather than infer trust from the module name.

## Decisions required at statement freeze

1. Pin and independently inspect the intended primary or authoritative source passage, including
   incorporated definitions, theorem number/page, assumptions, proof boundary, and errata.
2. Fix associativity, identity, zero-ring and nontriviality conventions, and whether left, right,
   or two-sided semisimplicity is meant.
3. Select the root form: forward existence, existence biconditional, a uniqueness-enhanced
   classification, or another explicitly sourced formulation.
4. Fix finite-product and matrix notation, the positivity of each matrix size, and whether `n = 0`
   or an empty product is admissible.
5. Decide whether division rings and matrix factors live in the same universe as `R`, and record
   any universe lift used by the formal encoding.
6. Determine whether the pinned mathlib theorem is the canonical target or an alternate encoding,
   and kernel-check every required implication or equivalence.
7. Separate the simple Artinian, algebra, finite-dimensional, algebraically closed, and uniqueness
   variants from the unrestricted root.

## Explicit exclusions

- Wedderburn's little theorem that every finite division ring is commutative.
- The separate `THM-M-0036` catalogue target, whose gloss is classification of central simple
  algebras; its exact relationship and any shared proof bodies require a later cross-target audit,
  but its algebra-specific root must not be silently absorbed here.
- Only the simple Artinian single-matrix-factor theorem when the selected root concerns arbitrary
  semisimple rings.
- Only a finite-dimensional central-simple-algebra specialization, including the foreign
  `THM-M-0424` Brauer-group wrapper.
- The algebraically closed field specialization to products of matrices over the base field.
- A uniqueness theorem, Artinian/semiprimitive characterization, or left-right symmetry result
  silently added to or removed from the source claim.
- A biconditional used in place of a forward theorem, or vice versa, without a source decision and
  checked relationship.
- A structure or hypothesis that assumes the desired decomposition.
- The catalogue `已验证` label, a theorem-name match, or the intake probe as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, alternate encoding, or
degenerate-case exclusion is frozen in this intake.
