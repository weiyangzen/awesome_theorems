# Proof outline — S5-CLM-00003516

## [fragment root-answer]

Hypotheses: the frozen question records `answer(True)` and quantifies over two
monic real-rooted cubics. Inference: unfold the yes/no wrapper and retain the
universal cubic claim. Output: the claimed answer is `True`. Formal anchor:
`claim_owned_four_3`. Downstream use: release root. Exceptional case: none.
Trust boundary: the frozen provider theorem is statement provenance only and
its `sorryAx` body is never used.

## [fragment normalize-cubics]

Hypotheses: each input is monic, real-rooted, and has degree three. Inference:
translate its roots to mean zero and write the centered cubic as
`x^3 - 3 a x - u`; real-rootedness gives `a ≥ 0`. Output: centered invariants
`(a,u)` and `(b,v)`. Formal anchor: source definitions `FourProp`, `Φ`, and
`finiteAdditiveConvolution`, frozen by the crosswalk. Downstream use:
`add-invariants` and `discriminant-bound`. Exceptional cases: repeated roots
are retained and sent to `repeated-root`. Trust boundary: this normalization
is a human algebraic reduction to be independently replayed by Master.

## [fragment add-invariants]

Hypotheses: centered cubic invariants `(a,u)` and `(b,v)`. Inference: expand the
degree-three finite additive convolution coefficient formula. Output: the
convolution has centered invariants `(a+b,u+v)`. Formal anchor:
`finiteAdditiveConvolution` at `n = 3`. Downstream use: `cauchy-core`.
Exceptional cases: centering commutes with the convolution; no division is
performed. Trust boundary: exact coefficient expansion is part of the Master
semantic replay.

## [fragment discriminant-bound]

Hypotheses: `x^3 - 3 a x - u` is real-rooted. Inference: its discriminant is
nonnegative. Output: `u^2 ≤ 4 a^3`, and analogously `v^2 ≤ 4 b^3`. Formal
anchor: cubic discriminant identity. Downstream use: denominator positivity.
Exceptional cases: equality is exactly the repeated-root boundary. Trust
boundary: standard polynomial discriminant algebra, explicitly recorded here.

## [fragment phi-identity]

Hypotheses: a centered cubic has distinct real roots and invariants `(a,u)`.
Inference: combine the three logarithmic-derivative sums over the roots and
clear the Vandermonde denominator. Output:
`1 / Φ = (4*a^3-u^2)/(6*a^2)` (with the corresponding ENNReal coercions).
Formal anchor: definition `Φ`. Downstream use: `cauchy-core`. Exceptional
cases: repeated roots are handled separately; `a=0` forces a triple root.
Trust boundary: rational-function identity to be checked after integration.

## [fragment cauchy-core]

Hypotheses: `a,b ≥ 0`. Inference: use
`(a+b)(b*u^2+a*v^2)-a*b*(u+v)^2=(b*u-a*v)^2 ≥ 0` and substitute the cubic
formula. Output: the desired superadditivity inequality after clearing the
positive denominators. Formal anchor: `cubic_cauchy_core` and
`weighted_square_le`. Downstream use: `assemble`. Exceptional cases `a=0` or
`b=0` reduce by continuity/equality. Trust boundary: Lean proves the displayed
polynomial identity without an oracle.

## [fragment repeated-root]

Hypotheses: an input or output cubic has a multiple root. Inference: by the
definition of `Φ`, its value is top, so its reciprocal is zero; the remaining
inequality follows from nonnegativity or from the discriminant equality case.
Output: all nodup failures are covered. Formal anchor: the `if` in `Φ`.
Downstream use: `assemble`. Exceptional cases: triple and double roots are
both included. Trust boundary: ENNReal top/inverse laws from Mathlib.

## [fragment assemble]

Hypotheses: the distinct-root and repeated-root branches above. Inference:
case split on the three `Nodup` tests, use the invariant and Cauchy branch in
the generic case, and the top branch otherwise. Output: `FourProp p q 3` for
all `p,q`, hence the affirmative equivalence. Formal anchor:
`source_to_target`, `target_to_source`, and `answer_true_iff`. Downstream use:
`claim_owned_four_3`. Exceptional cases: every nodup combination is explicit.
Trust boundary: final canonical compilation and exact provider transport are
Master-only gates.
