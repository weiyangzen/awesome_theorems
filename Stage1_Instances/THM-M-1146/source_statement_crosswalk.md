# Source-statement crosswalk

| Claim component | Available source anchor | Frozen intake interpretation | Status |
|---|---|---|---|
| Named result | `Docs/researches/math_theorems.md`, entry `Schwarz反射原理` | Schwarz reflection principle | Repository metadata only; not a primary source |
| Subject | Same entry: `调和函数的延拓` (continuation of harmonic functions) | Real-valued harmonic reflection, not the holomorphic real-boundary formulation | Exact historical/source wording is unresolved |
| Reflecting set | Not specified | Interior portion of the real axis in a conjugation-symmetric open domain | Chosen normalization; needs primary-source confirmation |
| Boundary hypothesis | Not specified | Continuous extension with value zero on the reflecting portion | Essential hypothesis made explicit rather than invented as proof evidence |
| Reflected function | Not specified | Odd reflection `-u(conj z)` below the axis | Sign is essential; statement-phase mutation required |
| Conclusion | "continuation" only | The reflected function is harmonic on the two-sided domain and agrees above | No uniqueness or maximality included |
| Attribution/date | Hermann Schwarz, 1869 | Discovery lead only | Edition, page/theorem, and historical date require audit |

The repository source does not identify a book, paper, theorem number, page, edition, assumptions,
or errata. Consequently this dossier makes no `H0`, `H1`, or `H2` claim. The intake uses `H3` and
records a specific source blocker: the anchor-audit phase must locate a primary statement and decide
whether the 1869 attribution concerns this harmonic zero-boundary form or a related holomorphic
form. If it differs, the frozen target must be revoked rather than broadened silently.

No Lean candidate is credited at intake. In particular, a theorem about holomorphic functions that
take real boundary values is not an exact anchor for this root without checked bridges through real
or imaginary parts, existence of a harmonic conjugate under the needed topology, and matching
boundary regularity. The statement phase must choose actual mathlib predicates and serialize the
elaborated expression before machine status can rise above `M4`.
