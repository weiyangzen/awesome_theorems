# THM-M-0081 frozen obligation architecture

Item: `S56-M-0081-OBLIGATION_TREE`. Registry version 1 freezes 11 obligations before the proof
phase assigns any closure credit. The denominator is
`f38e8efb0c7df7d14e55dc7e7e2a39d88921b21c20eda3ecfb2d6287dbbbf69d`.

## Typed proof route

```text
M0081-ROOT  exact canonical iff [open M4]
`-- M0081-T-ASSEMBLE  conditional checked composition
    |-- M0081-B-REFLECT  representable iso implies object iso
    |   |-- M0081-L-FF  Yoneda is fully faithful
    |   `-- M0081-L-PREIMAGE  fully faithful functors reflect isomorphisms
    `-- M0081-B-PRESERVE  object iso implies representable iso
        `-- M0081-L-MAPISO  functors preserve isomorphisms
```

`M0081-S-EXACT` owns the exact statement encoding. `M0081-X-PROVENANCE`, `M0081-X-SOURCE`, and
`M0081-X-TCB` are separate provenance, human-source, and trust overlays. They are root-relevant but
cannot be counted as mathematical proof bodies.

## Node ledger

### m0081-root
The exact `CanonicalTarget`, including universes, contravariance, and `Nonempty` on both sides.

### m0081-s-exact
The statement interface excludes the element-level lemma, a single implication, covariant
representables, object equality, and chosen isomorphisms.

### m0081-b-reflect
Consumes a natural isomorphism of representables and must produce an object isomorphism. The planned
route combines full faithfulness with `preimageIso`; the call remains a material bridge obligation.

### m0081-l-ff
Owns `CategoryTheory.Yoneda.fullyFaithful`, including its eventual terminal-body and transitive
dependency audit.

### m0081-l-preimage
Owns `CategoryTheory.Functor.FullyFaithful.preimageIso` and the construction of the reflected inverse.

### m0081-b-preserve
Consumes an object isomorphism and must produce a natural isomorphism of representables.

### m0081-l-mapiso
Owns `CategoryTheory.Functor.mapIso` and its functorial inverse-law dependencies.

### m0081-t-assemble
`ObligationTree.root_compose` is a kernel-checked composition certificate. It accepts both direction
packages as premises and therefore supplies no unconditional proof credit.

### m0081-x-provenance
Must resolve unique terminal bodies, wrapper identity, imports, and the transitive declaration graph.

### m0081-x-source
Must add pinpoint primary-source edition, theorem/page, assumptions, errata, and independent review.

### m0081-x-tcb
Must close the transitive axiom, artifact, toolchain, dependency, replay, and supply-chain boundary.

## Freeze boundary

All semantic leaf budgets are at most 100. Anchor availability was deliberately assigned zero closed
obligations. The frozen root cut is `M0081-B-REFLECT` and `M0081-B-PRESERVE`; proof, source,
readability, provenance, trust, audit completion, theorem completion, release, and master acceptance
remain open. Any split, merge, eligibility change, exclusion, or statement correction requires a new
registry version and invalidates this graph bundle.
