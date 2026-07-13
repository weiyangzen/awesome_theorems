# THM-M-0861 frozen obligation tree

This is the architecture record for `S56-M-0861-OBLIGATION_TREE`. It freezes a source-faithful
direct proof route before any proof-phase closure is credited. The canonical root remains open at
`[H1, M4, R4]`; every entry below is an obligation or conditional interface, not a completed proof.

## Root route

The exact root is the least-palette equality in `Statement.lean`. `ObligationTree.lean` defines its
exact upper and lower conjuncts as separate propositions and kernel-checks that both jointly yield
the canonical target. Neither proposition is inhabited. The upper route applies the stronger
fixed-`k` Satz C statement at `k = maxDegree`; the lower route restricts any proper coloring to each
finite incidence fiber and then takes the vertex-set supremum.

The machine proof cut is therefore `M0861-T-UPPER` and `M0861-T-LOWER`. Source, foundation,
provenance, trust, readability, workflow, validation, and release boundaries remain additional
theorem-completion cuts. Hall, line-graph, SimpleGraph coloring, Formal Conjectures, ATLAS, and the
matching-cover PR are not proof premises: the anchor audit classified them only as substrate,
mismatch, or rejected leads.

## Source-shaped Satz C route

The upper package follows Koenig's printed pages 455-456 rather than silently replacing the
multigraph by a simple graph. It uses strong induction on the finite actual-edge cardinality. The
source base is `ncard G.edgeSet <= k`: embed all actual edge identities injectively into `Fin k`.
In the large branch, choose one actual edge, delete precisely that identity while preserving the
ambient edge type and all parallel identities, and apply the induction hypothesis to the deletion
graph.

The deletion lowers both endpoint degrees, so each endpoint misses a palette value. A common
missing value permits direct insertion. Otherwise, construct the maximal trail alternating between
the two missing values. Properness makes its next edge unique; finite edgeSet and no repetition make
the trail terminate. Its color parity and the frozen Bool bipartition show that it cannot reach the
other endpoint. Swapping the two colors along this component preserves properness and creates a
common missing color, after which the deleted edge can be inserted.

This route owns the multigraph deletion graph, actual-edge subtype transports, alternating-trail
representation, termination, parity, swap boundary, and extension. Pinned mathlib currently has no
ready multigraph path or edge-coloring package that discharges these interfaces.

## Node ledger

Each anchor below is the stable public target referenced by `typed-graphs.json`. The registry and
typed bundle contain the exact formal target, output, H/M/R vector, risk, eligibility, source and
provenance IDs, validation recipe, ownership, validity, and structured semantic ledger for the
same obligation.

<a id="m0861-root"></a>
### M0861-ROOT
Exact canonical theorem. Conditional root composition is checked; both mathematical children remain open.

<a id="m0861-s-target"></a>
### M0861-S-TARGET
Exact arbitrary-carrier finite-actual-set interface from the statement expression fingerprint.

<a id="m0861-s-representation"></a>
### M0861-S-REPRESENTATION
`Graph Vertex Edge` preserves actual edge identity and parallel multiplicity.

<a id="m0861-s-bipartite"></a>
### M0861-S-BIPARTITE
The Bool bipartition separates every link endpoint and excludes loops.

<a id="m0861-s-coloring"></a>
### M0861-S-COLORING
Proper colorings act on actual-edge subtypes and least palettes are natural numbers.

<a id="m0861-s-boundary"></a>
### M0861-S-BOUNDARY
Empty, edgeless, Delta-zero, disconnected, nonregular, and parallel-edge cases remain included.

<a id="m0861-s-transport"></a>
### M0861-S-TRANSPORT
Definitional Iff between the least-palette root and its exact upper/lower conjunction.

<a id="m0861-s-foundation"></a>
### M0861-S-FOUNDATION
Open foundation, axiom, compiled-artifact, TCB, and no-oracle acceptance boundary.

