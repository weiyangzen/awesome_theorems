# Scope map

## Preserved theorem family

The intake preserves a structural claim about least upper bounds in the Turing degrees. The likely
standard shape is binary join: for degrees represented by oracles `A` and `B`, a source-specified
disjoint sum `A op B` has a degree above both, and every degree above both is above its degree.
This is a candidate family description, not the canonical statement.

The repository title says "supremum" while its gloss says "lattice structure." Neither fixes
whether the quantification is binary, finite, countable, or arbitrary. The inspected source leads
support an **upper semilattice**, not a full lattice or completeness claim.

## Decisions required at statement freeze

1. Select and independently review an immutable source edition, exact theorem/page or displayed
   result, incorporated definitions, proof boundary, corrections, and errata.
2. Fix whether degrees are equivalence classes of subsets, characteristic functions, total
   functions, or partial functions `Nat ->. Nat`, and check transports between any encodings.
3. Fix the definition of Turing reducibility, oracle semantics, equivalence relation, quotient
   order, universe, and every implicit totality or extensionality convention.
4. Choose binary join, all finite nonempty joins, a countable join under uniformity hypotheses, an
   arbitrary supremum, or another exact source proposition. These are not interchangeable.
5. For binary join, fix the representative construction, tags/pairing function, and prove both
   upper-bound inequalities plus leastness, independence of representatives, and quotient descent.
6. Decide whether the conclusion is an `IsLUB` predicate, an order equality, a `sup` operation with
   laws, or an instance such as `SemilatticeSup TuringDegree`.
7. Resolve empty-family, singleton, equal-degree, computable-degree, incompatible representative,
   partiality, undefined-value, and encoding boundary cases.
8. State explicitly whether bottom, meets, top, distributivity, completeness, or jump compatibility
   is included. None follows merely from the word "lattice."

## Neighbor boundaries

- `THM-M-0750` separately names Turing degrees and their degree structure. Its definitions may be
  dependencies, but its evidence cannot close this supremum target.
- `THM-M-0752` separately names the jump operator. Jump monotonicity or preservation results do not
  replace a least-upper-bound theorem.
- `THM-M-0749` is Friedberg-Muchnik incomparability. Incomparability is not existence of a join.

## Explicit exclusions

This target is not a generic order-theory theorem instantiated with an assumed `SemilatticeSup`, a
full `Lattice TuringDegree` claim, an arbitrary-family or complete-lattice supremum, a greatest
degree, a jump result, or only the construction of a tagged disjoint sum without the leastness
proof. A structure field or hypothesis storing the desired join, the untrusted catalog label, and
the discovery probe cannot supply proof credit.

## Formal boundary

`IntakeProbe.lean` checks the pinned `TuringReducible`, `TuringEquivalent`, `TuringDegree`, and
`TuringDegree.instPartialOrder` APIs. The pinned module ends with the partial-order instance and has
no supremum surface. Until source and encoding choices are frozen, there is no canonical Lean
expression, expression fingerprint, checked transport, formal anchor, or machine-proof claim.
