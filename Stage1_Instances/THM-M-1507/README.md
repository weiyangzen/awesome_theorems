# THM-M-1507 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `拉格朗日对偶` (Lagrangian
duality). The repository catalog gives only the gloss `约束优化的对偶问题` (the dual problem of
constrained optimization), attributes the entry to Joseph Lagrange and 1762, and labels it
`已验证`. Those are untrusted discovery metadata: they provide no citation, objective, constraint
model, assumptions, mathematical conclusion, proof, or formal artifact.

The title and gloss identify a broad theorem family rather than one proposition. They do not say
whether the target is the construction of a Lagrangian and dual problem, weak duality, strong
duality under a constraint qualification, dual attainment, or an optimality/saddle-point result.
Selecting any one would manufacture missing mathematics. The intake therefore freezes the
ambiguity boundary, not an exact mathematical or Lean statement.

The provisional root is `[H5, M4, R4]`. `H5` classifies this catalog entry as not yet a stable
proposition; it does not say that standard Lagrangian-duality results are false or open. `M4`
records that no source-identical usable formal artifact can be selected before the proposition is
fixed. `R4` records that no source-faithful proof reconstruction exists.

`IntakeProbe.lean` elaborates only pinned dual-cone and separation APIs. Mathlib's own module notes
say primal and dual cone programs and their weak and strong duality theorems are future work.
Those APIs establish feasibility context, not statement or proof credit for this target. The
lifecycle remains `planned`; every downstream task is open, and neither audit completion nor
theorem completion is claimed.

See `scope-map.md`, `source-statement-crosswalk.md`, and `validation.md` for the exact boundary and
self-test evidence.
