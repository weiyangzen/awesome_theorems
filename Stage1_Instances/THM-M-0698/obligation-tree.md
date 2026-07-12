# THM-M-0698 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 16 canonical obligations before the ordered proof
gate. The denominator digest is
`ff7e990ec12b0a3cbc19fa77dff8eb02bc9cbeef7452432467ce1392b52f61a4`.
Eligibility comes from the exact statement and the audited ultraproduct proof
architecture, not from whether pinned mathlib already contains a proof body.
The source boundary is human-only and the provenance overlay is informational;
neither can count as a mathematical proof premise.

## Typed proof route

```text
M0698-ROOT exact satisfiable iff finitely satisfiable [open M3]
`-- M0698-T-ASSEMBLE checked conditional iff composition
    |-- M0698-B-FORWARD checked monotonicity direction
    `-- M0698-B-REVERSE [remaining root cut]
        |-- M0698-C-FINITE-MODELS choose models of mapped finite subtheories
        |-- M0698-C-ULTRAFILTER extend the atTop filter
        |-- M0698-C-PRODUCT form the structured filter product
        |-- M0698-L-LOS imported Los sentence bridge
        |-- M0698-L-EVENTUALLY singleton/cofinal eventual-truth argument
        `-- M0698-T-MODEL package the product as ModelType.of
```

The proof graph records reciprocal `proof_requires` and `composes` edges.
Statement refinement, proof-body provenance, evidence, trust, documentation,
and workflow dependencies remain separate graphs. This prevents a source
citation, imported name, or review task from being mistaken for a proof
premise. Every semantic node has a budget of at most 100 steps; any later exact
ledger exposing another major theorem package requires a versioned split.

## Composition and status

`ObligationTree.lean` proves the forward implication solely by theory
monotonicity and checks that explicit forward and reverse interfaces compose to
the exact frozen `FirstOrderCompactnessTarget`. It deliberately does not call
`isSatisfiable_iff_isFinitelySatisfiable`. The reverse direction therefore
remains the honest cut even though the anchor audit found a matching terminal
body in pinned mathlib; proof credit belongs to the later ordered proof phase.

The four statement/foundation nodes are refinement and trust requirements, not
extra mathematical premises. Pinpoint primary-source review, transitive
provenance and TCB closure, readable reconstruction, independent validation,
and release evidence remain open. The root stays `[H2, M3, R4]`; neither audit
completion nor theorem completion is claimed.
