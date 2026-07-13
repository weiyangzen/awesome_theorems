# THM-M-0484 frozen obligation architecture

Item `S56-M-0484-OBLIGATION_TREE` freezes registry version 1 against the exact statement and
immutable anchor audit. Its 36 canonical IDs form the later inventory denominator. The machine,
human-source, and readable denominator sets are explicit and were derived from theorem roles and
the visible pinned source architecture, not from which proof candidates were already available.
Changing the target, a split or merge, an exclusion, an edge role, or a terminal proof-body identity
requires a new registry version and an append-only delta.

## Checked proof spine {#m0484-root}

```text
M0484-ROOT exact Lucas-Lehmer iff [recorded provisional M3]
`-- M0484-T-ASSEMBLE conditional exact iff composition
    |-- M0484-T-SUFFICIENCY pinned forward terminal [M1/E2 candidate; no credit]
    |   `-- M0484-B-SUFF-CONTRA checked conditional contrapositive
    |       |-- M0484-L-ORDER-INEQ checked conditional order/cardinality bound
    |       |   |-- M0484-L-ORDER-OMEGA checked conditional exact-order argument
    |       |   |   |-- M0484-L-OMEGA-NEGONE checked conditional formula/vanishing step
    |       |   |   |   |-- M0484-L-OMEGA-FORMULA
    |       |   |   |   `-- M0484-L-MERSENNE-VANISH
    |       |   |   |-- M0484-L-OMEGA-ONE checked by squaring NEGONE
    |       |   |   `-- M0484-L-TWO-LT-Q
    |       |   `-- M0484-L-X-CARD-UNITS
    |       `-- M0484-L-MINFAC-SQUARE
    `-- M0484-T-NECESSITY pinned reverse terminal [M1/E2 candidate; no credit]
        `-- M0484-B-NEC-TRACE checked conditional recurrence/closed-form/trace step
            |-- M0484-N-RECURRENCE-X
            |-- M0484-L-CLOSED-FORM
            `-- M0484-L-OMEGA-TRACE
```

### m0484-t-assemble

The terminal assembly consumes both exact directions to construct the iff and then returns the
canonical target unchanged. `root_of_directions` and `root_of_terminal` check both interfaces.

### m0484-t-sufficiency

The forward terminal is the exact proposition delivered by `lucas_lehmer_sufficiency` after the
canonical lower bound implies its `1 < p` premise. It is a candidate, not an accepted proof node.

### m0484-b-suff-contra

The checked conditional branch assumes the order inequality and generic least-factor square bound,
contraposes primality, and derives the impossible strict inequality `mersenne p < mersenne p`.

### m0484-t-necessity

The reverse terminal is the exact proposition delivered by `lucas_lehmer_necessity`, with the
canonical `3 <= p` and Mersenne primality premise. It is candidate-only like the forward terminal.

### m0484-b-nec-trace

The checked conditional branch rewrites `p = p' + 2`, transports the recurrence into `X`, applies
the closed form, and takes the first component of the zero trace identity.

Every `proof_requires` edge in this spine has a reciprocal `composes` edge naming one of ten
kernel-checked conditional declarations in `ObligationTree.lean`. Each certificate exposes all of
its exact child conclusions as arguments. No pinned terminal is supplied to the root in this phase.

## Visible source expansion {#visible-source-expansion}

The proof spine alone would still hide substantial work. The refinement graph therefore freezes 17
additional source-body decompositions, each explicitly labeled
`source_body_decomposition_unverified_as_child_to_parent_composition`. They include:

