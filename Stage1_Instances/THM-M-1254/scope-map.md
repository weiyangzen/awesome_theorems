# Scope map

| Surface | Repository evidence | Frozen intake boundary |
|---|---|---|
| Name | `基本解` (fundamental solution) | A name is not a proposition |
| Discovery statement | `微分算子的基本解` (fundamental solution of a differential operator) | Definition-shaped relation only; no existence or uniqueness quantifier is supplied |
| Candidate relation | `L E = delta_0` in a generalized-function sense | Discovery aid, not yet the canonical theorem |
| Operator | Unspecified differential operator | Order, coefficients, ellipticity, and constant/variable coefficient status remain open |
| Domain | Unspecified | Euclidean dimension, manifold/domain, boundary, and scalar field remain open |
| Solution object | Unspecified | Distribution, tempered distribution, function, measure, and normalization remain open |
| Claim kind | Unspecified | Definition, existence, uniqueness modulo homogeneous solutions, and explicit formula are distinct |
| Neighbor boundary | `THM-M-1255` is Malgrange-Ehrenpreis existence | Its constant-coefficient existence claim must not be reused here |
| Lean surface | No target-specific module or declaration found | Module, binders, universes, imports, and expression are intentionally unset |
| Trust/computation | Lean 4 plus pinned mathlib is the intended backend | Exact toolchain, axioms, TCB, and computation profile await a formal target |

Degenerate cases cannot yet be classified. In particular, `L = 0`, zero-dimensional domains,
nontrivial kernels, boundary conditions, and the normalization of `delta_0` depend on the missing
operator and solution-space choices. No narrower example, such as the Laplacian or heat operator,
is accepted as a replacement.

