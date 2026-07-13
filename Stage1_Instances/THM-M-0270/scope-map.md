# Scope map

## Received claim

`Docs/researches/math_theorems.md:1943-1948` supplies the title `法图引理` (Fatou's lemma), Pierre
Fatou, the year 1906, and the gloss `积分下极限的不等式` ("an inequality for the liminf of
integrals"). This identifies the classical measure-theoretic family but does not determine one
truth-valued proposition. The intake freezes the family boundary and the decisions required next;
it does not invent the canonical statement.

## Candidate classical boundary

A standard form starts with a measure space and a sequence of nonnegative measurable functions and
says that the integral of the pointwise liminf is at most the liminf of their integrals. This is a
candidate family description only. Source review and statement freeze must decide:

1. The carrier, sigma-algebra or `MeasurableSpace`, measure, and universe levels.
2. Whether the sequence is naturally indexed and whether a more general directed/filter form is
   part of the source claim.
3. Whether functions are nonnegative real-valued, `ENNReal`-valued, extended-real-valued, or real-
   valued with a common integrable lower bound.
4. Whether every function is measurable or merely a.e. measurable, and how representatives are
   treated when the conclusion uses pointwise `liminf`.
5. Whether `liminf` is pointwise, essential, or taken in another topology/order, and the exact
   `atTop` convention.
6. Whether the integral is the lower Lebesgue integral or a signed/Bochner integral requiring
   additional integrability hypotheses.
7. The orientation and scope of the inequality and whether any finite-measure, sigma-finite, or
   integrability premise appears in the selected source.

## Pinned Lean candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Integral.Lebesgue.Add` provides two declarations explicitly documented as
Fatou's lemma:

```text
MeasureTheory.lintegral_liminf_le'
  (forall n, AEMeasurable (f n) mu) ->
  integral^- (liminf f atTop) dmu <= liminf (fun n => integral^- (f n) dmu) atTop

MeasureTheory.lintegral_liminf_le
  (forall n, Measurable (f n)) ->
  integral^- (liminf f atTop) dmu <= liminf (fun n => integral^- (f n) dmu) atTop
```

Both use `f : Nat -> alpha -> ENNReal`; the first permits a.e. measurability relative to `mu`, and
the second is the measurable specialization. These are strong exact-topic interfaces, so the
provisional machine status is `M3`, not `M4`. Neither receives root or proof credit at intake: the
source variant, canonical expression, checked transport, terminal-body provenance, trust policy,
and master-accepted node receipt remain downstream.

## Boundary cases

The statement phase must explicitly resolve the zero measure, empty carrier, identically zero and
identically infinite functions, finite versus infinite integrals, pointwise changes on null sets,
nonmeasurable pointwise liminf representatives, constant and monotone sequences, strict inequality,
and functions with negative values or only a common lower bound. No case is excluded before one
source-mapped proposition is selected.

## Explicit exclusions

- The monotone or dominated convergence theorem in place of Fatou's inequality.
- Reverse Fatou lemmas, bounded-above variants, or signed-function generalizations without a
  checked implication to the selected root.
- An inequality for finite sums, series, expectations, probability measures only, or a fixed
  measure space used as the unrestricted theorem.
- The separately cataloged radial-boundary Fatou theorem `THM-M-0245` or complex-dynamics Fatou set
  `THM-M-1429`.
- A structure or hypothesis that stores the desired inequality as data.
- A theorem name, `#check`, URL, numerical example, or the catalog's untrusted verified label used
  as statement identity, source fidelity, or proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, alternate encoding, or
degenerate-case exclusion is frozen by this intake.
