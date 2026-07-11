# THM-M-1061 rev-5.6 intake

This is the `planned` intake for Varadhan's integral lemma. The Stage0 phrase
"Laplace principle" is too short to determine a formal proposition by itself. This
intake freezes the standard bounded-continuous integral lemma, not an equivalence
between an LDP and a Laplace principle and not an unbounded-function extension.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Ambient space | regular topological measurable space adequate for the LDP bounds and compactness argument | exact mathlib typeclasses are not selected |
| Probabilistic input | probability measures with a full LDP and good rate function at vanishing positive speed | weak-LDP and exponential-tightness transports are separate obligations |
| Test function | bounded continuous real-valued `F` | unbounded variants require an additional tail/moment hypothesis |
| Root result | logarithmic exponential-integral limit equals `sup_x (F x - I x)` | extended-real codomain and empty/infinite conventions remain statement work |
| Proof architecture | compact-sublevel upper bound, local LDP lower bound, tail control, passage to supremum | no leaf or terminal theorem is credited |
| Formal surface | future Lean 4 target using pinned mathlib measure, topology, and asymptotic APIs | no declaration has been found or elaborated in this phase |

The canonical binders, hypotheses, exclusions, conventions, and alternate encodings
are recorded in `intake.json`. Source-to-claim correspondence and its remaining
audit debt are recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed
theorem gate is the exact Lean statement gate: there is no selected declaration,
normalized expression, environment fingerprint, transport proof, or mutation test.
The source anchors are discovery-quality rather than accepted H0 receipts. The
theorem is not complete.

## Validation

The exact local checks and results are recorded in `validation.md`. They validate
manifest membership, repository-standard consistency, JSON syntax, and dossier
references only.
