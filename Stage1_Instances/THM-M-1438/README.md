# THM-M-1438 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Lanford证明` (Lanford proof). The catalog gloss, `Feigenbaum猜想的计算机辅助证明`
("computer-assisted proof of the Feigenbaum conjecture(s)"), identifies a proof program but not
one truth-valued proposition with fixed definitions, ordered binders, hypotheses, and conclusion.
The catalog value `已验证` is untrusted metadata under rev-5.6 and supplies neither human-source
nor Lean proof credit.

The likely primary source is Oscar E. Lanford III's 1982 announcement, "A computer-assisted proof
of the Feigenbaum conjectures." It announces a proof of "essentially all" of a family of
conjectures and states several distinct results: existence and analyticity of a renormalization
fixed point, hyperbolicity of its derivative, an unstable-manifold intersection with the simple
period-doubling surface, and a transverse stable-manifold crossing for the quadratic family. The
screened row does not select one result or their conjunction. These candidate clauses cannot be
silently merged into a convenient theorem.

This intake therefore freezes the source-suite ambiguity rather than manufacturing a canonical
claim. The provisional root vector is `[H5, M4, R4]`: `H5` classifies the catalog proof-description
as not yet a stable proposition, not Lanford's published results as false; `M4` records that no
exact usable Lean target or proof artifact is credited; and `R4` records that no readable proof
reconstruction can attach to an unidentified root.

The structured authority is `instance.json`. `scope-map.md` records the permitted boundary and
prohibited substitutions, while `source-statement-crosswalk.md` maps the repository wording to the
primary-source clauses and the decisions still required. All six downstream phases remain open in
`task-dag.json`. `IntakeProbe.lean` checks only adjacent pinned analytic, fixed-point, compact-
operator, and spectral APIs; it states no target theorem. Exact validation commands and limits are
recorded in `validation.md` and the provisional `intake-receipt.json`.

No H0, M0, R0, accepted proof state, audit completion, theorem completion, accepted receipt, or
master acceptance is claimed.
