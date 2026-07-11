# Source-statement crosswalk

| Claim component | Human source anchor | Lean target component | Intake assessment |
|---|---|---|---|
| Original gravitational field equations | A. Einstein, *Die Feldgleichungen der Gravitation*, Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften (1915), 844-847 | Future convention-specific tensor equation | Primary historical paper identified; exact scan hash, equation/page transcription, assumptions, and independent review remain open: `H1` |
| Consolidated 1916 presentation | A. Einstein, *Die Grundlage der allgemeinen Relativitätstheorie*, Annalen der Physik 49 (1916), 769-822, DOI `10.1002/andp.19163540702` | Definitions of metric, curvature, and the field equation | Primary exposition anchor only; notation and sign conventions require a page/equation-level audit |
| Einstein tensor | Modern notation `G_ab = Ric_ab - (1/2) R g_ab` | Definition of a covariant symmetric 2-tensor | Must be checked against the selected mathlib curvature convention |
| Matter-coupled equation | `G_ab = (8πG_N/c^4) T_ab` in conventional units | Equality of tensor fields | Units, constants, regularity, dimension, and index-free encoding are unresolved |
| Cosmological term | Einstein's 1917 extension `G_ab + Λ g_ab = κ T_ab` | Optional parameterized general form | Not present in the 1915 source; must not be attributed to it or added silently |
| Vacuum form | `T = 0`, with `Λ = 0` giving `G = 0` and, in the usual four-dimensional setting, `Ric = 0` | Candidate specialization and trace bridge | A neighboring encoding, not the unrestricted root |

The repository discovery text provides only “the fundamental equation of general relativity.” It
does not specify whether the target is the 1915 equation, the modern matter-coupled equation, the
1917 cosmological extension, a vacuum specialization, or a mathematical consequence. More
fundamentally, asserting a field equation as a physical law is not itself a theorem. Stage1's
physical-item policy requires a proposition inside a fixed axiomatic model. The statement phase
must therefore select a faithful proposition, rather than broadening the target or wrapping an
assumed equation in a trivial implication.

A likely nontrivial statement-level target is the equivalence of the expanded equation and the
Einstein-tensor form under explicit definitions. That remains only a candidate: it cannot receive
proof credit until its mathematical value and fidelity to this target are reviewed. The statement
phase must also freeze dimension, smoothness, signature, Riemann/Ricci signs, units, constants,
tensor equality, and the treatment of `Λ`; then elaborate and mutation-test the exact Lean target.

Discovery links (not immutable evidence receipts):

- 1915 bibliographic scan record: <https://echo.mpiwg-berlin.mpg.de/ECHOdocuView?url=/permanent/echo/einstein/sitzungsberichte/K7ZU0K1E/index.meta>
- 1916 article DOI: <https://doi.org/10.1002/andp.19163540702>

No `H0`, `M0`, or readable-proof closure is claimed. An immutable source capture, pinpoint
transcription, errata search, Lean candidate audit, and independent review remain required.
