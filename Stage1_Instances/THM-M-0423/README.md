# THM-M-0423 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Hasse principle. Because an unrestricted
local-global principle is false, the frozen mathematical root is the classical Hasse-Minkowski
theorem for quadratic forms over number fields. The historical Stage1 module is discovery input
only and contributes no accepted statement or proof evidence.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A nondegenerate quadratic form over a number field is isotropic iff it is isotropic over every completion | Prose-level root; exact Lean expression belongs to the dependent statement phase |
| Global objects | Finite-dimensional vector spaces over a number field and nondegenerate quadratic forms | Dimension conventions and the representation of nondegeneracy must be fixed in Lean |
| Local objects | Base change to every archimedean and nonarchimedean completion | Places, completions, scalar extension, and local isotropy require exact object models |
| Directions | Global-to-local base change and local-to-global Hasse-Minkowski implication | Neither direction receives proof credit at intake |
| Excluded claims | Arbitrary varieties, torsors, cubic forms, integral solutions, and unrestricted local-global equivalence | Hasse principles can fail in these settings; each needs a separate theorem and obstruction theory |
| Foundations | Lean 4 kernel, pinned mathlib, and a reviewed classical/choice/quotient policy | Toolchain, imports, axioms, and transitive TCB remain open |

The initial architecture is: freeze number fields and places; define completed scalar extensions;
relate isotropy under base change; cover real, complex, and nonarchimedean places; establish the
Hilbert-symbol/product-formula package; compose the local-to-global implication. This is a scope
map, not a frozen obligation registry.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. Primary sources have been
identified, but edition/page/assumption/errata mapping and independent review are open. No exact
Lean declaration has been accepted. The first failed theorem gate is the exact statement gate, and
the theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish manifest membership, rev-5.6 structural
consistency, valid dossier JSON, reference integrity, and clean whitespace only. They are not Lean
kernel evidence.
