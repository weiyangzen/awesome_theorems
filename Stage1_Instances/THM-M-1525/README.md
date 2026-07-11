# THM-M-1525 rev-5.6 intake

This directory is the `planned` intake for the time-dependent Schrodinger equation. It restricts
the physics label to a mathematical Hilbert-space evolution claim with an explicit Hamiltonian,
operator domain, initial state, differential equation, and source-selected conservation results.
The precise operator regime and primary-source theorem remain statement-phase work.

The legacy `S1_M_193.lean` module is discovery input only. Its `StatementShape` assumes proposition
fields for self-adjointness, generated unitary evolution, and spectral compatibility and uses a
bounded Hamiltonian; it is not accepted as the canonical statement or terminal proof. The
provisional root vector is `[H2, M4, R4]`. No theorem completion is claimed.

The scope map, source crosswalk, and open task DAG delimit downstream work. Intake validation and
its exact limits are recorded in `validation.md`.
