# THM-M-0527 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 34 root-relevant obligations for
`S56-M-0527-OBLIGATION_TREE`. All 34 belong to the machine, human-source, and
readable denominators. Their canonical registry projection digest is
`3b54d00ce59d2dba93b119edf669c1bf39c3f402e5e0d7dcb7139f013f135df1`.
No item is excluded or credited as closed. Planned leaf signatures describe
future proof work and are not elaborated declarations.

## Typed proof route

```text
M0527-ROOT [open M3]
|-- M0527-EX: construct a cover for every subgroup
|   |-- based-path representatives and the H-equivalence relation
|   |-- quotient total space and well-defined endpoint projection
|   |-- topology from admissible semilocally simply connected neighborhoods
|   |-- evenly-covered sheet decomposition
|   |-- connectedness and the constant-path basepoint
|   `-- both inclusions proving inducedSubgroup P_H = H
`-- M0527-FIB: characterize fibers by pointed isomorphism
    |-- equal ranges give comparison lifts in both directions
    |-- uniqueness makes the lifts inverse, hence a homeomorphism over X
    `-- a pointed isomorphism identifies induced maps and subgroup ranges
```

The proof graph recursively reaches every registered ID and is acyclic.
Provenance, evidence, trust, documentation, refinement, and workflow relations
are held in separate typed graphs so none can be counted as a proof premise.

## Leaf and composition policy

Every nonleaf is marked `split-required`. Each current leaf has a substantive
ledger and a budget of at most 100 steps. Future proof work must split a leaf
before closure if its exact Lean signature or implementation exposes hidden
semantic work. In particular, the quotient topology, representative-independent
sheet charts, covering-map certificate, and subgroup-range equality may not be
collapsed into an invocation of a deep theorem without recording that theorem
as a bridge and auditing its terminal body.

No child-to-parent composition certificate exists yet. `IsCoveringMap` lifting
and uniqueness declarations found by the anchor audit are candidate ingredients
only. They do not construct the cover associated to an arbitrary subgroup.

## Phase verdict

The obligation registry, receipt, and seven typed graphs are structurally
self-tested, and the exact root statement re-elaborates with the pinned Lean
toolchain. The remaining root cut set is `M0527-EX-COVER`,
`M0527-EX-RANGE`, and `M0527-FIB`. The root remains M3. This phase supplies no
proof body, source acceptance, composition certificate, audit completion, or
theorem-completion claim. Master acceptance is still required.
