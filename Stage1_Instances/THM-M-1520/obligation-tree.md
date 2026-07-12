# THM-M-1520 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 16 canonical semantic obligations for
`S56-M-1520-OBLIGATION_TREE` before proof execution. The selected route is the classical
canonical-coordinate argument: zero divergence of the Hamiltonian vector field, the spatial
variational equation, unit flow Jacobian, and a global change-of-variables bridge to
`MeasurePreserving`. This selection does not assert that pinned mathlib already supplies those
bridges; the anchor audit found that it does not.

The machine, human-source, and readable denominators are explicit ordered ID sets in
`obligation-registry.json`. Source and trust overlays are separated from proof edges and cannot
receive proof credit. Any later split or correction requires registry version 2 and an append-only
ID delta; status availability cannot change version 1 eligibility.

## Typed proof route

```text
M1520-ROOT  exact LiouvilleStatement [open M3]
|-- M1520-T-ALL-TIMES  complete analytic package [open M4]
|   `-- M1520-L-CHANGE  global change of variables
|       |-- M1520-L-JACOBIAN  determinant one
|       |   |-- M1520-C-VARIATION  spatial variational equation
|       |   |   `-- M1520-N-FLOW  regular diffeomorphic flow
|       |   |       |-- M1520-S-DOMAIN  exact hypotheses
|       |   |       `-- M1520-S-BOUNDARY  n=0, t=0, completeness
|       |   `-- M1520-B-DIVERGENCE  div X_H = 0
|       |       `-- M1520-S-DEFS  canonical coordinates and X_H
|       `-- M1520-L-MEASURABLE  measurable map and inverse
`-- M1520-T-ASSEMBLE  checked conditional root interface [M0-L]
```

`M1520-S-FOUNDATION`, `M1520-X-SOURCE`, `M1520-X-PROVENANCE`, and `M1520-X-TRUST`
remain release/source support nodes in their correctly typed graphs. They are not smuggled into the
mathematical proof graph. The reciprocal `proof_requires`/`composes` pairs, refinement, provenance,
evidence, trust, documentation, and workflow graphs are stored in `typed-graphs.json`.

## Leaf and composition policy

Each current leaf has a substantive planned ledger and budget at most 100. These are planning
ceilings, not readability or closure claims. Proof execution must split a node if its exact Lean
signature exposes a hidden case, representation transport, imported central theorem, or ledger
over 100 steps. In particular, neither the determinant evolution formula nor change of variables
may be replaced by a one-line opaque citation without its own provenance and composition evidence.

`ObligationTree.lean` checks only the final child-to-root interface. Its theorem consumes the
explicit `LiouvilleAnalyticPackage` premise and yields the exact `LiouvilleStatement`; it does not
construct the premise. Consequently `M1520-T-ASSEMBLE` is locally closed while the root remains
open with minimal root cut `M1520-T-ALL-TIMES`.

## Status boundary

The obligation registry and seven typed graphs are frozen and structurally tested. This phase does
not prove divergence cancellation, flow differentiability, the determinant formula, change of
variables, the analytic package, or the exact root. It does not establish H0/R0, audit completion,
hermetic replay, or theorem completion. Lifecycle remains `planned`, the root vector remains
`[H2, M3, R3]`, and master acceptance is still required.
