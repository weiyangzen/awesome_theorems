# THM-M-1343 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-1343`,
`李雅普诺夫直接法` (Lyapunov's direct method). The repository supplies only the gloss
`李雅普诺夫函数的稳定性判据` (a stability criterion using a Lyapunov function), attributes it to
Aleksandr Lyapunov in 1892, and labels it `已验证`. It gives no primary-source locator,
definitions, equation, state space, hypotheses, conclusion, proof, or formal artifact. Under
rev-5.6 the status label is untrusted metadata and grants no source or proof credit.

The wording names a theorem family rather than one proposition. It does not decide between
Lyapunov, asymptotic, exponential, local, uniform, or global stability; an autonomous or
time-dependent system; an equilibrium or invariant set; or weak versus strict decay of the
Lyapunov function. In particular, nonincrease and strict decrease generally support different
conclusions, while a global conclusion needs additional existence and coercivity assumptions.
Selecting a familiar textbook version would therefore substitute mathematics absent from the
catalog.

`instance.json` freezes that ambiguity as `[H5, M4, R4]`, `scope-map.md` records the
proposition-changing decisions, and `source-statement-crosswalk.md` preserves the exact repository
source boundary. A pinned Lean probe checks only adjacent ODE and derivative APIs; it is feasibility
evidence, not the target statement or proof. All six dependent phases remain open in
`task-dag.json`.

The lifecycle is `planned`. No H0, M0, R0, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
