# Source-statement crosswalk

## Candidate source statement

Allen Hatcher, *Algebraic Topology* (Cambridge University Press, 2002), Theorem 3.30, page 241,
states the standard closed-manifold form: if `M` is a closed `R`-orientable `n`-manifold with
fundamental class `[M] in H_n(M; R)`, then the maps
`D(α) = [M] cap α : H^k(M; R) -> H_{n-k}(M; R)` are isomorphisms for all `k`.

This is a stable discovery anchor for the modern statement, not yet an immutable source receipt or
an `H0` claim. Before `H0`, the source edition must be inspected directly, its coefficient-ring
conventions and surrounding definitions recorded, errata checked, and the mapping independently
reviewed. Historical attribution to Poincare does not by itself freeze a modern formal statement.

## Crosswalk

| Repository component | Candidate source component | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Poincare duality" | Hatcher Theorem 3.30 | cap product with a fundamental class is the operative map | leading candidate |
| "manifolds" | closed `R`-orientable `n`-manifold | manifold, compact/no-boundary, dimension, and orientation encodings required | included, encoding open |
| "homological duality" | `H^k(M;R) ≅ H_(n-k)(M;R)` for all `k` | homology/cohomology coefficient and grading APIs required | included |
| no coefficients stated | source uses a coefficient ring `R` and `R`-orientation | exact ring assumptions cannot be inferred from metadata | blocking |
| no boundary convention | source candidate is closed | relative/boundary variants must remain excluded unless a different source is selected | blocking |

## Lean discovery boundary

The generated blueprint mentions mathlib topology, manifold, homology, and cohomology APIs only as
search directions. No exact mathlib declaration, external Lean theorem, import closure, or terminal
proof body has been audited in this intake, so none receives machine-proof credit. That search is
owned by the later anchor-audit node after an exact statement is elaborated.
