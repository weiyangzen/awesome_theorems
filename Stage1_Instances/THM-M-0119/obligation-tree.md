# THM-M-0119 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 33 obligations before the proof phase assigns any
closure. Twenty-eight obligations are root-relevant machine requirements; five
are typed provenance, evidence, trust, or documentation overlays. All 33 remain
in the readable denominator, and no missing interface or difficult theorem is
excluded. The canonical registry projection digest is
`d9c76b6bb201afa0b50c3e3a38e86e6db4faab64d250009313606b3ae79592db`.

Only `M0119-ROOT` has an existing Lean source fingerprint. Planned signatures
are explicitly labeled `planned:v1`; they are not declarations and carry no
proof credit. Every leaf owns a two-step premise/inference/output ledger below
the 100-step threshold. Hidden branch work, a major imported theorem, or a
longer proof requires a versioned registry split before closure can be claimed.

## Typed proof route

```text
M0119-ROOT  exact projective klt-pair target [open M3]
`-- M0119-T  exact final composition
    |-- M0119-S  statement, data, hypotheses, degrees, transport, foundations
    |-- M0119-N  Q-Cartier index, log resolution, pullback and rounding
    |-- M0119-B  dimension-zero / positive-dimension exhaustive branches
    |-- M0119-C  resolution, discrepancy, rounding, pushforward constructions
    |-- M0119-L  smooth logarithmic vanishing, cohomology comparison, descent
    `-- M0119-X  missing formal APIs and imported boundaries
```

The proof graph reaches all 28 required machine obligations and is acyclic.
Refinement, provenance, evidence, trust, documentation, and workflow relations
are separate typed graphs, so source or validation links cannot act as proof
premises. `M0119-P`, `M0119-V`, `M0119-R`, `M0119-X-ANCHORS`, and
`M0119-X-TCB` remain informational graph overlays rather than proof-coverage
inflation.

## Current cut set

The first implementation cut is `M0119-X-APIS`, `M0119-N-RESOLUTION`,
`M0119-L-SMOOTH`, and `M0119-C-PUSH`: the pinned environment lacks the native
Q-divisor/klt/positivity/cohomology surface, a characteristic-zero log-resolution
bridge, the central smooth logarithmic vanishing theorem, and the pushforward
descent package. This is a concrete architectural cut, not a claim of
minimality or global absence.

`ObligationTree.lean` kernel-checks only two conditional logical compositions:
assembling degreewise vanishing over every positive degree and forming an
implication once its vanishing conclusion is already supplied. Both report no
axiom dependencies. They prove none of the substantive nodes and do not close
the root. H0, M0, R0, `AUDIT-Z`, `THEOREM-Z`, release, and master acceptance
remain open.
