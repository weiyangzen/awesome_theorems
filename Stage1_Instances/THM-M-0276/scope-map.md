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

## Candidate classical boundary

A familiar form says that a surjective bounded linear operator between real or complex Banach
spaces maps every open subset of its domain to an open subset of its codomain. This is a scope
description, not the frozen root. The statement phase must fix:

1. Whether scalars are `ℝ`, `ℂ`, either field, or a supported general nontrivially normed field.
2. Whether the domain and codomain are both explicitly complete normed spaces. Omitting either
   completeness hypothesis changes the theorem and permits counterexamples.
3. Whether "bounded linear operator" is represented by a bundled `ContinuousLinearMap`, or by a
   linear map plus a boundedness/continuity hypothesis and a checked equivalence.
4. Whether the operator is ordinary same-field linear or semilinear over a specified isometric
   scalar equivalence. Pinned mathlib's direct theorem is more general than the ordinary textbook
   form.
5. Whether surjectivity is `Function.Surjective f`, `LinearMap.range f = ⊤`, or another checked
   equivalent.
6. Whether "open" is `IsOpenMap f`, its expansion over images of every open set, or a local ball
   formulation with a checked bridge.
7. Ordered binders, universe levels, topology instances, the exact conclusion, and every alternate
   encoding with a checked direction.

## Boundary cases

The exact source crosswalk must resolve zero or trivial domain/codomain spaces, the zero map onto a
trivial codomain, noninjective quotient maps, real versus complex scalars, and incomplete source or
target spaces. Injectivity is not a hypothesis of the received theorem. A bijective bounded map
having bounded inverse is a corollary, not an equivalent root without an explicit bridge.

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
elaboration do not choose a source-faithful target, audit terminal bodies, or supply proof credit.

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
