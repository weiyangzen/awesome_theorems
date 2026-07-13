# Scope map

## Preserved repository scope

The repository fixes only the title `循环码`, the collective attribution `众多数学家`, the period
`20世纪`, and the gloss `循环移位不变的码`. The intake preserves the narrow cyclic-code family
identified by that wording: codes whose words are stable under a cyclic permutation of their
coordinates. This is a family boundary, not a frozen definition or theorem.

## Decisions required before statement freeze

An approved source decision must freeze all of the following without importing conventions from
memory:

1. The alphabet: an arbitrary finite type, additive alphabet, commutative ring, or finite field.
2. The block length, whether it is positive, and whether coordinates are `Fin n`, `ZMod n`, or
   another explicitly ordered cyclic index type.
3. Whether words are dependent functions, vectors, lists of fixed length, or residue classes of
   polynomials, together with checked transports for every credited alternate representation.
4. The shift direction and convention: left/right rotation, action on coordinates or values,
   precomposition by a permutation or its inverse, and closure under one generator or all powers.
5. The code object: a set, finite set, nonempty set, additive subgroup, submodule, or linear code,
   and any fixed-length, nontriviality, minimum-distance, or decoding data included in the term.
6. Whether "invariant" means forward closure, equality of the shifted set with itself, or stability
   of a subobject under a selected linear equivalence.
7. The actual truth-valued conclusion: a definition-characterization equivalence, polynomial-ideal
   correspondence, generator-polynomial theorem, duality theorem, dimension/distance result, or a
   different source-selected proposition.
8. The exact ordered binders, universes, typeclasses, hypotheses, conclusion, foundation and trust
   profiles, and every alternate encoding with a checked relationship.

These choices alter the target or its proof boundary. Intake makes none of them canonical.

## Candidate readings not credited

- A code `C` contained in `A ^ Fin n` is closed under one cyclic coordinate permutation.
- A linear subspace of `F ^ Fin n` is preserved by the corresponding linear equivalence.
- Cyclic linear codes of length `n` over `F` correspond to ideals or submodules of
  `F[X] / (X^n - 1)`.
- Every cyclic code has a source-defined generator polynomial dividing `X^n - 1`.
- The dual of a cyclic code is cyclic under specified field, inner-product, and shift conventions.

Each is standard-looking but adds a proposition not supplied by the repository. None receives
source, statement, or proof credit here.

## Degenerate and boundary cases

Source review must explicitly decide the empty and singleton alphabet; the zero ring; lengths
`n = 0` and `n = 1`; the empty code; singleton, zero, repetition, and full codes; nonempty-code
requirements; left/right shifts; closure versus equality when the shift is invertible; zero and
unit generator polynomials; the quotient by `X^0 - 1`; and whether minimum distance is defined for
codes having fewer than two words.

## Neighbor and substitution boundaries

- `THM-M-1585` (coding theory) is a broader topic and grants no statement or proof credit.
- `THM-M-1586` (Hamming bound) and `THM-M-1587` (Singleton bound) are code-size bounds, not a
  definition or characterization of cyclic codes.
- `THM-M-1589` (linear codes) cannot be folded into this target; cyclic codes may require an
  independently selected linear-code substrate.
- `THM-M-1591` (BCH codes) and `THM-M-1592` (Reed-Solomon codes) own concrete code families. The
  computer-science catalog's description of BCH codes as cyclic error-correcting codes does not
  select or prove this root.
- Circulant matrices, cyclic groups, list rotation, polynomial factorization, Hamming distance, or
  a structure field assuming shift closure are ingredients or non-substitutes, not proof.
- The catalog's `已验证` label is metadata only and supplies no H or M credit.

Statement ambiguity blocks obligation-tree construction. No canonical expression, discovery
protocol, obligation registry, graph, or closure state is frozen by this intake.
