# THM-M-0471 frozen obligation architecture

Item `S56-M-0471-OBLIGATION_TREE` freezes registry version 1 against the exact
natural-number/list/permutation statement and the immutable anchor inventory. The 22 canonical
IDs are the denominator for later machine, source, and readable coverage. Eligibility was selected
from the theorem architecture and the visible pinned source bodies before current closure status
was attached. Any correction, split, merge, exclusion, eligibility change, or terminal-body change
requires a new version and append-only delta.

## Proof route

```text
M0471-ROOT exact fundamental theorem of arithmetic target [open M3]
`-- M0471-T-ROOT-COMPOSE conditional exact child-to-root composition
    `-- M0471-T-ASSEMBLE existence and uniqueness package composition
        |-- M0471-C-WITNESS choose n.primeFactorsList
        |-- M0471-L-NONEMPTY use primeFactorsList_ne_nil
        |   `-- M0471-S-BOUNDARY retain n = 2 and exclude only zero and one
        |-- M0471-L-PRIMALITY recursively prove each minFac prime
        |-- M0471-L-PRODUCT recursively reconstruct n from minFac and division
        |   `-- M0471-N-NONZERO discharge reconstruction's n != 0 premise
        `-- M0471-L-UNIQUENESS use primeFactorsList_unique
            |-- M0471-N-NONZERO rule out a zero prime product
            `-- M0471-L-PERM-PRODUCT recursively match equal prime products
                |-- M0471-L-PRIME-DVD-PRODUCT locate a divisor of a product
                |-- M0471-L-MEM-PRIME-DIVISOR strengthen divisibility to membership
                |-- M0471-C-ERASE-PERM move and erase the matching factor
                `-- M0471-N-CANCEL-HEAD cancel the common nonzero prime and recurse
```

Every parent-to-child `proof_requires` edge has a reciprocal child-to-parent `composes` edge.
Statement refinement, source, provenance, evidence, trust, documentation, and workflow relations
remain separate and cannot receive proof credit.

## Node boundaries

### m0471-root

The exact target quantifies over `n : Nat`, assumes `1 < n`, constructs a nonempty `List Nat` of
primes with product `n`, and requires every alternative prime list to be related by `List.Perm`.

### m0471-s-interface

The ordered binders, natural domain, strict lower bound, multiplicity, product, and uniqueness up
to permutation are fixed. No integer signs, units, sorted-list equality, or exponent-map claim is
introduced.

### m0471-s-boundary

Zero and one are outside the root. Two, arbitrary primes, repeated prime factors, distinct factors,
and reordered lists remain in scope. The visible proof is uniform, so no independent case branch is
counted; that exclusion still awaits independent review.

### m0471-s-transport

`fundamentalTheoremOfArithmeticTarget_iff_expanded` checks only the direct expansion already frozen
by the statement phase. The integer and exponent-map representations remain uncredited.

### m0471-s-foundation

The anchor probe observed `propext`, `Classical.choice`, and `Quot.sound`. Complete transitive
foundation, executable TCB, artifact, and no-oracle review remains open.

### m0471-t-root-compose

`root_of_exactPrimeListAnchor` consumes the exact target as an explicit premise and returns it. It
checks endpoint identity but does not install the pinned mathlib candidate.

### m0471-t-assemble

`exactPrimeListAnchor_of_packages` consumes separate witness and pairwise-uniqueness packages and
constructs the exact root proposition. Both packages remain explicit premises.

### m0471-c-witness

`Nat.primeFactorsList` supplies the canonical increasing factor list. Its definition recursively
extracts `minFac`; naming the witness is not proof of nonemptiness, primality, product, or uniqueness.

### m0471-l-nonempty

`Nat.primeFactorsList_ne_nil` identifies nonemptiness exactly with `1 < n`; it preserves the
selected exclusion of zero and one without weakening the root.

### m0471-n-nonzero

Product reconstruction requires `n != 0`. Uniqueness separately rules out product zero because a
prime list cannot contain zero. These side conditions are explicit rather than hidden in wrappers.

### m0471-l-primality

`Nat.prime_of_mem_primeFactorsList` follows the recursive `minFac` definition: the head is prime,
and a tail member is handled at the strictly smaller quotient.

### m0471-l-product

`Nat.prod_primeFactorsList` recursively reconstructs the input after proving the quotient nonzero
and cancelling the selected `minFac` division.

### m0471-l-uniqueness

`Nat.primeFactorsList_unique` reduces uniqueness to equality of products and the generic
`perm_of_prod_eq_prod` theorem. Its one-line invocation does not make the deeper theorem a leaf.

### m0471-l-perm-product

`perm_of_prod_eq_prod` is the material terminal engine. It recursively matches a head prime in the
other list, moves that occurrence to the front, cancels the common nonzero factor, and recurses.

### m0471-l-prime-dvd-product

`Prime.dvd_prod_iff` supplies the prime-divides-a-product case split needed to locate a factor.

### m0471-l-mem-prime-divisor

`mem_list_primes_of_dvd_prod` combines prime divisibility with primality of every list element so
that divisibility by a member becomes equality and hence list membership.

### m0471-c-erase-perm

`List.perm_cons_erase` moves the selected occurrence to the head while preserving the remaining
multiset. This construction is why repeated primes are handled correctly.

### m0471-n-cancel-head

The matched prime is nonzero, so multiplicative cancellation reduces equality of products to the
tail products used by the recursive call.

### m0471-x-source

The Euclid web leads remain `H1`. A lawful pinned edition, translation and incorporated-definition
audit, complete modern derivation, errata disposition, node crosswalk, and independent source
review remain open.

### m0471-x-provenance

The visible terminal bodies are pinned to immutable blobs in `Mathlib/Data/Nat/Factors.lean` and
`Mathlib/Data/List/Prime.lean`. Full transitive declaration, compiled-artifact, license, trust, and
supply-chain closure remains downstream.

### m0471-x-readable

This architecture record is not an independently reviewed `R0` proof reconstruction. Node-specific
source anchors and a complete reader route through both recursive arguments remain required.

### m0471-x-workflow

Proof adoption, validation, hermetic replay, independent verification, freshness, revocation, and
release receipts remain open and do not act as proof premises.

## Freeze boundary

`ObligationTree.lean` checks two conditional compositions only. It never invokes the pinned
factorization family to construct the root. The anchor remains an unaccepted `M0-W` candidate, the
accepted proof state is empty, and the root remains `[H1, M3, R4]`. No H0, accepted M0, R0, audit
completion, release, theorem completion, or master acceptance is claimed.
