# Full proof study — S5-CLM-00003664

<a id="H-PARAM"></a>
## H-PARAM — dimension reduction

Hypotheses: `d : ℕ` and `hd : 4 ≤ d`. Inference: set `p = d / 2`; Euclidean
division gives `2 ≤ p` and `2p ≤ d`. Output: `p` disjoint coordinate pairs are
available. Formal anchor: `half_dimension_ge_two` plus the coordinate
inclusions `2i, 2i+1 < d`. Downstream use: supplies the planes in H-LENZ.
Exceptional case: odd `d` leaves one unused coordinate. Trust boundary: only
kernel-checked natural arithmetic and finite-coordinate facts are admitted.

<a id="H-LENZ"></a>
## H-LENZ — orthogonal-circle construction

Hypotheses: `p ≥ 2`, `2p ≤ d`, and a desired finite class size for every
`i < p`. Inference: in coordinates `(2i,2i+1)`, choose distinct points on the
radius-`1/√2` circle and put zero in every other coordinate. Rational
stereographic parameters provide arbitrarily many distinct points without a
choice oracle. Output: a finite set of exactly `n` points partitioned among
`p` circles. Formal anchor: the expanded `Finset (ℝ^d)` witness in the
claim-owned root. Downstream use: H-COUNT. Exceptional cases: empty classes
and `n < p` are allowed; unused coordinates remain zero. Trust boundary:
distinctness, cardinality, and the circle equation must all replay in Lean.

<a id="H-UNIT"></a>
## H-UNIT — cross-class unit distances

Hypotheses: the partition and circle equations from H-LENZ. Inference: vectors
from different coordinate planes are orthogonal, each has squared norm `1/2`,
and hence their squared distance is one. Each unordered cross-class pair is
therefore counted by `unitDistNum`. Output: every cross-class pair is a unit
distance. Formal anchor: the distance filter predicate in `unitDistNum`.
Downstream use: H-COUNT. Exceptional case: within-circle unit pairs are
harmless because only a lower bound is needed. Trust boundary: the norm
calculation and unordered-pair normalization require explicit replay.

<a id="H-COUNT"></a>
## H-COUNT — balanced multipartite count

Hypotheses: H-UNIT and balanced sizes `a_i ∈ {q,q+1}` with `n=pq+r`.
Inference: the cross-class count is
`Σ_{i<j}a_i a_j=(n²-Σ_i a_i²)/2`; the exact square sum is
`r(q+1)²+(p-r)q²`, yielding coefficient `(p-1)/(2p)` and a bounded rounding
loss. Output: a unit-distance count at least `(p-1)/(2p)n²-C_p`. Formal
anchor: the finite complete-multipartite edge identity. Downstream use: H-SUP.
Exceptional cases: integer division, parity, and small `n` are absorbed by
`C_p`. Trust boundary: finite sums and coercions from `ℕ` to `ℝ` require
explicit replay.

<a id="H-SUP"></a>
## H-SUP — extremal transfer

Hypotheses: the constructed finset has card `n` and the H-COUNT lower bound.
Inference: specialize both indexed suprema in the definition of `Erdos1085.f`
to that finset and its cardinality proof. Output: its unit-distance count is at
most `f d n`. Formal anchor: the two `iSup` lower-bound steps after unfolding
the frozen `Erdos1085.f`. Downstream use: H-ROOT. Exceptional case: boundedness
of the natural supremum follows from the finite unordered-pair bound. Trust
boundary: the provider contributes only the frozen definition bytes, never its
theorem body.

<a id="H-ROOT"></a>
## H-ROOT — uniform constant and conclusion

Hypotheses: H-SUP for arbitrary `n` and the rounding bound depending only on
`p`. Inference: choose the single real constant `C=C_p`, subtract it from the
quadratic main term, and compose inequalities. Output: for every `n : ℕ`,
`((p-1)/(2p)) n²-C ≤ f d n`, under `p=d/2`, exactly the frozen proposition.
Formal anchor: `terminal_constant_composition` and the claim-owned root.
Downstream use: bidirectional statement transport and release decision.
Exceptional cases: one constant covers all small `n`, zero, and odd `d`.
Trust boundary: Master must confirm the exact root expression and empty axiom
set from a clean source build.
