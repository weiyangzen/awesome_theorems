# THM-M-0848 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0848`, the repository label
`Erdős-Rényi随机图` (Erdos-Renyi random graph). The catalog supplies the authors, the year 1959,
and only the gloss `随机图模型的基本理论`, or "basic theory of the random-graph model." It supplies
no citation, definitions, quantified proposition, hypotheses, conclusion, or proof boundary. Its
`[已验证]`-style source status is untrusted metadata under rev-5.6.

## Intake result

The metadata names a model family rather than one truth-valued theorem. The inspected 1959
Erdos-Renyi paper defines a uniform fixed-edge model, now written `G(n, m)`, and proves several
different asymptotic results. The independent-edge `G(n, p)` model commonly included under the
modern umbrella name is instead represented by Gilbert's distinct 1959 paper. Definitions,
probability-mass formulae, connectivity limits, component laws, and stopping-time results are not
interchangeable conclusions.

The intake therefore preserves that ambiguity instead of selecting a convenient result. The
canonical human and Lean statements remain null. `instance.json` records the provisional root
vector `[H5, M4, R4]`: `H5` classifies the catalog phrase as not yet a stable proposition, not the
published random-graph theorems as false. `IntakeProbe.lean` checks only adjacent pinned mathlib
`G(V, p)` APIs and provides no target or proof credit. All six downstream tasks remain open in
`task-dag.json`.

No canonical statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
