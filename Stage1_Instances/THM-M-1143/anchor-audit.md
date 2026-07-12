# Anchor audit

Item: `S56-M-1143-ANCHOR_AUDIT`

The audit used the immutable mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`) with Lean 4.29.0. No dependency was
updated, cloned, or fetched.

## Candidate result

The closest formal result is
`InnerProductSpace.bounded_harmonic_on_complex_plane_is_constant` in
`Mathlib.Analysis.Complex.Harmonic.Liouville`. It has a real proof body at the pinned revision and
the narrow Lean check confirms its exact type and use for `f : Complex -> Real`. Its reported axiom
closure is `propext`, `Classical.choice`, and `Quot.sound`, the ordinary mathlib classical profile.

This declaration is not exact closure for the frozen theorem. It covers the complex plane only;
the canonical target quantifies over `EuclideanSpace Real (Fin n)` for every positive `n`. Even its
use for `n = 2` needs an explicit real-linear isometric transport. The supporting declarations
`Differentiable.apply_eq_apply_of_bounded`,
`Differentiable.exists_const_forall_eq_of_bounded`, and
`Differentiable.exists_eq_const_of_bounded` prove the holomorphic Liouville theorem and occur in the
plane harmonic proof, but do not bridge arbitrary-dimensional real harmonic functions.

Repo-local and pinned-mathlib searches found no all-dimensional candidate. Anonymous external
index probes found no independently inspectable additional Lean 4 candidate: GitHub code search
required sign-in, grep.app was rate-limited, and the probed LeanSearch/Moogle endpoints rejected the
requests. These failures are recorded rather than converted into a claim that no external proof can
exist.

## Classification

The plane declaration is an `anchor_only_not_exact_closure` candidate. It earns no root proof
credit, and machine debt stays `M4`. The next proof architecture must represent at least the plane
transport separately and, for general `n`, an n-dimensional Liouville argument (for example via a
mean-value/gradient estimate whose required mathlib ingredients must themselves be audited).

This phase's inventory and candidate classification are self-tested, pending master acceptance.
Human-source fidelity, obligation-tree acceptance, proof closure, hermetic replay, and theorem
completion remain open.
