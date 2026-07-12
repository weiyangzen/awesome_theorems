# THM-M-0651 rev-5.6 intake

This directory is the `planned` intake dossier for the classical omitting types theorem. The
human-level target is the simultaneous countable version: a consistent theory in a countable
first-order language has a countable model omitting each member of a countable family of partial
types, provided every type is nonprincipal over the theory.

The Stage0 phrase only says "conditions for omitting types in a model" and does not determine a
formal proposition. This intake therefore freezes the intended classical variant while leaving the
precise source edition, definitions, binder order, and Lean expression to the statement phase. The
single-type complete-theory version, an uncountable-language theorem, and a theorem that merely
realizes types are not substitutes.

The provisional root vector is `[H1, M4, R3]`. The pinned mathlib tree contains model-theory type
and satisfiability infrastructure, but the scoped repository search found no declaration named or
documented as the omitting types theorem. That observation is discovery evidence only; the formal
anchor audit remains open. No proof state, audit completion, or theorem completion is accepted.

See `scope-map.md` for the mathematical boundary, `source-statement-crosswalk.md` for the source and
encoding decisions, `task-dag.json` for the dependency-ordered open work, and `validation.md` for the
exact intake checks.
