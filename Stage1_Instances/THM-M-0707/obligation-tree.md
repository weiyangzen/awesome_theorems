# THM-M-0707 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 12 semantic obligations. The statement and pinned
anchor were already audited because the generated workflow orders this phase
after anchor audit; the receipt therefore does not claim a blind pre-discovery
freeze. Eligibility and denominators include every model, boundary, reduction,
source, foundation, and provenance obligation and are not reduced in response
to the available mathlib proof. Future changes require an append-only registry
delta.

## Typed proof route

```text
M0707-ROOT exact canonical proposition
`-- M0707-T-ASSEMBLE exact checked assembly
    |-- M0707-S-STATEMENT model and effective-decider identity
    `-- M0707-T-CONTRADICTION
        |-- M0707-X-HALTING pinned fixed-input theorem at zero
        `-- M0707-N-FIXED-ZERO restriction of a pair decider
            `-- M0707-L-RESTRICT both components of ComputablePred
                `-- M0707-C-PAIR-ZERO computable embedding c |-> (c, 0)
```

Each `proof_requires` edge has a reciprocal `composes` edge. Refinement,
provenance, evidence, trust, documentation, and workflow relations are stored
in separate graphs, so source and governance records cannot masquerade as
proof premises. Every leaf ledger is bounded by at most 100 substantive steps.

## Composition certificates

`fixedInputDecider_of_pairDecider` checks the restriction step, including both
the decision witness and its computable Boolean characteristic.
`root_of_fixed_input_anchor` consumes that result and an explicit fixed-input
anchor. `haltingProblemUndecidable_via_obligation_tree` instantiates the anchor
with `ComputablePred.halting_problem 0` and elaborates at the exact canonical
target.

## Status boundary

The kernel-checked route supports provisional `M0-W` evidence, but this worker
does not accept any obligation. The human primary-source map remains `H1`, the
public reconstruction remains `R3`, and foundation/TCB and transitive proof-body
provenance are not accepted. Independent validation, hermetic release replay,
master acceptance, `AUDIT-Z`, `THEOREM-Z`, and theorem completion remain open.
