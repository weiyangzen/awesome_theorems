# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Named theorem | Repository research row: `Docs/researches/math_theorems.md`, "Strong law of large numbers", attributed to Emile Borel (1909) | no unique declaration follows from the row | The row is metadata, not a primary proof source; it gives neither variables nor assumptions: `H1` |
| Human conclusion | Repository wording: "almost-sure convergence" | `Tendsto ... atTop ...` inside a `μ`-almost-everywhere quantifier | Direction agrees at slogan level, but the converging sequence and limit are absent from the source row |
| Random-variable family | Not stated in the repository source | `X : Nat -> Ω -> E` | Unresolved source-to-domain mapping |
| Independence | Not stated | pairwise independence of the coordinates | Material added hypothesis; primary-source justification or a deliberate modern normalization decision is required |
| Distribution | Not stated | every `X i` identically distributed with `X 0` | Material added hypothesis; not source-verified |
| Moment condition | Not stated | integrability of `X 0` | Material added hypothesis; not source-verified |
| Codomain | Borel's historical result is commonly associated with Bernoulli/digit-frequency settings, but no primary source was inspected in this phase | arbitrary complete real normed space with Borel structure | Likely generalization beyond the historical theorem; must not be credited as an exact crosswalk yet |
| Limit | Not stated | Bochner expectation `μ[X 0]` | Candidate modern conclusion; source mapping open |
| Existing formal artifact | Legacy Stage1 file, not a human source | `Mathlib.Probability.StrongLaw.ProbabilityTheory.strong_law_ae`, wrapped by `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_264.lean` | Valuable discovery input, but rev-5.6 rejects inherited proof credit |

The next statement phase must fail closed until it either (a) identifies and
pins the primary Borel source and formalizes its exact Bernoulli/frequency
claim, or (b) records an authorized canonicalization that explicitly chooses
the modern iid integrable theorem and proves the relationship to the source
claim in the needed direction. It must then elaborate the selected Lean
target, fingerprint the expression and environment, check all credited
transports, and mutation-test hypotheses, domains, binder scope, and boundary
cases.

No `H0` or machine-closure claim is made. Primary edition/page/theorem
pinpoints, translations, errata, and independent review remain outstanding.
