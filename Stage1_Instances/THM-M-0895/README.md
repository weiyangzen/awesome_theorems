# THM-M-0895 rev-5.6 intake

`THM-M-0895` is the repository catalog item "strongly regular graphs." The catalog attributes the
item to Raj Chandra Bose in 1963 and gives only the gloss "parameter constraints of strongly
regular graphs" plus an untrusted `verified` label. Those fields identify a theorem family, not a
binder-complete proposition.

## Intake result

This directory is a fail-closed `planned` dossier. Bose's 1963 paper *Strongly regular graphs,
partial geometries and partially balanced designs* is an exact bibliographic match for the title,
author, year, and subject. Its publisher landing page and bibliographic metadata were inspected,
but the catalog does not cite it, no pinpoint result or definition chain has been admitted, and no
independent source review exists. The phrase "parameter constraints" could mean the elementary
feasibility equation, adjacency-matrix identities, eigenvalue restrictions and multiplicities,
integrality conditions, complement parameters, partial-geometry parameters, or a conjunction.
These claims have different assumptions and conclusions.

## Formal boundary

Pinned mathlib contains a strongly regular graph structure and several close results in
`Mathlib.Combinatorics.SimpleGraph.StronglyRegular`. In particular,
`SimpleGraph.IsSRGWith.param_eq` proves the plausible parameter equation
`k * (k - l - 1) = (n - k - 1) * mu` under `0 < n`, while `matrix_eq` and `compl` prove other
parameter relations. `IntakeProbe.lean` authenticates these interfaces under the pinned toolchain.
Their presence is discovery-only evidence: the received gloss does not select any one of them as
the root, and intake does not credit their proof bodies or trust closure.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M3, R4]`: an exact 1963 source lead is identified but its statement mapping is not accepted;
close pinned formal interfaces exist but no source-approved target is selected; and no
source-faithful proof reconstruction can attach to an unfrozen root. All six downstream tasks
remain open. No accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
