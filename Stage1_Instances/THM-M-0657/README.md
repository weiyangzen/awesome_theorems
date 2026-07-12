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

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

Only `S56-M-0657-INTAKE` is addressed here. The dependent statement phase must
choose exact syntax/semantics/cardinal APIs, elaborate the proposition with
minimal pinned imports, settle the source conventions, fingerprint the
environment, and run the required mutations before proof discovery receives
credit.

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R3]`.
The first open theorem gate is the Lean statement gate. No accepted proof
state, audit completion, theorem completion, or master receipt is asserted.
The commands in `validation.md` validate only membership and dossier
structure.
