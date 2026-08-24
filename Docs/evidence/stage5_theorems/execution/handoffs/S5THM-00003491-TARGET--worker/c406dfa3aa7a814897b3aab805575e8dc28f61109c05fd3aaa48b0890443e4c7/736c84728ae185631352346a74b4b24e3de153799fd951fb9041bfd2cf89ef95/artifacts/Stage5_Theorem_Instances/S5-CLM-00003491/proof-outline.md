# Proof outline

## P00-frozen-statement

Hypotheses: n : ℕ; h : IsSquare n

Inference: Delta-expand F, maximalLength, IsIncreasing₂ and lt₂ under the pinned declaration.

Output: The claim-owned exact-root proposition.

Formal anchor: `Statement.lean:127`

Downstream uses: P10-square-root

Exceptional cases: No provider proof body is imported or trusted.

Trust boundary: Frozen provider statement bytes only; Master recomputes elaboration.

## P10-square-root

Hypotheses: h : IsSquare n; q = n.sqrt

Inference: Convert `IsSquare n` to an explicit power-two witness and apply `Nat.exists_mul_self'` to identify q^2 with n.

Output: q ^ 2 = n

Formal anchor: `Statement.lean:147`

Downstream uses: P20-construction; P30-range

Exceptional cases: Covers q = 0 and q = 1 without division.

Trust boundary: The definition of `IsSquare` and Mathlib theorem `Nat.exists_mul_self'`, replayed by Lean.

## P20-construction

Hypotheses: 0 ≤ a,b,c < q

Inference: List triples (a*q+b+1, a*q+c+1, b*q+c+1) in lexicographic a,b,c order.

Output: A list s of q^3 triples.

Formal anchor: `Statement.lean:142`

Downstream uses: P30-range; P40-pairwise; P60-supremum

Exceptional cases: When q = 0 the construction is empty.

Trust boundary: Explicit List.range/flatMap computation.

## P30-range

Hypotheses: a,b,c < q; q^2=n

Inference: Each block expression x*q+y+1 lies between 1 and q^2.

Output: Every coordinate of every constructed triple belongs to [1,n].

Formal anchor: `Statement.lean:154`

Downstream uses: P60-supremum

Exceptional cases: The empty q=0 list makes the universal statement vacuous.

Trust boundary: Presburger arithmetic plus Nat multiplication monotonicity.

## P40-pairwise

Hypotheses: Two distinct lexicographically ordered indices (a,b,c)<(d,e,f).

Inference: First differing a raises coordinates 0,1; b raises 0,2; c raises 1,2.

Output: s.Pairwise lt₂ after delta expansion.

Formal anchor: `Statement.lean:165`

Downstream uses: P60-supremum

Exceptional cases: Same-index elements are never compared by Pairwise.

Trust boundary: Structural List.Pairwise induction and checked inequalities.

## P50-boundedness

Hypotheses: u is any admissible increasing list over [1,n].

Inference: Pigeonhole the first two coordinates for n≥2; handle n=0,1 directly.

Output: u.length ≤ n^2, hence the length set is bounded above.

Formal anchor: `Statement.lean:198`

Downstream uses: P60-supremum

Exceptional cases: n=0 forces the empty list; n=1 forces length below 2.

Trust boundary: Finite pigeonhole theorem plus complete Fin 3 case split.

## P60-supremum

Hypotheses: s has length q^3; s is admissible; the length set is bounded.

Inference: Insert q^3 into the defining set and apply le_csSup.

Output: n.sqrt^3 ≤ maximalLength n after delta expansion.

Formal anchor: `Statement.lean:228`

Downstream uses: P70-transport

Exceptional cases: Natural-number sSup requires the explicitly proved upper bound.

Trust boundary: Mathlib complete-lattice lemma le_csSup.

## P70-transport

Hypotheses: P60 exact-root closure

Inference: Independently reconstruct the exact root in the self-contained audit, check identity transports both directions, and compose them in Audit.lean.

Output: Audited target theorem with no source oracle.

Formal anchor: `Audit.lean:262`

Downstream uses: S6-CLM-00008151; S6-VAR-00007039

Exceptional cases: Canonical Master must independently verify definitional equality to the frozen source expression.

Trust boundary: Worker evidence is provisional; only canonical trust-zero compilation accepts it.
