# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Primal-dual equality for transport | C. Villani, *Optimal Transport: Old and New*, Springer, 2009, Theorem 5.10 (Kantorovich duality), pp. 57-58 | Fresh compact/continuous declaration required | Primary monograph theorem located; exact edition hash, assumptions-to-binder audit, and errata review remain open (`H1`) |
| Couplings with prescribed marginals | Villani 2009, Definition 4.1 and the primal formulation preceding Theorem 5.10 | Historical `TransportPlan` | Object-model candidate only; its marginal maps and required measurability must be re-elaborated |
| Signed dual potentials and feasibility | Villani 2009, Theorem 5.10 dual constraint | Fresh real-valued continuous-potential structure | The historical `KantorovichDualPair` restricts potentials to nonnegative `ENNReal`; no equivalence is credited |
| Compact continuous specialization | Specialization of Theorem 5.10: compact spaces make continuous real costs bounded and integrable | Proposed canonical target in `intake.json` | Conservative root selected to avoid silently importing the full Polish/lower-semicontinuous theorem |
| Broader lower-semicontinuous formulation | Villani 2009, Theorem 5.10, including lower-semicontinuous costs and integrable bounds | Historical `LowerSemicontinuous`/`ENNReal` surfaces | Later generalization/transport candidate, excluded from the intake root until assumptions and codomains match |

The source theorem admits several formulations. This dossier deliberately freezes the familiar
compact/continuous signed-real specialization, not the broader theorem and not the existing
nonnegative-`ENNReal` data package. The statement phase must confirm that the proposed specialization
really follows from the pinned source formulation, then serialize the elaborated Lean expression
and mutation-test the topology, probability, continuity, marginal, potential-sign, and feasibility
assumptions.

Discovery links, not immutable evidence receipts:

- Villani book DOI: <https://doi.org/10.1007/978-3-540-71050-9>
- Historical origin for genealogy: L. V. Kantorovich, "On the translocation of masses," *Doklady Akademii Nauk SSSR* 37 (1942), 199-201 (English translation commonly cited; exact translation pin remains open).

No `H0` or source-completeness claim is made. Required follow-up includes an immutable scan or
publisher artifact hash, verbatim theorem transcription, premise-by-premise crosswalk, errata and
edition comparison, genealogy confirmation, and independent review.
