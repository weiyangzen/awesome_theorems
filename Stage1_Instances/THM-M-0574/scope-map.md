# Scope map

## Included theory family

- Topological K-theory, rather than algebraic or operator-algebra K-theory.
- Stable isomorphism classes of finite-rank complex vector bundles as the expected input to a
  Grothendieck-group construction.
- Reduced, relative, graded, functorial, cohomological, or representability formulations only as
  candidate theorem roots; intake does not conflate them.

## Statement decisions still required

An authority must select one theorem-sized root from a pinpoint source. That selection must fix:

- the category of spaces and hypotheses such as compact Hausdorff, compactly generated, or CW;
- complex versus real vector bundles (`K` versus `KO`);
- unreduced `K^0`, reduced `K~^0`, relative groups, or a spectrum-graded family;
- whether the conclusion is a group construction, functoriality law, exactness statement,
  representability equivalence, or cohomology-theory structure;
- ordered binders, universes, maps, naturality, boundary cases, and every hypothesis.

Only after those choices can the statement phase name a minimal Lean module and expression, compute
an elaborated-expression hash and environment fingerprint, or run statement mutations.

## Explicit exclusions

- Bott periodicity as the root: it belongs to adjacent target `THM-M-0575`.
- Algebraic K-theory of rings, exact categories, or schemes.
- C*-algebra K-theory and Kasparov KK-theory (`THM-M-0591`).
- The Atiyah-Singer index theorem or its families/equivariant variants.
- Treating the definition of a Grothendieck group, an abstract output package, or a generic
  vector-bundle API as proof of an unspecified "K-theory" theorem.

Empty spaces, disconnected spaces, trivial bundles, rank-zero virtual bundles, and degree
conventions remain boundary cases for the selected root; none may be silently discarded.

