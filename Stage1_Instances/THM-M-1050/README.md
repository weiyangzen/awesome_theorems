# THM-M-1050 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Krylov estimate".
The source inventory supplies only the phrase "moment estimate for diffusion processes", an
attribution to Nikolai Krylov, and the year 1980. That does not uniquely identify one of the
inequivalent results commonly called a Krylov estimate.

The legacy Lean module proposes an expected occupation-integral bound by a spacetime `L^p` norm.
That is useful discovery input, but the repository source does not establish that it is the intended
theorem, and its diffusion package assumes rather than derives the analytic model conditions. It
therefore receives no rev-5.6 statement or proof credit.

The provisional root vector is `[H4, M4, R4]`. No exact Lean target, source fidelity, audit
completion, or theorem completion is claimed. The scope map and crosswalk identify the first
downstream decisions, while `task-dag.json` records the open phases.
