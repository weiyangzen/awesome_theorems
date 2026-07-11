# Scope map

## Selected root

The canonical family is the cohomological AHSS obtained from the skeletal
filtration of a finite CW complex `X` for a reduced generalized cohomology
theory `E`. It must include all three linked assertions: the `E2` identification
`H^p(X; E^q(pt))`, differentials of bidegree `(r, 1-r)`, and convergence to the
skeletally filtered group `E^(p+q)(X)`. Naturality is part of the selected root.

## Required downstream surfaces

| Surface | Required content | Intake state |
|---|---|---|
| Space | A Lean representation of finite CW complexes and skeleta | open |
| Theory | A genuine generalized cohomology interface, not a proposition-valued skeleton | open |
| Exact couple | Construction from the skeletal filtration and relative groups | open |
| `E1` to `E2` | Cellular cochains and identification of their cohomology | open |
| Abutment | Finite exhaustive skeletal filtration and convergence statement | open |
| Naturality | Maps compatible with the chosen CW/skeletal construction | open |

## Exclusions

The homological AHSS and K-homology versions are alternate theorem families.
Equivariant, twisted, multiplicative, parametrized, and infinite-CW variants
are excluded. A theorem about an arbitrary mathlib `SpectralSequence` does not
establish this root unless it is connected by checked construction and
composition to the skeletal filtration and generalized cohomology theory.

The word "converges" is not allowed to hide an extension problem: the future
statement must expose the induced filtration and identify its associated
graded pieces. Indexing conventions must be frozen and transported by checked
wrappers rather than silently changing differential signs or bidegrees.
