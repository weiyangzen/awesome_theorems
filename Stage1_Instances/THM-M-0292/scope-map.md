# Scope map

## Received scope

The repository supplies only the family label Dini's theorem and the gloss "uniform convergence of
a monotone sequence of functions." Intake preserves that literal claim rather than silently adding
the familiar compactness, continuity, pointwise-convergence, and continuous-limit hypotheses.

The Chinese phrase `单调函数列` conventionally suggests monotonicity of the sequence under the
pointwise order. Without quantifiers or order variables, however, it could also describe a sequence
of functions that are each monotone in their domain variable. A source-approved proposition must
resolve this before statement elaboration.

## Candidate classical family, not yet canonical

The strongest current match among inspected sources and pinned formal artifacts is the classical
compact-domain family:

- a compact topological space, or a compact subset of a topological space;
- a sequence `F n` of continuous real-valued functions;
- pointwise monotonicity in `n`, increasing or decreasing;
- pointwise convergence of `F n x` to a continuous function `f`; and
- uniform convergence of `F n` to `f` on the domain.

This paragraph is a candidate scope boundary, not a frozen statement. The repository does not
select its compact-space or compact-set form, monotonicity direction, real or generalized codomain,
or exact convergence encoding.

## Decisions required at statement freeze

1. Admit and independently review an immutable source edition, exact theorem locator, incorporated
   definitions, proof boundary, translation, and correction or errata status.
2. Fix the domain as a closed interval, arbitrary compact space, or compact set, including the
   ambient topology and the behavior on the empty set.
3. Fix index-monotonicity rather than domain-variable monotonicity, and decide increasing,
   decreasing, or an explicit conjunction of both variants.
4. Fix the index type as `ℕ` or justify a general preorder, including empty or degenerate `atTop`
   behavior in any generalized form.
5. Fix the codomain as `ℝ` or justify mathlib's normed lattice additive commutative group
   generalization and all typeclass assumptions.
6. Fix pointwise convergence, continuity of the limit, and whether those are hypotheses or derived
   from a series presentation.
7. Fix the conclusion as `TendstoUniformly`, `TendstoUniformlyOn`, convergence in a continuous-map
   topology, or a supremum/epsilon form, with checked transports for every credited alternative.
8. Mutation-test removed compactness and continuity hypotheses, changed domain and codomain,
   changed binder scope and monotonicity direction, and empty or singleton boundary cases.

## Excluded substitutions

- A monotone sequence with no compactness, continuity, or pointwise-convergence hypotheses.
- Pointwise convergence alone, or locally uniform convergence on a noncompact domain, presented as
  the compact uniform theorem.
- Monotonicity of each function in the domain variable substituted for monotonicity of the sequence.
- A closed but noncompact domain, or a discontinuous pointwise limit, without a source-selected
  replacement hypothesis.
- The nonnegative-series form treated as definitionally identical to the monotone-sequence form;
  partial sums, increments, indexing, and uniform-convergence meanings require a checked transport.
- Mathlib's arbitrary preorder or normed-lattice generalization silently substituted for a
  source-selected `ℕ`-indexed real-valued theorem.
- A structure field, hypothesis, axiom, oracle, numerical experiment, or unchecked certificate that
  directly stores the desired uniform convergence.
- The catalog's `已验证` label or a successful API probe used as human-source or proof credit.

## Neighbor and collision boundary

A bounded search found one Dini record in the repository mathematics corpus and no second rev-5.6
target with the same name or gloss. That negative result is intake discovery only, not the exhaustive
anchor audit. Fejer's theorem (`THM-M-0291`) is adjacent in the catalog but concerns uniform
convergence of Fourier-Cesaro means and must not be used as this root.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.UniformSpace.Dini` provides increasing and decreasing locally uniform,
compact-space uniform, compact-set uniform, and continuous-map compact-open variants. Its unbundled
codomain assumptions are `NormedAddCommGroup`, `Lattice`, `HasSolidNorm`, and
`IsOrderedAddMonoid`. These are direct formal candidates, not the accepted scope of `THM-M-0292`.
Exact statement identity, source transport, terminal proof-body provenance, dependency closure,
axioms, and trust remain downstream work.
