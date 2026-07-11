# THM-M-1043 rev-5.6 intake

This directory is the `planned` intake for the Feynman-Kac formula. It freezes the intended family
as the continuous-time diffusion representation of a backward parabolic terminal-value problem,
including a killing potential and additive source. The exact regularity regime, diffusion model,
time convention, and primary-source statement remain statement-phase decisions.

The legacy Lean module is discovery input only. It contains useful convention records and typed
boundaries, but its probabilistic representation is supplied as structure data and it explicitly
does not prove the terminal formula. It receives no rev-5.6 statement or proof credit. The
provisional root vector is `[H2, M4, R4]`; no theorem completion is claimed.

The scope map, source crosswalk, and open task DAG delimit later work. Intake checks and exact
results are recorded in `validation.md`.
