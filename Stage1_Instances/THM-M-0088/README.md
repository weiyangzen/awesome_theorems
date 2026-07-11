# THM-M-0088 rev-5.6 intake

This is the `planned` dossier for the Yoneda embedding. It does not inherit proof credit from the
legacy `S1_M_137.lean` file or from the source label `已验证`.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | For every `C : Type u` with `[Category.{v} C]`, `yoneda : C ⟶ (Cᵒᵖ ⟶ Type v)` is fully faithful | Exact elaboration and fingerprints belong to the statement phase |
| Embedding meaning | Fullness, faithfulness, and the induced equivalence on every hom-set | Candidate consequences; none credited yet |
| Object model | Locally small Lean categories and contravariant `Type v`-valued presheaves | No preadditive, abelian, triangulated, or derived structure is assumed |
| Variants | Universe-raised Yoneda and co-Yoneda | Alternate targets requiring explicit checked relationships |
| Collateral | Yoneda lemma, naturality formulas, exactness and long exact sequences | Not part of this root; later work must not broaden the theorem |
| Foundations | Lean 4 kernel and versioned mathlib dependency | Toolchain, import, axiom, and TCB fingerprints remain open |

The root's intended force is fully faithful, not merely faithful and not essential surjectivity onto
the whole presheaf category. The source-to-formal distinctions are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the Lean statement gate: the normalized expression hash, environment fingerprint, checked
transports, and mutation results do not yet exist. The theorem is not complete.

## Validation

The commands and exact outcomes in `validation.md` establish manifest membership, standard
consistency, JSON syntax, and dossier hygiene only. They do not provide kernel evidence.
