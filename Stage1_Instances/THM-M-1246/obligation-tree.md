# THM-M-1246 frozen obligation architecture

Item: `S56-M-1246-OBLIGATION_TREE`.

The registry freezes 15 semantic obligations before proof execution. It selects the classical
punctured-domain divergence proof. The anchor audit found no exact Lean proof, and the source
pinpoint remains pending, so this architecture does not improve H debt or prove the theorem.

## Typed proof route

```text
M1246-ROOT exact canonical proposition
`-- M1246-T-ROOT-TRANSPORT checked conditional composition
    `-- M1246-T-ANALYTIC complete analytic package (open)
        |-- M1246-S-BOUNDARY dimension, singularity, and integrability
        |-- M1246-N-CUTOFF radial puncture cutoffs
        |-- M1246-L-DIVERGENCE divergence of x / ||x||^2
        |-- M1246-L-INTEGRATION-BY-PARTS compact-support identity
        |-- M1246-L-DERIVATIVE derivative and pairing calculation
        |-- M1246-L-CAUCHY-SCHWARZ cross-term estimate
        |-- M1246-L-LIMIT remove the puncture cutoff
        `-- M1246-L-REARRANGE obtain the exact sharp constant
```

Definitions, foundation policy, source mapping, provenance, evidence, trust, documentation, and
workflow edges are stored separately. They cannot count as proof premises.

## Node ledger

### m1246-root
Exact elaborated target. `[H2, M3, R4]`; no proof inhabitant is supplied.

### m1246-s-definitions
Checked statement vocabulary, binders, measures, and constant. `[H2, M0-L, R4]`.

### m1246-s-boundary
Dimension positivity, zero function, origin convention, measurability, and integrability package.
`[H2, M4, R4]`.

### m1246-s-foundation
Pending transitive axiom, import, Haar-volume, Bochner-integral, and TCB certificate. `[H2, M4, R4]`.

### m1246-n-cutoff
Construct smooth radial cutoffs around the origin and establish convergence. `[H2, M4, R4]`.

### m1246-l-divergence
Prove the dimension-dependent divergence identity away from zero. `[H2, M4, R4]`.

### m1246-l-integration-by-parts
Prove the compact-support integration-by-parts identity on the regularized domain. `[H2, M4, R4]`.

### m1246-l-derivative
Compute the derivative of `u^2` and its radial pairing with correct norm bounds. `[H2, M4, R4]`.

### m1246-l-cauchy-schwarz
Apply the integral Cauchy-Schwarz estimate to the cross-term. `[H2, M4, R4]`.

### m1246-l-limit
Remove the cutoff with a justified convergence theorem and recover the global integrals.
`[H2, M4, R4]`.

### m1246-l-rearrange
Handle nonnegativity and the zero case, then rearrange to `4/(n-2)^2`. `[H2, M4, R4]`.

### m1246-t-analytic
Assemble every analytic obligation into the exact frozen proposition. `[H2, M4, R4]`.

### m1246-t-root-transport
Kernel-checked identity composition from the exact terminal proposition to the exact root.
`[H2, M0-L, R4]`; its premise is open, so it supplies no root proof credit.

### m1246-x-source
Pending primary-source theorem/page/assumption/errata map for each material step. `[H2, M4, R4]`.

### m1246-x-provenance
Pending terminal-body, dependency, axiom, trust, and replay inventory. `[H2, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M1246-T-ANALYTIC`. The checked conditional transport proves neither
that premise nor the Hardy inequality. Any correction, split, merge, exclusion, or eligibility
change requires registry version 2 with an append-only delta. This phase supplies no theorem
completion, audit completion, H0, M0 root, or R0 claim.