<a id="m0861-n-bounded"></a>
### M0861-N-BOUNDED
Fixed-`k` degree-bound interface matching Satz C; definition elaborated, proof open.

<a id="m0861-t-assemble"></a>
### M0861-T-ASSEMBLE
Checked conditional assembly of exact upper and lower packages into the root.

<a id="m0861-t-upper"></a>
### M0861-T-UPPER
Upper coloring conjunct at the frozen maximum degree; open.

<a id="m0861-l-degree-le-max"></a>
### M0861-L-DEGREE-LE-MAX
Every actual vertex degree is bounded by the finite supremum; open.

<a id="m0861-t-lower"></a>
### M0861-T-LOWER
Every proper palette has size at least the maximum degree; open.

<a id="m0861-l-incidence-fin"></a>
### M0861-L-INCIDENCE-FIN
Incidence fibers inherit finiteness from the actual edge set; open.

<a id="m0861-l-color-injective"></a>
### M0861-L-COLOR-INJECTIVE
Properness restricts to an injection on one incidence fiber; open.

<a id="m0861-l-sup-lower"></a>
### M0861-L-SUP-LOWER
Pointwise degree bounds lift through `Finset.sup`; open.

<a id="m0861-b-edge-induction"></a>
### M0861-B-EDGE-INDUCTION
Strong induction over finite actual-edge cardinality; open.

<a id="m0861-b-edge-count-split"></a>
### M0861-B-EDGE-COUNT-SPLIT
Exhaustive source-shaped split between `ncard edgeSet <= k` and the deletion branch.

<a id="m0861-b-small-edge-count"></a>
### M0861-B-SMALL-EDGE-COUNT
Color every actual edge by a global injection when the edge count is at most `k`; open.

<a id="m0861-l-small-palette-embed"></a>
### M0861-L-SMALL-PALETTE-EMBED
Finite actual-edge subtype embeds into `Fin k`; open.

<a id="m0861-b-large-edge-count"></a>
### M0861-B-LARGE-EDGE-COUNT
Choose, delete, recolor, and reinsert one actual edge; open.

<a id="m0861-l-choose-actual-edge"></a>
### M0861-L-CHOOSE-ACTUAL-EDGE
Extract one edge and two distinct endpoints using bipartiteness; open.

<a id="m0861-c-erase-edge"></a>
### M0861-C-ERASE-EDGE
Deletion graph on unchanged ambient vertex and edge types; open.

<a id="m0861-l-erase-sets"></a>
### M0861-L-ERASE-SETS
Exact vertex, edge, and retained-link equations for deletion; open.

<a id="m0861-l-erase-card"></a>
### M0861-L-ERASE-CARD
Deletion removes exactly one actual edge and supplies the induction decrease; open.

<a id="m0861-l-erase-bipartite"></a>
### M0861-L-ERASE-BIPARTITE
The same side assignment proves the deletion graph bipartite; open.

<a id="m0861-l-erase-degree"></a>
### M0861-L-ERASE-DEGREE
Deletion preserves the global degree bound and strictly lowers both endpoint degrees; open.

<a id="m0861-c-ih-coloring"></a>
### M0861-C-IH-COLORING
Apply induction to the deletion graph and retain original edge identities; open.

<a id="m0861-l-actual-edge-transport"></a>
### M0861-L-ACTUAL-EDGE-TRANSPORT
Checked-equivalence plan for deletion and original actual-edge subtypes; open.

<a id="m0861-l-k-positive-of-edge"></a>
### M0861-L-K-POSITIVE-OF-EDGE
An actual edge under the degree bound forces a nonempty `Fin k`; open.

<a id="m0861-c-missing-colors"></a>
### M0861-C-MISSING-COLORS
Choose one absent color at each endpoint; open.

<a id="m0861-l-palette-pigeonhole"></a>
### M0861-L-PALETTE-PIGEONHOLE
Fewer than `k` incident colored edges omit a palette value; open.

<a id="m0861-b-missing-split"></a>
### M0861-B-MISSING-SPLIT
Exhaustive common-versus-distinct missing-color split; open.

