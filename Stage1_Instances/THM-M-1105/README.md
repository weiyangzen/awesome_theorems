# THM-M-1105 rev-5.6 intake

This directory is the fail-closed `planned` intake for the Wigner semicircle law. The repository
record fixes only the name, Eugene Wigner, the year 1955, and the phrase "eigenvalue distribution
of Wigner matrices". It does not fix a matrix ensemble, normalization, convergence mode, or moment
assumptions.

The statement phase freezes a bounded-entry, variance-one real-symmetric Wigner variant with almost
sure weak convergence to the standard semicircle probability measure. Its exact elaborated Lean
proposition is `Stage1.THM_M_1105.WignerSemicircleLaw` in `Statement.lean`; the selected modern
variant is not silently attributed verbatim to Wigner's original paper. The anchor audit found
supporting mathlib interfaces and one strict finite-combinatorial external candidate, but no exact
Lean 4 closure. The provisional root vector is `[H2, M3, R4]`. No source-fidelity review, proof
state, audit completion, or theorem completion is claimed.

`scope-map.md` records the choices that affect the proposition,
`source-statement-crosswalk.md` separates discovery sources from accepted evidence, and
`task-dag.json` records the handoff to downstream phases. Intake evidence is in `validation.md`;
the statement choice and elaboration evidence are in `statement-freeze.md` and
`statement-validation.md`; immutable formal-candidate evidence is in `anchor-inventory.json` and
`anchor-audit.md`.
