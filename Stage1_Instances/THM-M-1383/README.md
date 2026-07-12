# THM-M-1383 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `边值问题`
(boundary-value problems). The catalog supplies only that name, a collective twentieth-century
attribution, and the gloss `两点边值问题的理论` (the theory of two-point boundary-value problems).
It supplies no citation, equation, definitions, hypotheses, conclusion, or proof source. Its
`已验证` (`verified`) label is explicitly untrusted metadata under rev-5.6.

A boundary-value problem is a class of problems, not one truth-valued theorem. Even within ordinary
differential equations, the gloss could refer to existence, uniqueness, nonexistence, multiplicity,
a Fredholm solvability criterion, spectral structure, a Green-function representation, a priori
estimates, or convergence of a numerical method. It fixes neither the differential equation nor
the endpoint data. Selecting a familiar result from memory would silently substitute a new target.

This intake freezes that ambiguity instead of inventing the missing mathematics. The provisional
root vector is `[H5, M4, R4]`. `H5` records that the supplied problem-family label is not yet a
stable proposition; it does not say that standard boundary-value theorems are false or open. No
source-identical usable Lean artifact or source-faithful reconstruction can attach before a precise
root is selected.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Chapter 5, Section 5.1,
was inspected as an authoritative source-family discriminator. It begins with a fixed-endpoint wave
equation, then introduces a Sturm-Liouville eigenvalue problem and separates several facts one may
prove about it. This confirms that the catalog gloss does not determine one proposition. The
repository does not cite this book or select any of those results, so none is accepted as the
canonical claim or credited as `H0`.

`IntakeProbe.lean` checks only adjacent pinned interval, integral-curve, local initial-value
existence, and initial-value uniqueness APIs. It states no boundary-value theorem and receives no
statement or proof credit. The structured scope authority is `instance.json`; all six downstream
phases remain open in `task-dag.json`.

The lifecycle is `planned`. No canonical Lean expression, H0, M0, R0, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
