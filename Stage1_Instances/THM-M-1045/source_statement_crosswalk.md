# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Wiener measure is quasi-invariant under the admissible translations | R. H. Cameron and W. T. Martin, “Transformations of Wiener Integrals under Translations,” *Annals of Mathematics* 45 (1944), 386-396, DOI 10.2307/1969276 | future exact root in `AwesomeTheorems.Stage1.S1_M_238` | Primary paper identified, but theorem/page-level premise and errata mapping is not yet accepted: `H1` |
| Admissible directions are paths starting at zero, absolutely continuous, with square-integrable derivative | Same 1944 paper; modern Cameron-Martin-space formulation must be cross-checked against its notation and interval convention | future path-space predicate / Hilbert embedding | Mathematical scope frozen provisionally; exact interval and representative conventions remain statement work |
| Density is the exponential of the Wiener integral minus half the Cameron-Martin energy | Same 1944 paper | legacy `cameronMartinDensity`-style expression and future RN theorem | Translation sign and push-forward orientation must be checked before freezing the formula |
| Non-admissible translations yield mutually singular measures | E. Hewitt and L. J. Savage, “Symmetric Measures on Cartesian Products,” *Transactions of the AMS* 80 (1955), 470-501, as a historical route to the zero-one/singularity half; exact dependency genealogy remains to be audited | future negative/singularity branch | Required iff branch; no checked repo-local candidate identified at intake |
| Abstract Gaussian-space formulation | V. I. Bogachev, *Gaussian Measures*, AMS Mathematical Surveys and Monographs 62 (1998), Cameron-Martin chapter; edition/page pinpoint pending | legacy `CameronMartinModel` interface | Useful generalization and exposition candidate, not primary evidence for the original Wiener theorem |

The intended translation is the push-forward by `x ↦ x + h`. With this orientation the familiar
positive-sign exponential density is expected, but that statement is deliberately not credited
until the statement phase checks the map convention and RN derivative direction in Lean.

No `H0` claim is made. Follow-up must obtain immutable copies/hashes, pinpoint theorem and page
locations, map every assumption and interval convention, search corrections/errata, and obtain
independent review. The old source label `已验证` is untrusted metadata, not evidence.
