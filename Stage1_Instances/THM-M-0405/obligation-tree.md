# THM-M-0405 obligation tree

Item `S56-M-0405-OBLIGATION_TREE` freezes registry
`THM-M-0405-OBLIGATIONS-v1` before giving any mathematical node proof credit.
The architecture follows the Bilu-Hanrot-Voutier route identified by the
prerequisite audit. It is not a reconstruction of the published proof and does
not claim that the missing central theorem fits in a short Lean proof.

## Frozen route

```text
M0405-ROOT
`-- M0405-C-ROOT-COMPOSITION (checked interface)
    |-- M0405-B-LUCAS
    |   `-- M0405-T-LUCAS-ADAPTER
    |       `-- M0405-X-BHV-BRIDGE
    `-- M0405-B-LEHMER
        `-- M0405-T-LEHMER-ADAPTER
            `-- M0405-X-BHV-BRIDGE
                |-- M0405-N-PAIR-NORMALIZATION
                |-- M0405-C-CYCLOTOMIC-FACTOR
                |-- M0405-L-NONPRIMITIVE-BOUND
                |-- M0405-L-LARGE-INDEX-EXCLUSION
                `-- M0405-B-DEFECTIVE-CLASSIFICATION
```

`ObligationTree.lean` checks only that the exact Lucas and Lehmer branches are
equivalent to the two projections of `Statement` and jointly compose to it.
The branch hypotheses remain premises, so the checked term is interface
evidence rather than closure evidence.

## Node boundaries

### m0405-root

The exact frozen conjunction `Stage1.THM_M_0405.Statement`. It requires both
branches and the checked conjunction composition. `[H1, M4, R3]`.

### m0405-s-definitions

Audits the two pair structures, quotient identities, discriminants, and exact
primitive-divisor predicates. Elaborated definitions do not imply existence
of a prime. `[H1, M4, R3]`.

### m0405-s-foundation

Requires the eventual proof's transitive declaration, axiom, computation, and
TCB report. It cannot close before proof bodies exist. `[H1, M4, R3]`.

### m0405-b-lucas

The exact left conjunct for all canonical Lucas pairs and indices above 30.
It is separately required so Lehmer evidence cannot be substituted. `[H1,
M4, R3]`.

### m0405-b-lehmer

The exact right conjunct, including the parity-sensitive Lehmer sequence and
its squared even denominator. `[H1, M4, R3]`.

### m0405-n-pair-normalization

Packages either canonical pair as the normalized data used in the BHV proof,
preserving integrality, coprimality, nonzero conditions, quotient nontorsion,
and the stored sequence identity. `[H1, M4, R4]`.

### m0405-c-cyclotomic-factor

Constructs the homogeneous cyclotomic factor of the term and relates its
prime valuations to primitive divisors, including discriminant and earlier
term exclusions. `[H1, M4, R4]`.

### m0405-l-nonprimitive-bound

Turns absence of a primitive divisor into the explicit cyclotomic upper bound.
The `100` step budget is a mandatory future split boundary, not an assertion
that the published argument is already reconstructed. `[H1, M4, R4]`.

### m0405-l-large-index-exclusion

Combines certified cyclotomic lower estimates and the nonprimitive upper bound
to reduce defectiveness to a finite index range. Analytic inequalities and
any computation certificates remain explicit proof work. `[H1, M4, R4]`.

### m0405-b-defective-classification

Exhaustively classifies the remaining defective Lucas and Lehmer pairs and
establishes that their indices are at most 30. This deep finite branch must be
expanded before implementation if its semantic ledger exceeds 100 steps.
`[H1, M4, R4]`.

### m0405-x-bhv-bridge

The central common theorem: normalization, bounds, and exhaustive
classification imply a primitive divisor for every index above 30. No pinned
Lean terminal candidate was found, so this is open formalization debt rather
than an imported theorem. `[H1, M4, R3]`.

### m0405-t-lucas-adapter

Translates the common theorem to `LucasPair.IsPrimitiveDivisor`, including the
exact discriminant and every earlier positive term. `[H1, M4, R3]`.

### m0405-t-lehmer-adapter

Translates the common theorem to `LehmerPair.IsPrimitiveDivisor`, respecting
odd/even quotient identities and `squaredEvenDenominator`. `[H1, M4, R4]`.

### m0405-c-root-composition

`statement_of_branches` is a kernel-checked child-to-root interface. Its two
arguments are open proof obligations, so this node remains `M4` and receives
no terminal proof-body credit. `[H1, M4, R3]`.

### m0405-x-provenance

Requires content-addressed terminal bodies, transitive dependencies, axiom
inventory, computations, and source boundaries after implementation. The
negative anchor search is not provenance closure. `[H1, M4, R3]`.

## Frozen boundary

There are 15 canonical root-relevant, machine-required obligations; 12 require
human-source crosswalks and all 15 require readable treatment. No obligation
is closed. The minimal mathematical root cut is `M0405-X-BHV-BRIDGE`, but its
closure alone would not close the exact adapters, composition premises,
provenance, trust, or review gates. `audit_complete=false` and
`theorem_complete=false`.
