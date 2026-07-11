# Scope map

## Included subject boundary

- The local Langlands correspondence for `GL_n` over a nonarchimedean local field, in the form
  actually proved in the selected Harris--Taylor source.
- On the automorphic side: isomorphism classes of irreducible admissible smooth representations of
  `GL_n(F)` over a specified characteristic-zero coefficient field.
- On the Galois side: the source's chosen Weil-group or Weil--Deligne parameter objects of dimension
  `n`, including continuity, semisimplicity, and equivalence conventions.
- The normalization and compatibility clauses explicitly included by the selected source, which may
  involve local class field theory at rank one, twists, central characters, duals, and local factors.

## Statement-phase decisions

The primary source must fix the class of local fields (mixed characteristic only or all
nonarchimedean local fields covered), rank quantification, coefficient field, reciprocity-map
orientation, geometric versus arithmetic Frobenius, and whether the root is existence, uniqueness,
a bijection, or a characterized correspondence. Boundary cases `n = 0`, `n = 1`, and characteristic
of the local field must be addressed rather than silently inherited.

## Explicit exclusions

- Global Langlands, the function-field correspondence, and the local correspondence for groups
  other than `GL_n`.
- A bare bijection between abstract types or a structure whose desired conclusion is stored as a
  field; either would substitute an assumed interface for the theorem.
- The geometry and cohomology of Shimura varieties alone, without checked composition to the exact
  local correspondence statement.
- The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_062.lean` as rev-5.6 statement or proof
  evidence. Its header and abstract structures explicitly describe missing APIs.

Later phases must separately freeze the exact claim, environment fingerprint, transports,
hypothesis mutations, anchor inventory, and proof obligations. Partial low-rank results cannot be
promoted as closure of the general root.
