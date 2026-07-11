# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository claim | `Docs/researches/math_theorems.md`: "由特征函数恢复分布" (recover a distribution from its characteristic function) | No declaration selected | Authoritative local wording, but insufficient to determine a unique formula |
| Interval/CDF inversion | William Feller, *An Introduction to Probability Theory and Its Applications*, vol. II, chapter XV, section 3 (bibliographic candidate) | A theorem over `Measure Real`, characteristic functions, and truncated complex integrals | Primary-source edition, theorem/page, hypotheses, and errata still require audit |
| Density inversion | Standard Fourier inversion under absolute-integrability/density hypotheses | Fourier-transform APIs plus a measure-density bridge | Strictly stronger hypotheses and a different conclusion; cannot silently substitute for the root |
| Uniqueness | Characteristic functions uniquely determine probability laws | Measure extensionality/characteristic-function uniqueness candidate | A consequence or alternative recovery principle, not automatically the requested formula |

## Exact-scope blocker

The local source does not state a formula, normalization convention, hypotheses, or boundary rule.
In particular, distribution-function inversion at continuity points, interval-mass inversion with
half-atom endpoint terms, and density recovery by an inverse Fourier integral are not definitionally
or logically interchangeable without additional hypotheses and transports. Selecting one now would
broaden, narrow, or substitute the screened theorem.

The statement phase must first obtain an authoritative source pinpoint or an integration-lane scope
decision. It must then freeze endpoint ordering and continuity assumptions, atom behavior, Fourier
sign and normalization, integral/limit mode, and the exact recovered quantity. Only afterward may it
select minimal mathlib imports, elaborate an expression, check transports, and run mutations.

No `H0` or machine-closure claim is made. The Feller reference is a bibliographic discovery lead,
not an immutable source receipt; edition/page verification and independent review remain open.
