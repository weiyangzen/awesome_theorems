# THM-M-0349 frozen obligation architecture

Item: `S56-M-0349-OBLIGATION_TREE`.

The registry freezes 15 obligations before proof execution. It selects the classical Fourier-polynomial, weak-type estimate, interpolation, and continuous-extension route. This is an architecture choice, not proof or source credit.

## Typed proof route

```text
M0349-ROOT
`-- M0349-T-ASSEMBLE (kernel-checked conditional composition)
    |-- M0349-P-EXISTENCE
    |   |-- M0349-C-EXTEND
    |   |   |-- M0349-D-DENSE
    |   |   `-- M0349-C-POLYNOMIAL
    |   `-- M0349-L-FOURIER-ID
    |       |-- M0349-D-DENSE
    |       `-- M0349-C-POLYNOMIAL
    `-- M0349-P-BOUND
        |-- M0349-L-INTERPOLATE
        |   |-- M0349-L-WEAK11
        |   `-- M0349-L-L2
        `-- M0349-C-EXTEND
```

`M0349-S-ENDPOINTS` freezes the strict endpoints, unit circle, Haar measure, complex scalars, and zero Fourier mode. `M0349-X-SOURCE`, `M0349-X-TRUST`, and `M0349-X-PROVENANCE` are separate documentation, trust, and provenance boundaries and cannot masquerade as proof premises. Every semantic node has a step budget at most 100; the deep interpolation and weak-type invocations remain explicit obligations rather than short wrapper steps.

The minimal open root cut is `M0349-P-EXISTENCE` plus `M0349-P-BOUND`. The conditional assembly in `ObligationTree.lean` elaborates without placeholders but proves neither premise. Root debt remains `[H3, M3, R4]`; audit completion and theorem completion remain false. Registry changes require a new version and append-only delta.
