# THM-M-1342 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-1342`,
`李雅普诺夫稳定性理论` (Lyapunov stability theory). The repository supplies only the gloss
`平衡点的稳定性` (stability of an equilibrium), attributes it to Aleksandr Lyapunov in 1892,
and labels it `已验证`. It gives no dynamical system, definition of equilibrium or stability,
quantified proposition, hypotheses, conclusion, source locator, proof, or formal artifact. The
status label is untrusted metadata and grants no source or proof credit under rev-5.6.

The wording names a theory or subject family, not one theorem. An inspected modern source makes
the ambiguity concrete: Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*,
Section 6.5, page 198, separately defines Lyapunov, asymptotic, and exponential stability for fixed
points. Those notions have different quantifiers and are not interchangeable. The catalog does not
cite this source or choose one definition, criterion, characterization, or implication, so none is
adopted as the canonical claim.

`instance.json` freezes the unresolved root as `[H5, M4, R4]`, `scope-map.md` records the
proposition-changing choices, and `source-statement-crosswalk.md` preserves the exact source
boundary. A pinned Lean probe checks only adjacent ODE, topology, and convergence APIs; it neither
defines stability nor states or proves this target. All six dependent phases remain open in
`task-dag.json`.

The lifecycle is `planned`. No H0, M0, R0, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
