# THM-M-0373 frozen obligation architecture

Item: `S56-M-0373-OBLIGATION_TREE`.

## Proof route

The registry freezes 20 semantic records before proof execution. The proof
route normalizes the finite-generator lower bound, builds the finite Koszul
complex, constructs a smooth Bezout seed and its dbar defect, obtains
Carleson-measure estimates, solves dbar with a bounded solution, corrects the
seed to analytic coefficients, and separately proves analyticity, boundedness,
and the Bezout identity before exact existential assembly.

```text
M0373-ROOT
|-- S-DOMAIN / S-TRANSPORT
|-- N-L2 / N-SCALE
`-- T-ASSEMBLE
    |-- A-ANALYTIC
    |-- A-BOUNDED
    `-- A-BEZOUT
        `-- A-CORRECT
            |-- D-DATA / D-CLOSED
            |   `-- K-COMPLEX / K-ALGEBRA
            `-- E-DBAR / E-BOUND
                `-- E-CARLESON
```

Each node owns a substantive semantic ledger and a budget of at most 100
steps. A proof worker must split a node if its exact formal signature or body
exceeds that bound. In particular, `E-CARLESON` and `E-DBAR` are high-risk
bridge obligations, not names that may hide an imported theorem.

## Typed boundaries

Proof and refinement edges are distinct from provenance, evidence, trust,
documentation, and workflow edges. `X-SOURCE`, `X-TCB`, and `X-WORKFLOW` are
informational overlays and cannot discharge mathematics. The anchor audit
found no exact Lean candidate, so every mathematical proof body remains open.
Primary-source theorem/page and proof-step crosswalk, transitive axioms and
imports, artifact replay, independent receipts, freshness, and revocation also
remain open.

`ObligationTree.root_compose` checks only the definitional final-child to root
interface. It assumes `BoundedAnalyticBezout`; it neither constructs that
witness nor proves any analytic lemma. No obligation is recorded closed, the
root remains `M4`, and neither audit nor theorem completion is claimed.
