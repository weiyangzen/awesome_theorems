# THM-M-0278 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Riesz representation theorem.
The repository gives the Chinese gloss `Hilbert空间上线性泛函的表示` (representation of linear
functionals on Hilbert spaces), attributes it to Frigyes Riesz in 1909, and labels it `已验证`.
Under rev-5.6 that label is untrusted catalogue metadata, not a source audit, exact Lean
proposition, or proof receipt.

The gloss identifies the Fréchet-Riesz Hilbert-space theorem family, but it does not say whether
the scalar field is real, complex, or both; whether "linear functional" means algebraic,
continuous, or bounded; how completeness is expressed; which inner-product argument represents
the functional; whether uniqueness and norm preservation belong to the conclusion; or which
degenerate cases are included. Selecting those clauses from convention at intake would silently
strengthen or narrow the received claim.

Pinned mathlib has a direct and strong formal candidate. Module
`Mathlib.Analysis.InnerProductSpace.Dual` describes the Fréchet-Riesz theorem and defines
`InnerProductSpace.toDual`, a conjugate-linear isometric equivalence from a complete real or
complex inner-product space to its strong dual. `IntakeProbe.lean` authenticates that interface,
its representing-vector equation, and an explicit existence-and-uniqueness candidate wrapper.
These are real discovery facts. They are not yet a checked identity with a pinpoint, independently
reviewed human source, so they receive no M0 or H0 credit at intake.

The provisional vector is `[H1, M3, R4]`: the classical theorem family and a modern published
source lead are known but not source-audited; exact pinned interfaces exist but no canonical
source-to-Lean target is frozen; and no source-faithful readable proof reconstruction exists.
`instance.json` is the structured scope authority, while `task-dag.json` keeps all six downstream
phases open. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
