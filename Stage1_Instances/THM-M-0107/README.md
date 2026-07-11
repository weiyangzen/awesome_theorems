# THM-M-0107 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Zariski's Main Theorem. The legacy label
"properties of birational morphisms" does not determine one exact theorem: several related results
are commonly given this name. This intake therefore freezes the intended root as the modern
factorization form, while leaving exact source acceptance and Lean elaboration to their dependent
phases.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A quasi-finite separated morphism of schemes factors as an open immersion followed by a finite morphism | Provisional mathematical target; ordered Lean binders and expression fingerprint remain open |
| Objects | schemes `X`, `Y`, an intermediate scheme `Xbar`, and morphisms `f`, `j`, `g` | Universe levels and mathlib object names are not frozen |
| Hypotheses | `f : X -> Y` is quasi-finite and separated | Whether quasi-compactness is bundled into the selected quasi-finite API must be checked |
| Conclusion | existence of `Xbar`, `j : X -> Xbar`, `g : Xbar -> Y`, with `j` open, `g` finite, and `f = j ; g` | Equality orientation and categorical composition syntax remain open |
| Related forms | dense-open compactification, finite birational/open-immersion corollaries, local algebra formulations | Candidates only; none may silently replace the factorization root |
| Foundations | Lean 4 kernel, pinned mathlib, category-theory and scheme APIs | Exact toolchain, imports, axioms, and dependency closure remain open |

The proof architecture seed is: normalize morphism predicates; construct the relative affine
spectrum/finite envelope; define the comparison map; prove it is an open immersion; prove the
envelope map finite; verify the factorization. This is an open task map, not a frozen obligation
registry and not proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` records that primary-source
families and a modern statement anchor are identified but the precise edition/page/errata review is
not accepted. `M4` records that no exact Lean declaration has been elaborated. The first failed gate
is the exact-statement gate. The theorem is not complete.

## Validation

The commands and results in `validation.md` establish target membership, standard consistency,
JSON syntax, and dossier-local hygiene only. No Lean theorem or kernel evidence is claimed.
