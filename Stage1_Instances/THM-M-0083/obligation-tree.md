# THM-M-0083 frozen obligation tree

The frozen architecture separates the two directions of the universal-element
criterion and exposes both pinned mathlib bridges used by each direction. This
prevents the short exact wrapper from hiding its imported proof boundaries.

## M0083-ROOT

The exact `RepresentableFunctorTarget`. It requires `M0083-T-ASSEMBLE` and has
candidate `M0-W` kernel evidence, but no master acceptance or release receipt.

## M0083-S-DEFINITIONS

Freeze contravariance, `f.op`, evaluation at the selected element, bijectivity,
and the meanings of `IsRepresentedBy` and `IsRepresentable`.

## M0083-S-BOUNDARY

Keep empty categories in scope. `empty_category_boundary` checks that both
sides are false without adding a nonemptiness premise.

## M0083-S-FOUNDATION

Audit the observed `propext`, `Classical.choice`, and `Quot.sound` boundary and
the full Lean, mathlib, kernel, dependency, and no-oracle policy.

## M0083-N-REPRESENTED

`isRepresentedBy_iff` expands a selected element's representation property to
bijectivity of the evaluation map for every object.

## M0083-L-EXISTS

`IsRepresentable.iff_exists_isRepresentedBy` supplies and consumes the object
and element witnesses. This central imported result remains its own obligation.

## M0083-B-FORWARD

`forwardPackage_mathlib` converts a universal element into an
`IsRepresentedBy` witness and then a proof of representability.

## M0083-B-REVERSE

`reversePackage_mathlib` extracts a representing object and element and uses
the represented-by expansion to recover all required bijections.

## M0083-T-ASSEMBLE

`root_of_direction_packages` consumes both directed packages and yields the
exact iff. `representableFunctorTarget_mathlib` checks the complete composition.

## M0083-X-SOURCE

Primary human-source theorem/page/assumption/errata mapping remains a later
source-audit obligation and carries no machine-proof credit.

## M0083-X-PROVENANCE

Transitive wrapper/body identity, imports, axioms, TCB, replay, and independent
verification remain later release obligations and cannot close proof edges.

All leaf budgets are at most 40. These are decomposition thresholds, not proof
quality or readability evidence. The registry contains 11 unique semantic
obligations; aliases and wrappers add no duplicate coverage credit.
