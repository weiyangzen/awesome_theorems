# Full study

## Statement and hypotheses

The theorem has no external premise before the equivalence. Its right side quantifies a real `c` with `c > 0`, then asserts an eventual property over natural `n` at `Filter.atTop`. For every natural `K`, the hypothesis is `Erdos1004.IsDistinctTotientRun n K`, i.e. injectivity of `Nat.totient` on `Set.Icc (n + 1) (n + K)`. The output is the real inequality `(K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))`.

## Inference and formal closure

The source-to-target and target-to-source theorems are identity transports: their premise and conclusion are definitionally the same fully expanded proposition. Because the canonical Lean project lacks the FormalConjectures package, the replay surface expands `answer(True)` to `True` and the frozen source predicate to its `Set.Icc`/`Nat.totient` body under Mathlib. Audit elaboration repeats that expression independently. There is no claim-local definition or parser feature capable of changing `True`, `ℝ`, `ℕ`, `atTop`, `Set.Icc`, `Nat.totient`, `Real.exp`, `Real.log`, division, order, coercion, or exponentiation.

## Outputs and downstream use

The output is an unconditional `answer(True) ↔` characterization of the eventual bound. The statement node supplies the exact semantic crosswalk; the transport node supplies bidirectionality; the root node supplies machine closure; the audit node supplies replay evidence. All four nodes feed the provisional release decision and the later canonical-Master recomputation.

## Exceptional cases

No finite initial segment of `n` is claimed because the result uses `∀ᶠ n in atTop`. The universal quantifier retains `K = 0`; it is not silently dropped. Positivity of `c` is retained. Natural-to-real coercions are explicit at both `K` and `n`. The exponent is the real number `1/3`, not natural division. These cases and types are part of the exact imported expression.

## Trust boundary

The provider source is pinned at revision `2270d31e8dd611521f979de6d86da364930b7669`, file digest `a2519433ac453ebb6ea68da1de1f10ff04f0d3aae5cc68cc039c09eec5803bf7`, and declaration/type digests from the frozen member. Its body contains `sorryAx`, so it is statement authority and not silently promoted local proof authority. The target contributes no new oracle; its machine declarations are conditional transports. Worker validation is provisional; canonical Master must independently recompute all semantic hashes, review the import/provider boundary, and alone set acceptance.
