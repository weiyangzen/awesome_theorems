# THM-M-1376 rev-5.6 intake

`THM-M-1376` is the ordinary-differential-equations catalog item "Poincare recurrence theorem."
The catalog supplies only the gloss "bounded-system recurrence," attribution to Henri Poincare,
the year 1890, and an untrusted `verified` label. These fields identify a theorem family, not a
binder-complete proposition.

## Intake result

This dossier records a fail-closed `planned` instance. The familiar measure-theoretic theorem says
that a measure-preserving transformation of a finite-measure space returns almost every point of a
measurable set to that set infinitely often. Pinned mathlib contains that route through
`MeasurePreserving.conservative` and `Conservative.ae_mem_imp_frequently_image_mem`. The catalog,
however, does not say whether this discrete theorem is the root; whether it instead asks for
neighborhood recurrence; or whether it asks for an ODE or Hamiltonian corollary requiring a flow,
an invariant finite-measure region, and a checked time-map bridge.

The repository also assigns the identical attribution, date, and gloss to the distinct target
`THM-M-1521`. That target has legacy and provisional rev-5.6 artifacts, but rev-5.6 gives them no
status or proof credit here. An accountable integration reviewer must decide whether the records
are aliases, duplicates with one canonical root, or intentionally distinct specializations before
this target can borrow any scope.

## Formal boundary

`IntakeProbe.lean` elaborates the adjacent pinned conservative and recurrence declarations and the
foreign target's candidate expression type. It states no theorem and imports no foreign target
module. These checks show that a plausible Lean substrate exists; they do not transport it to the
unidentified `THM-M-1376` root or perform the downstream anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a classical theorem family and human-source lead are known; no usable exact formal
artifact is credited for the unidentified root, even though a foreign candidate expression and the
required mathlib interfaces are discovery leads; and no source-faithful reconstruction can attach
to an unfrozen root. All six downstream tasks remain open. Neither audit completion nor theorem
completion is claimed.
