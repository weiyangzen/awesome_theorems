# Source-statement crosswalk

## Candidate sources

- L. C. Evans, *Partial Differential Equations*, 2nd ed., AMS Graduate Studies in Mathematics 19
  (2010), section 5.6.3, Theorem 6 (Morrey's inequality). This is the principal modern statement
  candidate. The exact page, displayed formula, all local hypotheses, and errata have not yet been
  inspected from an immutable copy.
- C. B. Morrey Jr., "Functions of several variables and absolute continuity, II", *Duke
  Mathematical Journal* 6 (1940). This is a historical primary-source candidate; exact theorem and
  page mapping remain open.

These are discovery anchors, not `H0` evidence.

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Sobolev functions" | first-order `W^{1,p}` object | weak derivative, integrability, and AE quotient APIs | included; encoding open |
| "Holder continuity" | representative with exponent `1 - n/p` | representative agreement plus `HolderOnWith` or exact equivalent | included; transport unchecked |
| `p > n` | positive supercritical exponent gap | typed dimension/exponent comparison and positivity proof | mandatory; representation open |
| Morrey estimate | pointwise/Holder bound controlled by gradient or Sobolev norm | concrete inequality with explicit constant dependencies | mandatory; normalization open |
| bounded domain | extension/restriction route to the closure | domain regularity and extension operator APIs | candidate root boundary; source decision open |

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_175.lean` mentions a bounded-domain Morrey
embedding but explicitly describes the required domain/extension and Holder packages as missing.
It is therefore a search lead only, not a source match or terminal proof. The anchor-audit phase
must inspect its exact declarations at the pinned revision and search current mathlib independently.

Before `H0`, an independent reviewer must verify an immutable source edition, theorem/page/formula,
all assumptions, endpoint and boundary cases, constant and norm conventions, and known errata, then
approve a row-by-row source-to-Lean mapping.

