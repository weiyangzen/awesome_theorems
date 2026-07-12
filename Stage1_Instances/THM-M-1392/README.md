# THM-M-1392 rev-5.6 intake

`THM-M-1392` is the ordinary-differential-equations catalog item "Green function." The repository
supplies only the gloss "integral representation of boundary-value problems," an attribution to
George Green, the year 1828, and an untrusted `verified` label. Those fields identify a classical
construction family, not one binder-complete proposition.

## Intake result

This dossier creates a fail-closed `planned` instance and preserves the ambiguity. The catalog does
not select the differential operator, coefficient regularity, interval, boundary conditions,
solution spaces, nonresonance assumptions, kernel normalization, or representation identity. It
also does not say whether the target is existence, construction, uniqueness, inverse behavior, or
the representation of a solution. Choosing a familiar Sturm--Liouville or Dirichlet formula at
intake would invent mathematics.

The surrounding ODE catalog entries make regular Sturm--Liouville Green functions a plausible
interpretation, but catalog adjacency is not a citation. The separately scheduled PDE Green
function, symmetry, and eigenfunction-expansion targets do not transfer scope or proof credit.

## Source and formal boundary

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 5.4, was inspected
as an authoritative modern source lead. It exhibits one concrete regular Sturm--Liouville
realization: a weighted second-order operator with separated Robin boundary conditions, adapted
homogeneous solutions, a nonzero Wronskian, a piecewise Green kernel, an integral resolvent, and
two inverse identities. The repository does not cite or select this source, and its formulation is
only one member of the family. It therefore receives discovery credit, not `H0` or root identity.

`IntakeProbe.lean` elaborates only adjacent pinned ODE, derivative, and interval-integral APIs. A
bounded source search located no exact Green-function boundary-value declaration in pinned mathlib
or the repository-local Lean tree. This is intake discovery, not an exhaustive anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: `H5` classifies the received wording as not one stable truth-valued proposition;
it does not refute classical Green-function theorems. No exact usable formal artifact or
source-faithful proof reconstruction is credited. All six downstream tasks remain open. No exact
statement, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
