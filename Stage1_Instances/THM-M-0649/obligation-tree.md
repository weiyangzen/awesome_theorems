# Frozen obligation tree

Registry version 1 freezes 17 semantic obligations before proof execution. The route is a direct
formula-induction/Tarski-Vaught proof for each canonical `DirectLimit.of` map. No open
model-theory lemma receives proof credit from this architecture.

| Obligation | Role | Exact output | H/M/R | Budget |
|---|---|---|---|---:|
<a id="m0649-root"></a>
| `M0649-ROOT` | root | Exact `ElementaryChainTarget` | H1/M3/R3 | 5 |
<a id="m0649-s-statement"></a>
| `M0649-S-STATEMENT` | definition | Frozen typed target | H1/M0-L/R3 | 20 |
<a id="m0649-s-boundary"></a>
| `M0649-S-BOUNDARY` | branch | Degeneracy and scope policy | H1/M3/R3 | 25 |
<a id="m0649-s-foundation"></a>
| `M0649-S-FOUNDATION` | certificate | Foundation/TCB profile | H1/M4/R3 | 45 |
<a id="m0649-c-cover"></a>
| `M0649-C-COVER` | construction | A stage representative of a limit element | H1/M3/R3 | 25 |
<a id="m0649-c-upper"></a>
| `M0649-C-UPPER` | construction | Common comparison stage | H1/M4/R3 | 35 |
<a id="m0649-l-term"></a>
| `M0649-L-TERM` | lemma | Term-realization coherence | H1/M4/R3 | 70 |
<a id="m0649-l-rel"></a>
| `M0649-L-REL` | lemma | Atomic-relation equivalence | H1/M4/R3 | 80 |
<a id="m0649-l-bool"></a>
| `M0649-L-BOOL` | lemma | Boolean induction cases | H1/M4/R3 | 45 |
<a id="m0649-l-quant-forth"></a>
| `M0649-L-QUANT-FORTH` | lemma | Stage-to-limit quantified case | H1/M4/R3 | 75 |
<a id="m0649-l-quant-back"></a>
| `M0649-L-QUANT-BACK` | lemma | Limit-to-stage quantified case | H1/M4/R3 | 100 |
<a id="m0649-l-formula"></a>
| `M0649-L-FORMULA` | lemma | All-formula preservation/reflection | H1/M4/R3 | 90 |
<a id="m0649-t-tv"></a>
| `M0649-T-TV` | bridge | Exact `CanonicalTarskiVaught` interface | H1/M4/R3 | 40 |
<a id="m0649-t-assemble"></a>
| `M0649-T-ASSEMBLE` | transport | Exact root conditional on the bridge | H1/M0-L/R3 | 8 |
<a id="m0649-x-source"></a>
| `M0649-X-SOURCE` | source | Independently reviewed H0 crosswalk | H1/not_applicable/R3 | 80 |
<a id="m0649-x-provenance"></a>
| `M0649-X-PROVENANCE` | provenance | Terminal-body map | H1/informational/R3 | 45 |
<a id="m0649-x-trust"></a>
| `M0649-X-TRUST` | trust | Release evidence | H1/informational/R3 | 55 |

## Typed architecture

The proof spine is `ROOT -> T-ASSEMBLE -> T-TV -> L-FORMULA`. Formula induction separates term,
relation, Boolean, and two quantifier directions. The hard backwards quantifier branch explicitly
depends on limit coverage and a common upper stage. Proof/composition, refinement, provenance,
evidence, trust, documentation, and workflow remain distinct graphs. Source and trust overlays
cannot close proof premises. Every semantic budget is at most 100.

## Composition boundary

`elementaryChainTarget_of_tarskiVaught` kernel-checks the final child-to-parent composition by
calling mathlib's Tarski-Vaught bundler on exactly `DirectLimit.of`. It assumes rather than proves
`CanonicalTarskiVaught`. The first remaining root cut is therefore `M0649-T-TV`; root debt stays
M3, and theorem completion is false.
