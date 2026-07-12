# THM-M-0711 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 17 semantic obligations before proof execution. Its denominator digest
is `9fbdae321a68e51a301e942864c9a785fab407f21f25247ab04cb74277bd8d24`.
Eligibility derives from the exact fixed-presentation target and the construction-plus-reduction
architecture, not from available proof evidence. Source and provenance nodes are informational
overlays and cannot receive mathematical proof credit.

## Typed proof route

```text
M0711-ROOT exact NovikovBooneTarget [open M4]
|-- M0711-T-ASSEMBLE checked existential composition
|   `-- M0711-T-WITNESS fixed finite presentation witness
|       `-- M0711-L-NONCOMP identity predicate is noncomputable
|           `-- M0711-B-REDUCTION [principal open cut]
|               |-- M0711-C-PRESENTATION finite presentation construction
|               |-- M0711-C-COMPILER effective configuration-to-word compiler
|               |-- M0711-C-CORRECT reduction correctness iff
|               |-- M0711-L-MANYONE computability transfer
|               `-- M0711-L-HALTING pinned undecidable source predicate
`-- M0711-S-FOUNDATION trust and no-oracle policy [open]
```

The proof graph stores reciprocal `proof_requires` and `composes` edges. Refinement, provenance,
evidence, trust, documentation, and workflow graphs remain separate. Each node owns a structured
semantic ledger and a budget no larger than 100; a later implementation must version and split any
node that reveals a hidden high-risk package or longer proof.

## Composition and status

`ObligationTree.lean` defines the exact property of a proposed presentation and kernel-checks that
one such witness yields `NovikovBooneTarget`. This is only final existential packaging. It does not
construct the presentation or compiler, prove reduction correctness, or derive noncomputability.
The current remaining root cut is `M0711-B-REDUCTION` together with the release-level foundation
audit `M0711-S-FOUNDATION`.

Primary-source pinpoint review, all central construction and reduction bodies, terminal
provenance, readable reconstruction, independent verification, and master acceptance remain open.
The root stays `[H1, M4, R4]`; neither audit completion nor theorem completion is claimed.
