# THM-M-1466 rev-5.6 intake

`THM-M-1466` is the numerical-analysis catalog item "finite volume method." The repository gives
only the gloss "discrete method for conservation laws," attribution to many mathematicians, the
20th century, and an untrusted `verified` label. This identifies a broad numerical method family,
not a binder-complete truth-valued proposition.

## Intake result

This directory is a fail-closed `planned` dossier. It does not silently choose among exact local or
global conservation, consistency, monotonicity, positivity, stability, convergence to a weak or
entropy solution, an error estimate, or correctness of a particular finite-volume implementation.
Those results require materially different conservation laws, domains, meshes, fluxes, time
schemes, regularity assumptions, and conclusions that the catalog does not select.

The Eymard-Gallouet-Herbin handbook chapter is recorded only as a credible modern survey lead.
Crossref bibliographic metadata was inspected, but no immutable chapter passage, source-selected
theorem, proof, correction record, or independent review was admitted. Choosing a theorem from
that survey or another standard finite-volume text would therefore substitute missing mathematics.

## Formal boundary

`IntakeProbe.lean` elaborates pinned finite-sum interfaces that could support a later proof of flux
cancellation on a source-selected cell/face incidence structure. A bounded exact-topic search
found no finite-volume, numerical-flux, cell-average, or conservation-law discretization
declaration in pinned mathlib or repo-local Lean. The probe and search are discovery-only
observations, not target elaboration, an exhaustive anchor audit, or proof evidence.

The canonical human statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the catalog method label is not yet a stable proposition; no source-identical usable
formal artifact is credited; and no readable proof can attach to an unfrozen root. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
