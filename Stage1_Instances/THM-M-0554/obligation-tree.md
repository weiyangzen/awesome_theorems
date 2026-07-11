# THM-M-0554 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 32 canonical semantic obligations for
`S56-M-0554-OBLIGATION_TREE`. Thirty are root-relevant machine obligations;
`M0554-X-SOURCE` and `M0554-X-TCB` are informational source/trust overlays and
cannot contribute proof credit. The ordered machine, human-source, and readable
denominators are stored in `obligation-registry.json`; the canonical registry
projection digest is
`3c72072a40a15d829c40df68b5fc121b74662a883799f7f7c277fa9c6ed8048b`.

Eligibility follows semantic role, not available evidence. No obligation was
excluded because it is difficult or open. A target correction, split, merge,
eligibility change, or risk change requires registry version 2 and an
append-only delta. This architecture is frozen against the accepted statement
and anchor-audit records, but it admits no historical closure status.

## Typed proof route

```text
M0554-ROOT  exact quantified Statement [open M4]
|-- S-EXACT  checked target expansion
|   |-- S-THEORY / S-CW / S-DATA  frozen interfaces
|   `-- N-SKELETON / N-BIGRADE / N-COEFFICIENT  convention normalization
|-- S-FOUNDATION  foundation and universe policy
`-- T-ROOT -> T-INHABIT -> T-DATA
    `-- B-RECOMPOSE
        |-- B-E2 -> C-E2-MODEL
        |   |-- C-SPECTRAL -> C-EXACT-COUPLE
        |   `-- L-CELLULAR
        |-- B-DIFFERENTIAL -> C-SPECTRAL
        |-- B-CONVERGENCE
        |   |-- C-FILTRATION
        |   |-- L-STABILIZATION
        |   `-- L-STRONG
        `-- B-NATURALITY -> C-EXACT-COUPLE / C-FILTRATION

C-EXACT-COUPLE, C-FILTRATION, and L-CELLULAR require:
|-- X-CW  genuine finite-CW to frozen-interface bridge
`-- X-GENCOH
    |-- X-GENCOH-PAIR  relative theory and long exact sequence
    |-- X-GENCOH-EXCISION  excision for attachment layers
    `-- X-GENCOH-WEDGE  suspension and finite-wedge calculation
```

Every proof dependency has a reciprocal `composes` edge, but these edges record
the intended direction only. `composition_certificates_checked` is empty:
there is not yet a Lean term consuming exact child statements and returning
any nonleaf parent. Provenance, evidence, trust, documentation, and workflow
relations are separate typed graphs, so a source record or task dependency
cannot masquerade as a mathematical premise.

## Semantic leaves

Every current leaf has an explicit ledger of four or fewer substantive planned
steps. Nonleaves are marked `split-required`. These bounds establish the
decomposition threshold only; they do not establish exact leaf signatures,
proof closure, `R0`, or parent composition. Any later source or implementation
showing a hidden construction, case split, theorem package, or ledger beyond
100 steps must create a new registry version and split the affected node.

The generic pinned mathlib `E2CohomologicalSpectralSequence` container is
isolated at `M0554-X-SPECTRAL`. It is useful substrate, not an exact couple,
AHSS constructor, E2 identification, or convergence theorem. The generalized
cohomology pair/excision/wedge family is expanded into three separate critical
bridges rather than hidden behind the proposition-valued fields of the frozen
input structure.

## Root cut and status

The conservative open root cut is:

- `M0554-X-GENCOH`: generalized-cohomology infrastructure is absent;
- `M0554-C-EXACT-COUPLE`: no skeletal exact-couple construction exists;
- `M0554-C-E2-MODEL`: no checked cellular-cohomology E2 identification exists;
- `M0554-L-STRONG`: no checked AHSS strong-convergence theorem exists.

The registry and seven typed graphs are structurally self-tested. This phase
proves no AHSS field, accepts no composition certificate, and makes no H0, M0,
R0, `AUDIT-Z`, `THEOREM-Z`, validation, release, or master-acceptance claim.

<a id="m0554-root"></a>
## Root readable anchor

The exact root remains `Stage1.THM_M_0554.Statement`. Individual node anchors
are reserved by the machine-readable `public_readable_target` fields for later
structured reconstruction; this summary is not an independently reviewed R0
surface.
