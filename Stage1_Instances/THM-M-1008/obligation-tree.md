# THM-M-1008 frozen obligation architecture

Item: `S56-M-1008-OBLIGATION_TREE`.

The registry freezes 15 semantic obligations before proof execution. It separates the hard
Hewitt-Savage bridge from mathlib's already checked self-independence zero-one endpoint, so the
endpoint cannot be mistaken for a proof of finite-permutation invariance implying the conclusion.

## Typed proof route

```text
M1008-ROOT exact canonical proposition
`-- M1008-T-ASSEMBLE checked conditional composition
    |-- M1008-T-SELF-INDEPENDENCE exact event is independent of itself
    |   `-- M1008-L-LIMIT-FACTOR approximation limit gives factorization
    |       |-- M1008-N-CYLINDER finite-coordinate approximation
    |       |-- M1008-C-DISJOINT-BLOCK finite-support displacing permutation
    |       |-- M1008-L-IID-REINDEX independence and path-law preservation
    |       |-- M1008-L-SYMMETRY-TRANSFER exact event invariance
    |       `-- M1008-L-BLOCK-INDEPENDENCE disjoint-block independence
    `-- M1008-X-ZERO-ONE pinned self-independence endpoint
```

`M1008-S-DEFINITIONS`, `M1008-S-BOUNDARY`, and `M1008-S-FOUNDATION` are refinement/trust
obligations rather than proof children. `M1008-X-SOURCE` and `M1008-X-PROVENANCE` live in distinct
source, documentation, provenance, trust, and workflow graphs and receive no mathematical proof
credit.

## Semantic ledgers

### m1008-root
Exact elaborated path-space target. `[H1, M2, R3]`; no inhabitant has been found.

### m1008-s-definitions
The binder order, iid assumptions, measurable event, finite-support action, and pullback conclusion
are fixed by `Statement.lean`. `[H1, M0-L, R3]` for statement identity only.

### m1008-s-boundary
Constant processes, empty/universal events, and identity permutation remain included. Mere
exchangeability and almost-everywhere symmetry remain excluded. `[H1, M0-L, R3]`.

### m1008-s-foundation
Transitive import, axiom, TCB, no-oracle, and replay certification remains open. `[H1, M4, R3]`.

### m1008-n-cylinder
Obtain finite-coordinate measurable approximants with quantitative error control. This substantive
product-sigma approximation bridge is not supplied by the anchor audit. `[H1, M4, R3]`.

### m1008-c-disjoint-block
Construct a finite-support permutation sending the approximant's coordinate set to a disjoint
block, with support and disjointness invariants explicit. `[H1, M4, R3]`.

### m1008-l-iid-reindex
Use `iIndepFun.precomp`, `IdentDistrib.pi`, and measurable-preimage transport to preserve the
relevant iid/path-law structure. The anchor declarations are checked, but this exact composition
remains open. `[H1, M4, R3]`.

### m1008-l-symmetry-transfer
Turn the pointwise `IsSymmetricEvent` hypothesis into equality of the exact original and permuted
pullback events. `[H1, M4, R3]`.

### m1008-l-block-independence
Derive event independence from mutual independence on disjoint finite coordinate blocks, including
all measurability and generated-sigma-algebra premises. `[H1, M4, R3]`.

### m1008-l-limit-factor
Combine approximation errors, event equality, equal laws, and block independence, then pass to the
limit to obtain `mu (A inter A) = mu A * mu A`. `[H1, M4, R3]`.

### m1008-t-self-independence
Strengthen the factorization result to the exact `IndepSet A A mu` interface required by mathlib's
endpoint. This is the minimal open root cut. `[H1, M4, R3]`.

### m1008-x-zero-one
`measure_eq_zero_or_one_of_indepSet_self` is a pinned, kernel-checked proper sub-obligation. It does
not establish its self-independence premise. `[H1, M0-P, R3]`.

### m1008-t-assemble
`root_of_selfIndependencePackage` conditionally composes the exact package and endpoint into the
canonical target. `[H1, M0-L, R3]`; its open premise prevents root proof credit.

### m1008-x-source
Node-level primary-source theorem/page/assumption/errata mapping remains pending. `[H1, M4, R3]`.

### m1008-x-provenance
Terminal-body, wrapper, import, axiom, TCB, and replay inventory remains pending. `[H1, M4, R3]`.

## Freeze boundary

The remaining root cut is `M1008-T-SELF-INDEPENDENCE`. The checked endpoint and conditional
assembly do not prove that package. This phase supplies no root closure, audit completion, or
theorem completion. Any correction, split, merge, exclusion, or eligibility change requires a new
registry version and append-only delta.
