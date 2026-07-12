# THM-M-0768 frozen obligation architecture

Item: `S56-M-0768-OBLIGATION_TREE`.

The registry freezes 16 semantic obligations before proof execution. The selected route follows
the pinned mathlib relation-preserving fixed-point construction, while keeping that imported bridge
open and uncredited in this phase.

## Typed proof route

```text
M0768-ROOT exact raw-function proposition
`-- M0768-T-SPECIALIZE checked specialization to the relation True
    `-- M0768-L-RELATIONAL stronger relation-preserving bridge (open)
```

The relational bridge is substantively expanded in the refinement graph into the empty-carrier
branch, least-fixed-point construction and equation, inverse image identity, piecewise map,
surjectivity, injectivity with cross-piece cases, and relation preservation. These refinement nodes
describe the bridge body and do not create duplicate machine proof credit. Statement transport,
source, provenance, trust, documentation, and workflow edges live in separate typed graphs.

## Node ledger

### m0768-root
Exact frozen proposition. `[H2, M3, R4]`; the registry supplies no inhabitant.

### m0768-s-interface
Checked binders, universes, hypotheses, conclusion, and empty-carrier eligibility. `[H2, M0-L, R4]`.

### m0768-s-transport
Checked equivalence with bundled embeddings and equivalences. `[H2, M0-L, R4]`.

### m0768-s-boundary
The empty-carrier branch must derive emptiness of the other carrier and construct the empty
equivalence without a `Nonempty` premise. `[H2, M4, R4]`.

### m0768-l-relational
Exact stronger relation-preserving bridge. `[H2, M4, R4]`; this is the minimal open root cut.

### m0768-c-fixpoint
Construct the monotone complement-image operator and its least fixed point. `[H2, M4, R4]`.

### m0768-l-fixpoint
Turn the fixed-point equation into the required complementary image partition. `[H2, M4, R4]`.

### m0768-c-inverse
Construct `invFun g` and identify the complement image using injectivity of `g`. `[H2, M4, R4]`.

### m0768-c-piecewise
Define the candidate map from `f` and `invFun g` on complementary pieces. `[H2, M4, R4]`.

### m0768-l-surjective
Derive surjectivity by computing the union of both range pieces. `[H2, M4, R4]`.

### m0768-l-injective
Derive injectivity on each piece and discharge both cross-piece cases. `[H2, M4, R4]`.

### m0768-t-relation
Prove the arbitrary relation for either selected piece. `[H2, M4, R4]`.

### m0768-t-specialize
Kernel-checked conditional specialization of the relational package to `True`. `[H2, M0-L, R4]`.

### m0768-x-source
Pending primary-source theorem/page/assumption/errata crosswalk. `[H2, M4, R4]`.

### m0768-x-foundation
Pending transitive axiom, TCB, classical-choice, quotient, and no-oracle certificate. `[H2, M4, R4]`.

### m0768-x-provenance
Pending terminal-body/import/hash/replay inventory. `[H2, M4, R4]`.

## Freeze boundary

The checked specialization consumes the relational package as an explicit premise. It proves
neither that premise nor the root here. Normalization is inapplicable because the bridge consumes
arbitrary raw functions directly; computation is inapplicable because no solver, reflection,
certificate, or oracle participates. Any correction, split, merge, or eligibility change requires
a new registry version with an append-only delta. This phase claims no audit, theorem, validation,
or release completion.
