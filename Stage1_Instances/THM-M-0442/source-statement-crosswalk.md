# Source-statement crosswalk

| Claim component | Human/source anchor | Lean discovery candidate | Intake assessment |
|---|---|---|---|
| Complete rational torsion classification | Barry Mazur, "Modular curves and the Eisenstein ideal", *Publications Mathématiques de l'IHÉS* 47 (1977), 33-186, DOI `10.1007/BF02684339` | `S1_M_088.StatementShape` | Primary proof source identified; exact theorem/page and premise-by-premise audit remain open (`H1`) |
| Cyclic list | `Z/nZ`, `1 <= n <= 10` or `n = 12` | `IsMazurCyclicOrder`, `HasCyclicTorsionOrder` | Prose and Lean list agree syntactically; equivalence to the source formulation is not yet independently reviewed |
| Noncyclic list | `Z/2Z x Z/2mZ`, `1 <= m <= 4` | `IsMazurBicyclicSecondOrder n` and `ZMod 2 x ZMod n`, `n in {2,4,6,8}` | Requires checked reindexing `n = 2*m` and finite cyclic-group encoding transport |
| Rational elliptic curve | Elliptic curve over `Q` | `WeierstrassCurve Q` with `[E.IsElliptic]` | Isomorphism/model invariance and exact object-model adequacy remain statement obligations |
| Torsion subgroup | `E(Q)_tors` | `AddCommGroup.torsion E(Q)` | Candidate API exists; exact elaboration and membership semantics have historical wrappers only |
| Converse realizability | Often appended in expository formulations | No candidate in the frozen root | Explicitly excluded unless primary-source audit shows it is inseparable from the repository's intended claim |

The repository phrase "classification of rational torsion points on elliptic curves" is compatible
with the necessity/classification direction frozen here, but does not settle whether realizability
was intended. This dossier therefore does not silently broaden the root. The source audit must pin
an immutable scan, locate the exact numbered result and pages, enumerate hypotheses and conventions,
check corrections/errata, and obtain independent review before `H0` is possible.

Discovery links are not evidence receipts:

- NUMDAM bibliographic record: <https://www.numdam.org/item/PMIHES_1977__47__33_0/>
- DOI: <https://doi.org/10.1007/BF02684339>
