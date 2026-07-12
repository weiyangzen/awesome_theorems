# THM-M-1277 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 24 canonical obligations before the proof phase.
Twenty-two are required machine obligations; `M1277-X-SOURCE` is a human
source boundary and `M1277-X-PROVENANCE` is an informational release overlay.
The ordered eligibility projections and their canonical digest are stored in
`obligation-registry.json`. No obligation is excluded because it is difficult
or lacks an existing proof.

The freeze is bound to the exact bytes of `Statement.lean` and
`anchor-audit.json`. The audit found no exact Lean anchor, so the proof graph
expands a direct classical route: rearrangement and radial reduction for the
endpoint, and an explicit concentrating Moser sequence for sharpness.

## Typed proof route

```text
M1277-ROOT
`-- M1277-T-ASSEMBLE [checked conditional composition]
    |-- M1277-T-ENDPOINT-COMPLETE [open]
    |   |-- density/completion transport
    |   `-- M1277-T-ENDPOINT-SMOOTH
    |       |-- zero extension and Schwarz rearrangement
    |       |-- equimeasurability and Polya-Szego
    |       `-- radial reduction and critical 1D endpoint estimate
    `-- M1277-T-SHARP [open]
        |-- interior ball and explicit Moser sequence
        |-- W_0^{1,2} membership and energy normalization
        `-- supercritical exponential-integral divergence
```

The statement definitions, domain conventions, boundary cases, and foundation
policy are root refinements. Provenance, evidence, trust, documentation, and
workflow are separate typed graphs and cannot contribute proof closure.
Every proof requirement has a reciprocal `composes` edge. The structural
validator checks acyclicity and root reachability for every required machine
obligation.

## Leaf and composition policy

Each currently leaf-shaped obligation has a substantive premises/inference/
output/use ledger and a budget of at most 100 steps. These are planning budgets,
not proof metrics. Proof work must split a node if its exact Lean signature or
source expansion exposes hidden substantive work. No planned signature, source
mapping, or wrapper receives closure credit.

`statement_of_branches` is a kernel-checked exact composition theorem. Its two
premises are deliberately the complete endpoint and sharpness conjuncts; it
does not conceal analytic content. Both premises remain open and form the
current root cut set.

## Status boundary

This phase freezes architecture only. It proves neither the endpoint estimate
nor supercritical unboundedness, supplies no accepted source coverage or
terminal provenance closure, and makes no audit or theorem-completion claim.
The root remains M3 pending direct formalization of both analytic branches.
