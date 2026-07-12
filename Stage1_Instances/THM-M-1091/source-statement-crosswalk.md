# Source-statement crosswalk

## Available source record

The immediate repository source is `Docs/researches/math_theorems.md`. It gives the title
"Chapman-Kolmogorov equation", attribution to Sydney Chapman and Andrey Kolmogorov, year 1931,
and the gloss "semigroup property of transition probabilities". `Docs/Stage0_Blueprint.md`
repeats the gloss and says that the definitions, premises, proof path, and artifacts remain to be
supplied. Neither file provides a formula, bibliographic title, theorem number, page, edition, or
proof. Its `已验证` label is explicitly untrusted under rev-5.6.

Pinned mathlib's candidate documentation cites *Meyn-Tweedie*, Theorem 3.4.2, page 68 for its
kernel-power form. That is a useful source lead, but this intake did not establish the edition,
inspect the cited page, map its assumptions, or search errata. It therefore does not establish
`H0`.

## Crosswalk

| Source component | Conventional mathematical reading | Lean component needed | Intake assessment |
|---|---|---|---|
| `transition probabilities` | Kernels `P(s,t)(x,dy)` describing movement between times | measurable spaces, `Kernel`, and normally `IsMarkovKernel` | object family identified; normalization and indexing open |
| `semigroup property` | Direct transition equals composition through an intermediate time | kernel equality with fixed composition orientation | claim shape identified; homogeneous versus inhomogeneous scope open |
| Equation form | `P(s,u)(x,A) = integral P(t,u)(y,A) dP(s,t)(x,dy)` | `Kernel.comp_apply'`-style setwise equality for measurable `A` | conventional expansion; not quoted from an audited repository source |
| Mathlib `Kernel.pow_add` | `K^(m+n) = K^m` composed with `K^n` | exact pinned declaration in `Composition.Comp` | close discrete homogeneous candidate, not yet the accepted root |
| Mathlib integral theorem | setwise integral expansion of the power identity | `Kernel.pow_add_apply_eq_lintegral` | close candidate; exact declaration availability checked only |
| Chapman/Kolmogorov, 1931 | historical attribution | immutable primary publications and historical claim mapping | not independently audited |

## Neighboring claims that are not automatically the root

| Neighbor | Relationship | Boundary |
|---|---|---|
| Markov property | Usually supplies conditional laws whose consistency yields Chapman-Kolmogorov | separately owned by `THM-M-1090`; no implication is credited without a process model |
| Kernel composition associativity | Algebraic infrastructure for composing several transitions | does not show an independently specified transition family equals that composition |
| Matrix powers for a finite Markov chain | Countable/finite-state specialization | cannot replace the measurable-space theorem silently |
| Continuous-time transition semigroup | Homogeneous real-time specialization | requires a time monoid and a kernel-valued semigroup not selected by the source record |
| Kolmogorov forward/backward equations | Differential evolution equations for transitions | stronger analytic statements with generator and differentiability hypotheses |

## Source gate

No `H0` claim is made. Statement acceptance requires an independent reviewer to pin and inspect an
authoritative edition, give an exact theorem/page and definition crosswalk, map every premise, and
record an errata search. The review must specifically resolve the gap between the repository's
unqualified transition-probability family and mathlib's single-kernel natural-power theorem.
