# Scope map

## Repository boundary

The repository fixes target `THM-M-0944`, the Balog-Szemeredi-Gowers name,
the attribution Balog/Szemeredi/Gowers, the year 1994, and the Chinese gloss
`近似群的Freiman定理` ("the Freiman theorem for approximate groups"). These
fields identify an additive-combinatorics theorem family, not one
binder-complete proposition.

A later statement phase may select an exact root only from an immutable,
independently reviewed source passage. A standard family-level description is
that unusually many additive coincidences force a large portion of the input
to have controlled additive growth. This is a locator, not an accepted
canonical statement.

## Proposition-changing decisions

The source and statement phases must freeze all of the following:

1. The energy formulation versus a bipartite graph/restricted-sum formulation,
   and the exact checked implications among any credited variants.
2. One input set versus two equal-sized or unequal-sized sets, and whether the
   conclusion controls a self-sumset or a mixed sumset.
3. Abelian groups, general noncommutative groups, integers, finite fields, or a
   more specialized ambient structure.
4. The exact definition and normalization of additive energy, including the
   ordered quadruple equation and whether self-energy or mixed energy is used.
5. The parameter regime: positivity and upper bounds for the energy/density
   parameter, cardinality thresholds, equality of input sizes, and every
   sufficiently-large clause.
6. Exact quantitative subset-size and sumset bounds, including constants,
   exponents, and all dependencies.
7. Whether the conclusion gives one subset, two subsets, a translate, a
   symmetric set, small doubling, small difference, or an approximate subgroup.
8. Empty and singleton inputs, zero energy/density parameters, finite ambient
   groups smaller than the threshold, and casts between natural and real
   cardinalities.

Each choice changes the proposition. No prose equivalence can replace a
checked Lean transport.

## Explicit exclusions

- Freiman's theorem (`THM-M-0941`) or an inverse theorem classifying sets with
  small doubling.
- Ruzsa's covering lemma (`THM-M-0942`) or the Pluennecke-Ruzsa inequalities
  (`THM-M-0943`) used alone as the terminal result.
- A definition or elementary inequality for additive energy, doubling
  constants, Freiman homomorphisms, or approximate subgroups.
- A theorem whose hypotheses already assume the required large structured
  subset or small sumset.
- Specialized finite-field, asymmetric, noncommutative, almost-all,
  hypergraph, polynomial-loss, or qualitative variants selected for
  convenience.
- The 1994 bibliographic record, later secondary restatement, untrusted
  `verified` label, or Lean API probe treated as source fidelity or proof
  credit.

## Pinned formal surface

Pinned mathlib exposes `Finset.addEnergy`, the additive doubling constant
`Finset.addConst`, `IsApproximateAddSubgroup`, and
`Finset.ruzsa_covering_add`. A bounded topic search found no declaration named
for Balog, Gowers, popular sums, or the statistical theorem of set addition.
These interfaces show that adjacent vocabulary can elaborate; they do not
choose or prove the BSG root. Complete anchor discovery belongs to the later
anchor-audit node.

No canonical Lean target, expression fingerprint, alternate encoding,
discovery protocol, obligation registry, or proof state is frozen at intake.
