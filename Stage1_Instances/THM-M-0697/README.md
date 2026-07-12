# THM-M-0697 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "first-order
logic completeness". The ordinary mathematical reading is the completeness direction from
semantic consequence to derivability: for a first-order theory `T` and sentence `phi`, if every
model of `T` satisfies `phi`, then `phi` has a formal derivation from `T` in a fixed sound proof
calculus.

That reading is not yet an exact theorem statement. The repository source gives no language,
proof calculus, consequence convention, treatment of arbitrary versus finite assumptions, or
primary-source theorem locator. These choices affect both the proposition and its Lean encoding.
Intake therefore records the common theorem family while leaving the canonical claim and formal
target open rather than silently selecting a calculus.

Pinned mathlib supplies first-order syntax, semantics, model satisfaction, semantic consequence,
and compactness. `IntakeProbe.lean` checks only those ingredients. The bounded search found no
first-order derivability relation or theorem connecting semantic consequence to derivability, so
mathlib's compactness theorem is not substituted for the requested completeness theorem.

The provisional root vector is `[H1, M4, R3]`. This dossier claims only a self-tested planned
intake pending master acceptance. It claims no exact statement, source acceptance, formal proof,
audit completion, or theorem completion.
