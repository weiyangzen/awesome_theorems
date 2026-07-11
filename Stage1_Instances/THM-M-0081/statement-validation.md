# Statement-phase validation

The canonical target is `Stage1Instances.THM_M_0081.CanonicalTarget` in
`CanonicalStatement.lean`. Its only direct import is `Mathlib.CategoryTheory.Yoneda`; this is the
smallest repository-pinned module that directly supplies `CategoryTheory.yoneda` and the category
objects used by the target. Import minimality here means direct Lean imports, not the transitive
dependency closure of that mathlib module.

The binder order is `C`, its category instance, then `X Y`. Universes are explicit as `v u`:
`C : Type u`, `[Category.{v} C]`, and each representable has codomain `Type v`. The exact target is

```lean
Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y)
```

This is statement elaboration only. It assigns no proof credit, performs no anchor/provenance
audit, and does not claim H0, M0, audit completion, theorem completion, or master acceptance.

## Commands and results

Base revision: `c2687431b1d86bac7bd509c9abbfdc1e763c060c`.

The reused `Formalizations/Lean/.lake` resolves to the canonical pinned artifact directory; it was
not modified, updated, fetched, cloned, or rebuilt by this work.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0081/CanonicalStatement.lean` | exit 0; printed `CanonicalTarget.{v, u} ... : Prop` |
| `python3 -m json.tool Stage1_Instances/THM-M-0081/statement.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0081` | exit 0; rank 138, planned, theorem completion false |
| `git diff --check -- Stage1_Instances/THM-M-0081 .stage1-worker-selftest.json` | exit 0; no output |

The Lean source fingerprint is
`sha256:3f001ed0951c69caa05b5793ee91d4f6b9484e4c3a8ca75499e0a14a4bf34b75`.

Known downstream failures remain the exact primary-source pagination and errata audit, immutable
mathlib anchor/proof-body provenance, frozen obligation graphs, proof validation, hermetic replay,
independent verification, and master acceptance. These do not invalidate statement elaboration,
but they prevent any theorem-completion claim.
