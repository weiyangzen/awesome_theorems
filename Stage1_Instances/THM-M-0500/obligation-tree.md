# THM-M-0500 frozen obligation architecture

Item: `S56-M-0500-OBLIGATION_TREE`.

The registry freezes 14 semantic obligations from the exact statement and the source structure of
the pinned mathlib proof. Eligibility and the denominator do not depend on whether a declaration is
already available. The existing candidate is recorded only after the freeze in the status overlay.

## Typed proof route

```text
M0500-ROOT exact infinitude target
`-- M0500-T-ASSEMBLE finite-support contradiction (checked conditionally)
    |-- M0500-T-NONSUM prime-residue weighted series is not summable
    |   |-- M0500-L-LOWER pole lower bound near 1
    |   |   `-- M0500-C-AUX continuous pole-cancelled auxiliary function
    |   |       |-- M0500-L-LSERIES residue-class L-series identity
    |   |       |   `-- M0500-N-CHAR character-orthogonality decomposition
    |   |       `-- M0500-L-NONVANISH closed-half-plane L-function nonvanishing
    |   `-- M0500-L-NONPRIME non-prime prime-power contribution is summable
    `-- M0500-L-SUPPORT weighted support equals the target prime set
```

`M0500-S-SCOPE` and `M0500-S-FOUNDATION` refine the statement and trust boundary.
`M0500-X-SOURCE` and `M0500-X-PROVENANCE` are non-proof source/provenance overlays. Typed source,
evidence, trust, documentation, and workflow edges cannot supply proof premises.

## Node ledger

All substantive proof nodes are `H1` because the primary human-source theorem/page/assumption map
is not accepted. They are `R4` because no independently reviewed readable reconstruction exists.
The proof phase must recheck and integrate the pinned bodies before any machine-debt promotion.

### m0500-root
The exact elaborated proposition from `Statement.lean`. `[H1, M3, R4]`.

### m0500-s-scope
Nonzero natural modulus, unit `ZMod` residue, natural primes, and the included `q = 1` boundary.
`[H1, M0-L, R4]` for the statement interface only.

### m0500-s-foundation
Classical logic, choice, quotient soundness, complete transitive imports, and no-oracle policy.
`[H1, M4, R4]`; full trust closure is pending.

### m0500-n-char
Express the residue-class von Mangoldt function by Dirichlet-character orthogonality. `[H1, M3, R4]`.

### m0500-l-lseries
Pass that pointwise identity to an L-series/logarithmic-derivative identity on `re s > 1`.
`[H1, M3, R4]`.

### m0500-l-nonvanish
Supply analytic continuation and nonvanishing of Dirichlet L-functions on the closed half-plane.
This is a major imported bridge and cannot be hidden inside “by library.” `[H1, M3, R4]`.

### m0500-c-aux
Construct the pole-cancelled auxiliary function and prove continuity on `re s >= 1`.
`[H1, M3, R4]`.

### m0500-l-lower
Derive the real-axis lower bound as `x` tends to `1` from the right. `[H1, M3, R4]`.

### m0500-l-nonprime
Prove summability of the non-prime prime-power contribution using the prime-power decomposition and
geometric/r-power majorants. `[H1, M3, R4]`.

### m0500-t-nonsum
Combine the lower bound and non-prime summability to contradict summability of the prime part.
`[H1, M3, R4]`.

### m0500-l-support
Identify the support of the weighted prime part with the exact target set. `[H1, M3, R4]`.

### m0500-t-assemble
Turn finiteness into finite support and hence summability, contradicting `M0500-T-NONSUM`. The
child-to-parent composition is kernel-checked in `ObligationTree.lean`; its premises remain open for
this phase. `[H1, M0-L, R4]` as a conditional composition only.

### m0500-x-source
Pending primary-source edition/theorem/page/assumption/errata crosswalk. `[H1, M4, R4]`.

### m0500-x-provenance
Pinned terminal body, declaration closure, imports, axioms, TCB, license, and replay inventory.
`[H1, M4, R4]`; anchor evidence is not release provenance.

## Freeze boundary

The minimal open root cut is `M0500-T-NONSUM` plus `M0500-L-SUPPORT`. The checked conditional
assembly proves neither premise. The graph freeze supplies no accepted proof state, audit
completion, or theorem completion. Any semantic correction, split, merge, or eligibility change
requires registry version 2 with an append-only delta.
