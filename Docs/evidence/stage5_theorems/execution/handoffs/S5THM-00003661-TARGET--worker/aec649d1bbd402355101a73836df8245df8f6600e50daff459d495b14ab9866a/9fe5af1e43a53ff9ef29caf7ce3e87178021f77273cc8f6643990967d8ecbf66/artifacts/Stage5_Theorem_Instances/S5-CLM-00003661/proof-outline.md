# Proof outline — three-dimensional unit contacts

The frozen extremal quantity takes the largest number of unit-distance pairs
among `n` points in three-dimensional Euclidean space whose mutual distances
are at least one.

1. Bind the inlined extremal expression to the frozen `Erdos1084.f` source
   declaration without importing or using its sorry-backed theorem.
2. Use finite fragments of the face-centred-cubic packing. A boundary count
   removes only order `n^(2/3)` possible contacts, producing a constant `c₁`
   and the eventual lower estimate.
3. Regard unit-distance pairs as tangencies of radius-one-half balls. The
   three-dimensional contact-number inequality bounds their number by
   `6 n - c₂ n^(2/3)` for an absolute positive `c₂`.
4. Increase the two thresholds to a common threshold and combine the lower
   and upper estimates with `Filter.Eventually.and`.

The finite construction, quantitative contact theorem, and root composition
are separate DAG nodes. Their exact inputs, outputs, downstream uses,
exceptional cases, formal anchors, and trust boundaries are not compressed
away; they live once in `full-study.md` and are indexed by
`readability-review.json`.
