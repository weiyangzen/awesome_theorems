# Scope map

## Preserved theorem family

The intake preserves a recursion-theoretic self-reference theorem about effective program indices.
The catalog fixes the Chinese title `递归定理`, Stephen Kleene, 1938, and the gloss
`递归函数的自指`; it does not supply a formula, source locator, numbering convention, definition of
recursive function, or proof.

Two closely related mathematical shapes are candidates, not adopted statements:

- **Total index transformer:** for every total computable map on program indices, some program and
  its transformed index compute extensionally equal partial functions.
- **Parameterized partial-computable family:** for every partial-computable binary family of an
  index and an input, some program computes the family specialized to its own index.

The Spring 2024 Stanford Encyclopedia of Philosophy archive gives the first as Theorem 3.5 and the
second as Corollary 3.2. Pinned mathlib realizes analogous code-based shapes as
`Nat.Partrec.Code.fixed_point` and `Nat.Partrec.Code.fixed_point₂`. These facts locate the family
and formalization surface only.

## Decisions required at statement freeze

An approved source review must freeze all of the following before a candidate can become the
canonical claim:

1. A primary or approved authoritative source edition, exact result locator, incorporated
   definitions and assumptions, proof boundary, corrections and errata, and independent review.
2. Whether the root is the total index-transformer form, the parameterized form, another historical
   formulation, or a specifically checked equivalence between selected formulations.
3. The programming formalism and acceptable Goedel numbering: natural indices, mathlib's inductive
   `Code`, or another effective enumeration, with every universality and parameterization premise.
4. Whether the transformation is total computable on indices or a partial-computable two-argument
   family, including exact binder order and dependency.
5. Whether equality means syntactic code equality, equality of partial functions, equality of
   domains and values, or another observational equivalence. Neither source lead supports literal
   index equality `f n = n` as the recursion-theorem conclusion.
6. Whether the witness is a code, encoded natural index, or partial function and which transports
   between representations receive kernel-checked witnesses.
7. The roles of the universal evaluator and s-m-n theorem as definitions, imported lemmas,
   assumptions, or separately owned dependencies.
8. Foundation, TCB, and computation profiles; ordered binders, hypotheses, conclusion; and every
   malformed-code, empty-domain, constant-transformer, or other boundary convention.

## Neighbor and duplicate boundaries

- `THM-M-0743` separately owns the title `不动点定理` with the gloss `递归函数的不动点`. The
  recursion and fixed-point names may refer to the same historical theorem or to different
  formulations, but no accepted alias, distinction, transport, or evidence-ownership decision
  exists.
- `THM-M-0744` separately owns the s-m-n theorem. It is a likely proof dependency, not a substitute
  for this root, and transfers no evidence.
- `THM-C-0006` is outside the closed 1546-target Stage1 set and explicitly names Kleene's second
  recursion theorem with a fixed-point gloss. It is ambiguity evidence only and receives no Stage1
  slot or proof credit.

## Explicit exclusions

The target is not primitive recursion or a general recursive definition scheme. It is not the
diagonal lemma for formulas, a single quine, the universal-function theorem, s-m-n alone, syntactic
index equality, an arbitrary noncomputable transformation, or a topological, order-theoretic,
domain-theoretic, or programming-language fixed-point theorem. A structure or hypothesis that
stores the desired self-reference witness is circular. The catalog's untrusted `已验证` label and
the discovery probe supply no proof credit.

## Formal boundary

`IntakeProbe.lean` checks the exact types and axiom reports of the two pinned candidates without
declaring a target theorem or wrapper. Their bodies exist in the pinned dependency, but before
source identity and target ownership are frozen they remain uncredited: there is no canonical
expression fingerprint, checked source transport, statement acceptance, formal-anchor acceptance,
or `M0-W` claim.
