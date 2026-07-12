# THM-M-0464 frozen obligation architecture

Item: `S56-M-0464-OBLIGATION_TREE`. Registry version 1 freezes sixteen root-relevant
obligations against the exact statement and negative anchor inventory before proof execution.
Every obligation is machine- and readability-eligible; the denominator SHA-256 is
`91ec52d8f1edc34961cc95a24b77b3d4c396a74330c734aa85d20cbc700ed940`.

## Typed proof route

```text
M0464-ROOT exact PilaWilkieStatement
`-- M0464-T-ASSEMBLE conditional checked root unfolding
    |-- M0464-S-DEFINITIONS source-faithful encodings
    |-- M0464-S-DOMAINS binders, domains, and mutations
    |-- M0464-S-BOUNDARY degenerate cases
    |-- M0464-X-TRANSPORT representation equivalences
    `-- M0464-L-COUNT quantitative counting conclusion
        |-- M0464-N-CELL o-minimal decomposition/regularity
        |   `-- M0464-C-PARAM controlled parameterization
        |-- M0464-L-DETERMINANT determinant estimate
        |   `-- M0464-B-ALGEBRAIC algebraic-part separation
        |       `-- M0464-L-INDUCTION dimension/complexity induction
        `-- the same parameterization, separation, and induction packages
```

`M0464-S-FOUNDATION`, `M0464-X-SOURCE`, `M0464-X-PROVENANCE`, and
`M0464-X-TRUST` are separate foundation, human-source, provenance, and trust boundaries. They
cannot be substituted for mathematical premises or counted as proof closure.

## Semantic nodes

### m0464-root
The exact first-version theorem is the sole root. It is an elaborated `Prop` definition, not a
proved theorem, so its machine debt is `M3`.

### m0464-s-definitions
Validate the encodings of semialgebraicity, o-minimal definability, affine rational height,
rational points, and `algebraicPart`, including the positive-dimensional representation.

### m0464-s-domains
Check `n >= 1`, the fixed expansion, definability, `epsilon > 0`, and `T >= 1`, including statement
mutations for hypotheses, domains, scope, and boundaries.

### m0464-s-boundary
Account for empty and zero-dimensional sets and Lean's `Set.ncard` convention without weakening the root.

### m0464-s-foundation
Freeze classical logic, choice, quotients, real analysis, transitive axioms, TCB, and no-oracle policy.

### m0464-n-cell
Build the source-required o-minimal decomposition and regularity package. Pinned mathlib supplies none.

### m0464-c-param
Construct controlled smooth parameterizations, with coverage and derivative bounds.

### m0464-l-determinant
Formalize the determinant/interpolation estimate placing dense bounded-height rational points on
controlled algebraic hypersurfaces.

### m0464-b-algebraic
Separate positive-dimensional semialgebraic pieces into exactly `algebraicPart X` and control the
remaining intersections. A Zariski closure or arbitrary exceptional set is not a substitute.

### m0464-l-induction
Run dimension/complexity induction over residual hypersurface intersections, with explicit decreases.

### m0464-l-count
Combine all mathematical packages into `CountingConclusion n X epsilon`. This immediate premise remains `M4`.

### m0464-x-transport
Check every source-to-Lean representation boundary in the required direction.

### m0464-x-source
Map mathematical nodes to primary-source locators, hypotheses, and errata. Current `H1` remains open.

### m0464-x-provenance
Record immutable revisions, terminal bodies, wrappers, licenses, and dependencies for later candidates.

### m0464-x-trust
Audit axioms, placeholders, unsafe/oracle paths, pins, freshness, replay, and independent verification.

### m0464-t-assemble
`root_from_terminal_counting` checks exact definitional assembly but assumes the full terminal result.
It is conditional composition evidence only, not a Pila-Wilkie proof.

## Freeze boundary

The immediate mathematical cut set is recorded structurally in the registry. Human-source,
provenance, readability, trust, hermetic replay, and independent review also remain open. Changing
an obligation, eligibility class, or decomposition requires a new version and append-only delta.
`audit_complete=false` and `theorem_complete=false`.