<a id="m0861-b-common-missing"></a>
### M0861-B-COMMON-MISSING
Direct insertion using a common absent color; open.

<a id="m0861-b-distinct-missing"></a>
### M0861-B-DISTINCT-MISSING
Alternating-component recoloring route for distinct missing colors; open.

<a id="m0861-l-cross-color-present"></a>
### M0861-L-CROSS-COLOR-PRESENT
No common missing color forces each endpoint to see the other's missing color; open.

<a id="m0861-c-alt-state"></a>
### M0861-C-ALT-STATE
Local edge-identity-preserving alternating-trail state; open.

<a id="m0861-l-color-uniqueness"></a>
### M0861-L-COLOR-UNIQUENESS
At most one incident edge of a given color at any vertex; open.

<a id="m0861-c-alternating-trail"></a>
### M0861-C-ALTERNATING-TRAIL
Construct the deterministic maximal two-color trail; open.

<a id="m0861-l-trail-norepeat"></a>
### M0861-L-TRAIL-NOREPEAT
The alternating construction revisits neither vertices nor edges; open.

<a id="m0861-l-trail-terminates"></a>
### M0861-L-TRAIL-TERMINATES
Finite edgeSet and no repetition imply maximal finite termination; open.

<a id="m0861-l-trail-alternates"></a>
### M0861-L-TRAIL-ALTERNATES
Trail-edge colors alternate with the selected initial orientation; open.

<a id="m0861-l-endpoint-parity"></a>
### M0861-L-ENDPOINT-PARITY
Color parity conflicts with the opposite Bool sides if the trail reaches the second endpoint; open.

<a id="m0861-l-b-not-reached"></a>
### M0861-L-B-NOT-REACHED
The alternating component avoids the second endpoint; open.

<a id="m0861-c-swap"></a>
### M0861-C-SWAP
Exchange the two selected colors on precisely the alternating component; open.

<a id="m0861-l-swap-proper"></a>
### M0861-L-SWAP-PROPER
The exchange preserves properness across internal and boundary vertices; open.

<a id="m0861-l-swap-missing"></a>
### M0861-L-SWAP-MISSING
The exchange makes one color absent at both deleted-edge endpoints; open.

<a id="m0861-c-extend-edge"></a>
### M0861-C-EXTEND-EDGE
Extend a retained-edge coloring across the erased edge; open.

<a id="m0861-t-satz-c"></a>
### M0861-T-SATZ-C
Compose the full source-strengthened fixed-`k` upper theorem; open.

<a id="m0861-x-source"></a>
### M0861-X-SOURCE
Primary-source admission, translation, equality bridge, errata, node map, and review; open.

<a id="m0861-x-provenance"></a>
### M0861-X-PROVENANCE
Terminal-body and immutable-origin closure without alias duplication; open.

<a id="m0861-x-trust"></a>
### M0861-X-TRUST
Transitive axiom, TCB, unsafe/oracle, compiled-artifact, and replay audit; open.

<a id="m0861-x-readable"></a>
### M0861-X-READABLE
Complete independently reviewed proof outline and long reconstruction; open.

<a id="m0861-x-workflow"></a>
### M0861-X-WORKFLOW
Dependency-ordered proof through release acceptance; open.

## Typed-graph and status boundary

The bundle separates proof, refinement, provenance, evidence, trust, documentation, and workflow.
The conditional upper/lower-to-assembly edges and transport/assembly-to-root edges are `composes`;
all sixty-one other internal reverse relations are explicitly unverified `logical_decomposition` plans
until later proof work supplies exact Lean child-to-parent certificates. The evidence graph is empty because no obligation has an accepted
proof receipt. All fifty-four ledgers have a substantive budget at most 100, but that alone grants
neither R0 nor proof credit.

This phase freezes architecture only. It does not establish H0, M0, R0, AUDIT-Z, root closure,
theorem completion, validation, release, independent verification, or master acceptance.
