# THM-M-0914 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 19 semantic obligations before proof-phase
acceptance. Fourteen are machine-relevant statement or proof-route obligations;
the remainder expose source, provenance, trust, readability, and workflow
boundaries. The denominator is derived from stable registry fields and bound to
the exact statement and anchor-audit inputs.

No obligation is accepted closed. The pinned finite-type theorem is a shallow
wrapper over the finite-set terminal body, so they share one route rather than
receiving duplicate root credit. The independently located external theorem and
the duplicate instructional wrapper also receive no machine credit here.

## Typed proof route

```text
M0914-ROOT
`-- M0914-T-ROOT-COMPOSE
    |-- M0914-N-FIN-CARD-INEQUALITY
    |   |-- M0914-N-FIN-CARD-IDENTITY
    |   `-- M0914-N-SUCCESSOR-LT
    `-- M0914-A-FINTYPE-WRAPPER
        |-- M0914-N-UNIV-MAPS-TO
        `-- M0914-L-FINSET-COLLISION
            |-- M0914-L-CARD-INJON-BOUND
            `-- M0914-L-NO-COLLISION-INJON
```

The finite-set terminal uses contradiction: absence of a collision makes the
map injective on the source set, while injectivity and the maps-to premise force
the source cardinality not to exceed the target cardinality. That contradicts
the strict cardinality premise. The finite-type wrapper applies this terminal
to the two universes, and the root specializes it using the two `Fin`
cardinality identities and `n < n + 1`.

`ObligationTree.lean` kernel-checks every child-to-parent interface with the
imported terminal bodies retained as explicit premises. Its separate candidate
adapters identify the pinned declarations but are not consumed by the
conditional root certificate. Thus the architecture does not silently perform
the later proof phase.

## Node ledger

<a id="m0914-root"></a>
### M0914-ROOT

The exact frozen proposition over `Fin (n + 1) -> Fin n`, with no positivity
hypothesis and no general finite-type broadening. It remains `[H1, M3, R4]`.

<a id="m0914-s-interface"></a>
### M0914-S-INTERFACE

Owns the ordered `n` and placement binders, empty premise list, distinctness,
and equal-image conclusion. Statement checking is provisional interface
evidence only.

<a id="m0914-s-boundary"></a>
### M0914-S-BOUNDARY

Keeps `n = 0` in scope through the impossible total-function binder and checks
`n = 1` as the first inhabited case. These are scope fixtures, not an
exhaustive proof by finite computation.

<a id="m0914-s-box-transport"></a>
### M0914-S-BOX-TRANSPORT

Owns the checked iff to the explicit shared-box formulation. The selected
proof route returns equal images directly, so this transport is a refinement
edge rather than a proof premise.

<a id="m0914-s-foundation"></a>
### M0914-S-FOUNDATION

Owns acceptance of the disclosed `propext`, `Classical.choice`, and
`Quot.sound` dependencies plus the Lean, mathlib, and no-oracle policy.
Release-grade review remains open.

<a id="m0914-t-root-compose"></a>
### M0914-T-ROOT-COMPOSE

Consumes the exact finite-type collision interface and concrete `Fin`
cardinality inequality to return the root. The conditional composition is
checked locally; its finite-type premise remains uninstalled.

<a id="m0914-n-fin-card-inequality"></a>
### M0914-N-FIN-CARD-INEQUALITY

Rewrites both finite cardinalities and applies the successor inequality. The
composition and a local realization are checked, without supplying root proof
credit.

<a id="m0914-n-fin-card-identity"></a>
### M0914-N-FIN-CARD-IDENTITY

Exposes `Fintype.card_fin` as the exact representation-normalization leaf. It
is not folded invisibly into a `simp` call.

<a id="m0914-n-successor-lt"></a>
### M0914-N-SUCCESSOR-LT

Supplies the elementary arithmetic fact `n < n + 1`. It has no further case,
induction, external, or computational package hidden inside this route.

<a id="m0914-a-fintype-wrapper"></a>
### M0914-A-FINTYPE-WRAPPER

Is the exact general interface of
`Fintype.exists_ne_map_eq_of_card_lt`. The pinned body only applies the
finite-set terminal to `univ`, so the wrapper is not treated as the terminal
proof body or as an independent second proof.

<a id="m0914-n-univ-maps-to"></a>
### M0914-N-UNIV-MAPS-TO

Checks that every total map sends each member of the source universe to the
target universe. This is the finite-set wrapper's membership normalization.

<a id="m0914-l-finset-collision"></a>
### M0914-L-FINSET-COLLISION

Is the substantive terminal theorem
`Finset.exists_ne_map_eq_of_card_lt_of_maps_to`. Its two material proof steps
are explicit children rather than being hidden behind the short wrapper call.

<a id="m0914-l-card-injon-bound"></a>
### M0914-L-CARD-INJON-BOUND

Owns `Finset.card_le_card_of_injOn`: a map injective on `s` and mapping `s`
into `t` forces `card s <= card t`. Its short pinned body uses image
cardinality and subset monotonicity; further expansion is not currently
required by the 100-step or risk rules.

<a id="m0914-l-no-collision-injon"></a>
### M0914-L-NO-COLLISION-INJON

Turns absence of distinct equal-image members into `Set.InjOn`. The exact
logical conversion is locally checked and feeds only the terminal
contradiction composition.

<a id="m0914-x-source"></a>
### M0914-X-SOURCE

Tracks the modern finite-function statement lead and the unresolved historical
Dirichlet attribution. Pinpoint primary proof, assumptions, chronology,
errata, and independent review remain open, so H0 is not claimed.

<a id="m0914-x-provenance"></a>
### M0914-X-PROVENANCE

Separates the mathlib wrapper, finite-set terminal, cardinal helper, and local
composition bodies. Immutable source blobs are known from the anchor audit;
proof-phase adoption and complete transitive provenance remain open.

<a id="m0914-x-trust"></a>
### M0914-X-TRUST

Tracks the provisional axiom, placeholder, bodyless, and unsafe scans. Warm
worker checks do not supply compiled-artifact, supply-chain, hermetic, or
independent release trust.

<a id="m0914-x-readable"></a>
### M0914-X-READABLE

Requires a complete independently reviewed counting reconstruction mapped to
every proof node. This architecture is a labeled plan and boundary report, not
an R0 completed-proof claim.

<a id="m0914-x-workflow"></a>
### M0914-X-WORKFLOW

Requires dependency-ordered proof, validation, and release receipts plus
freshness and revocation decisions. Worker self-test cannot satisfy master
acceptance.

## Exclusions and open boundary

The route has no additional mathematical case split, constructed object,
certificate computation, oracle, or transport-back package. Those decisions
remain pending independent approval in the registry. The checked box-witness
iff and zero/one-box fixtures stay visible in the refinement graph without
being miscounted as proof children.

The first open machine cut is the pinned finite-type wrapper, its substantive
finite-set terminal, and the cardinal injectivity bridge. Source, foundation,
provenance, trust, readable-review, workflow, validation, release, and master
acceptance gates are also open. The root therefore remains `M3`; neither
`AUDIT-Z` nor theorem completion is claimed.
