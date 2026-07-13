# THM-M-1461 rev-5.6 intake

`THM-M-1461` is the numerical-analysis catalog item "finite element method." The repository gives
only the gloss "variational discretization of partial differential equations," attribution to
Richard Courant, the year 1943, and an untrusted `verified` label. This identifies a method and a
large theorem family, not a binder-complete truth-valued proposition.

## Intake result

This directory is a fail-closed `planned` dossier. It does not silently choose among well-posedness
of a discrete variational problem, Galerkin orthogonality, Cea quasi-optimality, interpolation or
energy-norm error estimates, convergence under mesh refinement, or correctness of a particular
element assembly. Those results require materially different PDE, domain, space, mesh, element,
regularity, and conclusion choices that the catalog does not make.

The Courant 1943 paper is recorded as a credible bibliographic lead because its title, year, and
pages match the catalog metadata, but only bibliographic metadata was available during intake. No
primary-source theorem, page passage, proof, or correction was admitted. Selecting a modern FEM
theorem from that lead or from later theory would therefore substitute missing mathematics.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned Lax-Milgram and orthogonal-projection APIs. A bounded
exact-topic search found no finite-element or Galerkin declaration in pinned mathlib or repo-local
Lean. The probe and search are discovery-only observations, not target elaboration, an exhaustive
anchor audit, or proof evidence.

The canonical human statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the catalog method label is not yet a stable proposition; no source-identical usable
formal artifact is credited; and no readable proof can attach to an unfrozen root. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
