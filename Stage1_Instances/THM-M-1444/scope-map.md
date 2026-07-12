# Scope map

## Preserved repository scope

The catalog fixes the named Banach fixed-point theorem, Stefan Banach, 1922, and only the gloss
"a fixed point of a contraction mapping." This identifies the contraction-mapping theorem family,
but not one binder-complete proposition. The intake therefore preserves fixed-point existence for a
contractive self-map as the family boundary while leaving the exact root proposition null.

The inspected historical candidate is Banach's Theorem 6 on printed pages 160-161. The preceding
source setting on printed pages 134-136 makes `E` an at-least-two-element real normed linear system
with a Cauchy-completeness axiom. In the source's notation, `U` is a continuous operation with
counter-domain contained in `E`; there exists a real
`M` with `0 < M < 1` such that

```text
|U(X') - U(X'')| <= M |X' - X''|
```

for all `X'`, `X''`; the stated conclusion is existence of `X` with `X = U(X)`. The proof chooses an
arbitrary `Y`, sets `X_1 = Y` and `X_(n+1) = U(X_n)`, proves norm convergence, and passes to the
limit. The role of the earlier axioms defining `E` and its completeness must be incorporated before
this is accepted as the canonical modern statement.

## Proposition-changing decisions

The statement phase must obtain an approved source decision for all of the following:

- a complete metric space, a complete nontrivial real normed linear space faithful to Banach's `E`, an extended
  metric space component, or a complete invariant subset;
- whether nonemptiness is a typeclass, an explicit witness, or an initial point, and whether the
  map is an ambient self-map, subtype self-map, or map preserving a subset;
- `ContractingWith K f`, a real or nonnegative contraction factor, a strict distance inequality, or
  another source-faithful formulation, including the exact range of the factor;
- whether continuity is retained as a source hypothesis or derived from the contraction premise;
- existence only, unique existence, convergence of all Picard iterates, an a priori or a posteriori
  estimate, or a source-approved conjunction of these conclusions;
- ordered binders, universes, equality orientation, topology, foundation and choice requirements;
  and
- how the 1922 result, a modern textbook formulation, and the catalog gloss are related rather
  than presumed definitionally identical.

## Boundary and mutation cases

Later statement tests must cover an empty carrier or subset, a singleton space (excluded by the
literal source's at-least-two-element axiom but included by a common modern generalization), a map
that is not a self-map, an initially fixed point, contraction factor zero, factor equal to one, weakening strict
contraction to nonexpansiveness, incomplete spaces, pseudometric zero without equality, infinite
extended distance, disconnected finite-distance components, and complete versus merely closed or
invariant subsets. Removing completeness, self-map closure, strict contraction, or nonemptiness is
a material mutation, not formatting.

## Explicit exclusions

- `THM-M-1443` fixed-point iteration, whose generic root-finding method label is a separate target.
- Brouwer, Schauder, Tychonoff, Kakutani, Markov-Kakutani, Lefschetz, or order-theoretic fixed-point
  theorems.
- A constant-map, singleton-space, or already-fixed-point example presented as the general theorem.
- A structure field or hypothesis that supplies the desired fixed point, uniqueness, convergence,
  or estimate.
- A finite trajectory, numerical convergence experiment, stopping event, or floating-point result.
- A pinned API name or the catalog's `已验证` label treated as statement identity or proof credit.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Topology.MetricSpace.Contracting` contains the relevant definitions and theorem family.
The owned probe authenticates selected signatures. It is neither the canonical statement nor an
anchor audit, and no declaration or terminal proof body is credited at intake.
