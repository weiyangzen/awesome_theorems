# THM-M-0087 obligation tree

Registry version 1 freezes 17 canonical obligations before any proof-phase
credit. The denominator hash is authoritative in `obligation-registry.json`.
Every local semantic ledger is bounded by 100 steps; these budgets are split
thresholds, not evidence that a body is proved.

## M0087-ROOT

The root is exactly the elaborated four-part statement: for every separator
`G`, the preadditive coyoneda functor is full and faithful, the displayed tensor
functor is its left adjoint, and the tensor functor preserves finite limits. The
explicit construction of a named Serre quotient and equivalence is deliberately
outside this frozen target and is recorded by `M0087-S-BOUNDARY` rather than
silently inferred.

## Statement boundary

`M0087-S-TARGET` owns universes, typeclasses, binder order, opposite-ring module
convention, and conjunction shape. `M0087-S-BOUNDARY` prevents the stronger
classical quotient formulation from receiving proof credit without a checked
transport. Both are refinement nodes and do not duplicate proof bodies.

## Proof architecture

| Obligation | Input | Output and downstream use |
|---|---|---|
| `M0087-B-FULL` | separator `G`; `M0087-L-KERNEL` | fullness package consumed by assembly |
| `M0087-L-KERNEL` | finite-subcoproduct and separator arguments | vanishing needed for fullness and injective extension |
| `M0087-L-EXTEND` | kernel vanishing and an injective target | extension across `d g`, used by injective preservation |
| `M0087-B-FAITHFUL` | separator-to-faithful equivalence | faithfulness package consumed by assembly |
| `M0087-B-ADJUNCTION` | right-adjoint construction | inhabited tensor-Hom adjunction package |
| `M0087-L-INJECTIVE` | `M0087-L-EXTEND` and Baer criterion | preservation of injective objects |
| `M0087-L-MONO` | adjunction and injective preservation | preservation of monomorphisms |
| `M0087-L-ADDITIVE` | left-adjoint coproduct preservation | additivity of `tensorObj G` |
| `M0087-L-HOMOLOGY` | monomorphisms, cokernels, additivity | preservation of homology |
| `M0087-B-FINLIM` | the four preceding exactness lemmas | finite-limit-preservation package |
| `M0087-T-ASSEMBLE` | four branch packages | exact root conjunction |

The Lean certificate `root_of_packages` checks the final child-to-parent
composition without proving any premise. The current root cut set is
`M0087-B-FULL`, `M0087-B-FAITHFUL`, `M0087-B-ADJUNCTION`, and
`M0087-B-FINLIM`.

## Assurance overlays

`M0087-X-SOURCE`, `M0087-X-PROVENANCE`, and `M0087-X-TRUST` are informational
overlays excluded from the machine-proof denominator. They separately track
primary-source acceptance, unique terminal bodies and transitive dependencies,
and kernel/TCB/replay evidence. They cannot be proof premises or contribute
duplicate proof-body credit.

No obligation is marked closed by this phase. The pinned mathlib declarations
remain audited candidates for the later proof phase; audit completion, theorem
completion, H0, R0, hermetic replay, and independent verification remain open.
