# Source-statement crosswalk

| Claim component | Located source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Entry identity | `Docs/Stage0_Blueprint.md`, `THM-M-1156` | none | Stable ID and title are known |
| Human wording | `定理内容: Newton位势与对数位势` | none | A topic phrase, not a truth-valued claim |
| Ambient space | not stated | none | Cannot choose dimension; Newtonian and logarithmic kernels have dimension-sensitive roles |
| Data and regularity | not stated | none | No density/measure, support, integrability, or differentiability hypotheses |
| Kernel convention | not stated | none | Constants and Laplacian sign convention are unspecified |
| Conclusion | not stated | none | Definition, harmonicity, Poisson identity, and representation theorem are materially different claims |
| Verification label | Stage0 says `已验证` | none | Explicitly untrusted metadata under rev-5.6; it grants neither H nor M credit |

No primary mathematical source, edition, theorem number, page, assumptions list, or errata record is
present in the repository entry. Consequently there is no honest source-to-binder or
source-to-conclusion mapping yet. The exact-statement phase must obtain a primary-source pinpoint
that states the intended proposition and fixes all conventions above. It must then elaborate that
same claim in Lean and mutation-test its dimension, hypotheses, kernel normalization, and boundary
cases. Until then, candidate mathlib declarations may be searched for discovery but cannot define
the target retroactively.

This crosswalk intentionally makes no `H0` claim and cites no secondary text as if it were the
missing source. Current source status is `H4`: the claim itself remains underdetermined.
