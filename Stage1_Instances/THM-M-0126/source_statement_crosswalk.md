# Source-statement crosswalk

| Claim component | Repository source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Topic | `Docs/Stage1_Blueprint.md`: "modular curve over a quaternion algebra" | namespace `AwesomeTheorems.Stage1.S1_M_045` | Topic correspondence only |
| Quaternion algebra | No field, ramification, or indefiniteness assumptions given | `QuaternionicModularDatum` | Candidate is materially more generic and cannot be credited as an exact translation |
| Order and level | Not present in source wording | `QuaternionicOrder`, `QuaternionicLevelStructure` | Locally invented interfaces, not source-backed definitions |
| Moduli problem | Not present in source wording | `QuaternionicModuliTarget`, `RepresentsQuaternionicModuli` | The predicates do not define the classical abelian-variety moduli problem |
| Curve theorem | No exact conclusion given | `QuaternionicModuliStatementShape` | Candidate asserts an existential package, but source fidelity is unestablished |

The manifest's `source_status_untrusted` value `已验证` is metadata and supplies neither a citation
nor proof evidence. Repository research notes repeat the same one-line wording and add no primary
source. Consequently there is no truthful mapping of ordered binders, hypotheses, degenerate cases,
or conclusion at intake.

Primary-source selection must identify an edition or immutable file, theorem/page, all arithmetic
assumptions, the exact claimed conclusion, and errata. Only then may the statement phase normalize
the claim and test the legacy Lean candidate. No `H0` or machine-closure claim is made.
