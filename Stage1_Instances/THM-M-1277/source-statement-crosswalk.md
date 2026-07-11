# Source-statement crosswalk

Primary discovery source: J. Moser, "A sharp form of an inequality by N.
Trudinger", *Indiana University Mathematics Journal* **20** (1971),
1077-1092, DOI `10.1512/iumj.1971.20.20101`. The article's Theorem 1 gives the
dimension-`n` bounded-domain zero-boundary Sobolev inequality and identifies
the sharp threshold; specializing `n = 2` yields `4*pi`.

| Claim component | Primary-source anchor | Intended Lean surface | Intake assessment |
|---|---|---|---|
| Bounded domain and zero boundary values | Moser (1971), Theorem 1 hypotheses | bounded open set in Euclidean space; `W_0^{1,2}` membership | Semantic match located; exact definitions unelaborated |
| Gradient normalization | Moser (1971), Theorem 1 normalization | integral of squared weak-gradient norm at most one | Norm/integral transport remains open |
| Endpoint exponential bound | Moser (1971), Theorem 1, specialized to dimension two | uniform finite bound for `exp (4*pi*u^2)` | Canonical root component; no Lean declaration selected |
| Optimality | Moser (1971), sharpness clause following the threshold in Theorem 1 | supremum infinite for every `alpha > 4*pi` | Canonical root component; quantifier encoding remains open |
| Historical antecedent | N. S. Trudinger, "On imbeddings into Orlicz spaces and some applications", *Journal of Mathematics and Mechanics* **17** (1967), 473-483 | source genealogy only | Not a substitute for Moser's sharp endpoint |

The source file, edition pagination, assumptions, and any errata have not yet
received immutable hashes or independent review, so this is `H1`, not `H0`.
The informal repository phrase "two-dimensional critical embedding" is too
weak to determine the endpoint, boundary condition, normalization, or
sharpness by itself; the crosswalk above freezes those choices rather than
silently broadening that phrase.

No public Lean candidate has been audited in this phase. In particular, no
similarly named theorem may receive proof credit until its complete type,
revision, imports, terminal body, axioms, and exact relationship to both the
endpoint and sharpness clauses are checked.

