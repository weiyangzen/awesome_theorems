# Scope map

## Preserved source scope

- Label: differential algebra.
- Attributed developers: Joseph Ritt and Ellis Kolchin, as repository metadata only.
- Period: the 1950s, as repository metadata only.
- Description: "the algebraic theory of differential equations."
- Repository classification: mathematical logic / model theory.

This information indicates a mathematical subject. It does not select a proposition within that
subject. In particular, "differential algebra" can concern ordinary or partial differential
algebra, differential polynomial rings and ideals, algebraic differential equations, differential
field extensions, elimination, dimension theory, or differential algebraic geometry.

## Decisions required before statement freeze

The statement phase must select an inspectable primary source and one exact theorem locator. It
must then freeze:

- ordinary versus multiple commuting derivations, including their index type;
- the ambient commutative ring or field, base object, characteristic, constants, and extension
  structure;
- the relevant differential-polynomial ring, ideal, variety, field extension, or equation system;
- every finiteness, primality, radicality, irreducibility, differential-closure, and separability
  hypothesis;
- ordered binders, universes, quantifier scope, conclusion, and all zero/empty/constant cases;
- a canonical Lean proposition and any checked transports to alternate encodings;
- foundation, trusted-computing-base, and computation profiles.

## Explicit exclusions

- No theorem of Ritt, Kolchin, Hilbert-basis type, elimination type, or Nullstellensatz type is
  selected merely because it is associated with the subject.
- A basic lemma about `Differential`, `DifferentialAlgebra`, a derivation, or logarithmic
  derivatives is not substituted for the unidentified root claim.
- The neighboring targets on differentially closed fields and differential Galois theory are not
  folded into this target.
- The untrusted `已验证` label supplies no human-source or kernel-proof credit.

`IntakeProbe.lean` establishes only vocabulary availability in pinned mathlib. It does not narrow
the source scope or freeze the theorem.
