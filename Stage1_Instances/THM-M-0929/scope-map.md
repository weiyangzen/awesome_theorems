# Scope map

## Preserved catalog scope

The received claim is exactly "orbit counting under a group action." Together with the title
`Burnside's lemma`, this identifies the classical finite-action orbit-counting family, but the
catalog is not a binder-complete mathematical source. Intake preserves that family without
silently selecting one of its related formulas.

The expected mathematical components, none yet credited as the canonical proposition, are:

- a group acting on a carrier;
- the fixed-point set for each group element;
- the quotient of the carrier by the same-orbit relation;
- finiteness sufficient to assign natural-number cardinalities to the group, fixed-point sets, and
  orbit quotient; and
- an identity relating the sum or average of fixed-point counts to the number of orbits.

## Proposition-changing decisions

An approved source and independent review must settle the following before statement execution:

1. Whether the theorem uses a finite group acting on a finite set, or the more general mathlib
   assumptions that separately require a finite group, every fixed-point subtype, and the orbit
   quotient to be finite.
2. Whether the canonical result is the natural-number multiplication identity, an average or
   division formula, or the underlying bijection between the sigma type of fixed pairs and the
   product of the orbit quotient with the group.
3. If an average form is selected, whether its codomain is `Nat`, `Rat`, or another exact carrier,
   and how nonzero group cardinality and division are handled.
4. The fixed-point convention (`MulAction.fixedBy` or an explicitly transported equivalent), the
   same-orbit relation and quotient convention, and whether quotient representatives occur.
5. The ordered universes, action and carrier types, group/action and finiteness instances, explicit
   versus implicit binders, hypotheses, and conclusion.
6. Whether the multiplicative formulation is canonical and the additive formulation is an
   alternate encoding, or vice versa, with a checked transport for any credited alternate.
7. The selected foundation, classical-choice, trusted-computing-base, and computation policies.

These are not merely display choices. Natural-number division can hide exact divisibility, and
finiteness of each fixed-point subtype plus the orbit quotient is not definitionally the same
binder context as `Fintype` on the entire acted-on carrier.

## Boundary and mutation cases

Statement review must resolve the empty acted-on carrier, the trivial group, trivial actions,
free actions, transitive actions, singleton carriers, actions with no fixed points for nonidentity
elements, and the identity element's fixed set. It must also test removal of a finiteness
hypothesis, a changed group or action domain, changed binder scope, and a relevant boundary case as
required by the rev-5.6 statement gate. Intake excludes none of these silently.

## Explicit non-substitutions

- Do not replace this target with `THM-M-0928` Polya enumeration, which adds a coloring setup and
  cycle-index or weighted counting data.
- Do not substitute orbit-stabilizer alone, the conjugation class equation, or a special action;
  these may support applications but are not the general fixed-point average identity.
- Do not confuse this target with `THM-M-0069`, Burnside's solvability theorem for groups of order
  `p^a q^b`, or with Burnside's normal `p`-complement/transfer theorem.
- Do not silently replace the multiplication identity by a division formula or the structural
  bijection without an approved source selection and checked relationship.
- Do not treat the Cauchy-Frobenius/Burnside naming history, a theorem name, module documentation,
  the catalog label `已验证`, or a successful API probe as source identity or theorem completion.
- Do not encode the result as an axiom, opaque premise, structure field, certificate, oracle, or a
  hypothesis that already contains the desired counting identity.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.GroupTheory.GroupAction.Quotient` explicitly labels
`MulAction.sigmaFixedByEquivOrbitsProdGroup` and
`MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group` as Burnside's lemma. The latter states
the multiplication form, while the former gives its structural cardinality witness. Their
additive analogues are generated alongside them. The discovery-only probe checks these declarations
and adjacent definitions. They are direct exact-topic candidates, not a frozen source transport or
an anchor-audit receipt. Canonical elaboration, expression and environment fingerprints, checked
transports, statement mutations, terminal-body provenance, full trust closure, and proof credit
remain downstream.
