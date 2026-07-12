# THM-M-1344 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-1344`,
`李雅普诺夫间接法` (Lyapunov's indirect method). The repository supplies only the gloss
`线性化稳定性` (stability by linearization), an attribution to Aleksandr Lyapunov, and the year
1892. It gives no equation, phase space, equilibrium, regularity, stability predicate, spectral
condition, source citation, or formal artifact. The catalog value `已验证` is untrusted metadata
under rev-5.6.

The named topic is recognizable, but it does not select one proposition. Standard formulations
separate a negative-spectrum branch giving local exponential stability from a positive-spectrum
branch giving instability. They also distinguish finite-dimensional ODEs from Banach-space
semigroup systems, and give no conclusion when the linearization has spectrum on the imaginary
axis without stronger hypotheses. Choosing one direction, joining both, or weakening exponential
stability to asymptotic or Lyapunov stability would change the target.

`IntakeProbe.lean` checks only adjacent pinned ODE, derivative, and spectrum APIs. The bounded
repo-local and pinned-mathlib search found no target-specific indirect-method or ODE stability
declaration. That is intake discovery evidence, not an exhaustive anchor audit or a global absence
claim.

The provisional root vector is `[H1, M4, R4]`. Here `H1` records a known published theorem family
whose exact statement, assumptions, branch selection, errata, and source mapping remain unaudited;
it does not say that the classical indirect-method theorems are false or open.
`instance.json` is the structured scope authority, the scope map and crosswalk freeze all unresolved
choices, and the six dependent phases remain open in `task-dag.json`. No H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
