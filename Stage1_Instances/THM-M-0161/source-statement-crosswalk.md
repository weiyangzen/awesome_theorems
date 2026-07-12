# Source-statement crosswalk

## Repository record

The repository inventory names `曲线论基本定理`, dates it broadly to the nineteenth century, and
glosses it as "a space curve is determined by curvature and torsion." It attributes the result to
multiple mathematicians and labels it `已验证`. Under rev-5.6 this is untrusted discovery metadata:
it does not identify a proposition, proof, formal declaration, or accepted validation result.

## Candidate proof sources

- Manfredo P. do Carmo, *Differential Geometry of Curves and Surfaces*, Prentice-Hall (1976), the
  curves chapter's section on the fundamental theorem of the local theory of curves. This is a
  stable published proof-source candidate for prescribed positive curvature and torsion, existence,
  and uniqueness up to a rigid motion.
- Dirk J. Struik, *Lectures on Classical Differential Geometry*, second edition, Dover (1988), the
  local theory of curves. This is a candidate independent exposition against which conventions can
  be checked.

These books are discovery anchors, not `H0` evidence. This intake did not pin or independently
inspect a specific scan/printing. The statement phase must record the selected edition's exact
theorem and page, verbatim assumptions, surrounding definitions, and known errata. It must also
resolve whether the source says "rigid motion" with an orientation convention strong enough to
preserve signed torsion.

## Statement crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "space curve" | sufficiently smooth curve in oriented Euclidean `R^3` | interval-valued map into `EuclideanSpace Real (Fin 3)` or source-equivalent concrete type | family included; encoding open |
| "curvature" | prescribed function `kappa` with `kappa(s) > 0` | derivative-based curvature predicate and pointwise positivity | positivity included; regularity open |
| "torsion" | prescribed signed torsion `tau` | triple-product/Frenet definition with orientation fixed | included; convention open |
| "determined" | uniqueness modulo a proper rigid motion | existence of translation and orientation-preserving orthogonal linear isometry relating two curves | intended relation frozen; exact source wording open |
| fundamental theorem | existence as well as uniqueness | construction of a unit-speed curve plus congruence theorem | included; repository gloss omits existence |
| arc length | common parameter `s` has speed one | derivative norm equals one on the interval | included; endpoint convention open |
| positive curvature | Frenet normal is defined everywhere | nonvanishing/positive curvature hypothesis | proposition-critical; must be mutation-tested |

## Source and machine boundary

A repository-wide search found no theorem-specific artifact for `THM-M-0161` and no local occurrence
of the English theorem name. A narrow text search of the pinned mathlib tree found no differential-
curve use of `curvature`, `torsion`, or `Frenet`; the returned `torsion` declarations concern
algebraic torsion or the torsion tensor of a covariant derivative, not curve torsion. This is intake
discovery evidence only, not the immutable exhaustive anchor audit required by the later phase.

Before `H0`, an independent reviewer must verify the selected source edition, locator, definitions,
every assumption, both existence and uniqueness, orientation/reflection behavior, and errata, then
approve the source-to-Lean mapping. Before any statement or machine credit, the exact target must
elaborate under pinned imports and checked transports must cover any split existence/uniqueness
encoding. No source identified here is claimed to provide a Lean proof.
