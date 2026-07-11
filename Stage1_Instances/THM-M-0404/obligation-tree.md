# THM-M-0404 frozen obligation architecture

Item: `S56-M-0404-OBLIGATION_TREE`.

The registry freezes 15 semantic obligations before proof execution. The route
uses the classical spectral/torsion architecture, but no primary-source
crosswalk has yet been accepted, so the architecture does not improve H debt.

## Typed proof route

```text
M0404-ROOT exact canonical proposition
`-- M0404-T-ASSEMBLE checked conditional composition
    |-- M0404-T-EVENTUAL recurrence zero sets are eventually periodic
    |   `-- M0404-B-DICHOTOMY residue class is identically zero or finite
    |       |-- M0404-N-SPECTRAL recurrence to exponential polynomial
    |       |-- M0404-N-TORSION common root-ratio torsion modulus
    |       |-- M0404-B-RESIDUES exhaustive residue partition
    |       |-- M0404-C-SUBSEQUENCES nondegenerate residual expressions
    |       `-- M0404-L-NONDEGENERATE finite zeros for nondegenerate expressions
    `-- M0404-L-COMBINATORIAL eventual periodicity to finite AP union
```

Statement definitions, boundary behavior, foundation policy, primary-source
mapping, and terminal provenance live in separate refinement, source, trust,
documentation, and workflow graphs. They cannot masquerade as proof premises.

## Node ledger

### m0404-root
Exact elaborated target. `[H3, M3, R4]`; no inhabitant exists.

### m0404-s-definitions
Checked statement definitions and historical-shape transport. `[H3, M0-L, R4]`.

### m0404-s-boundary
Checked empty, universal, and zero-step encoding cases. `[H3, M0-L, R4]`.

### m0404-s-foundation
Planned axiom, TCB, classical-choice, and no-oracle certificate. `[H3, M4, R4]`.

### m0404-n-spectral
Reduce arbitrary recurrence solutions to finite polynomial-exponential form,
including repeated characteristic roots and field extensions. `[H3, M4, R4]`.

### m0404-n-torsion
Choose one positive modulus killing all torsion root ratios. `[H3, M4, R4]`.

### m0404-b-residues
Partition and exhaust natural indices by residues modulo that modulus. `[H3, M4, R4]`.

### m0404-c-subsequences
Construct residual expressions and establish their nondegeneracy invariants. `[H3, M4, R4]`.

### m0404-l-nondegenerate
Central theorem: a nonzero nondegenerate characteristic-zero exponential
polynomial has finitely many natural zeros. `[H3, M4, R4]`; no Lean anchor was found.

### m0404-b-dichotomy
Split each residue expression into identically-zero or finite-zero branches and
recompose every branch. `[H3, M4, R4]`.

### m0404-t-eventual
Assemble residue information into `EventuallyPeriodicZeroSets`. `[H3, M4, R4]`.

### m0404-l-combinatorial
Convert an eventually periodic predicate into the exact finite-list encoding,
including the finite prefix. `[H3, M4, R4]`.

### m0404-t-assemble
Kernel-checked composition from both preceding packages to the exact root.
`[H3, M0-L, R4]`; its open premises prevent root proof credit.

### m0404-x-source
Pending node-level primary-source theorem/page/assumption/errata map. `[H3, M4, R4]`.

### m0404-x-provenance
Pending terminal-body, import, axiom, TCB, and replay inventory. `[H3, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M0404-T-EVENTUAL` plus
`M0404-L-COMBINATORIAL`. The checked conditional assembly is not a proof of
either premise. This phase supplies no root closure, audit completion, or
theorem completion. Any split, merge, correction, or eligibility change needs
a new registry version and append-only delta.
