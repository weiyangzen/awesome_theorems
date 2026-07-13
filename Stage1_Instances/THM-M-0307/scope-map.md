# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0307`, the title `迹定理`, the attribution Sergei Sobolev, the
year 1936, and the gloss `Sobolev函数在边界上的限制`. Importance `高` and status `已验证` are
inventory metadata, not human-source or kernel evidence. Intake preserves only the Sobolev
boundary-trace family identified by this wording.

The common bounded-Lipschitz-domain trace theorem is a scope locator, not the selected target. The
gloss is also compatible with smooth domains, half-spaces, higher-order or fractional spaces,
manifolds with boundary, and several different trace codomains and theorem strengths.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from a pinpoint immutable source:

1. The ambient Euclidean space or manifold, dimension, scalar or vector codomain, domain, measure,
   and whether the domain is open, bounded, Lipschitz, smooth, an extension domain, or another
   precisely defined class.
2. The exact boundary object and surface measure, including whether the target is the topological,
   reduced, measure-theoretic, or manifold boundary and how null sets are treated.
3. The Sobolev model: `W^{k,p}`, `H^s`, homogeneous or inhomogeneous, integer or fractional order,
   weak-derivative or Fourier/Bessel-potential encoding, and almost-everywhere quotient semantics.
4. All parameter ranges and endpoints: derivative order, exponent, dimension relation, trace
   threshold, fractional smoothness loss, and finite or infinite exponents.
5. The target space: `L^p` on the boundary, `W^{1-1/p,p}`, `H^{s-1/2}`, a Besov space, or another
   source-selected space, with its exact norm and quotient conventions.
6. The trace map's construction as the unique continuous extension of classical boundary
   restriction on a dense smooth class, and the exact agreement or representative clause.
7. Whether the conclusion is only existence and boundedness, or also uniqueness, surjectivity,
   existence of a bounded extension/right-inverse operator, kernel equality with a zero-trace
   Sobolev space, or a quantitative constant.
8. Ordered binders, universes, typeclass assumptions, constant dependencies, coercions, density
   hypotheses, and every empty, rough-boundary, zero-measure, low-dimensional, and endpoint case.

These choices yield inequivalent propositions. The list is a resolution ledger, not a theorem.

## Candidate branches not credited

- Boundedness of a trace operator from `W^{1,p}(Omega)` to `L^p(boundary Omega)` for a bounded
  Lipschitz domain and a source-selected range of `p`.
- A sharper trace into `W^{1-1/p,p}(boundary Omega)` or the corresponding Besov space, possibly
  with surjectivity and a bounded right inverse.
- The Hilbert-scale map `H^s(Omega) -> H^{s-1/2}(boundary Omega)` for a smooth domain and
  source-selected `s`.
- A half-space trace theorem followed by localization and boundary flattening.
- A manifold-with-boundary trace theorem under a selected Riemannian and measure model.

No candidate is canonical, asserted, or credited at intake.

## Explicit exclusions and neighbors

Pointwise restriction of an arbitrary almost-everywhere class is not a trace operator. Restriction
of a smooth or continuous function to a boundary is only the dense-class input, not the extension
theorem. A structure or hypothesis containing the desired trace, estimate, surjectivity, or right
inverse cannot serve as its proof.

The following separate targets cannot substitute for this root: `THM-M-0303` Sobolev embedding,
`THM-M-0305` Poincare inequality, `THM-M-0306` Friedrichs inequality, `THM-M-0308` Sobolev extension,
and `THM-M-0309` Rellich-Kondrachov compact embedding. In particular, a zero-trace inequality does
not construct the trace, and the extension theorem may be a dependency or right-inverse result but
is not silently included in this target.

The catalog repeats the same six trace-theorem lines at a second location. The generator retains
only `THM-M-0307` for this exact metadata signature. The repeated text is provenance, not a second
target, a second statement, or transferable evidence.

## Boundary cases

The eventual source must decide empty domains, empty or measure-zero boundaries, dimension zero or
one, disconnected and unbounded domains, rough or fractal boundaries, values of `p` at one or
infinity, critical trace thresholds, constant functions, zero trace, scalar versus vector values,
and equality of almost-everywhere representatives. No degenerate case is excluded at intake.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies `MeasureTheory.Lp` and `MemLp`,
measure restriction, a manifold boundary set, and smooth compact-support Gagliardo-Nirenberg-
Sobolev norm inequalities. These APIs elaborate but do not define a source-selected Sobolev space,
boundary surface measure, or trace operator and do not prove a trace theorem. The probe records
feasibility substrate only; exact imports, expression identity, mutations, and formal candidate
provenance belong to later phases.
