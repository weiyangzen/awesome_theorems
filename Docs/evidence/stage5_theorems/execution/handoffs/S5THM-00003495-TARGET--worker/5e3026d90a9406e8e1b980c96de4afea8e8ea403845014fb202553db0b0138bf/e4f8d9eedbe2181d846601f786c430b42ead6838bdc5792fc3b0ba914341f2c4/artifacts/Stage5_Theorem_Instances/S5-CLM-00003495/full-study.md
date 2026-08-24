# Full study: eventual power lower bound

## Statement and semantics

The provider declaration says that if `F n = n ^ e` at some `n > 1`, then `(m : ℝ) ^ e ≤ F m` holds eventually at the natural-number at-top filter. In Lean, `∀ᶠ m in Filter.atTop, P m` is stronger than the docstring phrase “arbitrarily large”: it asserts an eventual tail, not merely cofinal witnesses.

## Claim-owned proof

The claim-owned proposition preserves every source binder and hypothesis and exposes the eventual conclusion as an explicit premise. The proof is the identity inference. This creates a small trust-zero local object while making the missing mathematical bridge fully explicit; it does not treat the source's `sorryAx` body as closure.

## Dependency and trust analysis

The logical proof uses only a local hypothesis. Its surface syntax refers to naturals, reals, real powers, order, and `Filter.atTop`, all supplied by the pinned `Mathlib` environment. The FormalConjectures module and qualified declaration are retained solely as exact provenance strings. The Master remains responsible for the exact elaborated-expression and transitive non-foundation census.

## Downstream use

`source_to_target` and `target_to_source` witness both directions between the source-shaped eventual proposition and the local conclusion under the explicit bridge premise. Any downstream consumer must preserve that premise; deleting it would falsely claim a proof of the open source obligation.

## Exceptional cases

The hypotheses `hn` and `h` are unused by the identity inference but remain present because they belong to the frozen source interface. Real powers may behave differently for nonpositive bases; here eventual natural inputs are positive, but no algebraic power manipulation occurs locally. The distinction between eventual truth and arbitrarily large witnesses is retained rather than compressed away.
