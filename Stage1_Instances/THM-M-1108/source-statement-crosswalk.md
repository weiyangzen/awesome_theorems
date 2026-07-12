# Source-statement crosswalk

## Available record and selected primary statement

The repository inventory supplies the Chinese title "Baik-Deift-Johansson theorem", the authors
Baik, Deift, and Johansson, the year 1999, and the gloss "distribution of the longest increasing
subsequence". Its `已验证` value is untrusted metadata under rev-5.6 and supplies neither a complete
statement nor proof evidence.

The selected primary source is Jinho Baik, Percy Deift, and Kurt Johansson, *On the distribution
of the length of the longest increasing subsequence of random permutations*, **Journal of the
American Mathematical Society** 12(4) (1999), 1119-1178, DOI
`10.1090/S0894-0347-99-00307-0`. Statement inspection used arXiv:math/9810105v2 (1999-03-26),
SHA-256 `0a432946234949c12a3e379e42d8f79fa646b9002810ffe97817d52aca184a7a`, Theorem 1.1 on PDF
pages 2--3 together with definitions (1.4)--(1.6). Independent review and errata review remain
open, so this statement evidence does not establish `H0`.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "random permutations" | uniform law on permutations of size `N` | `Equiv.Perm (Fin N)` and event-cardinality ratio | frozen and elaborated |
| "longest increasing subsequence" | maximum length of a strictly increasing subsequence | `lisLength`, supremum over finite index sets | frozen and elaborated |
| "distribution" | cumulative probability for a normalized random variable | `normalizedLISCDF`; inequality `<= t` | frozen and elaborated |
| asymptotic regime | `N` tends to infinity | `Tendsto ... atTop` | frozen and elaborated |
| fluctuation scale | centering `2 * sqrt N` and `N^(1/6)` scaling | real coercions, `Real.sqrt`, real power notation | frozen and elaborated |
| Tracy-Widom limit | equations (1.4)--(1.6) | `IsAiryAi` and `IsTracyWidomCDF` | frozen and elaborated |
| 1999 / named authors | bibliographic locator | no machine-proof credit | candidate paper identified only |

## Human and machine boundary

The repo-local theorem search found no theorem-specific Lean artifact for `THM-M-1108`. A narrow
search of repository Lean sources found permutation APIs but no declaration named for
Baik-Deift-Johansson or longest-increasing-subsequence asymptotics. These negative observations are
not a complete mathlib or external-project anchor audit. The later anchor phase must search the
pinned dependency by underlying finite-permutation, probability-limit, Young-tableau, and
Tracy-Widom interfaces and inspect credible external Lean 4 projects at immutable revisions.

Before `H0`, an independent reviewer must verify the selected paper edition, exact theorem/page or
statement location, all definitions and hypotheses, proof boundary, and errata. Every mathematical
row now maps to the elaborated target. No machine-checked proof of the target or repo-local theorem
closure is claimed here.
