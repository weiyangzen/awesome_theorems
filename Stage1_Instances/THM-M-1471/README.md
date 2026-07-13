# THM-M-1471 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `先验误差估计`
(a priori error estimate). The repository supplies only the gloss `数值解的收敛阶` (the
convergence order of a numerical solution), attributes it to many mathematicians in the twentieth
century, and labels it `已验证`. That is a topic or result-family description, not a truth-valued
proposition with ordered binders, hypotheses, and a conclusion. The verified label is explicitly
untrusted metadata and supplies neither source nor proof credit.

An a priori estimate may concern finite elements, finite differences, finite volumes, spectral
methods, or an ODE time integrator. It may state quasi-optimality, an explicit bound such as an
error controlled by a power of a mesh or time step, or only an asymptotic order. Those alternatives
require different equations, spaces or schemes, regularity and stability assumptions, norms,
constants, exponents, refinement regimes, and boundary cases. The catalog selects none of them.
Choosing a Cea-type bound or any familiar PDE scheme would substitute proposition-changing
mathematics.

Pinned mathlib supplies generic asymptotic notation, coercive variational solvability, and Hilbert-
space best approximation. `IntakeProbe.lean` authenticates those adjacent interfaces only. It does
not define a numerical method or error family and supplies no canonical statement or proof credit.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog wording as not yet a
stable proposition; it does not refute correctly stated a priori error theorems. All six downstream
phases remain open. No `H0`, `M0`, `R0`, exact mathematical or Lean statement, accepted proof
state, audit completion, theorem completion, accepted receipt, or master acceptance is claimed.
