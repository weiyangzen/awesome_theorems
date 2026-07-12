# THM-M-0648 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 12 canonical obligations before the proof phase observes or awards
closure. Ten are root-relevant machine obligations; `M0648-X-SOURCE` and `M0648-X-TRUST` are
non-proof overlays. The ordered denominator and digest in `obligation-registry.json` are
authoritative. Any split, merge, exclusion, risk, or eligibility correction requires version 2
and an append-only delta.

## Typed proof route

```text
M0648-ROOT  exact paired target [open M4]
|-- M0648-S-EXACT
|-- M0648-S-BOUNDARY
`-- M0648-T-COMPOSE  checked conditional conjunction
    |-- M0648-D  exact pinned downward bridge [candidate M1]
    |   `-- M0648-D-SKOLEM  Skolem hull and cardinal control
    `-- M0648-U  exact pinned upward bridge [candidate M1]
        |-- M0648-U-DIAGRAM
        |-- M0648-U-COMPACT
        `-- M0648-U-SHRINK
            `-- M0648-D  shared downward terminal body, no duplicate credit
```

Separate provenance, evidence, trust, documentation, and workflow graphs prevent candidate names,
source mappings, or audit records from becoming proof premises. The upward anchor is expanded past
its short invocation because it hides an elementary-diagram construction, compactness, and a
downward cardinal reduction. Every leaf has a substantive ledger below the 100-step split limit.

## Node boundaries

### m0648-root
Exact paired theorem. It remains open.

### m0648-s-exact
Statement binders, lifts, containment, cardinal equalities, and embedding direction.

### m0648-s-boundary
Degenerate and equality cases admitted by the frozen hypotheses.

### m0648-d
Exact downward imported bridge; applicability is audited, not yet proof-credited.

### m0648-d-skolem
Skolem hull construction and exact cardinal control hidden by the imported bridge.

### m0648-u
Exact upward imported bridge; applicability is audited, not yet proof-credited.

### m0648-u-diagram
Elementary diagram and named-copy construction.

### m0648-u-compact
Compactness and fresh constants used to force the cardinal lower bound.

### m0648-u-shrink
Downward shrink retaining the named copy and yielding exact cardinality.

### m0648-t-compose
`ObligationTree.lean` checks that both exact direction packages yield the conjunction. It supplies
neither package and therefore closes nothing.

### m0648-x-source
Primary-source pinpoint and errata review remain open at H2.

### m0648-x-trust
Transitive provenance, trust, hermetic replay, and independent validation remain open.

No H0, M0, R0, audit completion, theorem completion, release acceptance, or master acceptance is
claimed by this architecture phase.
