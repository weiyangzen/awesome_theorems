# THM-M-0509 frozen obligation architecture

Item: `S56-M-0509-OBLIGATION_TREE`.

The registry freezes 15 semantic obligations before proof execution. It uses a
classical weighted-sieve route provisionally; pinpoint primary-source review is
still open, so the route supplies no improved human-source status.

## Typed proof route

```text
M0509-ROOT exact P + P2 target
`-- M0509-T-ASSEMBLE exact-root handoff
    `-- M0509-T-P2-EXTRACTION survivor implies frozen IsP2
        `-- M0509-T-POSITIVITY positive admissible count
            |-- M0509-L-WEIGHTED-SIEVE weighted lower bound
            |   |-- M0509-C-REPRESENTATION representation sequence
            |   |-- M0509-S-SIEVE-SETUP parameters and local densities
            |   `-- M0509-N-DISTRIBUTION primes in progressions estimate
            |-- M0509-L-SWITCHING unwanted-factor control
            |   |-- M0509-C-REPRESENTATION
            |   |-- M0509-S-SIEVE-SETUP
            |   `-- M0509-N-DISTRIBUTION
            `-- M0509-L-REMAINDER dominated aggregate error
                |-- M0509-N-DISTRIBUTION
                `-- M0509-S-SIEVE-SETUP
```

Definitions and boundary checks are refinement nodes. Foundation, source,
provenance, documentation, and workflow dependencies live in distinct typed
graphs and cannot count as proof premises.

## Node ledger

Every node has a structured premise/inference/output/use ledger in
`typed-graphs.json`; analytic leaves have a maximum budget of 100 steps.
`S-DEFINITIONS`, `S-BOUNDARY`, and the conditional `T-ASSEMBLE` handoff are
kernel checked. All analytic nodes, source review, provenance closure, and the
root remain open. In particular, `root_of_sieve_package` merely returns its
explicit `ChenTheoremTarget` premise and gives that premise no proof credit.

## Freeze boundary

The current root cut is `M0509-T-P2-EXTRACTION`, recursively exposing all
analytic children above. Any correction, source-driven rearchitecture, split,
merge, or eligibility change requires registry version 2 and an append-only
delta. This phase supplies no Chen-theorem proof, audit completion, or theorem
completion.
