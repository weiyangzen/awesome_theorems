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

## Statement-phase exactness boundary

The four contract-selected positive identity surfaces remain unresolved:

| Required surface | Source-backed value | Statement result |
|---|---|---|
| Ordered premises | None identified | Cannot remove or retain a hypothesis without inventing it |
| Domain and binder scope | None identified | Cannot choose the base field, quaternion algebra, order, level, model, universes, or quantifier scope |
| Conclusion | None identified | Cannot choose construction, algebraicity/canonical model, representability, smoothness/properness, or uniformization |
| Boundary cases | None identified | Cannot decide split/ramified, compact/noncompact, torsion/neat, coarse/stack, or degenerate conventions |

Accordingly the contract source `Statement.lean` is declaration-free and uses no imports. Its
successful kernel elaboration validates only the fail-closed boundary. `StatementInfrastructure.lean`
remains an adjacent API probe, and the legacy `S1_M_045` module remains unaccepted discovery input.
Neither selects a proposition, supplies an expression fingerprint, or makes any of the four required
mutations meaningful.
