# THM-M-0556 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Leray-Serre spectral
sequence target. The generated source phrase, "the spectral sequence of a
fibration", does not determine a single theorem: homology versus cohomology,
coefficients, local coefficient systems, convergence, and multiplicative
structure all change the claim. Intake therefore freezes that phrase as the
source claim and records the unresolved choices rather than silently selecting
a convenient formal theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Existence and convergence of a spectral sequence associated to a fibration | The exact proposition is blocked until variance, coefficients, hypotheses, pages, and convergence are fixed |
| Geometric input | A fibration `F -> E -> B`, including the fibre and base action on fibre (co)homology | The repository source does not specify the model of fibration or connectedness hypotheses |
| Algebraic output | Bigraded pages, differentials, page transitions, and an abutment filtration | No page convention or convergence notion is credited |
| Coefficient branch | Constant coefficients and the local-coefficient system induced by monodromy | Ring/module assumptions and trivial-action specializations remain open |
| Naturality | Maps of fibrations and induced morphisms of spectral sequences | Candidate proof architecture only |
| Multiplicative branch | Products and compatibility with the abutment, if intended | Excluded from the root until the human statement is clarified |
| Formal system | Lean 4 plus pinned mathlib | Exact imports, toolchain fingerprint, and declaration remain for the statement phase |

The provisional theorem-tree scope is: fibration data; filtration/model
construction; exact-couple or filtered-complex spectral-sequence construction;
identification of the early page; convergence/abutment; and naturality. These
are scope nodes, not accepted proof obligations or proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first
failed theorem gate is exact-statement identity: the source record is too terse
to choose one canonical Lean proposition without broadening or substituting
the theorem. The dependent statement phase must resolve this explicitly. No
Lean declaration or theorem completion is claimed.

## Validation

The commands and exact results for this intake are recorded in
`validation.md`. They validate target membership, repository structure, JSON
syntax, and local dossier hygiene only. Master acceptance remains outstanding.
