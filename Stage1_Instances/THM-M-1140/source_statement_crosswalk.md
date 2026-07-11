# Source-statement crosswalk

| Claim component | Human source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| A harmonic function with an interior maximum on a connected domain is constant | L. C. Evans, *Partial Differential Equations*, 2nd ed., AMS Graduate Studies in Mathematics 19 (2010), section 2.2, strong maximum principle discussion for Laplace's equation | No declaration selected | Standard source family identified, but exact theorem/page, edition hash, assumptions, and errata have not been independently audited: `H2` |
| Mean-value mechanism | S. Axler, P. Bourdon, W. Ramey, *Harmonic Function Theory*, 2nd ed., Springer GTM 137 (2001), opening chapters on harmonic functions and maximum principles | Future mean-value and integral API candidates | Secondary source discovery anchor only; no node-level premise crosswalk |
| Connectedness propagates local constancy | Same classical proof: the maximum level set is shown open and closed in the domain | Future topology connectedness API | Required root assumption; omitting it permits functions constant at different values on components |
| Strong minimum principle | Apply the maximum principle to `-u` | Future checked negation transport | Equivalent candidate, not part of the frozen root and not credited |
| General elliptic strong maximum principle | Evans, chapter 6, maximum-principle treatment for second-order elliptic equations | Out of scope | A strict generalization, not a substitute for the harmonic root |

The repository source text says only "the strong maximum principle for harmonic functions" and
labels it verified. That metadata label is untrusted under rev-5.6. The dossier therefore chooses
the conventional attained-interior-maximum formulation without claiming that a source audit or a
Lean encoding has already established exact fidelity.

The statement phase must choose the precise mathlib representation of a domain-restricted harmonic
function, inspect its binder order and type, elaborate the canonical expression, and mutation-test
connectedness, openness, nonemptiness, extremum locality, codomain, and dimension. The later anchor
audit must search repo-local mathlib and credible external Lean 4 projects at immutable revisions.

No `H0` or machine status better than `M4` is claimed. Exact ISBN/edition artifact hashes,
theorem/page pinpoints, assumption mapping, errata search, and independent review remain required.
