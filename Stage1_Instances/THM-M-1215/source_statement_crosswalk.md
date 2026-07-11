# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Catalogue phrase "well-posedness of periodic NLS" | `Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md`, THM-M-1215 record | none | Insufficient to identify a proposition: equation, dimension, power, regularity, and conclusion are absent |
| Likely 1993 source family | J. Bourgain, *Fourier transform restriction phenomena for certain lattice subsets and applications to nonlinear evolution equations. I. Schrödinger equations*, Geometric and Functional Analysis 3 (1993), 107-156 | future concrete periodic-NLS target | Plausible primary source from title, author, date, and subject; no theorem/page has been selected or audited, hence `H1`, not `H0` |
| Periodic initial-value problem | Same likely source, which treats nonlinear Schrodinger problems with periodic boundary conditions | no concrete PDE declaration found | Domain dimension, nonlinearity, sign, normalization, initial-data space, and solution notion must be frozen before Lean elaboration |
| Well-posedness package | One or more results in the likely source | none | Local/global scope, threshold, uniqueness class, persistence, continuous-dependence topology, and lifespan dependence remain unresolved |
| Analytic proof boundary | Periodic Fourier analysis, restriction/Bourgain spaces, multilinear estimates, contraction, and result-specific conservation laws | none | Scope map only; later phases own exact obligations and proof closure |

The bibliographic match does not license silently choosing a familiar cubic NLS formulation: the
likely paper contains a family of results, while the catalogue entry supplies no theorem number or
parameters. The statement phase must inspect a stable copy and record its hash or edition,
theorem/page, exact equation and torus dimension, nonlinear exponent and sign, regularity range,
local/global conclusion, solution and uniqueness spaces, dependence statement, conservation input,
and corrections or errata. It must then elaborate that exact proposition in Lean and mutation-test
the omitted dimensions, nonlinearities, hypotheses, and boundary regularities.

Discovery locator (not an immutable evidence receipt): DOI
<https://doi.org/10.1007/BF01206630>.

No source closure, source-to-Lean equivalence, machine closure, or theorem completion is claimed.
