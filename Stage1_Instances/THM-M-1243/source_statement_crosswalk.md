# Source-statement crosswalk

| Claim component | Source anchor | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Euclidean Nash inequality | John Nash, “Continuity of solutions of parabolic and elliptic equations,” *American Journal of Mathematics* 80(4) (1958), 931-954 | A theorem over Euclidean space, Lebesgue measure, `L1`/`L2` norms, and gradient energy | Primary paper identified; exact page/equation, hypotheses, and errata require audit: `H1` |
| L2/L1/gradient exponent relation | Same paper, subject to inspection of an immutable scan | Real-power or nonnegative-real norm expression | Exact exponent and constant placement deliberately not frozen at intake |
| Smooth compact-support version | Classical dense test-function presentation | `ContDiff` plus `HasCompactSupport`, or a bundled test-function API | Candidate domain only; no source equivalence or Lean elaboration checked |
| Sobolev extension | Standard completion/density consequence, source not yet pinned | `MemLp` plus weak-gradient/Sobolev API | Separate bridge obligation; cannot be silently folded into the historical statement |
| “Entropy and energy” wording | `Docs/Stage0_Blueprint.md` metadata | None | Insufficient to distinguish classical Nash interpolation from Nash entropy-family results |

The intended target is bounded to the classical Euclidean Nash interpolation family, rather than
its manifold, graph, discrete, semigroup, sharp-constant, or entropy-power generalizations. That
bound is a scope decision, not an assertion that one normalization has been sourced. The statement
phase must obtain an immutable copy of the primary paper, record the exact equation/page and all
assumptions, check corrections, select one faithful normalization, elaborate it in Lean, and prove
any norm/integral or smooth/Sobolev transports.

Discovery link (not an immutable evidence receipt):
<https://www.jstor.org/stable/2372841> (DOI `10.2307/2372841`).

No `H0` or machine-closure claim is made.
