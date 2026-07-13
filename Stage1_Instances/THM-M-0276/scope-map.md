# Scope map

## Received claim

`Docs/researches/math_theorems.md:1985-1990` gives the title `开映射定理`, Stefan Banach, 1929,
and the gloss `满射有界线性算子是开映射` ("a surjective bounded linear operator is an open
map"). An identical duplicate occurs at lines 2260-2265. The retained row lies under the
real-analysis catalog heading, while the duplicate lies under functional analysis; exact-field
deduplication explains the manifest category and does not itself restrict the theorem to real
scalars. Neither record supplies a citation, definitions, assumptions, proof boundary, or formal
artifact.

The wording identifies the Banach-space open mapping theorem. It excludes the distinct
complex-analytic open mapping theorem `THM-M-0235`, whose claim concerns nonconstant holomorphic
functions.

## Frozen statement boundary

A familiar form says that a surjective bounded linear operator between real or complex Banach
spaces maps every open subset of its domain to an open subset of its codomain. The immutable
Rotem/Tzorani source fixes its scalar convention to real or complex at TeX line 36, defines Banach
space at line 52, and supplies the open-map definition and Theorem 2.2.11 at lines 1133-1143. The
statement phase therefore freezes these choices:

1. The root is a closed conjunction of the `Real` and `Complex` cases, not an open `RCLike` or
   arbitrary nontrivially normed-field quantification.
2. Domain and codomain are each explicitly complete normed spaces. Omitting either completeness
   hypothesis changes the proposition.
3. "Bounded linear operator" is the ordinary same-field bundled `ContinuousLinearMap`.
4. Surjectivity is `Function.Surjective f`.
5. Openness is `IsOpenMap f`, with a checked definitional `Iff` to the source expansion over images
   of every open set.
6. Domain and codomain live in independent universes, and the structure, operator, and antecedent
   binders are ordered explicitly in `Statement.lean`.

## Boundary cases

Zero or trivial domain/codomain spaces, the zero map onto a trivial codomain, and noninjective
surjective maps remain admitted. Injectivity, finite dimensionality, separability, and nontrivial
carriers are not hypotheses. Incomplete source or target spaces are excluded by the two
`CompleteSpace` binders. A bijective bounded map having bounded inverse is a corollary, not an
equivalent root.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the direct candidate
`ContinuousLinearMap.isOpenMap` has the semilinear shape

```text
f : E ->SL[sigma] F
Surjective f -> IsOpenMap f
```

under normed additive commutative group and normed-space structures, completeness of both `E` and
`F`, compatible inverse scalar homomorphisms, and isometry assumptions. The definition `IsOpenMap
f` expands to `forall U, IsOpen U -> IsOpen (f '' U)`.

Supporting declarations expose the proof architecture: `exists_approx_preimage_norm_le` uses
Baire category, `exists_preimage_norm_le` turns approximate preimages into exact controlled ones,
and `isQuotientMap` is a corollary. `LinearEquiv.continuous_symm` is the bijective bounded-inverse
consequence. These direct interfaces justify provisional `M3`; their names and successful
elaboration do not audit terminal bodies or supply proof credit. The statement root instead uses
the lighter non-proof import `Mathlib.Analysis.Complex.Basic`.

## Explicit exclusions

- `THM-M-0235`, the open mapping theorem for nonconstant holomorphic functions.
- The bounded inverse theorem for bijective operators, the closed graph theorem `THM-M-0277`, or
  the uniform boundedness principle `THM-M-0275` as substitutes.
- Only the controlled-preimage lemma, quotient-map corollary, affine generalization, generic
  topological-group theorem, or a finite-dimensional special case.
- A theorem omitting completeness, or assuming injectivity when the source root requires only
  surjectivity.
- A structure or premise that already stores the desired openness conclusion.
- A theorem name, URL, `#check`, untrusted `已验证` label, or API probe as H0 or M0 evidence.
