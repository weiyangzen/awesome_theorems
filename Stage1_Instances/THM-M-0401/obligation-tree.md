# THM-M-0401 obligation tree

Item: `S56-M-0401-OBLIGATION_TREE`. This freezes registry version
`THM-M-0401-OBLIGATIONS-v1`; it is architecture evidence, not a proof receipt. The root remains
`M4`, and every composition certificate remains open.

## Frozen architecture

The proof route is the qualitative Subspace-Theorem route for the exact product-form target:

```text
M0401-ROOT
`-- M0401-T-FINITE-DENOMINATORS
    |-- M0401-L-FINITE-SUBSPACES
    |   |-- M0401-N-INTEGER-POINT
    |   |-- M0401-C-LINEAR-FORMS
    |   |-- M0401-C-HEIGHT-BOUND
    |   `-- M0401-L-SUBSPACE-BRIDGE
    `-- M0401-T-SUBSPACE-FINITE
        |-- M0401-L-RELATION-EXTRACTION
        `-- M0401-L-INDEPENDENCE-LIMIT
```

Root-relevant trust, definition, and provenance obligations are separately modeled rather than
being smuggled into proof edges. The coordinatewise formulation is a nonroot informational
transport. It is excluded from all required denominators and cannot inflate coverage.

## Node boundaries

### M0401-ROOT

The exact declaration is the normalized product-form proposition in `Statement.lean`. It consumes
the terminal finite-denominator result. Its source pinpoint, Lean proof, composition, trust, and
readable-review gates remain open.

### M0401-S-DEFINITIONS

This node owns the encodings of algebraicity, rational independence with one, nearest-integer
distance, and exceptional denominators. It is root-relevant even though it supplies a formal
encoding rather than an independent human theorem.

### M0401-S-FOUNDATION

This node will own the eventual machine-derived axiom and transitive TCB report. It cannot close
before the root has a proof body.

### M0401-N-INTEGER-POINT

Unpack each exceptional denominator, select the witnessing nearest integers, and package them with
the denominator as a single integer point. This is a representation bridge and therefore cannot be
hidden in a later tactic.

### M0401-C-LINEAR-FORMS

Construct `X0` and `alpha_i X0 - Xi` over an appropriate number field and establish the algebraic
coefficient and independence hypotheses demanded by the chosen Subspace Theorem interface.

### M0401-C-HEIGHT-BOUND

Convert the product inequality into the exact height inequality used by the Subspace Theorem. This
includes bounding the nearest integers, comparing point height with `q`, and reconciling `Real.rpow`
with the theorem's exponent convention.

### M0401-L-SUBSPACE-BRIDGE

This is the central external/formal boundary: a qualitative Subspace Theorem that yields finitely
many proper rational subspaces. The anchor audit found no pinned Lean 4 body. The node is required
and critical rather than excluded merely because it is difficult.

### M0401-L-FINITE-SUBSPACES

Compose the point, linear-form, height, and Subspace-Theorem obligations to cover all exceptional
points by finitely many proper rational subspaces.

### M0401-L-RELATION-EXTRACTION

Extract a fixed nonzero rational annihilator from each proper subspace, giving one relation among
the denominator and nearest integers.

### M0401-L-INDEPENDENCE-LIMIT

Show that infinitely many denominators satisfying one fixed relation would be unbounded; divide by
`q`, pass the nearest-integer errors to zero, and contradict linear independence of
`1, alpha_0, ..., alpha_(n-1)`. This limit argument is independently modeled because it carries
material proof work.

### M0401-T-SUBSPACE-FINITE

Combine relation extraction and the independence-limit lemma to obtain finiteness within one fixed
proper subspace.

### M0401-T-FINITE-DENOMINATORS

Take the finite union of the per-subspace denominator sets and identify it with the exceptional
set in the canonical conclusion.

### M0401-X-PROVENANCE

Resolve and content-address every eventual terminal proof body, wrapper, dependency, axiom, and TCB
boundary. It is currently open because no proof body exists.

### M0401-S-COORDINATEWISE-TRANSPORT

This alternate formulation is explicitly nonroot and informational. A future public-scope change
must create a new append-only registry version and eligibility delta.

## Denominator and status boundary

The canonical projection in `obligation-registry.json` hashes to
`3e0527abbf2146164c691c2e22b29bb7501997a0c80d5e6718b746159e762dcc`. There are 14 inventory
obligations, 13 required machine obligations, 10 required human-source obligations, and 13 required
readable obligations. Zero obligations are claimed machine-closed. The minimal architectural root
cut set highlights the missing Subspace-Theorem bridge and independence-limit package, but it does
not imply that closing only those two nodes closes the theorem: every dependency and composition
gate still applies.

## Validation

The structural validator checks the frozen hash, unique registry/node identities, complete node
schema, leaf budgets, typed reciprocal adjacency, proof-graph acyclicity, root reachability of all
required mathematical obligations, exact denominator projections, and the fail-closed root status.
Exact commands and results are recorded in `obligation-tree-validation.md`.
