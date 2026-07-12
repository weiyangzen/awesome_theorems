# Scope map

## Provisional included claim

- The classical cyclotomic Iwasawa main-conjecture family, not an arbitrary modern main
  conjecture bearing Iwasawa's name.
- A source-fixed cyclotomic `Z_p`-extension (or its character/idempotent components), with the
  inverse system of `p`-primary ideal class groups and its norm transition maps.
- The resulting finitely generated torsion module over a source-fixed completed Iwasawa algebra
  and its characteristic ideal or equivalent characteristic power series.
- The cyclotomic `p`-adic L-function in the same component and normalization.
- Equality of the algebraic and analytic ideals, rather than only one divisibility or a numerical
  consequence.

## Decisions required at statement freeze

The selected primary theorem must fix the base abelian/cyclotomic extension, odd-prime policy,
Galois group and completed group algebra, coefficient ring, involution convention, plus/minus or
character decomposition, primitive/imprimitive convention, class-group transition maps, torsion
statement, definition of characteristic ideal, periods and interpolation normalization, omitted
Euler factors, trivial or exceptional characters, exceptional zeros, and whether the conclusion is
ideal equality or association of generators. Binder order, universes, and boundary cases must
follow that source rather than a convenient abstract interface.

## Explicit exclusions

- The non-cyclotomic main conjecture for arbitrary totally real fields, elliptic curves, modular
  forms, motives, or noncommutative Iwasawa theory.
- The separately scheduled Mazur-Wiles historical target `THM-M-0024` as interchangeable proof
  credit; overlap in subject does not merge target identity or receipts.
- Class-number growth, Herbrand-Ribet, Leopoldt, or interpolation alone as a substitute for the
  root ideal equality.
- One ideal divisibility presented as the full equality without a checked converse.
- An arbitrary ring, module, and element quantified abstractly so that the missing arithmetic
  semantics become assumptions.
- `AwesomeTheorems.Stage1.S1_M_257.StatementShape`, whose abstract package nonemptiness is weaker
  than the theorem.
- The repository label `已验证` as evidence of a human proof or Lean kernel closure.

No canonical Lean target is frozen during intake. The later statement must use concrete or pinned
definitions for every root-relevant object, or record a precise infrastructure blocker.
