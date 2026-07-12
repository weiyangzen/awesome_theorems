# Frozen obligation tree

This is registry version 1 for the exact declaration `Stage1Instances.THM_M_1010.Target`. The
registry was fixed from the elaborated statement and the classical partition-coupling architecture,
without changing eligibility in response to available Lean closure. Its immutable denominator is
recorded in `obligation-registry.json`.

## Proof spine

The machine-relevant spine is:

```text
M1010-ROOT exact Target
`-- M1010-T-ASSEMBLE checked conditional conversion
    `-- M1010-C-COUPLING common-space construction
        |-- M1010-N-PARTITIONS refining null-boundary partitions
        |-- M1010-C-INTERVAL atomless interval coding space
        |-- M1010-L-MEASURABLE measurability of representatives
        |-- M1010-L-LAWS exact prescribed laws
        `-- M1010-L-METRIC-CONVERGENCE topology convergence
            `-- M1010-L-AE-STABILIZE a.e. stabilization of partition codes
```

The separate refinement graph attaches definitions, exact domains, and boundary branches to the
root. Provenance, evidence, trust, documentation, and workflow graphs remain distinct so that none
can accidentally receive proof credit. Every proof edge has a reciprocal `composes` edge.

## Node ledger

### m1010-root
The exact frozen target remains `M3`: no coupling theorem was found or implemented.

### m1010-s-definitions
The checked `WeakConvergence` and `Representation` declarations fix the conclusion's entire data
contract. This definition node proves no existence statement.

### m1010-s-domain
The universe and all topology, measurability, Borel, Polish, sequence, limit, and weak-convergence
binders are preserved. No Real-only or countability-restricted substitute is admitted.

### m1010-s-boundary
The later proof must explicitly retain atomic and countable spaces, constant sequences, and null
exceptional sets. This branch package is open.

### m1010-s-foundation
Classical-choice, quotient, transitive axiom, and TCB review is a release-critical open certificate.

### m1010-n-partitions
Construct nested or compatibly refining countable Borel partitions whose diameters tend to zero and
whose boundaries have zero `mu` measure. This is a substantive open construction.

### m1010-c-interval
Provide one atomless standard probability space plus the measurable interval allocation machinery
used for all laws. This interface is open and may not be replaced by separate sample spaces.

### m1010-c-coupling
Allocate compatible subintervals according to partition masses for `muSeq n` and `mu`, then select
representatives. The exact output is `CouplingPackage`; its child obligations are all mandatory.

### m1010-l-measurable
Establish a.e. measurability for each constructed map. A raw choice function is insufficient.

### m1010-l-laws
Prove the two exact `HasLaw` fields by pushforward equality, not merely equality on a selected
partition algebra.

### m1010-l-ae-stabilize
For almost every sample, finite-level codes must eventually agree at every fixed level. The null
sets must be combined into one exception set.

### m1010-l-metric-convergence
Use shrinking cells and the Polish topology to derive `Tendsto` for the full sequence, not a
subsequence and not convergence in measure.

### m1010-t-assemble
`target_of_couplingPackage` is a kernel-checked conditional composition certificate. It consumes
every field of `CouplingData` and yields the exact target, but gives the open package no proof credit.

### m1010-x-source
Pinpoint primary-source theorem/page/assumption and errata mapping remains required for H0.

### m1010-x-provenance
Terminal-body, transitive import/axiom, receipt, and replay closure remains required for release.

## Boundary

The registry freeze and conditional composition are self-tested only. Root closure, audit closure,
H0, R0, hermetic validation, independent review, and theorem completion all remain false. The
remaining root cut set is recorded structurally in `typed-graphs.json`; master acceptance is pending.
