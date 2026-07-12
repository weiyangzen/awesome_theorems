# THM-M-1550 frozen obligation architecture

Item: `S56-M-1550-OBLIGATION_TREE`. Registry version 1 freezes ten canonical obligations before
the proof phase assigns closure credit. The denominator is
`c5237144d3fec2b11708d76661dd79e4d1861cc904b45ffde79e05fa17079730`.

## Typed proof route

```text
M1550-ROOT  exact frozen LaxPairIsospectrality [open M3]
|-- M1550-S-EXACT  exact statement interface
|   `-- M1550-S-LAX  retained Lax-equation premise
`-- M1550-T-ASSEMBLE  conditional checked composition
    |-- M1550-B-TIMES  specialize evolution at t0 and t
    |   `-- M1550-C-WITNESS  obtain the conjugating unit witness
    `-- M1550-L-SPECTRUM  apply spectrum.units_conjugate
```

`M1550-X-PROVENANCE`, `M1550-X-SOURCE`, and `M1550-X-TCB` are separate overlays. They govern
formal provenance, human-source fidelity, and trust respectively, and never count as mathematical
proof bodies.

## Node ledger

### m1550-root
The exact universe-polymorphic finite-complex-matrix statement from `Statement.lean`, including both
premises and equality of algebra spectra at every two domain times.

### m1550-s-exact
Owns the exact binder order, arbitrary finite index type, real time domain, two named hypotheses,
and `IsospectralOn` conclusion. It excludes universal Lax representability and analytic construction
of a conjugating evolution.

### m1550-s-lax
Retains `LaxEquationOn L P timeDomain`. The architecture records explicitly that this premise is
not consumed mathematically once the stronger `ConjugatingEvolutionOn` premise is supplied; it may
not be silently deleted from the root.

### m1550-b-times
Fixes arbitrary `t0` and `t` with domain-membership proofs and specializes the universally
quantified conjugating-evolution hypothesis.

### m1550-c-witness
Owns the existential unit and exact multiplication order in `ConjugatesAt`: `L t` equals `L t0`
conjugated on the left by `U` and on the right by `U⁻¹`.

### m1550-l-spectrum
Owns the nontrivial spectrum-preservation leaf. The audited candidate is the pinned mathlib theorem
`spectrum.units_conjugate`; proof-phase work must implement the equality rewrite and terminal-body
provenance rather than infer closure from candidate availability.

### m1550-t-assemble
`ObligationTree.root_compose` is a kernel-checked conditional composition certificate. It consumes
a `SpectrumUnderConjugation` premise and specializes the evolution hypothesis. It supplies no
unconditional leaf or root proof credit.

### m1550-x-provenance
Must resolve wrapper identity, terminal proof bodies, import/declaration closure, and deduplication.

### m1550-x-source
Must add stable primary-source edition and page/equation pinpoints, assumption mapping, errata state,
and independent source review. The present broad Lax citation is not H0.

### m1550-x-tcb
Must close the transitive axiom, artifact, toolchain, dependency, replay, and supply-chain boundary.

## Freeze boundary

Every semantic leaf budget is at most 100, while the root is marked `split-required`. The registry
assigns zero closed obligations. The minimal mathematical root cut is `M1550-L-SPECTRUM`; the
proof phase must implement it against the exact witness shape. Proof, source, readability,
provenance, trust, audit completion, theorem completion, release, and master acceptance remain open.
Any correction, split, merge, eligibility change, exclusion, or statement change requires a new
registry version and an append-only delta.
