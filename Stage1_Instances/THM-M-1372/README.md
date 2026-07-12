# THM-M-1372 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-1372`, the repository label
`Nekhoroshev estimate`. The catalog supplies Nikolai Nekhoroshev, the year 1977, and only the gloss
`exponential stability of nearly integrable systems`. It gives no citation, Hamiltonian model,
domains, regularity, steepness or convexity condition, perturbation norm, smallness threshold,
trajectory convention, quantified drift bound, time scale, or boundary cases. Its `verified` field
is untrusted metadata under rev-5.6.

The original paper was inspected as a strong source lead: N. N. Nekhoroshev, *An exponential
estimate of the time of stability of nearly-integrable Hamiltonian systems*, Russian Mathematical
Surveys 32:6 (1977), 1-65, DOI `10.1070/RM1977v032n06ABEH003859`. Its precise main Theorem 4.4 on
printed page 30 has a detailed analytic, steep-Hamiltonian contract. The introductory Theorem 1.4
explicitly says it is not completely accurate, and some technical lemmas used by Theorem 4.4 were
proved in a later Part II. Modern quasi-convex, Gevrey, and finitely differentiable variants impose
different hypotheses and give different stability radii and times. The catalog selects none of
these proposition-changing alternatives.

There is also a non-covered physics record, `THM-P-0775`, with nearly identical subject wording.
It is outside the 1546-target rev-5.6 manifest and supplies no accepted alias, root ownership, or
evidence. It cannot determine or lend credit to this target.

`instance.json` therefore freezes a provisional `[H1, M4, R4]` root vector. `H1` records an
established published theorem family with primary source leads whose exact root, complete two-part
proof boundary, assumptions, corrections, and node mapping remain unaccepted; it is not an H0
claim. `IntakeProbe.lean` elaborates only adjacent pinned analytic-function, ODE, flow, real-power,
and exponential interfaces. The probe supplies no canonical statement or proof credit. All six
downstream tasks remain open in `task-dag.json`.

No canonical mathematical or Lean statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
