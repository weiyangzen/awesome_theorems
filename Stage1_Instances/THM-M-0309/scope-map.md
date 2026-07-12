# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0309`, the name "Rellich-Kondrachov compact embedding theorem",
the attribution Franz Rellich / Vladimir Kondrachov, the year 1930, and the gloss "compact embedding
of Sobolev spaces." Importance "high" and status `已验证` are catalog metadata, not source or
kernel evidence. Intake preserves only the compact-Sobolev-embedding family.

The common subcritical formulation for `W^{1,p}(Omega) -> L^q(Omega)` is a scope locator, not the
selected theorem. The catalog also fits an `H_0^1 -> L^2` Rellich theorem, a higher-order
`W^{k,p} -> W^{l,q}` result, or a compact-manifold version. No one variant is credited here.

## Proposition-changing decisions

An approved source selection must freeze:

- the exact historical or modern theorem and every incorporated definition, assumption, proof
  boundary, correction, and erratum;
- Euclidean domain versus manifold, ambient dimension, openness, boundedness, connectedness,
  boundary regularity, extension or cone property, and the measure on the domain;
- real versus complex scalars, weak-derivative convention, Sobolev order, homogeneous versus
  inhomogeneous norm, and `W^{k,p}` versus `W_0^{k,p}`;
- the encodings and complete ranges of `p`, `q`, and any critical exponent, including all endpoint
  and dimension branches;
- the concrete source and target spaces and the canonical inclusion map;
- compact operator, compact map, relative compactness of bounded images, sequence/subsequence
  convergence, or another source-matched formulation;
- universes, ordered binders, quantifier dependencies, typeclass assumptions, coercions, norm and
  quotient conventions, and whether each supporting result is a hypothesis or dependency; and
- every empty, zero, low-dimensional, irregular-domain, critical-endpoint, and infinite-exponent
  case.

These choices are not cosmetic transports. They change the proposition and sometimes its truth.

## Candidate families not credited

- For a bounded regular domain `Omega` in real `n`-space and `1 <= p < n`, compactness of the
  inclusion `W^{1,p}(Omega) -> L^q(Omega)` for `1 <= q < np/(n-p)`.
- The corresponding finite-`q` branch when `p >= n`, subject to the selected source's endpoint and
  regularity hypotheses.
- Compactness of `H_0^1(Omega) -> L^2(Omega)` on a bounded domain.
- Higher-order Euclidean Sobolev embeddings or compact `H^1 -> L^2` embeddings on compact
  Riemannian manifolds.

These are a resolution ledger only. Intake asserts none of them as the root.

## Explicit exclusions

A continuous Sobolev norm inequality or bounded inclusion does not establish compactness. The
critical embedding, an unbounded-domain statement without tightness, an abstract spectral Rellich
criterion, the Rellich inequality, and a finite-dimensional or one-dimensional special case may
not replace the selected source theorem. A data structure containing the desired compactness as a
field is an assumption package, not a proof of the theorem.

The distinct target `THM-M-1238` has the same broad catalog gloss in the PDE category. Its legacy
dossier and `S1_M_176.lean` file are discovery inputs only; their scope, state, or evidence is not
inherited. `THM-M-0303` concerns the broader Sobolev embedding family, where continuity alone is
not this target's compactness conclusion. `THM-M-1247` is the unrelated Rellich inequality.

## Boundary cases

The eventual source target must decide dimensions zero and one, `p = 1`, `p = n`, `p > n`,
`q = 1`, the critical exponent, `q = infinity`, empty or measure-zero domains, disconnected and
unbounded domains, rough boundaries, zero source/target spaces, quotient representatives, and
real/complex conjugation. It must also decide whether sequential compactness is used and under
which metrizability or completeness hypotheses it agrees with the chosen topological statement.

## Formal boundary

No canonical Lean expression is frozen. The pinned probe checks `MeasureTheory.Lp`, `MemLp`,
`IsCompactOperator`, a bounded-image characterization, and two Gagliardo-Nirenberg-Sobolev
inequalities. Those declarations are substrate only. They neither define the selected Sobolev
space nor construct its inclusion nor prove compactness. The later statement and anchor-audit
phases must determine exact imports, expression identity, formal candidates, and terminal proof
provenance.
