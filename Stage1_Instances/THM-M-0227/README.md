# THM-M-0227 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Riemann mapping theorem. The
repository gives Bernhard Riemann, the year 1851, and only the gloss "a simply connected domain is
conformally equivalent to the unit disk." Its catalog label `已验证` ("verified") is untrusted
metadata under rev-5.6 and supplies no human-source or Lean proof credit.

The gloss identifies a classical theorem family, but it omits proposition-changing hypotheses and
conventions. The usual planar theorem requires a nonempty simply connected proper open subset of
the complex plane and concludes the existence of a biholomorphic map to the open unit disk. The
catalog does not say whether "domain" already includes open and connected, whether the whole plane
is excluded, whether the ambient space is the complex plane or the Riemann sphere, whether
"conformal equivalence" requires holomorphicity of both directions, or whether a normalized
uniqueness clause is part of the target. Choosing these details at intake would silently strengthen
or alter the received statement.

This intake therefore freezes the theorem-family boundary and the decisions required for a later
exact statement, while leaving the canonical mathematical and Lean statements null. The
provisional root vector is `[H1, M4, R3]`: a historically proved theorem family is recognizable,
the exact source statement and assumptions are not yet audited, no usable exact Lean artifact has
been located, and only a scoped route explanation exists.

The structured authority is `instance.json`. `scope-map.md` records inclusions, ambiguities, and
prohibited substitutions. `source-statement-crosswalk.md` maps each catalog phrase to the
mathematical and Lean decisions still requiring review. All six downstream phases remain open in
`task-dag.json`. `IntakeProbe.lean` checks only adjacent pinned APIs and states no target theorem.
No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
