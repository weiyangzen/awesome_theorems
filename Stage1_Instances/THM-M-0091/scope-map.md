# Scope map

## Preserved theorem family

The intake preserves the catalog's compact-Lie-group representation-theory family: a formula for
the dimension of an irreducible representation. The conventional candidate is a product indexed
by positive roots whose factors pair a highest weight shifted by the Weyl vector against coroots,
divided by the corresponding Weyl-vector pairings. This description is recorded only to identify
the family and the decisions that alter its proposition; it is not frozen as the exact root.

## Decisions required at statement freeze

1. Preserve and independently review a lawful authoritative source edition, exact theorem or
   formula and page, all incorporated definitions, the proof boundary, translations, corrections,
   and errata.
2. Fix the group class: compact versus compact connected, semisimple versus reductive, and whether
   a simply connected cover or Lie-algebra formulation is part of the statement or only a bridge.
3. Fix the representation: finite-dimensional continuous complex representation, unitary
   representation, Lie-group module, or highest-weight Lie-algebra module, including the precise
   irreducibility and isomorphism conventions.
4. Fix a maximal torus and the resulting weight and root data, including finite root index, chosen
   positive system or base, roots versus coroots, and the normalization of the pairing.
5. Fix the highest weight `lambda`, its integrality and dominance hypotheses, and the Weyl vector
   `rho` as the half-sum of positive roots or an equivalent fundamental-weight construction.
6. Fix the exact product formula: factor order, numerator and denominator, scalar codomain,
   rational or integral interpretation, coercions, denominator nonvanishing, and equality with
   dimension or `finrank`.
7. Decide whether the root is derived directly from the Weyl character formula at the identity or
   stated independently, and require checked identity-limit transports for any credited derivation.
8. Fix ordered binders, universes, typeclasses, minimal imports, foundation/TCB/computation
   profiles, canonical expression, environment fingerprint, and all alternate encodings.

## Boundary cases

Source and statement review must explicitly dispose of the trivial group; a torus or nontrivial
center with empty semisimple root system; disconnected compact groups; rank zero; the trivial
highest weight; non-dominant or non-integral weights; reducible or zero-dimensional
representations; denominators before a positivity/nonzero proof; different positive-root choices;
isogenous groups with the same Lie algebra but different admissible weights; real versus complex
representations; and empty products. No case is excluded at intake.

## Explicit substitutions excluded

- The Weyl character formula is a neighboring theorem and does not become the dimension formula
  without a checked specialization or limit at the identity.
- The highest-weight theorem classifies irreducibles but is not the numerical product identity.
- The Weyl denominator identity, Weyl integration formula, Weyl law, Weyl group order formulas,
  and finite-group character dimension facts are different roots.
- A root-system product detached from a representation and a theorem relating that representation
  to its highest weight does not prove the catalog claim.
- A rank-one, classical-family, symmetric-power, `SU(2)`, or other special-case calculation cannot
  replace the general source-selected root.
- A structure, field, hypothesis, table, or computation that stores the desired dimension equality
  is circular and receives no proof credit.
- A theorem-name match, generic root or representation infrastructure, the catalog's `已验证`
  label, and the intake probe supply no source or proof credit.

## Neighbor boundaries

`THM-M-0090` owns the Weyl character formula and `THM-M-0093` owns the highest-weight theorem.
Their future accepted evidence may become dependencies, but it grants no statement identity,
status, or proof credit to this target. `THM-M-0089` (Peter-Weyl) concerns representation
decomposition rather than the product dimension formula.

## Formal boundary

Pinned mathlib exposes meaningful pieces of root systems, positive roots, Lie-algebra weights,
finite-dimensional representations, characters, and Lie groups. Intake does not freeze any piece
or combination as the canonical expression, claim minimal imports, audit terminal proof bodies, or
establish a compact-group/highest-weight/product bridge. The canonical expression and environment
fingerprint remain null.
