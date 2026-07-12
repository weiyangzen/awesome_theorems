# Scope map

## Included claim

- A family of operations `Sq^i` indexed by natural numbers and raising mod-2 cohomological degree
  by `i`.
- Naturality with respect to maps and stability under the suspension isomorphism.
- The normalizations `Sq^0 = id`, `Sq^i(x) = 0` for `i > degree(x)`, and
  `Sq^n(x) = x cup x` for `x` of degree `n`.
- Existence simultaneously for all indices and admissible spaces in the source-exact category.

These clauses make the intake claim nonvacuous. In particular, mere existence of arbitrary natural
transformations would be satisfied by zero maps and is not the intended theorem.

## Statement-phase decisions

Pinpoint source inspection must decide the category of spaces or pairs, whether the primary form is
reduced cohomology, how unreduced degree zero is recovered, the exact suspension sign/indexing
convention, and whether operations are constructed from cup-`i` products. Lean binder order,
universes, coefficients (`ZMod 2` or an equivalent field object), and equality of natural
transformations must follow those decisions.

Boundary tests must cover `i = 0`, `i > n`, `n = 0`, a point or contractible space, and suspension.
The statement gate must also mutation-test removal of naturality or stability, replacement of
`F_2`, altered degree shift, and loss of the top-square normalization.

## Explicit exclusions

- Cartan's formula, which has its own adjacent target `THM-M-0550`.
- Adem relations and a classification/presentation of the Steenrod algebra.
- Odd-prime reduced powers, Bockstein operations, or Pontryagin operations.
- A single operation at a fixed index, a computation on one chosen space, or a structure that takes
  the desired operations and laws as fields.
- Treating the Stage0 `已验证` label as either a human-source audit or kernel evidence.

The exclusions prevent a narrower special case, a stronger neighboring theorem, or an assumed API
package from being substituted for the frozen root.
