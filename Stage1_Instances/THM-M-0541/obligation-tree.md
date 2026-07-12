# THM-M-0541 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 36 canonical IDs for `S56-M-0541-OBLIGATION_TREE`: 35 required
mathematical obligations and one informational trust overlay, `M0541-X3`. The canonical
denominator digest is `6a11aa4b9895b88664431f07a1ac201371aaeaf2b71aeb773fa56b40dad7e50e`.
Eligibility was selected from the elaborated `StatementShape` and the direct combinatorial route,
not from observed proof closure. Every mathematical node is therefore in the machine, source, and
readable denominators even though no proof body is present.

The anchor audit's categorical `AlternatingFaceMapComplex.d_squared` remains provenance-only. It
does not replace the concrete construction from `AbstractSimplicialComplex` to the exact `Finsupp`
chains and basis formula. The frozen proof route instead exposes that missing construction and the
finite cancellation engine explicitly.

## Typed proof route

```text
M0541-ROOT  exact StatementShape [open M3]
|-- S  statement/foundation refinements
|   |-- S1 definitions                 |-- S4 route/transport boundary
|   |-- S2 domains and coefficients    `-- S5 axiom policy
|   `-- S3 degenerate cases
|-- N  normalization to basis coefficients and ordered deletion pairs
|   |-- N1 erased-simplex ordering     |-- N3 Finsupp extensionality
|   |-- N2 double-index normalization  `-- N4 basis reduction
|-- B  exhaustive relative-order split
|   |-- B1 first index smaller         |-- B3 sign cancellation
|   |-- B2 second index smaller        `-- B4 finite-sum recomposition
|-- C  construct the boundary family
|   |-- C1 face well-definedness       |-- C3 additive Finsupp extension
|   |-- C2 basis boundary              `-- C4 basis formula
|-- L  boundary-square cancellation engine
|   |-- L1 iterated-face identity      |-- L4 global paired-sum cancellation
|   |-- L2 opposite signs              `-- L5 double-boundary expansion
|   `-- L3 local singleton cancellation
|-- X  pinned APIs and trust boundary
|   |-- X1 Finsupp APIs  |-- X2 sum APIs  `-- X3 informational TCB overlay
`-- T  exact-root assembly
    |-- T1 alternating formula  |-- T2 square-zero on all chains  `-- T3 closure
```

The machine-readable bundle keeps proof, refinement, provenance, evidence, trust, documentation,
and workflow edges separate. Proof and refinement edges are acyclic and make every required
obligation reachable from `M0541-ROOT`. Source, trust, and workflow edges cannot discharge a proof
premise.

## Leaf and composition policy

Each current nonleaf is marked `split-required`. Each current leaf has a planned semantic ledger
and a budget no larger than 100, but these are planning bounds rather than proof counts. Exact Lean
signatures still have to be implemented for planned lemmas, and any leaf that reveals a hidden
theorem, branch, representation crossing, or oversized ledger must be split in a later registry
version.

No child-to-parent composition certificate is credited here. Proof work must construct checked
harnesses binding child and parent statement fingerprints, consume every required child, and show
the complete parent conclusion. In particular, the short categorical anchor cannot serve as an
unexpanded terminal leaf.

## Root cut and status boundary

The first concrete root cut is `M0541-C3` (additive boundary construction), `M0541-L1` (iterated
face identity), `M0541-L4` (global finite cancellation), and `M0541-T2` (extension to all chains).
This architecture freeze closes none of them. It establishes no proof, H0/R0 review, composition
certificate, audit completion, or theorem completion; the root remains `M3`.

