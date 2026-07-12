# THM-M-0657 rev-5.6 intake dossier

This is the `planned` rev-5.6 instance for Morley's categoricity theorem. The
repository describes the target only as "characterization of uncountably
categorical theories." The frozen root uses the standard transfer theorem:
a first-order theory in a countable language that is categorical in one
uncountable cardinal is categorical in every uncountable cardinal. The
metadata label `已验证` is untrusted discovery input and gives no proof credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Transfer from categoricity in one uncountable cardinal to every uncountable cardinal | The exact Lean expression belongs to the statement phase |
| Language and theory | First-order theories in countable languages | Countability encoding and any explicit completeness assumption require source audit |
| Categoricity | Existence plus uniqueness up to structure isomorphism at a cardinal | The Lean definition must rule out vacuous categoricity |
| Cardinal range | One uncountable source cardinal and every uncountable target cardinal | Finite and countably infinite targets are excluded |
| Mathematical architecture | Definitions/source alignment, structural analysis, target-cardinal existence, uniqueness, and transfer recomposition | These are scope nodes, not a frozen obligation registry or proof claims |
| Lean surface | Lean 4 with repository-pinned mathlib | No suitable model-theory API, module, declaration, expression hash, or environment fingerprint is claimed yet |
| Foundations | Later explicit classical choice, quotient, cardinal-arithmetic, and TCB profiles | No axiom or imported result is credited at intake |

The canonical claim, ordered binders, exclusions, candidate alternate
encodings, and provisional debt vector are authoritative in `intake.json`.
The relationship between repository wording and the primary paper is recorded
in `source-statement-crosswalk.md`.

## Statement phase

The exact target now elaborates as
`Stage1Instances.THM_M_0657.MorleyCategoricityTarget` in `Statement.lean`.
`statement.json` freezes its expression and environment fingerprints, explicit
nonvacuous categoricity convention, checked existential-source transport,
mutations, and boundary probes. This remains statement-only work at `M3` and
does not supply a proof of Morley's theorem.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

`S56-M-0657-INTAKE` and the provisional worker statement node are addressed.
Master acceptance is still required. Anchor audit and all later phases remain
open.

## Intake verdict

Lifecycle is `planned`; the provisional root vector after statement
elaboration is `[H1, M3, R3]`. No accepted proof state, audit completion,
theorem completion, or master receipt is asserted. `validation.md` remains the
intake record; `statement-validation.md` records the scoped Lean evidence.
