# THM-M-0660 rev-5.6 intake

This directory is the `planned` dossier for the repository label **主公式定理** (literally,
"main formula theorem"). The inherited gloss says only "the existence of a main formula in a
stable theory." It does not define *main formula* or cite a source, so this intake deliberately does
not guess a standard model-theory theorem or manufacture a Lean proposition.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | The exact repository phrase: existence of a main formula in a stable theory | Mathematical referent and primary source unresolved |
| Ambient objects | A first-order language, theory, models/types, formulas, and a stability predicate are expected discovery surfaces | Signatures, arities, parameters, cardinal assumptions, and universes cannot yet be fixed |
| Result object | Whatever the source means by `主公式` | No translation such as fundamental formula, defining formula, or canonical formula is accepted |
| Lean target | Lean 4 plus pinned mathlib | No declaration/expression may be chosen before source identification |
| Proof architecture | syntax -> semantics/types -> stability hypothesis -> source-specific construction -> existence | Architecture is provisional discovery scope, not a frozen obligation registry |
| Foundations | Lean kernel and an explicit later policy for classical logic/choice/quotients | Profile, toolchain, imports, and environment fingerprint remain open |

The Stage0 attribution to Saharon Shelah and the year 1978 are unreferenced metadata, not evidence.
The legacy status `已验证` is explicitly untrusted under rev-5.6 and supplies no proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H5, M4, R4]`. The first failed gate is primary
source identification, which also blocks exact-statement freeze. The next phase must locate a
primary source whose statement unambiguously matches the Chinese label, then record edition,
theorem/page, definitions, assumptions, and errata before proposing a Lean target. The theorem is
not complete.

## Validation

The exact commands and results in `validation.md` establish manifest membership, standard
consistency, JSON syntax, and dossier-local integrity only. They do not validate a theorem statement.
