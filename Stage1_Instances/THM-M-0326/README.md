# THM-M-0326 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the theorem commonly summarized as
"nuclear spaces have the approximation property." It inherits no proof credit from the legacy
`S1_M_215.lean` artifact or from the manifest's untrusted source-status label.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Every nuclear locally convex space has the approximation property | The precise separation, completeness, and scalar-field conventions require primary-source audit |
| Nuclearity | Grothendieck nuclear locally convex spaces, not merely a normed identity decomposition | A canonical Lean object model has not been selected |
| Approximation property | Identity lies in the closure of finite-rank continuous endomorphisms for uniform convergence on compact sets | Net/filter encoding and topology must be frozen and elaborated in the statement phase |
| Scalars | Real and complex cases are intended candidates | Whether a single `RCLike` target exactly represents the source remains open |
| Legacy Lean surface | `AwesomeTheorems.Stage1.S1_M_215.StatementShape` and its supporting definitions | Discovery input only; its custom hypotheses are not accepted as the source theorem |
| Special cases | Finite-dimensional spaces and normed nuclear-decomposition truncations | Supporting branches only; they cannot close the locally convex root |
| Foundations | Lean 4 kernel and pinned mathlib with an explicit classical/choice/quotient policy | Exact environment and TCB fingerprints remain open |

The canonical human claim, candidate domains, ordered binders, boundary cases, and provisional Lean
surface are recorded in `intake.json`. Source fidelity and the unresolved ambiguity between the
classical locally convex theorem and the legacy normed surrogate are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact-statement gate: the primary-source theorem/page and conventions have not been independently
audited, and no canonical Lean expression or environment fingerprint has been accepted. This intake
does not claim theorem completion.

## Validation

The commands and exact outcomes in `validation.md` establish target membership, rev-5.6 structural
consistency, valid dossier JSON, and local reference integrity only. No Lean proof is introduced by
this phase.
