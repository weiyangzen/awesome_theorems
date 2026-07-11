# Source-statement crosswalk

## Repository source

| Repository field | Recorded value | Intake interpretation |
|---|---|---|
| Name | `KMT定理` | The Komlos-Major-Tusnady theorem family |
| Statement | `随机游走向布朗运动的强逼近` | Strong approximation of a random walk by Brownian motion; no formula or assumptions supplied |
| Authors/year | Komlos / Major / Tusnady, 1975 | Bibliographic discovery data, not an accepted pinpoint citation |
| Status | `已验证` | Untrusted metadata; no human-proof or machine-proof credit |

## Primary-source candidates

| Claim component | Primary source candidate | Mapping at intake |
|---|---|---|
| Strong approximation of partial sums | J. Komlos, P. Major, G. Tusnady, *An approximation of partial sums of independent RV's, and the sample DF. I*, Zeitschrift fur Wahrscheinlichkeitstheorie und Verwandte Gebiete 32 (1975), 111-131, DOI `10.1007/BF00533093` | Title, authors, year, volume, and pages identify the leading original source. Exact theorem number, hypotheses, constants, and scanned-edition hash still require audit. |
| Continuation and variants | J. Komlos, P. Major, G. Tusnady, *An approximation of partial sums of independent RV's, and the sample DF. II*, Zeitschrift fur Wahrscheinlichkeitstheorie und Verwandte Gebiete 34 (1976), 33-58 | A primary continuation candidate. Its exact relationship to the chosen root and its immutable identifier remain open. |
| Repository phrase "random walk" | Partial sums `S_k = X_1 + ... + X_k` of centered normalized independent increments | This is the intended object-level reading, but the source must determine i.i.d. versus non-identical assumptions and normalization. |
| "Brownian motion" | A standard Wiener process `W`, jointly constructed with copies of the increments | The eventual statement must distinguish construction on a new space from coupling pre-existing variables and must specify marginals. |
| "strong approximation" | A uniform-in-`k <= n` discrepancy bound of logarithmic order, commonly accompanied by an exponential deviation estimate | The almost-sure asymptotic consequence and quantitative tail theorem are related but not interchangeable roots until the source pins the direction and constants. |

Discovery links, not immutable evidence receipts:

- Original paper I: <https://doi.org/10.1007/BF00533093>
- Springer bibliographic record: <https://link.springer.com/article/10.1007/BF00533093>

## Statement decisions still open

The statement phase must resolve all of the following before setting an expression hash:

1. Select paper I or II and an exact theorem/page from a content-addressed edition.
2. Transcribe the precise exponential-moment assumption and normalization.
3. Record whether the quantified input is a distribution, an existing sequence, or newly coupled copies.
4. Freeze independence, equality-in-law, Brownian covariance, filtration, and probability-space binders.
5. Freeze the exact maximum, time range, logarithm convention, constants, deviation parameter, and probability inequality.
6. Decide whether the root is the quantitative tail theorem or only its almost-sure asymptotic consequence, then check the transport direction.
7. Audit corrections/errata and obtain independent review of the source-to-statement mapping.

No `H0` claim is made. No Lean declaration has been located or credited in this intake. The current
crosswalk supports `[H1, M3, R3]` only and must not be read as theorem completion.
