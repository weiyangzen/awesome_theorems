# THM-M-0420 Frozen Obligation Tree

Item: `S56-M-0420-OBLIGATION_TREE`  
Registry version: `1`  
Status: architecture self-test only; root open

The registry freezes 16 root-relevant semantic obligations before proof execution. All are
machine-, human-source-, and readability-required. The machine-readable authority is
`obligation-registry.json`; `typed-graphs.json` separates proof, refinement, provenance, evidence,
trust, documentation, and workflow edges.

## Proof Route

```text
M0420-ROOT exact Hilbert class field target
`-- M0420-T checked conditional composition
    |-- M0420-C coherent finite extension candidate
    |   `-- M0420-C1 trivial-modulus global class field construction
    |       `-- M0420-X1 global class field theory terminal bridge
    |-- M0420-L1 abelian Galois property
    |   `-- M0420-X1
    |-- M0420-L2 finite-prime unramifiedness
    |   |-- M0420-N1 ramification-convention normalization
    |   `-- M0420-X1
    |-- M0420-L3 Artin reciprocity class-group isomorphism
    |   |-- M0420-N2 Artin-map convention normalization
    |   `-- M0420-X1
    `-- M0420-L4 maximality among comparison extensions
        |-- M0420-B comparison-family exhaustion
        `-- M0420-X1
```

`M0420-S`, `S1`, and `S2` refine the statement interface. `M0420-X2` is a release-only trust and
provenance boundary, not a mathematical premise. `M0420-T` consumes one shared candidate and all
four required properties; the checked theorem proves none of those hypotheses.

## Node Ledger

### m0420-root
Exact `HilbertClassFieldTarget`. `[H1, M3, R3]`; no root proof body exists.

### m0420-s
Frozen definition, universe, finite-place, reciprocity, and maximality interface. `[H1, M3, R3]`.

### m0420-s1
Checked equivalence with the expanded historical candidate shape. `[H1, M0-L, R3]`; transport only.

### m0420-s2
Checked reversal of the reciprocity isomorphism. `[H1, M0-L, R3]`; transport only.

### m0420-n1
Planned equivalence between the prime-ideal predicate and the source finite-place convention.
`[H1, M4, R3]`.

### m0420-n2
Planned normalization of Artin maps, class groups, and automorphism conventions. `[H1, M4, R3]`.

### m0420-b
Planned exhaustive treatment of every comparison extension in universe `uM`. `[H1, M4, R3]`.

### m0420-c
Construct one coherent finite extension candidate shared by the property nodes. `[H1, M4, R3]`.

### m0420-c1
Construct the trivial-modulus global class field and establish finiteness. `[H1, M4, R3]`.

### m0420-l1
Prove the shared candidate is abelian Galois. `[H1, M4, R3]`.

### m0420-l2
Prove finite-prime unramifiedness of the shared candidate. `[H1, M4, R3]`.

### m0420-l3
Prove the frozen class-group/Galois-group reciprocity isomorphism. `[H1, M4, R3]`.

### m0420-l4
Prove every finite unramified abelian comparison extension embeds into the candidate. `[H1, M4, R3]`.

### m0420-x1
Global class field existence and reciprocity terminal bridge. `[H1, M4, R3]`; the anchor audit found
no compatible placeholder-free Lean declaration.

### m0420-t
Kernel-checked conditional composition from `C`, `L1`, `L2`, `L3`, and `L4` to the exact root.
`[H1, M0-L, R3]`; all five premises remain open.

### m0420-x2
Terminal proof-body, axiom, dependency, provenance, and reproducibility audit. `[H1, M4, R3]`;
release-only.

## Boundary

This is an execution architecture, not a Hilbert class field proof. Planned signatures are not Lean
declarations. No H0/R0, substantive construction or property closure, unconditional root proof,
hermetic replay, independent verification, theorem completion, or master acceptance is claimed.
