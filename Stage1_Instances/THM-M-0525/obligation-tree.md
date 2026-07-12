# THM-M-0525 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes ten canonical obligations from the exact forward-concatenation target
and audited quotient API. Eligibility was selected before root proof execution. Source and
provenance overlays receive no machine-proof credit; aliases and the existing reverse-composition
`FundamentalGroup` instance do not add denominator entries.

## Typed proof route

```text
M0525-ROOT exact Statement [open M2]
`-- M0525-T-GROUP conditional checked composition
    |-- M0525-S-SCOPE exact carrier and operation convention
    |-- M0525-C-QUOTIENT well-defined quotient operations
    |-- M0525-L-ASSOC forward concatenation associativity
    |-- M0525-L-ONE-LEFT constant-loop left identity
    `-- M0525-L-INV-LEFT reversal left inverse
```

`Group.ofLeftAxioms` derives the right identity and right inverse fields, so duplicating them as
required construction premises would inflate the canonical proof denominator. Foundation, source,
and provenance remain separate release-relevant nodes. The machine bundle keeps proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs distinct.

## Composition boundary

`ObligationTree.lean` checks that three explicitly supplied quotient laws construct a `Group` and
package exactly the multiplication, identity, and inverse equations frozen by `Statement.lean`.
It deliberately accepts those laws as hypotheses and therefore does not prove the root. The
kernel-available mathlib laws remain component evidence pending the proof phase and master review.

The root stays `[H1, M2, R3]`. Primary-source pinpoint acceptance, transitive trust/provenance,
proof-phase integration, readable reconstruction, hermetic replay, and independent validation are
open. Neither audit completion nor theorem completion is claimed.
