# THM-M-0875 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Weisfeiler-Lehman算法`. The catalog supplies only `图同构的启发式算法` ("a heuristic algorithm
for graph isomorphism"), the attribution `Weisfeiler/Lehman`, the year 1968, and an untrusted
`已验证` status. These fields identify an algorithm family, not one truth-valued proposition with
ordered binders, hypotheses, and a conclusion.

The standard historical spelling is Weisfeiler-Leman. A 2018 English translation of the original
paper by B. Yu. Weisfeiler and A. A. Leman is a strong source-family lead, but the repository does
not cite it. The paper describes a finite-multigraph canonical-form procedure and several distinct
properties and conjectures. Its 2018 preface explicitly says that the conjectures that the method
solves graph isomorphism were incorrect. Thus generic graph-isomorphism completeness cannot be
silently selected from the catalog's heuristic gloss.

The label could instead lead to one-dimensional color refinement, a higher-dimensional tuple
variant, coherent closure, isomorphism invariance, sound rejection, stabilization, a complexity
bound under a fixed implementation, a class-specific completeness theorem, or a counterexample
result. These are not interchangeable. The graph model, initialization, update, comparison,
stopping rule, output, dimension, cost model, hypotheses, conclusion, and boundary cases all remain
open.

Pinned mathlib supplies finite simple graphs, graph isomorphisms, neighborhoods, and degrees.
`IntakeProbe.lean` authenticates only that adjacent substrate. A bounded search found no
Weisfeiler-Leman or color-refinement implementation or theorem in repo-local Lean or pinned
mathlib; exhaustive candidate work remains downstream.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog wording as not yet a
stable proposition; it does not deny established Weisfeiler-Leman results. All six downstream
phases remain open. No exact statement, H0, M0, R0, accepted proof state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
