# THM-M-0540 obligation tree

Registry version 1 freezes nine canonical obligations before proof-phase credit. The proof graph is
rooted at `M0540-ROOT`; aliases, the statement witness, and the audit wrapper add no denominator or
terminal-body credit. Every node has a substantive budget at most 100 steps.

## M0540-ROOT

The exact `CanonicalTarget` from `Statement.lean`. It requires the checked assembly node and remains
`[H1, M3, R4]`; no accepted root receipt exists.

## M0540-D-CHAINS

Fix the integral coefficient object, `TopCat.of X`, Nat grading, and the specialization of
`singularChainComplexFunctor`. This prevents a change to reduced, nonintegral, large-universe, or
negative-degree homology.

## M0540-D-HOMOLOGY

Fix `IntegralSingularHomology X n` as the corresponding specialization of
`singularHomologyFunctor`. The output is the exact left side of the root equality.

## M0540-N-SPECIALIZE

Normalize the pinned mathlib definition: `singularHomologyFunctor` is the singular-chain-complex
functor followed by `homologyFunctor` at degree `n`. This is the root-critical imported bridge.

## M0540-T-UNFOLD

Using the two definition nodes and normalization bridge, establish `UnfoldingEquation` for every
`X` and `n`. The anchor audit found an exact `rfl` candidate, but the ordered proof phase must own
its proof receipt, terminal-body identity, and trust closure. It is the current minimal root cut set.

## M0540-T-ASSEMBLE

`root_of_unfolding` is a kernel-checked composition certificate from `UnfoldingEquation` to
`CanonicalTarget`. Its one semantic step is identity transport; it does not prove its premise and
therefore does not close the root.

## M0540-X-SOURCE

Pinpoint and independently review primary passages for singular simplices, integral chains,
alternating boundary, and cycles modulo boundaries. Existing broad citations leave this `[H1]`.

## M0540-X-PROVENANCE

Bind local wrapper/composition roles to the actual pinned mathlib definition, source hash,
dependency declarations, and one deduplicated terminal proof-body identity. This is informational
for machine eligibility but root-critical for assurance.

## M0540-X-TRUST

Record the transitive axiom set, imports, Lean kernel and compiled artifacts, placeholder scan, and
no-oracle computation boundary. This assurance overlay receives no semantic proof coverage.

## Typed graph boundary

`typed-graphs.json` stores separate proof, refinement, provenance, evidence, trust, documentation,
and workflow graphs with reciprocal `proof_requires`/`composes` edges. The frozen required-machine
path is `ROOT -> T-ASSEMBLE -> T-UNFOLD -> {N-SPECIALIZE, D-CHAINS, D-HOMOLOGY}`. Source,
provenance, and trust edges do not masquerade as proof edges.
