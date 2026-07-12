# THM-M-0769 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the axiom of choice. The repository
claim is: "every family of nonempty sets has a choice function." `Statement.lean` now freezes its
ordinary indexed-family meaning over `Sort` universes as
`Stage1Instances.THM_M_0769.AxiomOfChoiceTarget`.

The claim is foundational rather than a theorem derivable in a choice-free base. Lean exposes
`Classical.choice` as an axiom and `Classical.axiomOfChoice` as its dependent-family formulation.
The statement artifact elaborates with the pinned toolchain, checks its pointwise transport, and
distinguishes removed-hypothesis, domain, binder-scope, and boundary mutations. It deliberately
does not use those APIs as proof evidence or complete the anchor-audit, proof, validation, or
release phases. The obligation-tree phase additionally freezes a nine-node denominator and seven
separate typed graphs. `ObligationTree.lean` checks the conditional composition from a dependent
fiber selector to the exact root, but deliberately leaves that selector as an open premise.

The intake root remains `[H2, M3, R4]`: statement/interface work does not promote machine closure,
and the primary-source edition/page/translation review remains open. Intake evidence is in
`validation.md`; exact statement commands and results are in `statement-validation.md`, and the
architecture boundary is recorded in `obligation-tree-validation.md`.
