# Scope map

## Received claim

The repository supplies the title "Brauer group theorem" and the gloss "classification of central
simple algebras over a field." This is not a truth-valued proposition. Intake therefore freezes a
theorem-family boundary rather than choosing a familiar formulation from memory.

## Materially different candidate roots

The statement phase must select exactly one sourced root and record checked relationships to the
others. The current candidates are:

1. **Stable-equivalence classification.** Finite-dimensional central simple algebras over a field
   are classified by equivalence after stabilization with positive-size matrix algebras; equality
   in a quotient represents this equivalence.
2. **Brauer group construction.** Stable-equivalence classes form an abelian group, with tensor
   product inducing multiplication, the base field or split matrix algebras representing the
   identity, and the opposite algebra representing the inverse.
3. **Division-algebra representative theorem.** Each finite-dimensional central simple algebra is
   a matrix algebra over a division algebra, and each Brauer class has an appropriate unique
   division-algebra representative. The existence part is related to Artin-Wedderburn, but the
   uniqueness and class statement are additional content.
4. **Morita or arithmetic classification.** Brauer equivalence may be characterized by Morita
   equivalence, or a Brauer group may be identified/computed through cohomological, local, or
   global invariants. These are not implied merely by defining the quotient.

The phrase "classification" does not reveal which conclusion, or which conjunction of conclusions,
the source intends.

## Pinned formal-candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Algebra.BrauerGroup.Defs` provides:

- `CSA K`, bundling a `K`-algebra that is central, simple, and finite-dimensional;
- `IsBrauerEquivalent A B`, witnessed by positive-size matrix stabilizations that are
  `K`-algebra equivalent;
- `IsBrauerEquivalent.refl`, `.symm`, `.trans`, and `.is_eqv`;
- `Brauer.CSA_Setoid K` and `BrauerGroup K`, the quotient by that relation.

These APIs support a possible encoding of stable-equivalence classes. They do not alone prove a
classification theorem. In particular, quotient equality versus the defining relation is quotient
exactness, while the module's TODO list says that the tensor-product group structure,
field-functoriality, and Morita equivalence characterization are not supplied there.

## Decisions required at statement freeze

1. Pin and independently inspect the intended primary or authoritative source passage, including
   edition or scan, theorem and page/section, incorporated definitions, proof boundary, and errata.
2. Resolve the catalogue's 1932 attribution against earlier Brauer work and the 1932 joint paper
   metadata; a year/title match is not a source-to-statement crosswalk.
3. Choose the exact root among stable quotient classification, abelian group construction,
   division representative/uniqueness, Morita classification, or an explicitly sourced alternative.
4. Fix fields, unital associative algebras, finite dimensionality, centrality, simplicity, matrix
   sizes, universes, algebra equivalences, and ordered binders.
5. Specify whether the claim is about representatives, equivalence classes, existence of a
   structure, equality of classes, uniqueness, or an explicit invariant.
6. Resolve split algebras, base-field and opposite-algebra representatives, zero matrix sizes,
   universe lifts, and any nontriviality assumptions.
7. Decide whether a pinned declaration is the canonical expression or an alternate encoding, and
   kernel-check every claimed implication or equivalence.
8. Audit overlap with `THM-M-0036` and `THM-M-0424` without inheriting their state, evidence, or
   proof bodies.

## Explicit exclusions

- Quotient exactness used as a substitute for the full tensor-product abelian group theorem.
- Artin-Wedderburn matrix-over-division-ring existence used as the entire Brauer classification.
- A unique division representative asserted when only matrix normal-form existence is sourced.
- The `THM-M-0424` selected root, wrappers, or lifecycle state silently copied to this target.
- The `THM-M-0036` central-simple Artin-Wedderburn target silently substituted for this target.
- Brauer groups of arbitrary commutative rings or schemes through Azumaya algebras.
- Galois-cohomological, local/global, or number-field computations without source authorization.
- A definition, an interface structure with no inhabitant, or an assumption of the desired group
  law presented as a proof.
- The catalogue `已验证` label, a matching theorem name, or the intake probe used as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, alternate transport, or
degenerate-case exclusion is frozen by this intake.
