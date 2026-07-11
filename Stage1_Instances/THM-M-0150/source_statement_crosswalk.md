# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Finite generation of the canonical ring for a smooth projective variety of general type over `C` | C. Birkar, P. Cascini, C. D. Hacon, J. McKernan, *Existence of minimal models for varieties of log general type*, JAMS 23 (2010), Corollary 1.1.2 | No declaration identified | Primary theorem pinpoint located; edition/hash, assumptions, and errata review remain open: `H1` |
| Canonical ring `R(X,K_X)` | Same source, Corollary 1.1.2, expressed as the log canonical ring with boundary specialized to zero | Future definition from varieties, canonical divisor/sheaf, global sections, graded direct sum | No Lean expression has been elaborated: `M4` |
| Smooth, projective, general type, characteristic zero | Repository gloss plus the standard specialization of BCHM | Future predicates/structures | Binder order, implicit hypotheses, and exact field assumptions must be frozen in the statement phase |
| Attribution "Hacon-McKernan theorem" and date 2006 | Repository metadata only | none | Not accepted as a precise bibliographic claim; the published primary source has four authors and appeared in 2010 |
| Canonical-model formulation | Standard consequence via `Proj` of the canonical ring | Future transport candidate | Out of root scope unless an exact checked implication/equivalence is supplied |

The source theorem is more general than the frozen root: it concerns log canonical rings/minimal
models under characteristic-zero hypotheses. Later work must verify the `Delta = 0` specialization
and must not claim that a proof of a broader but differently conditioned statement automatically
closes the root.

Primary discovery reference (not an immutable evidence receipt):

- DOI: <https://doi.org/10.1090/S0894-0347-09-00649-3>
- Bibliographic citation: J. Amer. Math. Soc. 23 (2010), no. 2, 405-468.

No `H0` or machine-checked claim is made. Required follow-up: obtain and hash the primary source,
audit Corollary 1.1.2 and its hypotheses/errata, identify feasible Lean primitives, serialize the
normalized target, and mutation-test every domain and hypothesis.
