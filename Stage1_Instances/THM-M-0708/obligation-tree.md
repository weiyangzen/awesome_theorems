# THM-M-0708 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 13 canonical obligations before the proof phase adopts any candidate.
Eligibility follows the exact functional statement and the fixed-point architecture exposed by the
pinned `ComputablePred.rice` body, not ease of closure. The source boundary is human-only and the
provenance overlay is informational; neither receives mathematical proof credit.

## Typed proof route

```text
M0708-ROOT exact RiceTheoremTarget [open M3]
`-- M0708-T-ASSEMBLE checked conditional composition
    |-- M0708-N-WITNESSES unpack represented f and g
    |-- M0708-L-RICE-BRIDGE [remaining root cut]
    |   |-- M0708-L-FIXED-POINT fixed_point2 interface
    |   |-- M0708-C-COND conditional partial-recursive construction
    |   `-- M0708-L-SEMANTIC-TRANSFER extensional fixed-point argument
    `-- M0708-T-CONTRADICTION apply g not-in C
```

The proof graph has reciprocal `proof_requires` and `composes` edges. Refinement, provenance,
evidence, trust, documentation, and workflow relations are separate typed graphs, preventing source
or governance nodes from being counted as proof premises. Every leaf budget is at most 100; the
central upstream theorem is expanded rather than hidden behind its short invocation.

## Composition and status

`ObligationTree.lean` proves that an exact `RiceBridge` premise yields the exact frozen root, and
the kernel reports no axioms for this conditional wrapper. This phase deliberately does not use
`ComputablePred.rice` to construct that premise; doing so would be proof-node adoption.

The remaining root cut is `M0708-L-RICE-BRIDGE`. Human-source pinpoint acceptance, terminal-body
provenance closure, readable reconstruction, proof adoption, independent verification, and release
remain open. The root therefore remains `[H1, M3, R3]`; neither audit completion nor theorem
completion is claimed.
