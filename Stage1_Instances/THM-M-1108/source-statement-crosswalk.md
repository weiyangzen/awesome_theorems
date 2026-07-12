# Source-statement crosswalk

## Available record and primary-source candidate

The repository inventory supplies the Chinese title "Baik-Deift-Johansson theorem", the authors
Baik, Deift, and Johansson, the year 1999, and the gloss "distribution of the longest increasing
subsequence". Its `已验证` value is untrusted metadata under rev-5.6 and supplies neither a complete
statement nor proof evidence.

The primary-source candidate is Jinho Baik, Percy Deift, and Kurt Johansson, *On the distribution
of the length of the longest increasing subsequence of random permutations*, **Journal of the
American Mathematical Society** 12(4) (1999), 1119-1178, DOI
`10.1090/S0894-0347-99-00307-0`. This is a bibliographic discovery anchor only. The exact theorem
number/page, displayed normalization, definition of the limiting distribution, dependencies,
corrections, and errata have not yet undergone pinned-edition inspection and independent review,
so this intake does not establish `H0`.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "random permutations" | uniform law on permutations of size `N` | finite symmetric group and uniform probability measure | intended model identified; encoding open |
| "longest increasing subsequence" | maximum length of a strictly increasing subsequence | finite subsequence predicate and maximum statistic | intended statistic identified; boundary convention open |
| "distribution" | cumulative probability for a normalized random variable | event probability and real distribution function | conclusion family identified; exact inequality open |
| asymptotic regime | `N` tends to infinity | filter limit of real-valued probabilities | included; binder order open |
| fluctuation scale | centering near `2 * sqrt N` and `N^(1/6)` scaling | real coercions, powers, and normalized statistic | provisional; exact source formula open |
| Tracy-Widom limit | source-defined limiting distribution function | concrete analytic distribution or pinned equivalent characterization | family identified; definition and normalization open |
| 1999 / named authors | bibliographic locator | no machine-proof credit | candidate paper identified only |

## Human and machine boundary

The repo-local theorem search found no theorem-specific Lean artifact for `THM-M-1108`. A narrow
search of repository Lean sources found permutation APIs but no declaration named for
Baik-Deift-Johansson or longest-increasing-subsequence asymptotics. These negative observations are
not a complete mathlib or external-project anchor audit. The later anchor phase must search the
pinned dependency by underlying finite-permutation, probability-limit, Young-tableau, and
Tracy-Widom interfaces and inspect credible external Lean 4 projects at immutable revisions.

Before `H0`, an independent reviewer must verify the selected paper edition, exact theorem/page or
statement location, all definitions and hypotheses, proof boundary, and errata. Before statement
credit, every crosswalk row must map to an elaborated Lean target. No public machine-checked proof
or repo-local closure is claimed here.
