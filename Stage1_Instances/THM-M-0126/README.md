# THM-M-0126 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the source label "Shimura curve theorem".
It inherits no proof credit from the legacy Stage1 module or from the source metadata label.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Human claim | The manifest wording "modular curve over a quaternion algebra" | The wording does not identify a field, order, level, moduli problem, or a single theorem |
| Arithmetic data | Quaternion algebra, an order, and level data | Maximal/Eichler conditions and admissibility assumptions are not supplied by the source record |
| Moduli data | A precisely specified moduli functor and topology | Objects, morphisms, equivalence relation, and representability claim remain to be sourced |
| Geometric result | Existence of a representing curve and its stated properties | Base, dimension, smoothness, properness, and compact/noncompact cases are unresolved |
| Lean discovery surface | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_045.lean` | Its `QuaternionicModuliStatementShape` is a discovery artifact, not the frozen source theorem |
| Foundations | Lean 4 kernel and pinned mathlib | Exact toolchain, imports, TCB, and computation profiles belong to later phases |

The anticipated architecture is arithmetic datum -> moduli problem -> local/descent conditions ->
representability -> curve properties. This is only a scope map. No obligation registry or proof
coverage is frozen at intake.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is source
identification: the repository source supplies only a short topic label, so choosing one of the
several inequivalent Shimura-curve theorems would broaden or substitute the claim. The dependent
statement phase must remain blocked until a primary source and pinpoint theorem are selected by the
authoritative lane. The theorem is not complete.

Validation commands and their exact outcomes are recorded in `validation.md`.
