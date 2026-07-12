# THM-M-0578 frozen obligation architecture

Item: `S56-M-0578-OBLIGATION_TREE`.

The registry freezes 13 root-relevant obligations before proof execution. It
uses the historical Milnor-bundle route and keeps topology, smooth obstruction,
source, trust, and provenance in separately typed graphs.

## Typed proof route

```text
M0578-ROOT exact canonical proposition
`-- M0578-T-PACKAGE checked conditional composition
    |-- M0578-C-BUNDLE construct a smooth Milnor bundle total space
    |   `-- M0578-C-BOUNDARY parameter/orientation/dimension conventions
    |-- M0578-T-HOMEO homeomorphism to the fixed unit S^7
    |   `-- M0578-T-HOMOTOPY homotopy-sphere computation
    `-- M0578-O-NONDIFF rule out every diffeomorphism
        |-- M0578-I-CANDIDATE compute the candidate invariant
        `-- M0578-I-STANDARD compute the standard-sphere invariant
```

## Node ledger

`M0578-ROOT` is the exact target `[H3, M4, R4]`. `M0578-S-MODELS`
kernel-checks the statement models `[H3, M0-L, R4]`. `M0578-C-BUNDLE` and
`M0578-C-BOUNDARY` own construction and its conventions. `M0578-T-HOMOTOPY`
and `M0578-T-HOMEO` own the topological comparison. `M0578-I-CANDIDATE`,
`M0578-I-STANDARD`, and `M0578-O-NONDIFF` own the normalized invariant
computations, invariance, and resulting `IsEmpty` statement. These mathematical
nodes remain `[H3, M4, R4]`.

`M0578-T-PACKAGE` is a kernel-checked composition from a complete witness
package to the root `[H3, M0-L, R4]`; its premise is open, so it gives no root
credit. `M0578-X-SOURCE`, `M0578-X-FOUNDATION`, and
`M0578-X-PROVENANCE` separately own primary-source mapping, trust closure, and
terminal-body provenance. The provenance node is informational and cannot
count as mathematical proof.

## Freeze boundary

The minimal open root cut is `M0578-C-BUNDLE`, `M0578-T-HOMEO`, and
`M0578-O-NONDIFF`. This phase supplies no root closure, audit completion, or
theorem completion. Any registry correction, split, merge, or eligibility
change requires a new version and append-only delta.
