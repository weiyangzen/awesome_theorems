# THM-M-0822 frozen obligation architecture

Item `S56-M-0822-OBLIGATION_TREE` freezes registry version 1 against the exact positive uniform
maximum-value statement and the visible bodies of the target-owned star construction and pinned
`Finset.erdos_ko_rado`. The 27 canonical IDs are the denominator for later machine, source, and
readable coverage. Proof availability did not change eligibility or risk. Any correction, split,
merge, exclusion, eligibility change, or proof-body identity change requires a new registry version
and an append-only delta.

## Proof route

```text
M0822-ROOT exact maximum-value target [open M3]
`-- M0822-T-ASSEMBLE exact conjunction assembly
    |-- M0822-T-ATTAINMENT attaining family package
    |   |-- M0822-C-STAR select a center and construct its star
    |   |   `-- M0822-L-GROUND-ELEMENT choose a center from the range assumptions
    |   |-- M0822-L-STAR-INTERSECTING shared-center intersection
    |   |-- M0822-L-STAR-SIZED r-uniformity
    |   |-- M0822-L-STAR-CARD choose(n-1,r-1) cardinality
    |       `-- M0822-L-STAR-IMAGE identify it as an insert image
    `-- M0822-T-UPPER-ADAPTER reorder the terminal interface
        `-- M0822-T-MATHLIB-EKR pinned universal upper bound
