# THM-M-0454 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label
"Shafarevich-Tate group". The source row names a mathematical object, not a proposition, and does
not say which abelian variety, global field, or property is intended. Intake therefore preserves
that ambiguity instead of inventing a theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source record | Stage0 label `椭圆曲线的Tate-Shafarevich群` and untrusted status `已验证` | The status supplies no claim or proof citation |
| Mathematical object | The usual Shafarevich-Tate group associated to an elliptic curve over a global field | A definition is not substituted for the missing theorem |
| Exact root | Not identifiable from repository source metadata | Statement phase is blocked until an authoritative proposition is selected |
| Plausible claims | Kernel/local-triviality definition, torsor interpretation, finiteness conjecture, duality, or a computation for a specified curve | These are mutually different targets; none is credited |
| Domain | Elliptic curve/abelian variety and global field with completions/places | Exact domains and ordered binders remain open |
| Lean surface | Lean 4 plus pinned mathlib | No declaration or expression is claimed at intake |
| Foundations/TCB | rev-5.6 Lean kernel policy | Exact toolchain, imports, axioms, and dependency closure remain open |

## Intake verdict

Lifecycle remains `planned`; provisional root vector is `[H5, M4, R3]`. The first failed gate is
the exact human statement gate: the repository gives only an object name. This dossier claims no
source fidelity, Lean elaboration, machine proof, or theorem completion. The next phase must not
choose among the candidate claims without an authoritative source amendment or independently
reviewed scope decision.

## Validation

The exact structural and dossier checks are recorded in `validation.md`. They validate this intake
artifact, not the unnamed theorem.
