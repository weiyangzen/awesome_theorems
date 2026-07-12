# THM-M-0540 rev-5.6 statement dossier

This directory is the `planned` intake for singular homology. The Stage0 phrase names a theory or
construction rather than a single theorem, so the dossier freezes the intended mathematical scope
without pretending that an exact terminal proposition has already been supplied.

The statement phase selects ordinary, unreduced singular homology with integer coefficients. For
each small topological space `X` and `n : Nat`, the canonical target identifies mathlib's integral
singular-homology functor value with degree-`n` homology of its integral singular chain complex.
[`statement.json`](statement.json) freezes the binders, exclusions, profiles, expression, checked
alternate encoding, environment, and mutation results.

`Statement.lean` elaborates with the pinned toolchain and three minimal imports. Its definitional
witness confirms that the two mathlib views cohere, but this statement-phase witness is not proof
credit for the later proof phase. The provisional root vector remains `[H1, M3, R4]`. No H0 source
audit, accepted proof state, audit completion, or theorem completion is claimed.

The obligation-tree phase freezes nine semantic obligations in `obligation-registry.json` and
stores separate typed graphs in `typed-graphs.json`. `ObligationTree.lean` checks only the exact
child-to-root composition. The audited `rfl` definition remains the open proof-phase obligation
`M0540-T-UNFOLD`, so the accepted root remains open.
