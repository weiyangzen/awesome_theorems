# THM-M-1373 rev-5.6 intake

`THM-M-1373` is the ordinary-differential-equations catalog item "Hamiltonian systems." The
repository attributes it to William Hamilton in 1834 and supplies only the gloss "a mathematical
framework for classical mechanics" plus an untrusted `verified` label. A framework is not a
truth-valued proposition with fixed binders, assumptions, and conclusion.

## Intake result

This dossier records a fail-closed `planned` instance and preserves the received wording without
silently replacing it by Hamilton's equations, Hamiltonian/Lagrangian equivalence, energy
conservation, preservation of a symplectic form or phase volume, Noether's theorem, or the
Liouville-Arnold theorem. Those are inequivalent statements and several have their own repository
targets.

Hamilton's 1834 paper *On a General Method in Dynamics* is a plausible historical source-family
lead. Bibliographic metadata identifies DOI `10.1098/rstl.1834.0017`, *Philosophical Transactions
of the Royal Society of London* issue 124, pages 247-308. The source was not successfully inspected
in this intake, the catalog does not cite it, and the paper contains a method rather than a catalog-
selected theorem. It therefore supplies no `H0` credit.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned integral-curve, flow, canonical symplectic-matrix, and
symplectic-group APIs. The historical `THM-M-1516` Lean artifact and its Physlib lead are discovery
inputs owned by another target. They are not an exact source transport for this target and receive
no inherited statement or proof credit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`. Here `H5` classifies the received framework label as not yet a stable proposition;
it does not say that Hamiltonian mechanics is false or open. No usable exact formal artifact is
identified, and no source-faithful reconstruction can attach to an unfrozen root. All six
downstream tasks remain open. No accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
