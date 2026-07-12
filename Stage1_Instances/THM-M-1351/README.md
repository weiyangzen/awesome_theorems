# THM-M-1351 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Poincaré映射` (Poincare map). The catalog supplies only that name, an attribution to Henri
Poincare, the year 1881, and the gloss `周期轨道的稳定性` (stability of periodic orbits). It
supplies no cited proposition, definitions, hypotheses, conclusion, or proof source. Its `已验证`
(verified) status is explicitly untrusted metadata.

A Poincare map is a construction used by several distinct results, not one theorem by itself. The
catalog may be gesturing at existence and regularity of a local first-return map, equivalence
between stability of a periodic orbit and stability of the corresponding fixed point, a derivative
or characteristic-multiplier stability criterion, or invariance under the choice of transversal.
Those claims require different hypotheses and conclusions. Selecting one from mathematical memory
would silently substitute a nearby theorem for the repository target.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 12.2, was inspected
as an authoritative discovery source. It separates the return-map definition, the orbit/fixed-point
stability equivalence (Lemma 12.2), a derivative criterion (Corollary 12.3), and a monodromy-spectrum
comparison (Theorem 12.4). The catalog does not cite or select any one of them, so none is accepted
as the canonical claim at intake.

The root is provisionally `[H5, M4, R4]`: the catalog wording is not yet one stable truth-valued
proposition; this does not say that standard Poincare-map results are false or open. A narrow pinned
Lean probe confirms only generic flow, orbit, periodic-point, derivative, and implicit-function
substrates. It does not define a transversal or first-return map and receives no statement or proof
credit.

The structured scope authority is `instance.json`; the open work queue is `task-dag.json`; exact
self-test commands and boundaries are in `validation.md` and `intake-receipt.json`. No canonical
Lean expression, H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
