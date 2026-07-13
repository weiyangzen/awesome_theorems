# Scope map

## Preserved theorem family

The intake preserves exactly the named Bose-Chowla family and the catalog gloss "construction of
Sidon sets." Publisher metadata links Bose and Chowla to a 1962 paper about difference sets and
`B_2` sequences, but neither the catalog nor the admitted preview selects an exact numbered result.
This family description is not a canonical proposition.

## Decisions required before statement freeze

| Surface | Unresolved choice | Why it changes the proposition |
|---|---|---|
| Source root | one `B_2` result, a general `B_h` result, or a corollary stated for integers | the parameters, ambient object, and conclusion differ |
| Parameter | prime `p`, prime power `q`, finite field, or another admissible order | existence and cardinality assumptions differ |
| Ambient object | cyclic group such as order `q^2 - 1`, a quotient, or an integer interval | equality of sums and wraparound have different meanings |
| Sidon predicate | ordered pairs, unordered pairs, differences, or unique two-term multisets | diagonal pairs and swapped summands are treated differently |
| Repetition | allow equal summands or require distinct summands | this changes the `B_2` property |
| Cardinality and bound | exact size, lower bound, optimality, or asymptotic claim | construction and extremal conclusions are not interchangeable |
| Construction data | existential set, finite-field logarithm construction, or effective map | witness and computation requirements differ |
| Generalization | `B_2` only or every fixed `h` with unique `h`-term representations | quantifier order and ambient group order change |

An approved statement must freeze the source edition and locator, every incorporated definition,
the full ordered binders and hypotheses, the exact ambient group and equality, cardinalities,
construction witness, conclusion, checked alternate encodings, foundation profile, and proof
boundary. The catalog's date conflict must also be reconciled rather than hidden.

## Boundary cases

Source review must explicitly address the smallest prime powers; zero or one parameters if natural
numbers are used; empty and singleton sets; diagonal representations; swapped summands; equality
modulo the ambient order versus equality in integers; zero residues; representatives at interval
endpoints; and whether a general `B_h` statement includes `h = 0`, `h = 1`, or only `h >= 2`.
No case is excluded at intake.

## Excluded substitutions

- `THM-M-0956` (Erdos-Turan construction) has the identical one-line Sidon-construction gloss but
  separate attribution and ownership. Its construction and proof credit cannot be borrowed.
- A generic existence theorem for Sidon sets, a probabilistic construction, Singer difference
  sets, or a later finite-field construction cannot replace the source-selected Bose-Chowla root.
- A `B_2` theorem cannot replace a selected general `B_h` theorem, nor conversely.
- A finite computation for one field or modulus cannot establish the uniform construction.
- Additive energy, a Freiman predicate, finite-field cyclicity, or primitive-element infrastructure
  is only substrate; none states the construction.
- A definition or hypothesis storing a Sidon witness, the catalog's `已验证` label, or the API probe
  supplies no root proof credit.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks `IsAddFreimanHom`,
`isAddFreimanHom_two`, `Finset.addEnergy`, `FiniteField.card`, `Fintype.card_units`, and
`IsCyclic.exists_generator`. They support possible later encodings but do not define a Sidon set or
prove a Bose-Chowla construction. Exact imports, expression and environment fingerprints, checked
transports, mutations, and proof-body provenance belong to downstream phases.
