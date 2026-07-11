# THM-M-0580 frozen obligation architecture

Item: `S56-M-0580-OBLIGATION_TREE`

The registry freezes 20 root-relevant obligations for the exact declaration
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. Its denominator is bound
to the elaborated statement and bounded anchor audit. Any corrected statement,
split, merge, exclusion, or eligibility change requires an append-only registry
revision; proof availability cannot change this frozen denominator.

## Typed proof route

The proof graph first separates the compatible topological smoothing boundary
(`M0580-N-SMOOTH`) from the smooth Perelman package
(`M0580-T-SMOOTH-POINCARE`). The smooth route exposes initial metric
construction, short-time Ricci flow, no-local-collapsing, canonical
neighborhoods, surgery construction and iteration, finite extinction, prime
decomposition, and the final fundamental-group elimination. These are distinct
semantic obligations rather than one opaque invocation of "Perelman".

`root_of_smoothing_and_smooth_poincare` kernel-checks the binder-preserving
composition of the two abstract packages into the exact topological target.
Neither package is inhabited in `ObligationTree.lean`, so this conditional
certificate supplies no proof credit for the root.

## Mandatory layers

### M0580-S-DEFINITIONS

The statement models a three-manifold using charts over real Euclidean
three-space and concludes a homeomorphism with the unit sphere in real
Euclidean four-space.

### M0580-S-DOMAIN

The ordered universe and typeclass binders remain fixed. In particular,
orientability is not silently added, and connectedness is not duplicated when
it is already carried by `SimplyConnectedSpace`.

### M0580-S-BOUNDARY

Empty, disconnected, noncompact, non-Hausdorff, and boundary-manifold variants
are not substitutes for the canonical target. Exact boundary consequences and
mutation checks remain proof-lane obligations.

### M0580-S-TRANSPORT

The local aliases have a checked definitional equivalence. Homotopy, smooth,
PL, and source formulations require explicit directional transports and do not
inherit root credit by name.

### M0580-S-FOUNDATION

Classical principles, quotients, imported axioms, kernel trust, and the
no-oracle policy require a transitive release audit.

### M0580-N-SMOOTH

A compatible smooth structure must be installed on the exact fixed topological
manifold. Replacing its topology or chart structure would not compose with the
root.

### M0580-C-METRIC

A smooth Riemannian metric must be constructed with the compactness and
geometric invariants needed by the flow.

### M0580-L-SHORT-TIME

The initial metric must produce a controlled short-time Ricci flow.

### M0580-L-NONCOLLAPSE

The no-local-collapsing package must provide the precise quantitative input
used in singularity analysis.

### M0580-L-CANONICAL

High-curvature regions require canonical-neighborhood and curvature-control
theorems with compatible constants.

### M0580-C-SURGERY

Surgery parameters, necks, and caps must be constructed, and every invariant
needed for continued flow must survive the operation.

### M0580-L-SURGERY-EXISTS

The surgery process must iterate without forbidden accumulation while
preserving the analytic estimates.

### M0580-L-FINITE-EXTINCTION

Simple connectedness must imply finite extinction under the exact surgery-flow
hypotheses; an isolated extinction slogan is not a terminal proof.

### M0580-B-DECOMPOSITION

Finite extinction must be translated into an exhaustive prime-decomposition
classification and recomposed back to the original manifold.

### M0580-L-PI1-ELIMINATION

Fundamental-group calculations must eliminate nontrivial spherical space
forms, bundle factors, and multiple connected-sum factors, leaving `S^3`.

### M0580-T-SMOOTH-POINCARE

All analytic and topological children must compose into the smooth
three-dimensional Poincare conclusion.

### M0580-T-ASSEMBLE

The checked local theorem consumes compatible smoothing and the smooth result
to return the exact frozen topological proposition.

### M0580-X-SOURCE

Every material node still needs pinpoint primary and reviewed-exposition
crosswalks, including conventions and errata. The existing paper list is not
H0 node coverage.

### M0580-X-PROVENANCE

Terminal bodies, wrappers, imports, axioms, unsafe features, TCB inputs, and
replay receipts remain an informational release overlay and earn no semantic
proof credit.

## Step and closure boundary

Every leaf has a prospective semantic budget of at most 100 substantive
steps. Central packages remain explicitly expanded because a short call to a
deep theorem cannot satisfy the leaf rule. Typed proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs are stored
separately in `typed-graphs.json`.

Only the statement alias/transport surfaces and conditional final composition
are locally checked. The root remains `M4`; `audit_complete=false`,
`root_closed=false`, and `theorem_complete=false`. The immediate root cut set
is compatible smoothing plus the entire smooth Perelman package.
