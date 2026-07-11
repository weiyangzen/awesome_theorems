# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Subadditive process over a measure-preserving transformation | J. F. C. Kingman, "The Ergodic Theory of Subadditive Stochastic Processes", *Journal of the Royal Statistical Society, Series B* 30(3), 1968, 499-510 | `KingmanProcess.subadditive_cocycle` | Primary paper identified; theorem/page premise mapping and errata review remain open (`H1`) |
| Integrability and lower expectation control | Same paper; exact numbered hypothesis requires source audit | `process_integrable`, `lowerBoundedExpectedAverages` | Plausible modern specialization, not yet source-certified |
| Almost-everywhere normalized limit | Same paper's main subadditive ergodic result | first conjunct of `KingmanConclusion` | Candidate uses an input `limit`; existential/selected-limit equivalence is unchecked |
| Ergodic constant and expectation infimum | Ergodic specialization of the main result | `ergodicKingmanValue`; final conjunct of `KingmanConclusion` | Positive-index set is explicit, but finiteness and exact equality hypotheses need audit |
| Invariance of the limit | Standard intermediate conclusion in the ergodic argument | middle conjunct of `KingmanConclusion` | Candidate only; no checked derivation or source-node crosswalk |

Discovery links, not immutable evidence receipts:

- DOI: <https://doi.org/10.1111/j.2517-6161.1968.tb00749.x>
- Legacy repo candidate: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_249.lean`

No `H0` or machine-closure claim is made. The source audit must obtain an immutable copy,
verify bibliographic pagination and theorem numbering, map every premise and conclusion,
check corrections/errata, and receive independent review. The statement phase must then
elaborate the root, fingerprint its environment, check transports, and mutation-test the
domain, binder order, lower-bound hypothesis, cocycle inequality, and `n = 0` boundary.
