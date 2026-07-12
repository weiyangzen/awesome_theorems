# Scope map

## Preserved theorem family

The intake preserves a recursion-theoretic fixed-point theorem about effective program indices. The
catalog fixes the Chinese title `不动点定理`, Stephen Kleene, 1938, and the gloss
`递归函数的不动点`; it does not supply a formula, numbering convention, source theorem, or proof.

Two related mathematical shapes are candidates, not adopted statements:

- **Effective code transformer:** for every total computable map from program codes to program
  codes, some code and its image compute extensionally equal partial functions.
- **Parameterized partial-recursive family:** for every partial-recursive binary family of a code
  and an input, some program computes the family specialized to its own code.

Pinned mathlib realizes the first shape as `Nat.Partrec.Code.fixed_point` and the second as
`Nat.Partrec.Code.fixed_point₂`. Their presence establishes a concrete formalization lead only.

## Decisions required at statement freeze

An approved source review must freeze all of the following before one candidate can become the
canonical claim:

1. The primary or authoritative source edition, theorem locator, incorporated definitions, proof
   boundary, correction history, and independent review.
2. Whether the root is Rogers' fixed-point formulation, Kleene's second recursion theorem, another
   historical formulation, or a checked equivalence between specifically selected formulations.
3. The programming formalism and acceptable Goedel numbering: natural indices, an inductive code
   type, or another effective enumeration, together with the universality and parameterization
   properties required of that numbering.
4. Whether the transformer is total computable on codes or a partial-recursive two-argument family,
   including the exact order and dependency of binders.
5. Whether equality means syntactic code equality, equality of partial functions, equality of
   domains and values, or another observational equivalence. The pinned theorem gives extensional
   equality of evaluations, not `f c = c`.
6. Whether the fixed point is a code, its encoded natural index, or a computed partial function, and
   which encoding transports must be checked.
7. The roles of the universal evaluator and s-m-n/parameter theorem, including whether they are
   assumptions, imported lemmas, or separately owned neighboring theorem targets.
8. The exact foundation profile, ordered binders, hypotheses, conclusion, and every degenerate or
   malformed-code convention.

## Neighbor and duplicate boundaries

- `THM-M-0742` is separately cataloged as `递归定理` with the gloss `递归函数的自指`. It may overlap
  Kleene's second recursion theorem, but no accepted alias or root-ownership decision exists.
- `THM-M-0744` separately owns the s-m-n theorem. Its proof content may later become a dependency,
  but its statement and evidence cannot be counted as this target's root.
- `THM-C-0006` is an outside-Stage1 computer-science record explicitly titled Kleene's second
  recursion theorem and glossed "every computable function has a fixed point." It is boundary
  evidence for ambiguity only and receives no Stage1 slot or proof credit.

## Explicit exclusions

The target is not a topological, metric, order-theoretic, domain-theoretic, or programming-language
`fix` theorem. It is not syntactic equality `f c = c`, a fixed point of an arbitrary noncomputable
map, the diagonal lemma for formulas, a quine example, the universal-function theorem, or s-m-n
alone. A theorem assuming the desired fixed point as data, or the catalog's untrusted `已验证` label,
cannot supply proof credit.

## Formal boundary

`IntakeProbe.lean` checks the exact types and axiom reports of the two pinned candidates without
declaring a target theorem or wrapper. The full candidate bodies exist in the pinned dependency,
but until the catalog/source ambiguity is resolved they remain uncredited: there is no canonical
expression fingerprint, checked source transport, formal-anchor acceptance, or `M0-W` claim.
