# Source-statement crosswalk

| Claim component | Source anchor | Candidate formal shape | Intake assessment |
|---|---|---|---|
| Inherited claim | `Docs/Stage0_Blueprint.md`, THM-M-1207: `Schrodinger方程等` | none | A topic/example phrase, with no truth-valued conclusion: `H4/M4` |
| Free Schrodinger decay | Journé, Soffer, Sogge, *Decay estimates for Schrödinger operators*, Communications on Pure and Applied Mathematics 44 (1991), 573-604, DOI 10.1002/cpa.3160440504 | an `L^1 -> L^infinity` bound for an evolution operator, after selecting the paper's precise hypotheses | Primary candidate for discovery only; edition, theorem pinpoint, assumptions, errata, and exact scope are not accepted |
| Abstract dispersive-to-spacetime route | Keel and Tao, *Endpoint Strichartz estimates*, American Journal of Mathematics 120 (1998), 955-980, Theorem 1.2, DOI 10.1353/ajm.1998.0039 | abstract energy and decay hypotheses imply spacetime bounds | Neighboring THM-M-1209 territory; must not silently replace this target |
| Strichartz estimates | Same evolution family, with mixed spacetime norms | a typed mixed-norm estimate | Reserved neighboring THM-M-1208 territory unless a primary-source scope decision explicitly distinguishes the root |
| Local smoothing | Same broad equation family, different gain/integrability conclusion | a local smoothing inequality | Reserved neighboring THM-M-1210 territory |

## Decision required

The phrase “dispersive equations” can denote a class, while “Schrodinger equations, etc.” does not
identify even a single equation. Before statement work, a source auditor must choose a precise root,
preferably a fixed-time dispersive estimate so the adjacent Strichartz, endpoint, and local-smoothing
targets remain distinct. The audit must record an immutable edition, exact theorem/page, every
operator and potential hypothesis, dimension, data/solution spaces, time exclusions, constant
dependence, and errata. This preference is not itself the canonical claim.

No cited result is asserted to exist in Lean or to be repo-locally closed. No `H0` or machine-proof
claim is made.
