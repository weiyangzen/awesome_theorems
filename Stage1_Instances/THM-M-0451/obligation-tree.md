# THM-M-0451 frozen obligation architecture

Item: `S56-M-0451-OBLIGATION_TREE`.

The registry freezes 17 root-relevant obligations before proof execution. It
uses the defining dyadic-limit route and preserves the exact `xHeight / 2`
normalization. No anchor found by the preceding audit supplies a terminal proof.

## Typed proof route

```text
M0451-ROOT exact package
`-- M0451-ASSEMBLE checked conditional field assembly
    |-- M0451-HEIGHT/LIMIT construction and convergence
    |   `-- M0451-APPROX uniform naive-height estimate
    |       `-- M0451-XHEIGHT exact coordinate-height boundary
    |-- M0451-BOUNDED
    |-- M0451-QUADRATIC (all integer scalars)
    |-- M0451-PARALLELOGRAM
    |-- M0451-NONNEGATIVE
    `-- M0451-TORSION-KERNEL
        |-- M0451-TORSION-ZERO
        `-- M0451-ZERO-TORSION
```

The source, provenance, foundation, evidence, trust, documentation, and
workflow boundaries are separate typed graphs and earn no proof credit.

## Semantic ledgers

Each proof node has a substantive target and a budget of at most 100 steps.
`M0451-HEIGHT` is already marked split-required: construction, Cauchy control,
and limit identification must not be collapsed into one opaque task. The
estimate node must supply a uniform constant with the statement's projective
coordinate convention. The scalar node includes negative integers and zero.
The torsion equivalence is split into its two logically independent directions;
the difficult zero-to-torsion direction cannot be inferred from nonnegativity.

`M0451-SOURCE` must crosswalk a primary theorem and proof, page, assumptions,
normalization, and errata to the individual mathematical nodes. `M0451-PROVENANCE`
must trace every terminal body, import, alias, and adapter. `M0451-TRUST` owns
axiom output, pinned replay, freshness, and independent validation.

## Freeze boundary

`ObligationTree.engine_compose` kernel-checks only the implication from an
uninhabited polymorphic engine to the exact root. It does not construct a
canonical height. Root debt remains `[H1, M3, R3]`; audit completion and theorem
completion are false. Any registry correction requires a new version and an
append-only delta.
