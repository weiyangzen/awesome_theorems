# THM-M-0417 Frozen Obligation Tree

## m0417-root

`M0417-ROOT` is the fingerprinted strict Minkowski target from `Statement.lean`. It retains the
explicit additive fundamental domain and Haar-measure covolume model, strict inequality, central
symmetry, convexity, and nonzero subgroup witness. There are nine required root-relevant
obligations and zero exclusions.

## m0417-s-context

`M0417-S-CONTEXT` owns universes, typeclass assumptions, coercions, the strict boundary, and exact
root identity. `root_exact_type` checks definitional equality between the composition-harness root
and the frozen statement. The compact equality theorem and a `ZLattice` presentation remain
separate encodings and receive no root credit here.

## m0417-n-half-volume

`M0417-N-HALF-VOLUME` is the analytic normalization in upstream lines 70-75. Haar scaling of
`(2^-1) • s` and extended-nonnegative-real arithmetic convert the root threshold into
`mu F < mu ((2^-1) • s)`. This is substantive proof work, not a computation leaf.

## m0417-l-blichfeldt

`M0417-L-BLICHFELDT` is the imported Blichfeldt bridge. Convexity makes the half-body null
measurable; the strict measure bound then yields two distinct lattice translates with nonempty
overlap. The bridge has its own pinned terminal body and must be audited rather than hidden inside
the short Minkowski invocation.

## m0417-c-collision

`M0417-C-COLLISION` owns the witness structure returned by non-disjoint translates: distinct
`x,y : L`, half-body points, and their common translated image. It makes the construction boundary
between Blichfeldt and the final lattice difference explicit.

## m0417-t-difference

`M0417-T-DIFFERENCE` forms `x-y`. Distinctness gives nonzeroness. Rewriting the overlap equation,
central symmetry sends one recovered body point to its negative, and convexity at weights one half
and one half places the difference back in `s`.

## m0417-t-compose

`root_compose` conditionally consumes the half-body volume result, the Blichfeldt collision bridge,
and difference extraction, and produces the exact root without an undeclared premise. Lean checks
this child-to-parent wiring and reports only `propext`, `Classical.choice`, and `Quot.sound` for its
axioms. It does not discharge the three child assumptions. The unique pinned mathlib Minkowski body
is the later proof-phase candidate; the local legacy and Atlas wrappers share its proof-body identity
and do not enlarge any denominator.

## m0417-x-source

`M0417-X-SOURCE` keeps the human-source boundary open. The 1896 monograph and mathlib's Clark
reference are discovery anchors, but exact theorem/page, assumption, edition, errata, and independent
review evidence have not reached H0.

## m0417-x-trust

`M0417-X-TRUST` owns terminal declaration provenance, the complete transitive declaration/import
closure, foundation and axiom comparison, TCB inventory, and independent replay. The anchor audit's
local axiom print is useful but does not close this later validation and release boundary.

This phase freezes architecture, typed edges, exact structured recipes, and semantic ledgers of at
most five steps. The bounds establish decomposition only. H0, M0, R0, audit completion, theorem
completion, release, and master acceptance remain open.
