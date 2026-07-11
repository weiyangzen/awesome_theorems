# THM-M-1092 rev-5.6 intake

This directory is the `planned` intake for the Kolmogorov forward and backward equations. It
freezes the intended family as the continuous-time, time-homogeneous Markov transition equations,
while leaving the exact state-space, generator-domain, regularity, and operator-versus-density
formulation to the statement phase.

The historical `S1_M_216.lean` file is discovery input only. Its terminal conclusion package takes
the desired equations as data, while its checked Chapman-Kolmogorov material is discrete-time
substrate. Neither receives rev-5.6 statement or proof credit. The provisional vector is
`[H1, M4, R4]`; no elaborated canonical target, audit completion, or theorem completion is claimed.

The scope map, source crosswalk, and dependency-ordered open task DAG define the downstream work.
The exact intake checks and their results are recorded in `validation.md`.
