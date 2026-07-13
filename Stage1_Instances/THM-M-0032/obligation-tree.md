# THM-M-0032 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 38 semantic obligations before proof-phase work or closure credit. Its
content-derived denominator is bound to the exact `Statement.lean` and immutable anchor-audit
record. Every obligation remains absent from accepted proof state; the root stays `H1/M3/R4`.

The architecture selects a modern Kaplansky route while retaining both the primary PNAS route and
Stacks tag `0AG0` as separate source graphs. It rejects three tempting substitutions: adding an
`IsDomain` premise to the root, proving only the dimension-at-most-three theorem, and requiring
every nonzero prime ideal to be principal. The last claim is false in regular local rings of higher
dimension; only a height-one prime selected under a nonzero principal ideal is principalized.

## Typed proof route

```text
M0032-ROOT
`-- M0032-T-ASSEMBLE
    |-- M0032-N-DOMAIN
    |-- M0032-X-KAPLANSKY
    `-- M0032-A-PRIME-ELEMENT
        `-- M0032-T-PRIME-GENERATOR
            |-- M0032-C-MINIMAL-PRIME
            |-- M0032-L-PRINCIPAL-HEIGHT
            |-- M0032-L-MINIMAL-HEIGHT-ONE
            `-- M0032-L-HEIGHT-ONE-PRINCIPAL
                `-- M0032-T-HEIGHT-ONE
                    `-- M0032-B-DIMENSION-INDUCTION
                        |-- M0032-B-DIM-ZERO
                        `-- M0032-B-DIM-POSITIVE
                            |-- M0032-C-PARAMETER
                            |-- M0032-L-QUOTIENT-REGULAR
                            |-- M0032-L-QUOTIENT-DOMAIN
                            |-- M0032-L-PARAMETER-PRIME
                            |-- M0032-B-PRIME-CONTAINS
                            `-- M0032-B-PRIME-AVOIDS
                                |-- M0032-L-LOCALIZATION-REGULAR
                                |-- M0032-L-DIMENSION-DROP
                                |-- M0032-C-LOCALIZED-IDEAL
                                |-- M0032-L-INVERTIBLE
                                |-- M0032-L-TRIVIALIZATION
                                |-- M0032-C-CLEAR-DENOMINATOR
                                |-- M0032-L-ATOMIC-FACTORIZATION
                                `-- M0032-L-LIFT-PRIMALITY
