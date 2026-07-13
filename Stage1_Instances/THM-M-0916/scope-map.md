# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0916`, the title `欧拉五边形数定理`, Leonhard Euler, the
year 1750, and the gloss `整数分拆的生成函数恒等式`. Importance `高` and status `已验证` are
catalog metadata, not source or kernel evidence. No displayed identity, source, theorem locator,
definitions, binders, hypotheses, or proof accompanies the record.

Intake preserves that family without choosing a formula from memory. In particular, the phrase
"partition generating-function identity" does not say whether the pentagonal expansion itself or
its reciprocal partition interpretation is the root.

## Candidate readings requiring a source decision

1. **Product to pentagonal series.** In a source-selected formal or analytic setting, the product
   over positive `m` of `(1 - X^m)` equals a signed series supported on the generalized pentagonal
   numbers. This is the theorem most directly suggested by the name, but the catalog supplies no
   formula or semantics.
2. **Paired natural-index form.** The same intended identity may be displayed as a constant term
   plus paired terms with exponents `k(3k-1)/2` and `k(3k+1)/2` for positive `k`. Equivalence to an
   integer-indexed form requires checked reindexing, exponent arithmetic, and sign conventions.
3. **Partition generating function.** The reciprocal product may be identified with the power
   series whose `n`th coefficient is the number of partitions of `n`. This uses another identity
   and an inverse/non-zero-divisor boundary; it is not merely a typographical rewrite.
4. **Coefficient recurrence.** Extracting coefficients gives Euler's generalized-pentagonal
   recurrence for `p(n)`. This is a consequence only after a checked coefficient and inverse
   argument, not a definitionally identical root.
5. **Analytic q-series.** A source may work with complex `q` under `|q| < 1` instead of formal power
   series. The convergence, product ordering, and coefficient transport are proposition-changing.

No candidate is canonical or receives source or proof credit during intake.

NIST DLMF E4-E5 is the strongest exact modern root candidate located at intake: it explicitly names
the theorem and gives the paired natural-index identity and exponent definition. E2-E3 provide its
analytic product and partition context. That observation narrows source work but does not admit the
source, decide analytic versus formal encoding, or complete the statement phase.

## Statement-phase decisions

An immutable, independently reviewed source must freeze:

- whether the root is the product expansion, reciprocal partition generating function, recurrence,
  or a source-specified conjunction, and the logical relationships to all alternate forms;
- the exact coefficient domain, formal power-series or analytic-q semantics, topology, convergence
  hypotheses, and definition/order of the infinite product and sum;
- the integer-indexed or paired-natural indexing, generalized-pentagonal exponent definitions,
  integrality/nonnegativity proofs, sign parity, and handling of `k = 0`;
- the definition of an integer partition and `p(n)`, including labelled representation and `p(0)`;
- all ordered binders, universes, typeclasses, hypotheses, conclusion, and coercions;
- source edition, theorem/page or section locator, incorporated definitions, proof boundary,
  corrections or errata, and reconciliation of the catalog's 1750 date with the selected work;
- minimal Lean imports, canonical expression and environment fingerprints, checked alternate-form
  transports, and the required removed-hypothesis, changed-domain, binder-scope, and boundary
  mutations.

## Degenerate and boundary cases

The selected source must decide the constant coefficient, empty product, `k = 0` duplication,
negative integer indices, `p(0)`, exponents larger than the coefficient index in the recurrence,
`q = 0`, approach to the analytic boundary `|q| = 1`, characteristic two, zero divisors, and any
requirements needed to invert the product. No case is excluded at intake.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the module
`Mathlib.Combinatorics.Enumerative.Partition.GenFun` defines `Nat.Partition.genFun` and proves the
generic weighted product formula `Nat.Partition.hasProd_genFun` and equality
`Nat.Partition.genFun_eq_tprod`. Its documentation says that specializing the weight to one should
give the ordinary partition function, but marks that specialization TODO. A bounded search found no
pentagonal-named declaration in pinned mathlib or repo-local Lean.

These APIs are adjacent infrastructure, not the signed pentagonal expansion. The distinct theorem
`Nat.Partition.card_odds_eq_card_distincts` in `Glaisher.lean` is sometimes called Euler's partition
theorem and is explicitly outside this root.

## Explicit exclusions

- No substitution of Glaisher's theorem or equality of odd-part and distinct-part counts.
- No presentation of generic `genFun` infrastructure as the pentagonal-number theorem.
- No substitution of a recurrence for a source-selected series identity, or vice versa, without a
  checked directional transport.
- No finite product, truncated series, handful of coefficient checks, numerical q evaluation,
  computer-algebra expansion, or unchecked certificate as a universal identity.
- No structure, hypothesis, or definition that stores the desired equality as data.
- No borrowing of statement or proof credit from `THM-M-0915`, `THM-M-0917`, or `THM-M-0918`.
- No theorem-name match, URL, untrusted catalog label, or `#check` used as proof evidence.

## Statement retry condition

An independent q-series/history reviewer must admit an immutable primary or authoritative edition,
select one exact source result, resolve the date and identity boundary, and approve a complete map of
formula, definitions, premises, conclusion, boundary cases, proof boundary, and corrections. The
statement phase may then elaborate that exact root and checked alternate transports.
