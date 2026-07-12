# THM-M-1228 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 15 canonical obligations before proof-phase closure is observed. Eleven
are root-relevant machine obligations; four are source, provenance, trust, and documentation
overlays. All 15 require readable coverage. No node is marked closed. Planned fingerprints bind
each child statement and formal target; corrections require a versioned append-only delta.

The semantic fields in `CKNSourceSemantics` are not analytic implementations. Accordingly the tree
owns a concrete-definition branch rather than treating those parameters as assumptions from which
the theorem may be extracted.

## Typed proof route

```text
M1228-ROOT  exact semantic-interface target [open M4]
`-- M1228-T-ASSEMBLE  checked conditional binder composition
    `-- M1228-T-PERSOLUTION  every suitable solution has measure-zero singular set
        |-- M1228-S-REGULAR  concrete source regular-point definition
        `-- M1228-L-MEASURE  terminal parabolic measure conclusion
            |-- M1228-G-PARABOLIC  anisotropic geometry and measure
            `-- M1228-C-COVER  bad-cylinder covering estimate
                `-- M1228-E-EPSILON  epsilon regularity
                    |-- M1228-D-DECAY  compactness and decay
                    `-- M1228-S-SUITABLE  concrete suitability clauses
```

## Node ledgers

### root

`M1228-ROOT` is exactly `CaffarelliKohnNirenbergTarget`. It is not global smoothness, a
two-dimensional result, or a Euclidean Hausdorff-measure surrogate.

### s-concrete

`M1228-S-CONCRETE` owns the checked transport from concrete analytic definitions to the three
semantic slots. This prevents an arbitrary interpretation of `CKNSourceSemantics` from receiving
proof credit. Its children separately own suitability, regularity, and parabolic geometry.

### s-suitable

`M1228-S-SUITABLE` must encode the distributional Navier-Stokes equation, incompressibility,
velocity and pressure spaces, locality, and local energy inequality from the pinned primary source.

### s-regular

`M1228-S-REGULAR` fixes the source regular-point convention and neighborhood quantifiers. Regularity
cannot be assumed as a field of solution data.

### g-parabolic

`M1228-G-PARABOLIC` constructs backward cylinders, anisotropic scaling, covers, content, and the
one-dimensional parabolic Hausdorff zero predicate. Ambient product-metric Hausdorff measure is
explicitly excluded.

### e-epsilon

`M1228-E-EPSILON` owns the scale-invariant epsilon-regularity theorem. A short invocation of a
future imported theorem remains a bridge obligation requiring exact type and provenance checks.

### d-decay

`M1228-D-DECAY` owns the compactness, limiting equation, and quantitative decay mechanism. Its
95-step budget requires a later split if substantive expansion exceeds 100 steps.

### c-cover

`M1228-C-COVER` covers singular points with bad parabolic cylinders and bounds the sum of radii.
It owns selection/disjointness and limiting arguments rather than hiding them in the measure node.

### l-measure

`M1228-L-MEASURE` converts arbitrarily small covering content into zero one-dimensional parabolic
Hausdorff measure for the domain-restricted singular set.

### t-persolution

`M1228-T-PERSOLUTION` generalizes the terminal analytic result over each source-suitable solution.
It remains open and is the premise consumed by the logical assembly certificate.

### t-assemble

`M1228-T-ASSEMBLE` is checked by `ObligationTree.root_compose` against a standalone structural
mirror bound to the hashed statement by the validator. It only introduces the frozen binders and
applies the open per-solution family. This conditional theorem proves no CKN analysis or root.

### x-source

`M1228-X-SOURCE` remains `H1`: exact definitions, theorem and lemma pages, assumptions, corrections,
and independent review are not accepted.

### x-provenance

`M1228-X-PROVENANCE` records that the bounded anchor audit found no exact terminal Lean candidate.
Any later candidate must identify its immutable body and wrapper chain.

### x-tcb

`M1228-X-TCB` owns transitive imports, axioms, kernel, executable tools, and release trust closure.

### x-doc

`M1228-X-DOC` requires a readable proof reconstruction with node-specific source and formal anchors.

## Status boundary

The root remains `M4`. The frozen proof-phase cut set is `M1228-S-CONCRETE`,
`M1228-E-EPSILON`, `M1228-C-COVER`, and `M1228-L-MEASURE`. The graphs separately type proof,
refinement, provenance, evidence, trust, documentation, and workflow edges. This phase claims no
closed proof obligation, human-source acceptance, theorem completion, release, or master acceptance.
