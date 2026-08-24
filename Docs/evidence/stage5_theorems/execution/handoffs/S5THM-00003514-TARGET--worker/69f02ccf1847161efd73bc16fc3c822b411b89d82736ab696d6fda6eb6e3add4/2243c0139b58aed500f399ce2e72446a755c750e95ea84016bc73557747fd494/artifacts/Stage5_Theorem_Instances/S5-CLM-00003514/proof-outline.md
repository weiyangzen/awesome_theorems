# Proof outline

Let the roots of a monic real-rooted polynomial be `λᵢ`.  On the simple-root
branch, its score at `λᵢ` is

`sᵢ = ∑_{j ≠ i} (λᵢ - λⱼ)⁻¹`,

and the provider's `Φ` is the squared norm `∑ᵢ sᵢ²`.  For finite free additive
convolution, the score of the output is a conditional projection of a weighted
combination of the two input scores.  Conditional expectation contracts the
squared norm, so for every `0 ≤ a ≤ 1`,

`Φ(p ⊞ₙ q) ≤ a² Φ(p) + (1-a)² Φ(q)`.

Minimizing the right side and then applying order-reversing inversion gives

`1 / Φ(p) + 1 / Φ(q) ≤ 1 / Φ(p ⊞ₙ q)`.

The repeated-root branch is encoded by `Φ = ⊤`, whose reciprocal is zero; zero
and top denominators are split before any cancellation.  Reintroducing the six
`FourProp` hypotheses and the universal quantifiers yields the proposition
inside the frozen `answer(True)` equivalence.  The exact formal semantic
transport remains a Master obligation; the worker does not use the provider's
sorry-backed proof body.
