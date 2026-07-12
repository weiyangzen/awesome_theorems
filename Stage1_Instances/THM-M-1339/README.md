# THM-M-1339 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-1339`,
`解对初值的连续依赖性` (continuous dependence of solutions on initial values). The repository's
one-line gloss is broader: `解对初值和参数的连续性` (continuity with respect to initial values and
parameters). It gives no equation, state or parameter space, interval, topology, regularity,
uniqueness hypothesis, source citation, or formal artifact. The catalog value `已验证` is untrusted
metadata under rev-5.6.

Those omissions leave several inequivalent roots: a quantitative estimate between solutions of
two vector fields; continuity of the solution map in initial time and state; or continuity in an
explicit external parameter. A modern ODE source inspected during intake presents these as
different theorems. Selecting one, or conjoining them, would silently narrow or broaden the target.

Pinned mathlib does expose a strong nearby result: under `IsPicardLindelof`, it constructs a local
flow that is Lipschitz in the initial state and jointly continuous in state and time. It does not
quantify an external parameter. `IntakeProbe.lean` checks these declarations only as candidate
formal anchors; they receive no exact-statement, source-fidelity, or proof credit.

The provisional root vector is `[H5, M4, R4]`. Here `H5` classifies the received title/gloss pair as
not yet one stable proposition; it does not claim the standard continuous-dependence theorems are
false or open. `instance.json` is the structured scope authority, the scope and source crosswalks
freeze the ambiguity, and all six dependent phases remain open in `task-dag.json`. No H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
