# Source-statement crosswalk

| Claim component | Source anchor available at intake | Lean candidate | Intake assessment |
|---|---|---|---|
| Density evolves by a forward equation | Repository research record, `Docs/researches/math_theorems.md`, lines around the THM-M-1093 entry: "probability-density evolution equation," attributed to Fokker/Planck (1914) | `StatementShape`; `SolvesClassicalFokkerPlanck` | The repository wording does not specify a stochastic model, signs, coefficients, dimensions, hypotheses, or conclusion strength; it cannot support `H0` |
| One-dimensional differential operator | Historical module comment gives `partial_t rho = -partial_x (b rho) + (1/2) partial_xx (a rho)` | `fokkerPlanckForwardOperator` | Plausible modern normalization with `a` interpreted as variance, but not yet cross-checked against a pinned primary edition |
| Classical pointwise solution | No primary pinpoint accepted | `SolvesClassicalFokkerPlanck` | Candidate encoding only; domain, differentiability, initial and boundary data are underspecified |
| Weak generator identity | No primary pinpoint accepted | `SolvesWeakFokkerPlanck` | Candidate modern formulation; test-function class and analytic transports require independent source and Lean checks |
| Existence, preservation, and uniqueness | Not asserted by the short repository source statement | `StatementShape` and `FokkerPlanckDensityEvolution` | These are substantial additions in the historical artifact. They remain provisional and must not be silently attributed to the named equation |
| Relation to diffusion laws | Primary theorem and assumptions not yet located | `lawEvolutionAgreement`, `sdeGeneratorCompatibility` fields | Unproved proposition fields are architecture markers, not a formal bridge or evidence |

## Source leads, not evidence receipts

- A. D. Fokker, *Die mittlere Energie rotierender elektrischer Dipole im
  Strahlungsfeld*, Annalen der Physik 348 (1914), 810-820. This bibliographic lead must be checked
  from an immutable scan for the actual equation, notation, assumptions, and page/equation number.
- M. Planck, *Ueber einen Satz der statistischen Dynamik und seine Erweiterung in der
  Quantentheorie*, Sitzungsberichte der Koeniglich Preussischen Akademie der Wissenschaften
  (1917), 324-341. The date differs from the repository's compact 1914 attribution and needs a
  genealogy audit rather than automatic co-attribution.

No edition/file hash, verified quotation, equation pinpoint, translation record, errata search, or
independent review exists yet. Accordingly the human/source status is conservatively `H3`. The
statement phase must first decide whether the target is merely the PDE identity, a derivation from
an SDE/Markov semigroup, or an existence-and-uniqueness theorem. It must then freeze every binder and
hypothesis and check classical/weak/measure-valued transports. Until then, the historical
`StatementShape` is not the canonical claim and the repository label `已验证` is untrusted metadata.
