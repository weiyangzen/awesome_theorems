# THM-M-0118 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 14 canonical obligations before proof execution. Its
denominator is content-addressed in `obligation-registry.json`. Eligibility is
assigned from the exact abstract statement and the standard
Dolbeault-Hodge/Bochner-Kodaira-Nakano route, not from current Lean availability.
The source and provenance nodes cannot receive mathematical proof credit.

## Typed proof route

```text
M0118-ROOT exact NakanoVanishingTarget [open M3]
`-- M0118-T-ASSEMBLE checked conditional composition
    |-- M0118-S-INTERFACES native-to-abstract checked transport
    |-- M0118-S-VANISHING zero-group encoding
    `-- M0118-T-COHOMOLOGY [remaining root cut]
        |-- M0118-G-DOLBEAULT bundle-valued Dolbeault complex
        |-- M0118-A-HODGE cohomology/harmonic comparison
        `-- M0118-A-HARMONIC-ZERO
            |-- M0118-G-HERMITIAN connection, curvature, and L2 setup
            |-- M0118-A-BOCHNER Bochner-Kodaira-Nakano identity
            `-- M0118-A-CURVATURE degree-range positivity estimate
```

The proof graph has reciprocal `proof_requires` and `composes` edges. Separate
refinement, provenance, evidence, trust, documentation, and workflow graphs
prevent governance or source records from being counted as proof premises.
Every node has a substantive semantic ledger and a budget no greater than 100;
the critical analytic packages must be split in a versioned registry delta once
their native formal interfaces make a finer honest decomposition possible.

## Composition and status

`ObligationTree.lean` checks only that an explicit `AnalyticNakanoPackage`
composes to the exact root. That package is definitionally the expanded target,
so it is an interface boundary, not a circular proof or terminal-body credit.
The kernel reports no axioms for either transparent composition declaration.

The remaining root cut is `M0118-T-COHOMOLOGY`. The pinned closure lacks native
Kahler/Nakano/Dolbeault interfaces and supplies no terminal theorem, as recorded
by the prior anchor audit. Primary-source pinpointing, analytic construction,
terminal-body provenance, trust closure, readable reconstruction, independent
verification, and release remain open. The root stays `[H2, M3, R3]`; neither
audit completion nor theorem completion is claimed.
