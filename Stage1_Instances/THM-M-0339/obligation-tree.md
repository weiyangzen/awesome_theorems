# THM-M-0339 frozen obligation tree

This version-1 tree is architecture, not proof credit. All 19 obligations remain open. The exact
root is MSS Corollary 1.5; the Kadison-Singer equivalence chain is outside the root.

## Root

`M0339-ROOT` is the exact proposition printed by `Statement.lean`. It requires the terminal
Corollary 1.5 derivation and conditional exact-root assembly.

## S-exact

Freeze `d m r : Nat`, `delta : Real`, positive `r`, nonnegative `delta`, the complex Euclidean
vectors, identity rank-one sum, and pointwise squared-norm bound.

## S-partition

Use `color : Fin m -> Fin r`; its fibers are labeled parts and may be empty.

## S-boundary

Retain `d = 0`, `m = 0`, `delta = 0`, and empty parts. Split `r = 1` from `1 < r`; `r = 0` is
excluded by the frozen hypothesis.

## S-foundation

Lean 4.29.0 and mathlib `8a178386` are pinned. Transitive axioms, dependency trust, and release TCB
review remain open.

## N-operators

Translate source `u_i u_i*` notation to `InnerProductSpace.rankOne C (u i) (u i)`, preserve
positivity, and use the continuous-linear-map operator norm. Pinned mathlib supplies only these APIs.

## B-rone

Prove the one-part case from the identity-sum hypothesis and the frozen numeric bound.

## B-rmany

For `1 < r`, reduce the deterministic partition conclusion to the random-vector theorem via random
labels. This branch carries the substantive MSS architecture.

## C-random

Construct independent uniform labels, place appropriately scaled copies of each `u_i` in block
coordinates, and verify finite support, isotropic expectation, and the expected squared-norm bound.

## C-mcp

Define mixed characteristic polynomials for independent rank-one positive operators and prove the
differential/operator identities required by the MSS argument.

## L-realrooted

Prove the mixed characteristic polynomial is real-rooted and relates its largest root to the sampled
positive operator's spectral norm.

## L-interlacing

Construct the interlacing family and select an outcome whose largest root is no larger than the
largest root of the expectation polynomial.

## L-barrier

Formalize the barrier-function induction that bounds the largest root by `(1 + sqrt epsilon)^2`.

## L-theorem14

Compose the random-vector assumptions, mixed characteristic polynomial, real-rootedness,
interlacing selection, and barrier estimate into MSS Theorem 1.4. This is the frozen critical cut.

## T-cor15

Apply Theorem 1.4 to the random-label construction. Read one successful outcome as the fibers of
`color`, undo scaling, and obtain `(1 / sqrt r + sqrt delta)^2` for every part.

## T-assemble

`ObligationTree.root_compose` checks only that the explicit `PartitionEngine` premise has exactly the
root type. It supplies no proof of that premise.

## X-upstream

The anchor audit found pinned rank-one infrastructure but no target theorem or terminal proof body.

## X-source

The primary source is arXiv:1306.3969v4. Page-level proof-node crosswalk, errata review, and
independent source approval remain open, so all material nodes remain `H1`.

## X-tcb

Release-grade transitive dependency, axiom, executable, SBOM, offline replay, and independent-runner
evidence remains outside this phase.
