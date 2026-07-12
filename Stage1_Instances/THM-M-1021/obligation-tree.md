# THM-M-1021 frozen obligation architecture

## Freeze boundary

This is registry version 1 for `S56-M-1021-OBLIGATION_TREE`. It freezes 50
canonical IDs before proof execution: 46 root-relevant mathematical
obligations and four informational trust/provenance overlays. The ordered
machine, human-source, readable, and inventory denominators are stored in
`obligation-registry.json`; their canonical projection digest is
`032b467a59ae30caf2d637b9707358e6ba7259edf774ba0bd8bf162e48924688`.
No mathematical obligation is excluded because no proof was found. The
`M1021-X*` overlays are excluded from proof and source denominators solely
because they record external-body provenance and trust rather than a
mathematical conclusion.

## Typed proof route

```text
M1021-ROOT  exact BochnerTarget biconditional [open M3]
|-- M1021-S  definitions, domains, boundary cases, transports, foundation
|-- M1021-N  Hermitian, Fourier-sign, finite-family, and continuity normalizations
|-- M1021-B  exhaustive forward/reverse direction split
|   |-- BF  probability measure implies continuity, normalization, positivity
|   |-- BR  normalized continuous positive-definite function has a measure
|   `-- BM  exact biconditional merge
|-- M1021-C  reverse-direction representing-measure construction [root cut]
|   |-- C1  test-function Fourier algebra
|   |-- C2  positive functional induced by phi
|   |-- C3  Riesz-Markov representation boundary
|   |-- C4  total-mass normalization
|   `-- C5  pointwise recovery of phi
|-- M1021-L  forward analytic engine
|   |-- L1  characteristic-function continuity
|   |-- L2  value at zero
|   `-- L3  quadratic sum as an integral of a square
`-- M1021-T  forward, reverse, root, and trust composition certificates
```

The full reciprocal edges appear in `typed-graphs.json`. Proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs are separate.
The combined proof/refinement graph is acyclic and reaches all 46 required
mathematical obligations from the root. In particular, the anchor-only
mathlib continuity and normalization declarations remain provenance links and
cannot masquerade as the missing reverse representation theorem.

## Leaf and composition policy

Every nonleaf has `step_budget: "split-required"`. Each currently leaf-shaped
record has a small planned semantic ledger, but none is certified as a final
proof leaf: most formal targets remain planned signatures, primary-source
pinpoints remain incomplete, and no child-to-parent composition certificate
exists. Proof work must split any leaf when its exact Lean signature or proof
reveals a hidden central theorem, case split, construction invariant, or
ledger over 100 substantive steps.

The reverse direction is deliberately expanded through a positive functional,
Riesz-Markov boundary, probability normalization, and pointwise transform
recovery. Naming Riesz-Markov is not proof credit: `M1021-C3.1` and
`M1021-C3.2` must identify the exact test space, hypotheses, pinned declaration
or local body, statement transport, and trust closure. Similarly, the forward
positivity branch expands the finite quadratic sum into an integral of a
pointwise squared modulus instead of treating positivity as immediate.

No parent composition is credited. The proof phase must add checked harnesses
that bind exact child and parent fingerprints, consume every required child,
and yield the complete declared parent without undeclared premises.

## Provenance and trust boundary

The audit found pinned mathlib characteristic-function APIs, including
`continuous_charFun` and `charFun_zero`, but no exact reverse Bochner theorem.
Those candidates are recorded at `M1021-X1`. The still-absent terminal body for
the representation engine is `M1021-X2`; Lean, imports, axioms, compiled
artifacts, and executable validation recipes are `M1021-X3`. These overlay
nodes are readable and root-relevant for release trust, but are informational
for mathematical coverage and supply no closure.

## Phase verdict

The registry and seven typed graphs are frozen and structurally self-tested,
and `BochnerStatement.lean` re-elaborates under the pinned toolchain. This
phase proves neither direction and admits no existing body. The root remains
`[H1, M3, R3]`; its immediate remaining cut set is the reverse implication
`M1021-BR` and representing-measure construction `M1021-C`. There is no
`AUDIT-Z` or `THEOREM-Z` claim, and master acceptance is still required.
