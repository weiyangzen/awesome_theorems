# Frozen obligation tree

Registry version 1 freezes 19 semantic obligations before proof execution. The selected route is
Milnor's sphere-bundle construction: build the total space, establish its topological sphere
property, and separate its smooth structure from the standard sphere by a bounding-manifold
obstruction. No geometric or topological proof body is credited by this architecture.

| Obligation | Kind | Exact output | H/M/R | Budget |
|---|---|---|---|---:|
<a id="m0605-root"></a>
| `M0605-ROOT` | root | The canonical proposition. | H1/M4/R3 | 8 |
<a id="m0605-s-defs"></a>
| `M0605-S-DEFS` | definition | Exact smooth-manifold and comparison definitions. | H1/M0-L/R3 | 20 |
<a id="m0605-s-domain"></a>
| `M0605-S-DOMAIN` | definition | Exact universes, dimensions, and instances. | H1/M0-L/R3 | 18 |
<a id="m0605-s-boundary"></a>
| `M0605-S-BOUNDARY` | branch | Dimension/radius/degeneracy policy. | H1/M4/R3 | 24 |
<a id="m0605-s-transport"></a>
| `M0605-S-TRANSPORT` | transport | Exact source-marker/canonical transport. | H1/M4/R3 | 35 |
<a id="m0605-s-foundation"></a>
| `M0605-S-FOUNDATION` | certificate | Foundation and TCB profile. | H1/M4/R3 | 45 |
<a id="m0605-c-bundle"></a>
| `M0605-C-BUNDLE` | construction | Selected Milnor sphere bundle with fixed clutching data. | H1/M4/R3 | 95 |
<a id="m0605-c-total"></a>
| `M0605-C-TOTAL` | construction | Smooth seven-manifold total space. | H1/M4/R3 | 90 |
<a id="m0605-l-homotopy"></a>
| `M0605-L-HOMOTOPY` | core lemma | Homotopy-seven-sphere data. | H1/M4/R3 | 95 |
<a id="m0605-x-topo-pc"></a>
| `M0605-X-TOPO-PC` | bridge | Homeomorphism to the standard topological sphere. | H1/M4/R3 | 70 |
<a id="m0605-l-bounding"></a>
| `M0605-L-BOUNDING` | construction | Compatible bounding eight-manifold. | H1/M4/R3 | 90 |
<a id="m0605-l-obstruction"></a>
| `M0605-L-OBSTRUCTION` | computation | Certified nonstandard smooth obstruction. | H1/M4/R3 | 100 |
<a id="m0605-l-standard"></a>
| `M0605-L-STANDARD` | core lemma | Standard obstruction and diffeomorphism invariance. | H1/M4/R3 | 90 |
<a id="m0605-l-nondiff"></a>
| `M0605-L-NONDIFF` | terminal | Canonical `IsEmpty Diffeomorph`. | H1/M4/R3 | 45 |
<a id="m0605-t-witness"></a>
| `M0605-T-WITNESS` | terminal | Manifold plus homeomorphism and non-diffeomorphism certificates. | H1/M4/R3 | 20 |
<a id="m0605-t-assemble"></a>
| `M0605-T-ASSEMBLE` | transport | Exact canonical proposition, conditional on the witness package. | H1/M0-L/R3 | 4 |
<a id="m0605-x-source"></a>
| `M0605-X-SOURCE` | terminal | H0-eligible primary-source crosswalk. | H1/not_applicable/R3 | 80 |
<a id="m0605-x-provenance"></a>
| `M0605-X-PROVENANCE` | certificate | Terminal-body provenance map. | H1/informational/R3 | 45 |
<a id="m0605-x-trust"></a>
| `M0605-X-TRUST` | certificate | Release-gate trust evidence. | H1/informational/R3 | 50 |

## Typed architecture

The proof spine is `ROOT -> T-ASSEMBLE -> T-WITNESS`. The witness requires `C-TOTAL`,
`X-TOPO-PC`, and `L-NONDIFF`. The topological branch uses `C-BUNDLE -> L-HOMOTOPY ->
X-TOPO-PC`; the smooth branch uses the same bundle, builds `L-BOUNDING`, computes
`L-OBSTRUCTION`, and combines it with `L-STANDARD` in `L-NONDIFF`. Sharing the bundle node does
not duplicate proof credit.

Proof/composition, refinement, provenance, evidence, trust, documentation, and workflow graphs
remain separate. Source, provenance, documentation, and trust edges cannot close the root. Every
leaf budget is at most 100, but these planning budgets establish granularity only, not R0.

## Composition boundary

`exoticSevenSphereExists_of_witness` kernel-checks the final child-to-parent map and consumes a
specific `SmoothSevenManifold`, its homeomorphism, and its non-diffeomorphism certificate. It does
not construct any input. The first remaining root cut is `M0605-T-WITNESS`; root debt remains M4
and theorem completion is false.
