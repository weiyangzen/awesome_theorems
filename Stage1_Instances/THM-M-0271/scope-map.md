# Scope map

## Preserved theorem family

The intake preserves the classical Fubini theorem family named by the catalog: under suitable
integrability and measurability assumptions, a multiple integral over a product or planar region
agrees with one or both corresponding iterated integrals. This is a family boundary, not a frozen
canonical proposition.

The historical source lead concerns a scalar Lebesgue-integrable function on a planar region whose
horizontal and vertical sections satisfy a stated measurability condition. Pinned mathlib instead
offers an abstract Bochner formulation on product measurable spaces with s-finite measures. A later
statement phase may select a source-reviewed formulation and checked transports, but intake does
not identify these differently scoped statements by name alone.

## Decisions required at statement freeze

An exact source-reviewed statement must decide all of the following:

1. Whether the integral is Lebesgue/Bochner, Riemann, an interval or set integral, or another
   source-defined integral, and how a planar region is represented.
2. Whether the function is real-valued, complex-valued, or valued in a real normed space or Banach
   space, including all universe, normed-group, scalar-action, completeness, and separability data.
3. The two measurable spaces, measures, and whether finite, sigma-finite, s-finite, complete, or
   source-specific hypotheses are required.
4. Whether the root equates the product integral with one iterated order, with both orders, or only
   asserts equality of the two iterated integrals.
5. Whether the hypothesis is integrability on the product, absolute integrability, an explicit
   measurable-plus-integrable package, or separate conditions on almost all sections and their
   norms.
6. Whether section integrability and measurability are conclusions, hypotheses, or incorporated
   definitions, and whether they hold everywhere or only almost everywhere.
7. Whether the formal function is curried or uncurried, which product-measure order is canonical,
   and which equality or `Iff` transports are credited.
8. The exact ordered binders, hypotheses, conclusion, foundation profile, and treatment of all
   degenerate and exceptional cases.

These choices change the proposition or proof boundary. They are a resolution ledger, not a
canonical statement.

## Degenerate and boundary cases

Source review must explicitly resolve zero and infinite measures; empty or null regions; zero,
constant, and almost-everywhere-zero functions; functions integrable on the product but with
exceptional nonintegrable sections; functions whose iterated integrals exist without product
integrability; incomplete codomains; nonmeasurable sections or regions; swapped product-measure
order; and extended-valued versus finite-valued integrals. No case is excluded at intake.

Mathlib's `integral_prod` type does not require `CompleteSpace E`. Its implementation separates the
complete case and reduces the non-complete case through mathlib's convention that the Bochner
integral is zero there. Whether the canonical mathematical claim should instead quantify a Banach
codomain is a source and statement decision, not a harmless omitted typeclass.

## Excluded substitutions

- Tonelli's theorem for nonnegative or `ENNReal`-valued functions is separately owned by
  `THM-M-0272`; `MeasureTheory.lintegral_prod` cannot substitute for this Fubini target.
- A finite rectangle, continuous compact-support, interval-only, counting-measure, or finite-sum
  special case cannot replace a source-selected general statement.
- Equality of iterated integrals alone cannot silently replace a product-integral theorem, nor can
  one order replace a source statement asserting both orders without checked transport.
- An abstract Bochner theorem cannot silently replace the historical planar scalar formulation, or
  vice versa, merely because both carry the name Fubini.
- A hypothesis, structure, or definition storing the desired equality does not prove it.
- A theorem name, `#check`, axiom report, catalog status, or API probe supplies no source identity
  or accepted proof credit.

## Neighbor target boundaries

`THM-M-0272` separately owns Tonelli's nonnegative multiple-integral theorem. The neighboring
dominated-convergence (`THM-M-0268`), monotone-convergence (`THM-M-0269`), and Fatou (`THM-M-0270`)
targets may later become explicit proof dependencies, but their status and evidence do not transfer.
`THM-M-0273` separately owns the Radon-Nikodym theorem. This dossier changes none of their paths or
states.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.MeasureTheory.Integral.Prod` provides
`integrable_prod_iff`, almost-everywhere section-integrability lemmas, product-to-iterated formulas
in both orders, and an iterated-order swap theorem. The narrow probe checks representative APIs and
their current axioms. This is real feasibility evidence supporting provisional `M3`, not an exact
source match, a terminal-body audit, or `M0` proof credit.
