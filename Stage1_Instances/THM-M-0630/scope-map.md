# Scope map

## Preserved catalog scope

The intake preserves the classical Stone-Cech compactification family indicated jointly by the
title, Stone/Cech attribution, year 1937, and gloss "the greatest compactification of a completely
regular space." The likely modern components, none yet credited as the canonical theorem, are:

- a source-selected completely regular/Tychonoff space `X`;
- a compact Hausdorff space containing `X` as a dense embedded subspace;
- extension of continuous maps from `X` to compact Hausdorff targets; and
- a greatestness or universal property expressed by a factor map from the Stone-Cech space to every
  competing compactification, with the source-selected uniqueness convention.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved source:

1. Whether "completely regular" includes T0, T1, Hausdorff, or no separation axiom.
2. Whether a compactification is a compact or compact Hausdorff carrier and whether its unit is an
   embedding, dense embedding, or merely a continuous map with dense range.
3. The competitor package and direction of the compactification preorder behind "greatest."
4. Whether the root is existence, a greatest-element assertion, a continuous-extension property,
   a unique-extension property, an adjunction, or a checked conjunction of these.
5. Whether maps are bundled continuous maps or functions plus `Continuous`, and whether factor-map
   equality is function equality, pointwise equality, or a commuting-triangle equation.
6. The universe policy for compact Hausdorff targets and whether universe lifting is required.
7. The exact edition, theorem/page, incorporated definitions, proof boundary, corrections, errata,
   translation, and reconciliation of the Stone and Cech source roles.
8. The foundation, classical-choice, TCB, and computation policies.

These are statement-resolution tasks, not assumptions silently supplied by this intake.

## Degenerate and mutation cases

Source review must explicitly dispose of empty and singleton spaces, already compact Hausdorff
spaces, discrete spaces, completely regular spaces lacking T0/T1, non-Hausdorff spaces, empty
competitor carriers, and competing maps whose ranges are not dense. Statement mutations must also
test removal of complete regularity or separation, replacement of compact Hausdorff by compact,
reversal of the factor-map direction, loss of extension uniqueness, and changed universe scope.
No case is silently excluded at intake.

## Neighbor and substitution exclusions

- `THM-M-0620` separately owns Tychonoff's product theorem; it may support construction but cannot
  substitute for this compactification root.
- `THM-M-0629` separately owns the one-point compactification; its local-compactness conditions and
  one-point boundary are not this greatest compactification claim.
- `THM-M-0628` names local compactness, which is neither the intended domain condition nor a
  replacement for complete regularity.
- The reflection of an arbitrary topological space into compact Hausdorff spaces is not silently
  called a compactification when its unit is not injective.
- The ultrafilter compactification of a discrete type, the one-point compactification, and a mere
  construction of `StoneCech X` do not alone express greatestness for a source-selected
  compactification order.
- The catalog's `已验证` label, a structure containing the desired factor map, or a hypothesis that
  assumes the universal property supplies no proof credit.

## Formal boundary

Pinned mathlib provides a compact Hausdorff `StoneCech X`, a continuous unit with dense range, a
unique continuous extension into every compact Hausdorff target, dense inducing/embedding results
under complete-regularity/T3.5 assumptions, and a categorical hom-set equivalence. These strong
interfaces justify `M3`, but the canonical expression, minimal imports, environment and expression
fingerprints, checked source transport, mutations, terminal-body provenance, and trust closure
belong to later nodes.