```

Every `proof_requires` edge has a reciprocal `composes` edge and a provisional Lean composition
certificate. The target-owned attainment hierarchy has explicit child-consuming harnesses at
construction, cardinality, and attainment. The imported terminal's internal source route is
recorded as informational `expository_decomposition`; those nodes share the pinned terminal body
and receive no independent machine or coverage credit.

## Node boundaries

### m0822-root

The root is exactly `ErdosKoRadoMaximumTarget`: for every `1 <= r <= n / 2`, attainment and the
universal upper bound are conjoined. `rootOfExactAssembly` consumes only `ExactAssembly`, the exact
output of `M0822-T-ASSEMBLE`, and yields the canonical root. It does not classify equality families.

### m0822-s-target

The `Nat` binders, labeled ground set `Fin n`, family type, positive rank, inclusive half-size
boundary, existential and universal scopes, and binomial expression are frozen by the statement
fingerprint. This overlay receives no independent proof credit.

### m0822-s-boundary

Rank zero and the inadmissible empty and singleton ground sets lie outside the root. Rank one and
`r = n / 2` remain in scope. In particular, the architecture adds no uniqueness-of-extremizer
branch at the equality boundary.

### m0822-s-foundation

The checked route currently reports `propext`, `Classical.choice`, and `Quot.sound`. Complete
transitive declaration, compiled-artifact, executable, axiom, and supply-chain acceptance remains
open.

### m0822-t-assemble

`composeRoot` consumes both `AttainmentPackage` and `UpperBoundPackage` as explicit premises and
yields `ExactAssembly`, which is definitionally the exact root target. It checks composition but
does not install either child.

### m0822-t-attainment

`attainment_of_starPackages` consumes the construction, intersection, sizing, and cardinality
packages to check the complete existential result. `attainment_of_localStar` supplies those packages
from target-owned bodies. The result remains candidate-only until proof-phase adoption and master
acceptance.

### m0822-c-star

`starConstruction_of_groundElement` consumes the range-derived ground element and returns the
canonical star, which filters the `r`-slice by membership of that center. It does not by itself
establish intersection, sizing, or cardinality.

### m0822-l-star-image

`erdosKoRadoStar_eq_image` gives the bijective representation obtained by inserting the center into
each `(r - 1)`-subset avoiding it. Erasure supplies the reverse direction.

### m0822-l-star-intersecting

Every two star members contain the center, so disjointness contradicts the two membership facts.

### m0822-l-star-sized

Membership in `powersetCard r univ` supplies cardinality `r` for every star member.

### m0822-l-star-card

`starCard_of_image` consumes the image representation and combines injectivity of insertion away
from the center with the powerset-slice cardinality formula to obtain `choose (n - 1) (r - 1)`.

### m0822-l-ground-element

The inequalities `1 <= r <= n / 2` imply `0 < n / 2` and hence `0 < n`; this constructs the center
`x : Fin n` used by the star.

### m0822-t-upper-adapter

`upperBound_of_mathlibTerminal` only transports binder order from the literal terminal proposition
to `UpperBoundPackage`. The positive-rank premise is not needed by the more general mathlib theorem.

### m0822-t-mathlib-ekr

`Finset.erdos_ko_rado` is the pinned terminal body for the upper-bound conjunct. The wrapper
`pinnedMathlibUpperBound` is deduplicated to that body. Current evidence is below release-grade E1,
so this remains M3 candidate evidence rather than accepted M0-W.

### m0822-b-rzero

The imported terminal first handles `r = 0`: an intersecting zero-uniform family cannot contain the
empty set and is therefore empty. This is an explanation of the pinned body, not separate proof
credit for the positive-rank root.

### m0822-c-complements

In the positive branch, the body constructs the family of complements and its `(n - 2r)`-fold
iterated shadow. This imported construction remains a deduplicated source-body overlay.

### m0822-l-shadow-disjoint

An original member cannot lie in the iterated shadow of a complement: that would place it inside
the complement of another original member and contradict intersection.

### m0822-l-complement-card

Complementation preserves family cardinality. Binomial symmetry rewrites the assumed strict excess
as the lower-bound premise for the complement family's shadow.

### m0822-l-complement-sized

Complements of `r`-subsets of `Fin n` have size `n - r`, so the complement family is uniformly
sized for the Kruskal-Katona invocation.

### m0822-l-kk-lovasz

`kruskal_katona_lovasz_form` lower-bounds the selected iterated shadow by
`choose (n - 1) r`. This deep theorem is a named bridge, not treated as a primitive citation.

### m0822-l-binomial-contradiction

The alleged strict excess plus the shadow lower bound and the binomial recurrence imply that the
disjoint union has more than `choose n r` members.

### m0822-l-slice-card

The union remains `r`-uniform, so `Set.Sized.card_le` bounds it by the total number of `r`-subsets,
contradicting the previous strict inequality.

### m0822-x-source

The 1961 paper supports H1, but a complete node-level proof and assumption crosswalk, correction and
errata disposition, and independent source review remain open.

### m0822-x-provenance

The target-owned star bodies and pinned upper-bound body have distinct terminal identities.
Wrappers, Atlas's wrapper, and source-body presentation nodes are deduplicated. Full transitive
content-addressed provenance remains downstream.

### m0822-x-trust

Warm node-local elaboration is not release-grade trust evidence. Cold offline replay, artifact and
executable identities, complete axiom/unsafe/oracle closure, SBOM, and supply-chain review remain
open.

### m0822-x-readable

This architecture is an R4 proof plan, not an independently reviewed R0 reconstruction. Each
substantive imported bridge still needs a complete reader route and formal/source mapping.

### m0822-x-workflow

The predecessor receipts and this packet remain provisional. Proof adoption, validation,
independent verification, release, freshness, revocation, and master acceptance cannot act as proof
premises.

## Freeze boundary

The frozen metric surfaces report all 27 inventory IDs as classified, zero accepted required
machine leaves, terminal bodies, interfaces, H0 nodes, or R0 nodes, and an open root and critical
path. The eight imported presentation nodes share one pinned terminal-body identity; adding wrappers,
aliases, or presentation splits therefore cannot change an accepted numerator.

`ObligationTree.lean` elaborates eight conditional/candidate declarations, including six distinct
abstract-child composition certificates. The concrete local and pinned candidates are checked
without recording accepted closure; the accepted obligation set is empty and the root remains
`[H1, M3, R4]`. No H0, accepted M0, R0, `AUDIT-Z`, theorem completion, release, or master acceptance
is claimed.
