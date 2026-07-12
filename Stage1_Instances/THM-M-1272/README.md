# THM-M-1272 rev-5.6 intake

This directory is the `planned` intake for the classical Fountain theorem. It freezes the intended
claim as a multiplicity result for an even variational functional: Fountain geometry and the
relevant compactness hypothesis yield critical values unbounded above. The statement phase now
freezes a separable real Hilbert-space specialization with an orthonormal total sequence, explicit
finite cores and orthogonal tails, global Palais-Smale compactness, strict two-radius geometry, and
critical values tending to positive infinity. `Statement.lean` kernel-elaborates this proposition.

The legacy Lean module is discovery input only. It exposes useful statement vocabulary, but its
hard compactness and minimax content is supplied as proposition-valued structure data, so it earns
no rev-5.6 proof credit. The provisional root vector is `[H2, M3, R4]`: the selected statement is
self-tested pending master acceptance, while source audit and every proof gate remain open. No
audit completion or theorem completion is claimed.

The scope map, source crosswalk, and open task DAG define downstream work. Intake checks and exact
results are recorded in `validation.md`.
