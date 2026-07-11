# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Meromorphic continuation of general Artin L-series | Richard Brauer, "On Artin's L-series with general group characters," *Annals of Mathematics* 48 (1947), 502-514 | Future exact root; legacy `StatementShape` is discovery input | Primary theorem source identified, but edition hash, pinpoint theorem text, assumptions, and errata are not yet audited: `H1` |
| Artin L-series and Euler factors | Emil Artin, "Uber eine neue Art von L-Reihen," *Abhandlungen aus dem Mathematischen Seminar der Universitat Hamburg* 3 (1923), 89-108 | Future concrete Artin local-factor definition using Frobenius on inertia invariants | Genealogical primary source identified; convention-by-convention crosswalk remains open |
| Integral character decomposition by induced linear characters | Brauer 1947, the character-theoretic reduction used for general group characters | Mathlib representation/induction APIs plus an as-yet-unidentified exact Brauer-induction theorem | Required proof bridge, not evidence of root closure |
| Continuation of one-dimensional factors | Brauer's reduction to abelian/Hecke L-series, with the exact cited analytic input to be pinned during source audit | Dirichlet continuation and Dedekind-zeta APIs in the legacy module are only nearby anchors | Number-field Hecke-character scope is broader than Dirichlet characters over the rationals; no substitution is allowed |
| Product and quotient preserve meromorphicity | Standard complex-analytic consequence after the integral character identity | `Meromorphic.mul` and `Meromorphic.div` candidates | Local analytic operation only; does not supply the arithmetic factorization |

The title "Brauer theorem" is ambiguous in isolation. The manifest context fixes this target to
Brauer's meromorphic-continuation theorem for Artin L-functions, not Brauer's fixed-point theorem,
Brauer's induction theorem by itself, or Artin holomorphy. The statement phase must freeze the exact
extension data, representation equivalence conventions, ramified local factors, Euler-product
domain, meaning of global meromorphic continuation, and treatment of zero/trivial representations.

Discovery links, not immutable evidence receipts:

- Brauer article: <https://doi.org/10.2307/1969121>
- Artin article bibliographic record: <https://eudml.org/doc/204318>

No `H0` status is claimed. Required follow-up includes obtaining immutable source files and hashes,
pinpointing theorem and premise locations, checking corrections and later convention changes, and
mapping every source premise to the eventual typed obligation registry.
