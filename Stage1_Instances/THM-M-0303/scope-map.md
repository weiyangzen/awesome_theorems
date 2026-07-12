# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0303`, the name `索伯列夫嵌入定理`, the attribution Sergei
Sobolev, the year 1936, and the gloss `Sobolev空间到连续函数空间的嵌入`. Importance "high" and
status `已验证` are inventory metadata, not source or proof evidence.

The gloss identifies a continuous-representative Sobolev embedding family. It does not select a
specific Sobolev space, function-space embedding, domain, parameter regime, theorem strength, or
source.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from a pinpoint source:

- Euclidean, manifold, metric-measure, or other ambient domain; its dimension, scalar field,
  universes, measure, and whether the result is global, local, or on a bounded domain;
- integer or fractional differentiability order, homogeneous or inhomogeneous Sobolev convention,
  weak-derivative or Fourier/Bessel-potential encoding, and almost-everywhere quotient semantics;
- integrability exponent and exact dimension-order-exponent relation, including whether the target
  is the supercritical regime only and how `p = infinity` is treated;
- domain regularity such as open, bounded, Lipschitz, extension-domain, cone-condition, or smooth
  boundary assumptions, and whether the conclusion is on the domain or its closure;
- scalar or vector-valued functions and all finite-dimensional, Banach-space, separability, and
  completeness hypotheses;
- existence and uniqueness convention for a concrete representative and the exact meaning of
  agreement with the Sobolev equivalence class;
- continuous, bounded-continuous, Holder, or another target function space, together with its norm,
  seminorm, exponent, embedding operator, constant dependencies, and qualitative versus
  quantitative conclusion; and
- zero-dimensional, empty-domain, zero-function, endpoint, unbounded-domain, irregular-domain, and
  boundary cases.

These choices produce inequivalent propositions. This list is a resolution ledger, not a theorem
statement.

## Candidate branches not credited

- A first-order supercritical theorem `W^{1,p}(Omega) -> C^{0,1-n/p}` for `p > n` on a bounded
  extension domain, with a Holder representative and quantitative estimate.
- A higher-order theorem `W^{k,p} -> C^m` or `C^{m,alpha}` under an appropriate inequality between
  `k`, `p`, `m`, and the dimension.
- A whole-space or compact-support Morrey inequality followed by density, extension, restriction,
  and representative bridges.
- Endpoint or critical embeddings into BMO, exponential Orlicz, or other non-continuous targets.

Only the first branches resemble the catalog gloss, and even they differ in domains, hypotheses,
and conclusions. None is canonical or credited at intake.

## Neighbor and duplicate boundaries

- `THM-M-0304` (Morrey theorem) separately owns the gloss "Holder continuity of Sobolev functions".
- `THM-M-1242` separately owns Morrey's inequality.
- `THM-M-0309` and `THM-M-1238` separately own Rellich-Kondrachov compact embeddings.
- `THM-M-1237` is a separately retained source record with the same English gloss. Its planned
  supercritical scope and historical `S1_M_175.lean` module cannot be copied into this target.

The duplicate identities require later integration-lane reconciliation. They do not authorize
merging targets, sharing receipts, or importing another target's chosen proposition.

## Explicit exclusions

- A compactly supported `C^1` Gagliardo-Nirenberg-Sobolev `L^p` norm inequality presented as an
  embedding into continuous representatives.
- Morrey Holder continuity, Rellich-Kondrachov compactness, Trudinger critical embedding, a
  Poincare inequality, or the definition of a Sobolev space substituted for this target.
- A finite-dimensional or smooth-function special case presented as a general Sobolev-space root.
- A structure field or hypothesis that assumes the desired representative, continuity, embedding,
  or norm estimate and then projects it tautologically.
- The untrusted `已验证` label, a theorem name, a nearby Lean declaration, or another target's
  passing build used as source or proof credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides compact-support or bounded-support
Gagliardo-Nirenberg-Sobolev norm inequalities in
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality` and the predicate `HolderOnWith` with its
positive-exponent continuity consequence. These APIs elaborate, but they neither define the
source-selected Sobolev membership and representative relation nor prove existence of a continuous
representative. The probe is intake feasibility evidence only, not an exact statement, exhaustive
anchor audit, or proof.
