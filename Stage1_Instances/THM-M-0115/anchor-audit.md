# THM-M-0115 Anchor Audit

## Decision

The bounded immutable inventory contains no valid Lean 4 proof anchor for the
frozen Grothendieck-Riemann-Roch target. The root remains `H4 / M3 / R4`.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
provides the scheme, over-base, smooth, proper, quasi-affine, sheaf-module,
quasi-coherent, sheaf-cohomology, derived-category, and generic commutative-
monoid group-completion APIs checked by `AnchorAudit.lean`. These are useful
object-model surfaces, but none is scheme `K_0`, rational Chow homology, either
required proper pushforward, a Chern character, algebraic tangent/Todd data,
cap product, or GRR. In particular, `Scheme.Modules.pushforward` is ordinary
sheaf direct image, `Sheaf.H` is not Chow homology, `IsQuasiAffine` is not
quasi-projectivity, and `Algebra.GrothendieckGroup` has no exact-sequence or
scheme connection.

The only public Lean 4 declaration with the GRR name found by the bounded
Sourcegraph audit is
`GRR.grothendieck_riemann_roch` in
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`.
Its body is literally `by sorry`, and `grr_trivial_todd` depends on it. Its
abstract input also omits the frozen scheme/base/smooth/quasi-projective/cap
surface. Matching Lean and mathlib pins do not cure a direct placeholder; its
restrictive license adds a separate integration concern. It is classified
`M5`, rejected, and creates no integration debt.

The graph, arbitrary-curve, and function-field Riemann-Roch projects returned
by broader repository search concern different theorems. None transports to
GRR for a proper morphism with K-theory and Chow characteristic classes.

## Search Boundary

The discovery protocol freezes nine rows: the canonical statement, one legacy
shape, three mathlib support families, the invalid Atlas GRR declaration, and
three false positives. All nine are classified. That is inventory coverage,
not exhaustive discovery. Sourcegraph is a bounded public index; GitHub code
search hit the shared anonymous rate limit, and grep.app returned HTTP 429.
Those are explicit access limitations rather than evidence of global absence.

## Reopen Conditions

Reopen candidate integration only when an immutable Lean 4 revision supplies
a placeholder-free theorem with a checked transport to the exact frozen
target, complete dependency/toolchain pins, terminal proof-body provenance,
machine-derived axiom and unsafe/oracle closure, compatible licensing, and a
successful repo-local pin/import/check. Otherwise the obligation tree must
treat the missing native interfaces and terminal proof as open formalization
work.

## Status Boundary

This node records a self-testable formal-anchor audit only. It does not clear
the open source convention and pinpoint review, establish `H0` or `R0`, freeze
an obligation registry, prove GRR, reach `M1` or `M0`, complete `AUDIT-Z`, or
claim theorem completion or master acceptance.
