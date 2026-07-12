# THM-M-1361 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-1361`, the repository label
`跨临界分岔` (transcritical bifurcation). The catalog supplies only a collective twentieth-century
attribution and the gloss `平衡点交换稳定性的分岔` (a bifurcation in which equilibria exchange
stability). It supplies no cited proposition, definitions, hypotheses, conclusion, or proof source.
Its `已验证` field is untrusted metadata under rev-5.6.

The wording identifies a phenomenon and theorem family, not one binder-complete claim. It does not
choose between a definition, the scalar normal-form example `x' = mu*x - x^2`, a general local
bifurcation theorem, or a normal-form classification. It also leaves the system model, state and
parameter spaces, equilibrium branches, regularity, stability predicate, locality, genericity and
nondegeneracy conditions, parameter orientation, and conclusion bundle open. Selecting any of
these from memory would change rather than transcribe the target.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 6.5, printed page
200, was inspected as a discovery lead. It calls the scalar equation `x' = mu*x - x^2`
transcritical and says its fixed points collide and exchange stability. The same sentence calls
both fixed points stable for nonzero `mu`, which conflicts with the immediately preceding
one-dimensional derivative criterion and the derivatives of the displayed equation. No matching
official erratum was found. The catalog does not cite this source, and the example is not silently
promoted to the catalog's canonical theorem.

`instance.json` therefore freezes the provisional root vector `[H5, M4, R4]`. `H5` classifies the
catalog wording as not yet a stable truth-valued proposition; it does not refute standard
transcritical bifurcation results. `IntakeProbe.lean` elaborates only adjacent pinned calculus, ODE,
flow, and fixed-point interfaces. These interfaces provide no statement or proof credit. All six
downstream tasks remain open in `task-dag.json`.

No canonical mathematical or Lean statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
