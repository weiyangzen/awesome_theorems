# THM-M-1285 rev-5.6 intake

This directory is the `planned` dossier for Schwarz symmetric decreasing rearrangement. The source
metadata calls it "Schwartz对称化", but the mathematical operation normally used in the PDE and
rearrangement literature is **Schwarz** symmetrization. This correction is provisional until the
source audit; it must not silently turn the entry into a different theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | existence and equimeasurability of the radial decreasing rearrangement of a nonnegative measurable function on Euclidean space | Exact Lean type and equality convention are not frozen |
| Distribution layer | positive superlevel sets and their Lebesgue measures | Strict versus non-strict levels and exceptional levels need mutation tests |
| Geometric layer | centered balls having the same measure as superlevel sets | Ball-radius/generalized-inverse construction is not yet formalized |
| Function layer | radiality, monotonicity in radius, measurability, and equimeasurability of `f*` | Pointwise representative versus a.e. equivalence remains open |
| Exclusions | Pólya-Szegő, Faber-Krahn, Talenti, polarization convergence, signed/complex extensions | These consequences cannot be substituted for the root |
| Foundations | Lean 4 kernel, pinned mathlib measure theory, an accepted classical-choice and a.e.-quotient policy | Toolchain, imports, TCB, and axiom closure remain open |

The manifest's phrase "functions' symmetric rearrangement" names a construction rather than a
unique theorem. The least broadened theorem-shaped reading is existence plus the defining
equimeasurability, radiality, and radial monotonicity properties. The statement phase must either
elaborate that claim exactly or record a source-driven correction; it may not use the nearby
Pólya-Szegő inequality as a replacement.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The human-source wording is too
coarse and possibly misspelled, and no Lean declaration has been identified. The first failed gate
is therefore exact-statement identification/elaboration. No historical "已验证" label is credited, and
the theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish manifest membership, baseline standard
consistency, JSON syntax, and dossier-local integrity only.
