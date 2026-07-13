# THM-M-1493 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `单纯形法`
(simplex method). The catalog supplies only the gloss `线性规划的算法` (an algorithm for linear
programming), attributes it to George Dantzig in 1947, and labels it `已验证`. An algorithm family
and purpose are not a truth-valued proposition with ordered binders, hypotheses, and a conclusion.
The verified label is untrusted metadata and supplies neither human-source nor kernel-proof credit.

## Intake result

The record does not select a linear-program representation, coefficient domain, feasibility and
boundedness assumptions, initialization procedure, pivot rule, treatment of degeneracy, output
contract, or theorem family. Plausible roots include one-step invariant preservation, finite
termination under nondegeneracy or a specified anti-cycling rule, optimality of a terminal basis,
infeasibility or unboundedness detection, end-to-end partial correctness, or a complexity result.
These are inequivalent. Choosing the familiar standard-form simplex theorem would invent or
substitute mathematics absent from the catalog.

A strong historical source-family lead is George B. Dantzig's chapter "Maximization of a Linear
Function of Variables Subject to Linear Inequalities" in the 1951 Cowles monograph *Activity
Analysis of Production and Allocation*. The author-hosted scan identifies Dantzig's 1947 work and
contains several distinct theorems under a nondegeneracy setup, including finite basis iteration,
an optimality criterion, and feasibility construction. The catalog does not cite this chapter or
select one of those results. No exact source proposition, incorporated definitions, assumptions,
corrections, or independent review is admitted as `H0` here.

## Formal boundary

Pinned mathlib contains a genuine meta-level simplex implementation used as a `linarith`
certificate-search oracle. `IntakeProbe.lean` elaborates its matrix, tableau, pivot, LP reduction,
runner, and oracle interfaces. The implementation comments describe Bland pivoting and termination,
but the inspected module exposes definitions rather than a kernel theorem proving the catalog's
general simplex-method claim. A successful probe therefore establishes API availability only.

The canonical human statement and Lean expression remain null. The provisional root vector is
`[H5, M4, R4]`: the received catalog wording is not yet a stable proposition; no usable formal
artifact for an exact, source-identified root has been located; and no readable proof can attach to
an unidentified root. The adjacent pinned implementation does not lower root machine debt. `H5`
does not refute standard simplex-method theorems. All six downstream tasks remain open. No accepted state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
