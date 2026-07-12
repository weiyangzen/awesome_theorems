# THM-M-1397 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Adams方法`
(Adams method). The catalog supplies only that name, an attribution to John Couch Adams, the year
1883, and the gloss `多步数值方法` (multistep numerical methods). It supplies no cited proposition,
formula, assumptions, conclusion, or proof source. Its `已验证` status is explicitly untrusted
metadata under rev-5.6.

"Adams method" names a family of algorithms and results, not one binder-complete theorem. It can
refer to the explicit Adams-Bashforth recurrence, the implicit Adams-Moulton recurrence, a
predictor-corrector iteration, coefficient derivation by interpolation, an order or local-error
formula, consistency and convergence, zero-stability or absolute stability, or a variable-step
procedure. These readings require different hypotheses and conclusions. Selecting one from memory
would silently substitute a new theorem for the repository target.

Encyclopedia of Mathematics, permanent revision 45150 of "Adams method," was inspected as a
source-family discriminator. It separately presents explicit extrapolation, implicit
interpolation, predictor-corrector iteration, an asymptotic error claim, a stability example, and
comments identifying Adams-Bashforth and Adams-Moulton subfamilies. The catalog neither cites this
entry nor chooses one of those claims, so none is accepted as the root.

The provisional root vector is `[H5, M4, R4]`. `H5` records that the supplied method name and gloss
are not yet a stable truth-valued proposition; it does not say that standard Adams-method results
are false or open. `IntakeProbe.lean` checks only pinned interpolation, interval-integration, ODE,
and finite-sum interfaces adjacent to a future encoding. It states no Adams theorem and receives no
statement or proof credit.

The structured scope authority is `instance.json`; the open work queue is `task-dag.json`; exact
self-test commands and boundaries are in `validation.md` and `intake-receipt.json`. No canonical
Lean expression, H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
