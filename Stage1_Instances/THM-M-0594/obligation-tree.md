# Frozen obligation architecture

## Freeze boundary

Version 1 freezes 16 root-relevant semantic obligations for
`S56-M-0594-OBLIGATION_TREE`. Eligibility was assigned from the unrestricted
statement and proof architecture before recording closure. The compact mathlib
theorem is an explicit provenance overlay and strict subtarget; it is not a
proof child of the unrestricted root and cannot inflate root coverage.

The planned claims below have content hashes but are not represented as
elaborated declarations. Their `M4` state says exactly that. The paper's
lemma-level correspondence remains `H1` pending pinpoint source review rather
than being reconstructed from theorem folklore.

## Typed proof graph

```text
M0594-ROOT
`-- M0594-T-ASSEMBLE [checked conditional constructor]
    |-- M0594-C-GLOBAL
    |   |-- M0594-N-EXHAUSTION
    |   |-- M0594-N-DIMENSION
    |   |-- M0594-C-LOCAL
    |   |-- M0594-L-DIFFERENTIAL
    |   |   |-- M0594-C-LOCAL
    |   |   `-- M0594-N-DIMENSION
    |   |-- M0594-L-POINT-SEPARATION
    |   |   |-- M0594-N-EXHAUSTION
    |   |   `-- M0594-C-LOCAL
    |   `-- M0594-L-PROPERNESS
    |       |-- M0594-N-EXHAUSTION
    |       `-- M0594-C-LOCAL
    `-- M0594-L-TOPOLOGICAL
        |-- M0594-L-POINT-SEPARATION
        `-- M0594-L-PROPERNESS
```

`S-DEFINITIONS` and `S-BOUNDARY` refine the statement. `S-FOUNDATION` is a
trust dependency. `X-SOURCE`, `X-PROVENANCE`, and `X-COMPACT` live only in
source, provenance, trust, or documentation graphs. None is silently treated
as a mathematical premise.

## Obligation ledgers

<a id="m0594-root"></a>
`M0594-ROOT`: introduce the exact manifold context and consume only the final
assembly. No compactness or dimension bound may be added.

<a id="m0594-s-definitions"></a>
`M0594-S-DEFINITIONS`: preserve `CMDiff`, `IsEmbedding`, and pointwise
injectivity of `mfderiv` with the statement's ordered instances.

<a id="m0594-s-boundary"></a>
`M0594-S-BOUNDARY`: preserve empty and zero-dimensional cases,
second-countability, boundarylessness, and existential target dimension.

<a id="m0594-s-foundation"></a>
`M0594-S-FOUNDATION`: derive the transitive axiom, quotient, choice, import,
kernel, and no-oracle boundary for every eventual terminal body.

<a id="m0594-n-exhaustion"></a>
`M0594-N-EXHAUSTION`: obtain a countable locally finite atlas and compact
exhaustion, checking coverage, nesting, local finiteness, and chart domains.
This central package must split before implementation if its ledger exceeds
100 steps.

<a id="m0594-n-dimension"></a>
`M0594-N-DIMENSION`: choose one finite target dimension sufficient for all
coordinates. A sharp `2m` or `2m+1` bound is not part of this target.

<a id="m0594-c-local"></a>
`M0594-C-LOCAL`: build bump-supported chart coordinates and prove global
smooth extension, support control, local finiteness, and cotangent spanning.
The construction and invariant proofs are an expansion trigger.

<a id="m0594-l-differential"></a>
`M0594-L-DIFFERENTIAL`: obtain a finite coordinate selection with injective
derivative at every point. Any transversality, general-position, or projection
theorem used here must become its own bridge obligation.

<a id="m0594-l-point-separation"></a>
`M0594-L-POINT-SEPARATION`: separate every pair of distinct points, including
pairs in different exhaustion layers, with finitely many selected coordinates.

<a id="m0594-l-properness"></a>
`M0594-L-PROPERNESS`: construct a smooth exhaustion coordinate and prove that
the assembled map has compact inverse images of compact sets.

<a id="m0594-c-global"></a>
`M0594-C-GLOBAL`: assemble a finite Euclidean tuple, prove componentwise
smoothness, and carry derivative, injectivity, and properness invariants.

<a id="m0594-l-topological"></a>
`M0594-L-TOPOLOGICAL`: prove the exact proper-injective-to-`IsEmbedding`
bridge with the frozen Hausdorff/local-compactness assumptions made explicit.

<a id="m0594-t-assemble"></a>
`M0594-T-ASSEMBLE`: the Lean declaration
`root_of_smooth_embedding_witness` checks that a dimension and witness with the
three required properties produce precisely the canonical target. It does not
construct that witness.

<a id="m0594-x-compact"></a>
`M0594-X-COMPACT`: record the pinned compact theorem and local wrapper as one
shared terminal proof body for a strict specialization only.

<a id="m0594-x-source"></a>
`M0594-X-SOURCE`: supply primary-source page/theorem anchors, premise mapping,
and errata for every material construction and bridge. This has no machine
proof credit.

<a id="m0594-x-provenance"></a>
`M0594-X-PROVENANCE`: inventory terminal bodies, wrappers, declarations,
imports, axioms, trust, and replay receipts without duplicating proof credit.

## Phase boundary

The registry and seven typed graphs are structurally self-tested. Four narrow
interfaces are locally checked, but the root remains `[H1, M3, R3]`. The next
root cut set is the global noncompact construction and the topological bridge.
No proof, audit completion, or theorem completion is claimed.
