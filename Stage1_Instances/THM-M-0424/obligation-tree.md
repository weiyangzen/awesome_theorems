# THM-M-0424 frozen obligation architecture

Item: `S56-M-0424-OBLIGATION_TREE`. Registry version: 1. The 18 semantic
obligations were frozen from the exact `BrauerGroupLawData` interface before
any machine-closure credit was assigned.

## Typed proof route

```text
M0424-ROOT exact BrauerGroupStatement
`-- M0424-T-COMPOSE checked conditional adapter
    `-- M0424-T-LAWDATA universal bundled law data
        |-- M0424-C-TENSOR-CSA
        |   `-- M0424-C-TENSOR-ALG
        |-- M0424-C-TENSOR-CONGR
        |-- M0424-C-ONE
        |-- M0424-C-OPPOSITE
        |-- M0424-L-DESCENT
        |-- M0424-L-ASSOC
        |-- M0424-L-COMM
        |-- M0424-L-UNIT
        `-- M0424-L-INVERSE
```

The checked adapter only shows that a package with the exact required fields
returns the canonical proposition. It is not a proof body and earns no root
closure credit. The refinement, provenance, evidence, trust, documentation,
and workflow graphs are separately typed in `typed-graphs.json`.

## Node ledgers

### m0424-root
The exact elaborated target for every field and both universe parameters. It
remains M3 because no terminal package inhabits it.

### m0424-s-target
Freezes `CSA`, stable matrix equivalence, quotient classes, and every data and
law field. This interface elaborates but proves none of those fields inhabited.

### m0424-s-boundary
Arbitrary fields and split matrix algebras remain included; no perfectness,
characteristic, finite-degree, or nontrivial-Brauer-class assumption is added.

### m0424-s-foundation
Quotient soundness, classical choice, kernel, and transitive dependency trust
must be audited after bodies exist. No oracle or native computation is allowed.

### m0424-c-tensor-alg
Supply the required scalar algebra structure on `TensorProduct K A B`.

### m0424-c-tensor-csa
Prove tensor products preserve finite dimensionality, centrality, and
simplicity, then package the result as `CSA`. This is not present in the
audited mathlib Brauer definitions.

### m0424-c-tensor-congr
Show the packaged tensor construction respects stable matrix equivalence in
both variables, including compatibility of the chosen representatives.

### m0424-c-one
Package the base field as a central simple algebra in the selected carrier
universe and exhibit the specified algebra equivalence.

### m0424-c-opposite
Package `MulOpposite A` as a CSA and exhibit the specified equivalence, with
the correct scalar action and centrality transfer.

### m0424-l-descent
Use tensor congruence to define quotient multiplication without dependence on
representatives. Quotient equality alone is not this construction.

### m0424-l-assoc
Transport tensor associativity through the packaging and quotient descent.

### m0424-l-comm
Transport tensor symmetry through the packaging and quotient descent.

### m0424-l-unit
Prove tensoring with the packaged base field yields the same Brauer class on
both sides and connect that class to the chosen group identity.

### m0424-l-inverse
Prove `A tensor A^op` is stably equivalent to the base field and connect this
to the chosen group inverse. This is a central theorem package, not a routine
rewrite.

### m0424-t-lawdata
Assemble precisely the nine open construction/law packages into one
`BrauerGroupLawData` value for every field. Every listed child must be consumed.

### m0424-t-compose
`brauerGroupStatement_of_lawData` elaborates the child-to-root transport and
prints its axiom surface. Its premise is still uninhabited.

### m0424-x-source
Pinpoint primary-source theorem/page/assumption/errata mappings remain open for
the substantive construction and law nodes, so H0 is not claimed.

### m0424-x-provenance
The immutable definition anchors are recorded, but terminal proof-body and
transitive trust provenance cannot close until proof bodies exist.

## Freeze boundary

The machine root stays `M3`; the remaining root cut set is the nine substantive
children of `M0424-T-LAWDATA`. Source, readability, hermetic replay, and
independent review also remain open. This phase claims only a structurally
self-tested architecture, never proof, audit completion, theorem completion,
or master acceptance. Any architecture or eligibility correction requires a
new registry version and append-only delta.
