# Scope map

## Preserved catalog scope

The intake preserves only a theorem family: limits of integrals for a monotone sequence of
functions. The real-analysis category, Lebesgue attribution, and 1902 date make the classical
monotone convergence theorem the intended family, but the catalog gloss is not a binder-complete
proposition and does not distinguish its standard variants.

Axler's Theorem 3.11 supplies a credible modern candidate, not yet the canonical root:

- an arbitrary measure space `(X, S, mu)`;
- an increasing sequence `0 <= f 1 <= f 2 <= ...` of `S`-measurable functions;
- values in `[0, infinity]` and the pointwise limit `f(x) = lim_k f_k(x)`; and
- `lim_k integral f_k dmu = integral f dmu`, with infinity permitted.

Pinned mathlib's closest form uses `f : Nat -> alpha -> ENNReal`, pointwise measurability and
monotonicity, and equality between the lintegral of the pointwise `iSup` and the `iSup` of the
lintegrals. Its almost-everywhere and explicit-limit variants are alternate candidate interfaces.

## Proposition-changing decisions

The statement phase must freeze each choice from an admitted source and checked formal target:

1. Whether the domain is an arbitrary measure space or a real interval with Lebesgue measure.
2. Whether functions take values in nonnegative extended reals, nonnegative reals, or ordinary
   reals with separate nonnegativity and integrability premises.
3. Whether measurability and monotonicity hold everywhere or almost everywhere.
4. Whether monotonicity means `f n <= f (n + 1)` or the full `Monotone f` relation, and whether
   equality between successive functions is permitted.
5. Whether the limit is represented by a pointwise supremum or by an explicit function and
   pointwise/almost-everywhere `Tendsto` premise.
6. Whether the conclusion is an extended-real equality of suprema, convergence in `ENNReal`, or
   convergence of finite real-valued Bochner integrals.
7. The natural-number indexing convention, binder order, implicit measure, equality orientation,
   typeclass context, and treatment of infinite values.
8. The source edition, theorem/page, incorporated definitions, proof boundary, historical
   attribution, translation, correction or errata record, and independent review.
9. The foundation, axiom, TCB, computation, freshness, and revocation profiles for the selected
   Lean target and its minimal imports.

## Boundary and mutation cases

The standard nonnegative extended-real version includes the zero measure, zero functions,
constant sequences, equality between successive functions, infinite pointwise limits, and infinite
integrals. The statement gate must test removal of measurability or monotonicity, reversal to a
decreasing sequence without a finiteness premise, replacement of the pointwise limit, change from
everywhere to almost-everywhere hypotheses, and an illicit finite-integral conclusion.

No convergence rate, uniform convergence, integrability bound, domination hypothesis, finite
limit, strict increase, or conclusion about convergence of the functions in a norm is implicit in
the catalog gloss.

## Explicit exclusions

- Dominated convergence, Fatou's lemma, Tonelli's theorem, Fubini's theorem, or continuity of a
  measure from below substituted for the root.
- The decreasing-sequence theorem, which needs an appropriate finite-integral premise.
- A bounded, finite-measure, finite-sequence, simple-function, indicator-only, or constant-function
  special case.
- A real-valued integrable corollary selected in place of the nonnegative extended-real theorem
  without a source decision and checked transport.
- A hypothesis that already assumes convergence or equality of the integrals.
- The catalog's `已验证` label, a theorem name, a doc index, or the intake API probe used as source,
  statement-identity, or proof credit.

## Formal boundary

The pinned source module explicitly identifies and implements several monotone convergence
variants. The probe authenticates seven interfaces and reports direct axioms for four. It does not
choose the source-exact formulation, audit terminal proof-body provenance, freeze an expression,
or grant machine proof credit. The directed-family and real-valued variants are discovery leads,
not additional roots. Exhaustive anchor and provenance review belongs to the downstream audit.
