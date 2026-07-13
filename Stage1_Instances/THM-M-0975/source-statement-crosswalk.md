# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:7120-7125` and `:7287-7292` contain identical uncited records:

- title: `Azuma-Hoeffding不等式`;
- attribution: Kazuoki Azuma / Wassily Hoeffding;
- year: 1967;
- gloss: `鞅差序列的集中` ("concentration of martingale difference sequences");
- importance: high;
- untrusted status: `已验证`.

Git history attributes all twelve lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Neither record contains a formula, definition,
ordered binders, hypotheses, conclusion, theorem locator, proof boundary, errata, reviewer, or
formal artifact. `Docs/Stage0_Blueprint.md:26578-26603` repeats the gloss while explicitly leaving
the exact premises, proof route, dependencies, alternate forms, axioms, and machine state open.

The same catalog also gives `THM-M-1080`, Azuma's inequality, the identical gloss at
`Docs/researches/math_theorems.md:7912-7917`. Rev-5.6 keeps the IDs distinct: `THM-M-1080` is rank
522 in the stochastic-process category and `THM-M-0975` is rank 1509 in counting combinatorics.
This duplication is a source-identity blocker, not permission to share target state.

## Inspected primary source lead

Kazuoki Azuma, "Weighted sums of certain dependent random variables," *Tohoku Mathematical
Journal*, Second Series 19(3) (1967), 357-367, DOI `10.2748/tmj/1178243286`, was inspected through
the J-STAGE journal scan on 2026-07-13. The observed 11-page PDF is 537,047 bytes with SHA-256
`cf45e97090958a8d4ab5dae3364cc064bfc6c4611d057bc55f078e68f79464d9`.

- Printed page 357 defines bounded martingale differences by almost-sure boundedness and zero
  conditional expectation, then records properties `[G]` and `[M]`.
- `[G]` is the conditional MGF inequality
  `E[exp(t x_n) | A_(n-1)] <= exp(c_n^2 t^2 / 2)` almost surely.
- `[M]` combines `|x_n| <= K_n` almost surely with vanishing expectations of increasing-index
  products.
- Lemma 1, printed pages 357-358, proves
  `E exp(t * sum_{k=1}^n b_(n,k) x_k) <= exp((t^2/2) * sum b_(n,k)^2)` under `[M]` with `K_n = 1`.
- Remark 1, printed page 358, derives `[G]` with parameter at most `K_n` from bounded martingale
  differences.
- Lemma 2 and Theorems 1-3 concern maximal exponential moments and asymptotic behavior of weighted
  sums; none is presented verbatim as the familiar finite-horizon tail theorem named by the modern
  catalog.

The journal article strongly anchors Azuma's contribution, but intake has not accepted which
historical result or modern corollary the catalog intends, completed the Hoeffding genealogy,
audited every definition and proof boundary, certified corrections or errata, or obtained an
independent review. It supports H1, not H0. The PDF remains outside the repository and its observed
digest is discovery evidence, not a durable source receipt.

## Clause crosswalk

| Catalog/source component | Azuma 1967 lead | Pinned Lean candidate | Intake state |
|---|---|---|---|
| martingale differences | bounded, conditionally mean-zero `x_n` | strongly adapted process plus conditional sub-Gaussian hypotheses | family aligned; exact premise transport open |
| concentration | MGF and asymptotic weighted-sum results | finite one-sided sum-tail probability bound | exact root open |
| bounds | `K_n`, `[G]` parameter `c_n`, and weights `b_(n,k)` | NNReal variance proxies `cY i` | normalization and squaring map open |
| horizon/indexing | infinite sequence with finite partial sums and asymptotics | `Finset.range n`, separate initial term | binder and boundary mapping open |
| exponent | MGF exponent `(t^2/2) * sum b^2` | tail exponent `-epsilon^2/(2 * sum cY)` | Chernoff relationship expected but unchecked |
| Hoeffding attribution | not an author of the inspected paper | bounded-variable Hoeffding lemma exists nearby | historical and mathematical crosswalk open |
| `已验证` | no such source claim | pinned theorem name alone is not root identity | no H0/M0 credit |

## Formal candidate boundary

The intake probe elaborates the following pinned declarations:

| Declaration | Role | Unclosed gate |
|---|---|---|
| `ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF` | exact-topic finite-sum upper-tail candidate | canonical source root, bounded-difference bridge, exact type match, provenance and trust audit |
| `ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF` | conditional MGF aggregation | cannot replace the selected tail theorem without checked composition |
| `ProbabilityTheory.HasCondSubgaussianMGF` | conditional sub-Gaussian premise | source-to-definition equivalence and parameter normalization open |
| `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero` | ordinary bounded centered Hoeffding lemma | conditional version and filtration bridge not inferred |

The repo-local declaration
`AwesomeTheorems.Stage1.S1_M_276.azuma_hoeffding_tail_bound` wraps the same mathlib tail theorem for
a different legacy target and stronger premise package. It is discovery input only, is not owned by
this target, and supplies no rev-5.6 proof credit.

Before H0, an independent reviewer must admit an immutable source edition and approve the exact
root, incorporated definitions, assumptions, normalization, proof boundary, attribution, and
errata. Before statement acceptance, Lean work must freeze minimal imports and an elaborated
expression, check every alternate encoding, and mutation-test hypotheses, domains, binder scope,
direction, constants, and boundary cases.
