# Scope map

## Received claim

`Docs/researches/math_theorems.md` contains the Hahn-Banach entry twice, at lines 1971-1976 and
2246-2251. Both records give only the gloss `线性泛函的保范延拓`, "norm-preserving extension of
linear functionals." This is a recognizable theorem family, not a definition-complete
proposition. The intake freezes the family boundary and the decisions required before statement
elaboration; it does not invent a canonical root.

## Candidate analytic boundary

A common real analytic formulation starts with a real normed or seminormed vector space `E`, a
linear subspace `p`, and a continuous real-valued linear functional `f` on `p`. It asserts the
existence of a continuous real-valued linear functional `g` on `E` which agrees with `f` on `p`
and has the same operator norm. This shape matches the catalogue gloss, but source review must fix:

- real scalars only, complex scalars, or a uniform real/complex statement;
- normed versus seminormed ambient spaces and whether completeness is assumed;
- an algebraic dominated-functional form versus the continuous norm-preserving corollary;
- how the subspace, its inclusion, and restriction or pointwise agreement are represented;
- whether the conclusion requires norm equality, only a norm bound, or another domination clause;
- all universes, typeclasses, ordered binders, coercions, and empty/trivial/zero cases.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Normed.Module.HahnBanach` provides two exact-topic candidates:

```text
Real.exists_extension_norm_eq
  (p : Subspace Real E) (f : StrongDual Real p) ->
  exists g : StrongDual Real E, (forall x : p, g x = f x) and norm g = norm f

exists_extension_norm_eq
  [NontriviallyNormedField K] [IsRCLikeNormedField K]
  (p : Subspace K E) (f : StrongDual K p) ->
  exists g : StrongDual K E, (forall x : p, g x = f x) and norm g = norm f
```

Both use a `SeminormedAddCommGroup E` and `NormedSpace` structure; neither requires completeness of
`E`. The second derives the complex-like result through the real theorem. The same source also
contains the more general finite-dimensional-range corollary, which has no norm estimate and is
not a substitute for the scalar-valued root.

These strong candidates justify provisional `M3`, not `M0`. No source-approved canonical
expression, checked real/complex transport, terminal proof-body provenance, transitive trust
closure, or node-specific accepted receipt is frozen at intake.

## Required statement decisions

1. Admit an immutable primary or authoritative source and independently review its exact theorem,
   incorporated definitions, ordered premises, conclusion, proof boundary, corrections, and errata.
2. Resolve the catalogue's duplicate records and historical Hahn/Banach attribution without using
   either duplicate as additional evidence.
3. Select real, complex, or uniform scalar scope and normed or seminormed hypotheses without
   strengthening or weakening the source.
4. Fix the functional, subspace, extension-equality, operator-norm, universe, coercion, and binder
   encodings, then elaborate their exact Lean expression with minimal imports.
5. Prove checked relationships for alternate real, complex, dominated, restriction, or subtype
   encodings and mutation-test every proposition-changing premise.
6. Resolve the zero subspace, whole space, zero functional, trivial ambient space, and seminorm
   kernel cases rather than excluding them silently.

## Explicit exclusions

- The algebraic sublinear-domination theorem used alone when the root requires a continuous
  norm-preserving extension, or the converse substitution.
- Geometric Hahn-Banach separation theorems, dual-vector corollaries, Banach-Steinhaus, open
  mapping, or closed graph theorems as the root.
- A finite-dimensional-range extension with no norm estimate, a finite-dimensional special case,
  or a theorem only over one scalar field used as an unrestricted root.
- A structure or premise that stores the desired extension, agreement, or norm equality as data.
- The duplicate catalogue entry, theorem-name match, `docs/1000.yaml` row, or `已验证` label used as
  proof or source-fidelity credit.

No canonical Lean expression, ordered binder list, checked alternate encoding, or accepted proof
state is frozen by this intake.
