# Source-statement crosswalk

| Claim component | Repository source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Name | `Docs/researches/math_theorems.md`: `志村五重积恒等式` | none | A label is not an exact proposition |
| Attribution and date | same record: Goro Shimura, 1979 | none | No title, journal, theorem, or page is supplied; attribution is unverified |
| Subject | same record: `模形式的恒等式` (identity of modular forms) | possible modular-form and q-expansion APIs only | Too broad to determine objects, parameters, or equality |
| Formal status | same record: `已验证`; manifest stores it as `source_status_untrusted` | none | Explicitly untrusted metadata; it is not kernel or source evidence |
| Product formula | absent | none | Number and identity of factors, indices, exponents, and normalization are unknown |
| Hypotheses and conclusion | absent | none | No binder, domain, modularity condition, convergence condition, or exact equality can be crosswalked |

Repository-wide text search locates no formula, primary citation, or Lean artifact for this theorem.
The Stage0 blueprint repeats the same short metadata and marks all exact-definition, dependency,
foundation, and artifact fields as pending. Consequently no human-source assurance beyond `H4` is
claimed, and there is no source-faithful Lean candidate to elaborate.

The source audit must locate a primary 1979 Shimura publication (or correct the metadata through the
authoritative process), pin an immutable edition, record exact theorem/page and errata, and map each
symbol and assumption to the intended root. Search results for a similarly named identity are
discovery leads only; they cannot resolve attribution or theorem identity by name matching.
