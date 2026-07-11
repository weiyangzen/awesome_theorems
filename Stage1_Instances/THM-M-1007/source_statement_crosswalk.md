# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Independent real random variables and almost-sure convergence of their series | A. N. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung* (1933), English translation *Foundations of the Theory of Probability*, 2nd ed., Chelsea, 1956, Chapter VI, section 4, theorem on convergence of series of independent random variables | A new `Stage1.THM_M_1007.StatementShape` over mathlib probability spaces | Classical primary monograph located; exact scan/page, translation alignment, and errata audit remain open, hence `H1` |
| Large-jump condition | Finiteness of `sum_n P(|X_n| > c)` in the three-series theorem | `Summable (fun n => P {omega | c < abs (X n omega)})` after a coercion to `ENNReal`/`Real` is fixed | Measure codomain and strict cutoff are normalization risks |
| Truncated-mean condition | Convergence of `sum_n E[X_n 1_{|X_n| <= c}]` | Bochner integral of the truncated real random variable followed by `Summable` | Integrability follows from bounded truncation only after measurability is established; no bridge checked |
| Truncated-variance condition | Finiteness of `sum_n Var(X_n 1_{|X_n| <= c})` | mathlib variance/covariance API or an explicit second centered moment | Exact API and finiteness conventions are not frozen |
| Biconditional | The preceding three conditions are necessary and sufficient for almost-sure convergence | `AE` convergence of partial sums iff the conjunction of three series predicates | The root is explicitly an iff; neither implication may replace it |

The repository's legacy summary, "conditions for convergence of a series of independent random
variables," is too broad to be a formal statement. This crosswalk selects the standard real-valued,
fixed-positive-cutoff biconditional. It does not silently generalize to Banach-valued variables or
weaken mutual independence to pairwise independence.

The statement phase must resolve four material choices before elaboration: mathlib's independent
family predicate, the probability-series codomain, variance for truncated variables, and whether
series convergence is expressed by `Summable` or convergence of partial sums. It must also check
the `<` versus `<=` cutoff transport; atoms at `|X_n| = c` make this more than syntactic rewriting.

Discovery links (not immutable evidence receipts):

- Kolmogorov book record: <https://archive.org/details/foundationsofthe00kolm>
- Springer encyclopedia overview: <https://encyclopediaofmath.org/wiki/Three-series_theorem>

No `H0` or machine-closure claim is made. Required source follow-up includes a page-level scan hash,
edition/translation comparison, assumptions-to-node mapping, correction/errata search, and
independent review.