- `M0484-C-OMEGA-UNIT`, the unit made from `omega` and its inverse;
- `M0484-C-X-RING`, the quadratic ring `X q` and its structures;
- `M0484-C-MINFAC`, the positive least-factor construction `q p`;
- `M0484-N-INDEX`, the shared `p = p' + 2` and `p - 2 = p'` normalization;
- `M0484-N-PRIME-EXPONENT`, primality and oddness of the exponent;
- `M0484-L-LEGENDRE-TWO` and `M0484-L-LEGENDRE-THREE`;
- `M0484-C-X-FROBENIUS`, the characteristic and power identities feeding the trace;
- the recurrence, closed-form, cardinality, minimum-factor, and vanishing dependencies reused by
  both directions, including the explicit `two_lt_q` premise used by the unit-cardinality bound.

These edges document real pinned source structure and prevent major calls from being mistaken for
leaves. They do not claim machine closure. Each requires a future exact composition certificate
before its parent can receive accepted machine status. Aliases, statement transports, the anchor
wrapper, and concrete Mersenne examples receive no duplicate terminal-body credit.

### m0484-n-index

The shared exponent normalization writes `p = p' + 2` and then reduces the residue index `p - 2`
to `p'`. It remains a distinct semantic obligation even though arithmetic automation discharges it
inside the conditional harness.

## Assurance nodes

### m0484-s-target

The root preserves `p : Nat`, `3 <= p`, both directions of the iff, the exact
`LucasLehmerTest p` predicate, and `Nat.Prime (mersenne p)`. Its elaborated expression fingerprint
is `6bd6024b...3151aea`.

### m0484-s-encodings

The registry separately freezes the Mersenne function, integer recurrence, `ZMod` recurrence,
reduced integer recurrence, residue at zero-based index `p - 2`, and test predicate. These are
shared semantic interfaces, not six competing root theorems.

### m0484-s-boundary

All natural exponents `p >= 3` remain in scope, including composite exponents. Values 0 and 1 are
degenerate; `p = 2` is a checked counterexample because `mersenne 2` is prime while the residue is
not zero. No redundant prime-exponent premise is added.

### m0484-s-transport

The test-to-`ZMod` transport and the `ZMod`-to-reduced-integer transport are checked once and do not
inflate semantic or proof-body coverage.

### m0484-s-foundation

The candidate audit observed exactly `propext`, `Classical.choice`, and `Quot.sound`, with no
bodyless nonaxiom or unsafe declaration. Complete serialized closure, imported compiled-artifact
provenance, executable TCB inventory, and independent replay remain open.

### m0484-x-source

The catalog has no formula or citation. A modern source lead gives an odd-prime, one-based version
and omits the necessity proof; the 1930 primary paper was not inspected. Domain, index, assumptions,
complete proof, corrections, and independent review remain open at `H1`.

### m0484-x-provenance

The two distinct terminal body identities are `8ec5fa60...99efaf` for sufficiency and
`8f45e13a...d01dd` for necessity in pinned source blob `36af7002...82e84bd4`. The local anchor and
conditional composition declarations are adapters, not new terminal proof bodies.

### m0484-x-trust

The trust-zero anchor walk covered 35,389 declarations in 1,243 modules. A complete sorted closure
hash, imported oleans, tool executables, cold replay, and release-grade trust attestation remain
downstream gates.

### m0484-x-readable

This architecture is not a complete independently reviewed proof reconstruction. Every node has a
substantive budget at most 55 steps and a split rule, but `R4` remains until the mathematical route
is reconstructed and reviewed node by node.

### m0484-x-workflow

Proof installation, validation, hermetic replay, independent verification, release, freshness, and
revocation receipts remain separate from proof premises and remain open.

## Freeze boundary

The two pinned directions are at most `M1` candidates under nonrelease `E2` worker evidence. The
predecessor packet recorded `M0-W/E2`, but rev-5.6 section 4 requires `E1` for `M0-W`; this freeze
therefore fails closed rather than inheriting that label. The candidates have `closure_credit=false`;
the accepted closed set is empty, and the authoritative vector remains `[H1, M3, R4]`. The immediate
machine cut set is the two terminal directions. The release cut set additionally contains source,
foundation, provenance, trust, readability, and workflow gates. Neither `AUDIT-Z` nor theorem
completion is claimed.