```

## m0032-root

`M0032-ROOT` is the exact unrestricted proposition for every `R : Type u` with `CommRing R` and
`IsRegularLocalRing R`. It has no explicit domain, dimension, completeness, or characteristic
premise.

## m0032-s-interface

`M0032-S-INTERFACE` owns the universe, ordered typeclass binders, and
`UniqueFactorizationMonoid R` conclusion without adding hidden structure.

## m0032-s-boundary

`M0032-S-BOUNDARY` records that the regular-local antecedent excludes the zero ring but includes
fields, dimension zero, and all positive dimensions. The checked `Rat` witness authenticates the
field boundary.

## m0032-s-encoding

`M0032-S-ENCODING` owns the checked iff between instance-bound and explicit regularity. An
explicit `IsDomain` binder is deliberately not an alternate root encoding.

## m0032-s-foundation

`M0032-S-FOUNDATION` owns the final foundation, axiom, computation, import, and TCB decision.
Transitive acceptance and independent replay remain open.

## m0032-n-domain

`M0032-N-DOMAIN` is the first substantive open package: derive `IsDomain R` from the exact frozen
regular-local context. The anchor audit found no compatible pinned declaration that closes it.

## m0032-a-prime-element

`M0032-A-PRIME-ELEMENT` is the theorem-specific Kaplansky premise: every nonzero prime ideal
contains a prime element. It is not the false stronger assertion that every nonzero prime ideal is
principal.

## m0032-c-minimal-prime

`M0032-C-MINIMAL-PRIME` chooses a nonzero `a` in the given prime `P`, then a prime `Q` minimal
over `(a)` with `Q <= P`. Existence, containment, and the nonzero side condition remain explicit.

## m0032-l-principal-height

`M0032-L-PRINCIPAL-HEIGHT` applies the principal ideal theorem to bound `Q.height <= 1`. The
pinned theorem is support only until all side conditions and transports are checked.

## m0032-l-minimal-height-one

`M0032-L-MINIMAL-HEIGHT-ONE` combines domainhood and nonzeroness with the upper bound to obtain
`Q.height = 1`.

## m0032-l-height-one-principal

`M0032-L-HEIGHT-ONE-PRINCIPAL` is the central deep theorem: a height-one prime in a regular local
ring is principal. It is recursively expanded into dimension induction rather than hidden behind a
"standard" label.

## m0032-b-dimension-induction

`M0032-B-DIMENSION-INDUCTION` owns the well-founded dimension induction and its exhaustive
zero/positive split.

## m0032-b-dim-zero

`M0032-B-DIM-ZERO` shows that a zero-dimensional regular local domain is a field and hence has no
height-one prime.

## m0032-b-dim-positive

`M0032-B-DIM-POSITIVE` chooses a regular parameter and splits on whether the height-one prime
contains it. Every mathematical child of this branch remains visible in the proof graph.

## m0032-c-parameter

`M0032-C-PARAMETER` chooses `x` in the maximal ideal and outside its square.

## m0032-l-quotient-regular

`M0032-L-QUOTIENT-REGULAR` establishes regularity of `R/(x)`.

## m0032-l-quotient-domain

`M0032-L-QUOTIENT-DOMAIN` applies the domain package to that regular quotient.

## m0032-l-parameter-prime

`M0032-L-PARAMETER-PRIME` converts quotient domainhood into primality of `x` and `(x)`.

## m0032-b-prime-contains

`M0032-B-PRIME-CONTAINS` proves `P = (x)` when `x` belongs to the height-one prime.

## m0032-b-prime-avoids

`M0032-B-PRIME-AVOIDS` is the localization/descent branch when `x` is not in `P`.

## m0032-l-localization-regular

`M0032-L-LOCALIZATION-REGULAR` supplies regular-local structure at the relevant nonmaximal prime
localizations.

## m0032-l-dimension-drop

`M0032-L-DIMENSION-DROP` proves strict dimension decrease and invokes the induction hypothesis to
principalize localizations of `P`.

## m0032-c-localized-ideal

`M0032-C-LOCALIZED-IDEAL` packages `P_x` as finitely presented and locally free of rank one.

## m0032-l-invertible

`M0032-L-INVERTIBLE` converts those module properties into invertibility.

## m0032-l-trivialization

`M0032-L-TRIVIALIZATION` trivializes the invertible ideal over `R_x`. This central bridge has its
own 100-step budget and cannot be compressed into a library slogan.

## m0032-c-clear-denominator

`M0032-C-CLEAR-DENOMINATOR` writes a localized generator as `x^e f` with `f` in `P`.

## m0032-l-atomic-factorization

`M0032-L-ATOMIC-FACTORIZATION` factors `f` and selects an irreducible factor lying in `P`.

## m0032-l-lift-primality

`M0032-L-LIFT-PRIMALITY` lifts primality of that factor from `R_x` back to `R` using primality of
`x`.

## m0032-t-height-one

`M0032-T-HEIGHT-ONE` will be the checked recomposition of the contains/avoids branches. Its
composition declaration remains planned, so no closure is credited.

## m0032-t-prime-generator

`M0032-T-PRIME-GENERATOR` extracts a prime generator of `Q` and maps its membership through
`Q <= P`, yielding the exact Kaplansky premise.

## m0032-x-kaplansky

`M0032-X-KAPLANSKY` is the pinned generic criterion
`UniqueFactorizationMonoid.iff_exists_prime_mem_of_isPrime`. The local wrapper elaborates, but it
does no theorem-specific work and is not accepted proof state.

## m0032-t-assemble

`M0032-T-ASSEMBLE` is checked by `root_of_domain_primeElement_and_kaplansky`. It consumes the
domain, prime-element, and generic Kaplansky packages and yields the actual frozen root. Because
the first two packages remain premises, this conditional theorem is not a root proof.

## m0032-x-primary-source

`M0032-X-PRIMARY-SOURCE` preserves the PNAS Proposition 1, Corollary 2, Theorem 3, Corollary 4,
Nagata reduction, and Theorem 5 boundaries. Imported definitions, date/errata review, and an
independent source decision remain open.

## m0032-x-modern-source

`M0032-X-MODERN-SOURCE` maps the separate modern dimension-induction route at Stacks tag `0AG0`.
It is corroborating architecture, not a replacement for primary-source H0.

## m0032-x-provenance

`M0032-X-PROVENANCE` owns wrapper/body identity, source blobs, dependencies, revisions, licenses,
and alias deduplication. Full terminal-body closure remains open.

## m0032-x-trust

`M0032-X-TRUST` owns transitive declarations, axioms, artifacts, executables, replay, unsafe/oracle
boundaries, and supply-chain evidence for release.

## m0032-x-readable

`M0032-X-READABLE` requires a complete independently reviewed reconstruction. This architecture
document is a provisional map, not `R0`.

## m0032-x-workflow

`M0032-X-WORKFLOW` binds proof, source, validation, freshness, revocation, independent verification,
and release tasks without becoming a mathematical premise.

## Status boundary

All seven graph roles remain separate. The checked Lean harness reports only `propext`,
`Classical.choice`, and `Quot.sound` for its conditional declarations. No root proof body, H0,
accepted M0, R0, full trust/provenance closure, `AUDIT-Z`, validation, release, theorem completion,
or master acceptance is claimed.
