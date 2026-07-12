# Scope map

| Surface | Preserved scope | Open boundary |
|---|---|---|
| Family | Stable laws as the possible nondegenerate limits of normalized iid sums | biconditional root selected |
| Random objects | Borel probability laws on `Real` | iid sums encoded as convolution powers |
| Normalization | `(x - b_n) / a_n` with `a_n > 0` | frozen in `normalizedLaw` |
| Convergence | weak convergence of laws | bounded-continuous real test functions |
| Limit | nondegenerate stable probability law | stability defined by every convolution power `n >= 2` |
| Attraction | laws whose normalized convolution powers converge to a stable law | analytic tail/regular-variation criterion excluded from this root |

Degenerate point-mass limits, the ordinary Gaussian CLT alone, triangular-array CLTs, and statements
that merely assume stability are excluded. Boundary probes must cover zero/nonpositive scaling,
degenerate limits, Gaussian `alpha = 2`, asymmetric stable laws, and centering conventions.

`Statement.lean` freezes every binder and side condition and checks an expanded definitional
transport. Exact primary-source pinpointing remains an H-axis task for the anchor/source audit. The
scope seeds likely proof surfaces: convolution powers, normalization transport,
tightness/subsequence reasoning, stability of limit laws, and the converse construction. They are
not yet accepted obligations.
