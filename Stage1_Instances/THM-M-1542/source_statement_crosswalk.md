# Source-statement crosswalk

| Claim component | Human source anchor | Lean target status | Intake assessment |
|---|---|---|---|
| Self-dual Yang-Mills solutions have a twistor description | R. S. Ward, *On self-dual gauge fields*, Physics Letters A 61 (1977), 81-82, DOI `10.1016/0375-9601(77)90842-8` | No declaration selected | Primary historical anchor identified, but its exact hypotheses, conventions, and corrections have not received a pinned text audit: no `H0` |
| Gauge field equation | Historical literature varies between self-dual and anti-self-dual sign/orientation conventions | Future curvature predicate | The generated phrase "self-dual Yang-Mills" cannot determine the sign of `*F`; orientation and Hodge-star conventions must be frozen |
| Holomorphic twistor object | Ward's construction associates gauge fields with holomorphic bundle data over twistor space | Future bundled structure | Twistor-space model, rank/structure group, reality condition, and line-triviality predicate remain unformalized |
| Forward transformation | Integrability of the lifted distribution yields holomorphic data | Future map on quotient objects | Construction, regularity, and invariance under gauge transformations remain open |
| Inverse transformation | Triviality along twistor lines permits reconstruction of a gauge field | Future inverse map | Existence and uniqueness depend on the exact category and analytic hypotheses |
| Full correspondence | Forward and inverse constructions agree modulo the selected equivalences | Future equivalence/bijection theorem | This is the intended root, but neither domain nor codomain is exact enough to elaborate at intake |

The repository's legacy summary, "twistors and self-dual Yang-Mills," is a topic-level description.
It does not say whether the target is local or global, Euclidean or complex, framed or unframed,
smooth or analytic, on `R^4`, `S^4`, or another anti-self-dual four-manifold. Those choices change
both hypotheses and conclusion. Selecting one without a source audit would substitute a narrower
theorem, so intake deliberately records `M4` rather than inventing a Lean statement.

Discovery references, not immutable evidence receipts:

- Ward 1977 DOI: <https://doi.org/10.1016/0375-9601(77)90842-8>
- M. F. Atiyah, N. J. Hitchin, and I. M. Singer, *Self-duality in four-dimensional Riemannian geometry*, Proceedings of the Royal Society A 362 (1978), 425-461, DOI `10.1098/rspa.1978.0143` (geometric context and conventions; not by itself a substitute root statement).

The statement phase must obtain immutable copies or hashes, pinpoint the theorem/prose formulation
and assumptions, inspect errata and later corrections, choose one non-broadened variant, and map
every hypothesis to the normalized Lean expression. Independent source review remains required.
