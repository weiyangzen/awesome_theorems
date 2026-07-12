# THM-M-0161 frozen obligation architecture

Item: `S56-M-0161-OBLIGATION_TREE`.

The registry freezes 21 semantic obligations before proof execution. The selected route is the
classical Frenet-frame ODE construction followed by frame alignment and ODE uniqueness. Pinned
mathlib declarations are bridge ingredients only. No exact existence or uniqueness proof was found.

## Typed proof route

```text
M0161-ROOT exact canonical proposition
`-- M0161-T-ASSEMBLE checked conditional conjunction
    |-- M0161-T-EXISTENCE exact existence package
    |   |-- M0161-N-BASEPOINT choose point, position, proper frame
    |   |-- M0161-C-FRENET-GLOBAL global Frenet frame
    |   |   |-- M0161-C-FRENET-LOCAL local ODE solution
    |   |   |   `-- M0161-X-ODE pinned ODE bridge
    |   |   `-- M0161-L-FRAME-INVARIANTS preserve Gram matrix and determinant
    |   |-- M0161-C-CURVE integrate the tangent
    |   |-- M0161-L-REGULARITY prove C3 regularity
    |   |-- M0161-L-CURVATURE prove unit speed and curvature kappa
    |   `-- M0161-L-TORSION prove signed torsion tau
    `-- M0161-T-UNIQUENESS exact uniqueness package
        |-- M0161-N-ALIGN align position and proper frames
        |-- M0161-L-ODE-UNIQUENESS identify frames
        |   `-- M0161-X-ODE pinned ODE bridge
        `-- M0161-L-CURVE-UNIQUENESS identify curves
```

Statement definitions and boundary cases are a refinement graph. Foundation and provenance are
trust graphs; primary-source mapping is a provenance/documentation graph; execution order is a
workflow graph. None can masquerade as a proof premise.

## Node ledger

### m0161-root
Exact elaborated target. `[H3, M3, R4]`; the checked assembly still has two open premises.

### m0161-s-definitions
Checked statement encoding of derivatives, invariants, realization, and proper rigid motion.
`[H3, M0-L, R4]`.

### m0161-s-boundary
Checked mutations distinguish zero curvature, omitted existence, reflections, and a closed-domain
hypothesis. Later proof must still establish all open-interval derivative side conditions.
`[H3, M0-L, R4]`.

### m0161-s-foundation
Planned transitive axiom, classical-choice, noncomputability, TCB, and no-oracle audit.
`[H3, M4, R4]`.

### m0161-n-basepoint
Choose a point inside the nonempty interval and proper orthonormal initial data. `[H3, M4, R4]`.

### m0161-c-frenet-local
Encode the time-dependent Frenet system and discharge local existence hypotheses. The pinned
Picard-Lindelof theorem is not this bridge theorem. `[H3, M4, R4]`.

### m0161-l-frame-invariants
Prove preservation of pairwise dot products and orientation determinant. `[H3, M4, R4]`.

### m0161-c-frenet-global
Continue compatible local frame solutions across the entire arbitrary open interval. Local
existence alone cannot close this node. `[H3, M4, R4]`.

### m0161-c-curve
Integrate the global tangent and prove the exact within-derivative identity. `[H3, M4, R4]`.

### m0161-l-regularity
Bootstrap the constructed curve to the target's `ContDiffOn Real 3`. `[H3, M4, R4]`.

### m0161-l-curvature
Derive unit speed and `curvature = kappa`, including conversion to the frozen coordinate length.
`[H3, M4, R4]`.

### m0161-l-torsion
Derive the frozen signed triple-product formula and prove its denominator is nonzero.
`[H3, M4, R4]`.

### m0161-t-existence
Assemble the preceding construction and identities into `ExistencePackage`. `[H3, M4, R4]`.

### m0161-n-align
Construct the proper orthogonal map and translation aligning two realizing curves at a base point.
`[H3, M4, R4]`.

### m0161-l-ode-uniqueness
Show both Frenet frames solve the same Lipschitz ODE and instantiate pinned open-interval uniqueness.
`[H3, M4, R4]`.

### m0161-l-curve-uniqueness
Use equal tangents and the aligned base point to identify the curves on the connected interval.
`[H3, M4, R4]`.

### m0161-t-uniqueness
Package dot preservation, determinant one, translation, and pointwise equality as
`UniquenessPackage`. `[H3, M4, R4]`.

### m0161-t-assemble
Kernel-checked composition from `ExistencePackage` and `UniquenessPackage` to the exact root.
`[H3, M0-L, R4]`; it proves neither premise.

### m0161-x-ode
Pinned names and types for Picard-Lindelof existence and Gronwall uniqueness elaborate. The missing
Frenet encoding, Lipschitz proofs, and global continuation keep the mathematical bridge open.
`[H3, M0-L, R4]` as an interface audit only.

### m0161-x-source
Pending theorem/page/assumption/orientation/errata mapping for every material node. `[H3, M4, R4]`.

### m0161-x-provenance
Pending distinct terminal-body, import closure, axiom, TCB, and replay inventory. `[H3, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M0161-T-EXISTENCE` plus `M0161-T-UNIQUENESS`. Each leaf has a
substantive ledger capped at 100 steps; the cap is a future execution budget, not closure evidence.
Any correction, split, merge, or eligibility change requires registry version 2 and an append-only
delta. This phase supplies no source acceptance, audit completion, root closure, or theorem completion.
