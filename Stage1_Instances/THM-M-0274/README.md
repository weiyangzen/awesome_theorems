# THM-M-0274 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Hahn-Banach theorem. The
repository catalogue attributes the item to Hans Hahn and Stefan Banach, dates it to 1927, and
gives only the gloss "norm-preserving extension of linear functionals." Its `已验证` label is
untrusted metadata under rev-5.6 and supplies no human-source, statement, or proof credit.

The gloss identifies the analytic extension family but not one proposition. It does not select
real versus complex scalars, normed versus seminormed ambient space, a complete versus incomplete
space, an algebraic versus continuous functional, a subspace representation, the exact extension
equality, or whether norm equality is an explicit conclusion. Choosing a familiar textbook form
at intake would silently add proposition-changing decisions.

Hans Hahn's 1927 paper *Uber lineare Gleichungssysteme in linearen Raumen* was located in a stable
digitized volume and inspected at printed pages 214-229. Its Theorem III on page 217 is a matching
real norm-preserving extension result in the paper's terminology, but the definition chain,
translation, Banach attribution, corrections or errata, and independent review remain open.

Pinned mathlib contains the strong exact-topic candidates `Real.exists_extension_norm_eq` and
`exists_extension_norm_eq` in `Mathlib.Analysis.Normed.Module.HahnBanach`. The intake probe checks
both declarations and their reported axiom sets. They are discovery evidence only because the
catalogue has not selected the real or `IsRCLikeNormedField` form and no source-to-Lean transport,
terminal-body audit, or accepted receipt exists.

The provisional vector is `[H1, M3, R4]`: a matching primary source and exact-topic pinned formal
candidates are known, but exact source fidelity, canonical statement identity, and readable proof
reconstruction remain open. All six downstream phases remain open in `task-dag.json`. No H0, M0,
R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
