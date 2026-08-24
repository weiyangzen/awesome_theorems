# Proof outline — S5-CLM-00003528

The frozen proposition says that `True` is equivalent to summability of

\[
  n \longmapsto \frac{(2/3+(1/3)\sin n)^n}{n}, \qquad n\in\mathbb N_{>0}.
\]

The proof package separates five obligations.

1. Bind the exact provider expression and the claim-owned expression without changing the real carrier, positive-natural index, coefficients, sine argument, natural exponent, real denominator, or `Summable` predicate.
2. Close the analytic summability obligation independently of the provider's sorry-backed body. A finite partial-sum approximation is not evidence for this step.
3. Reconstruct the outer biconditional: summability supplies the `True → Summable` direction, while the converse concludes `True` directly.
4. Record source-to-target and target-to-source transport over the elaboration-identical expression. The provider import/declaration remains provenance and supplies no proof.
5. Cold-replay and audit the root, constants, dependencies, axioms, substitutions, anchors, and cut sets before canonical release.

The detailed hypotheses, inference, output, formal anchor, downstream uses, exceptional cases, and trust boundary for each obligation appear once in `full-study.md`; structured inventories remain in JSON.
