# THM-M-0028 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 25 canonical obligations against the exact `Statement.lean` target and
the audited terminal-body inventory. The denominator was derived before candidate status was
attached. No obligation is accepted closed, and the root remains `[H1, M3, R3]`.

The local audit adapter and the two Atlas wrappers are presentation packages, not additional
proof bodies. They reduce to the distinct pinned `isNoetherianRing_iff_ideal_fg` and
`monotone_stabilizes_iff_noetherian` bodies and receive no duplicate coverage.

## Typed proof route

```text
M0028-ROOT
`-- M0028-T-ROOT-COMPOSE
    |-- M0028-B-FG-NOETHERIAN
    |   `-- M0028-X-FG-BODY
    |       |-- M0028-N-RING-REGULAR
    |       `-- M0028-D-NOETHERIAN-CLASS
    `-- M0028-B-NOETHERIAN-CHAIN
        `-- M0028-N-CHAIN-IFF
            `-- M0028-X-CHAIN-BODY
                |-- M0028-N-NOETHERIAN-WF
                |   |-- M0028-L-FG-COMPACT
                |   `-- M0028-C-LATTICE-WF
                `-- M0028-L-WF-CHAIN
                    |-- M0028-L-PREORDER-CHAIN
                    `-- M0028-L-PARTIAL-EQUALITY
```

The three `proof_requires` arcs have reciprocal `composes` arcs and are backed by two exact
conditional Lean declarations. Internal pinned-body relations remain open
`logical_decomposition` edges until later proof work supplies checked composition harnesses.
Provenance, evidence, trust, documentation, and workflow graphs are separate and carry no proof
credit.

<a id="m0028-root"></a>
## M0028-ROOT

This is the exact universe-polymorphic proposition in `Statement.lean`: for any unital
commutative ring, finite generation of every ideal implies eventual equality of every ascending
Nat-indexed ideal chain. Its only proof child is the terminal bridge package.

<a id="m0028-s-interface"></a>
## M0028-S-INTERFACE

This node preserves the `CommRing` binder, every-ideal-FG premise, `Nat ->o Ideal R` chain, and
tail equality conclusion. It excludes no zero ring and introduces no domain, field,
characteristic, countability, or carrier-finiteness premise.

<a id="m0028-s-regular-transport"></a>
## M0028-S-REGULAR-TRANSPORT

This definitional checked iff identifies ideals with regular submodules. It transports the carrier
but does not own another ascending-chain proof.

<a id="m0028-s-monotone-transport"></a>
## M0028-S-MONOTONE-TRANSPORT

This checked iff identifies OrderHom chains with functions carrying an explicit monotonicity
proof. Its proof body is distinct from the definitional regular-submodule transport.

<a id="m0028-s-zero-ring"></a>
## M0028-S-ZERO-RING

The subsingleton boundary theorem and `PUnit` probe keep the zero ring in scope. Adding
`Nontrivial R` is a distinct mutation, not a harmless elaboration choice.

<a id="m0028-s-foundation"></a>
## M0028-S-FOUNDATION

The candidate reports `propext`, `Classical.choice`, and `Quot.sound`. Acceptance of those
principles, the kernel and compiled artifacts, complete transitive dependencies, and the no-oracle
policy remains an open release gate.

<a id="m0028-t-root-compose"></a>
## M0028-T-ROOT-COMPOSE

`bridgePackage_of_bridges` consumes both exact bridge propositions and returns their conjunction.
`root_of_bridgePackage` consumes that conjunction and yields the canonical target. These checks
prove composition only; they do not supply either bridge premise.

<a id="m0028-b-fg-noetherian"></a>
## M0028-B-FG-NOETHERIAN

This exact interface converts the target's premise, finite generation of every ideal of `R`, into
`IsNoetherianRing R`. It is a proof-phase cut until the pinned body is installed and accepted.

<a id="m0028-b-noetherian-chain"></a>
## M0028-B-NOETHERIAN-CHAIN

This exact interface converts `IsNoetherianRing R` into stabilization of every ideal OrderHom
chain. It is distinct from the finite-generation bridge and depends on the separate terminal body
owned by `M0028-X-CHAIN-BODY`.

<a id="m0028-x-fg-body"></a>
## M0028-X-FG-BODY

The pinned `isNoetherianRing_iff_ideal_fg` body is
`isNoetherianRing_iff.trans isNoetherian_def`. It is an audited `M0-W/E2` candidate, not installed
or master-accepted proof state.

<a id="m0028-x-chain-body"></a>
## M0028-X-CHAIN-BODY

The pinned `monotone_stabilizes_iff_noetherian` body rewrites by `isNoetherian_iff'` and
`wellFoundedGT_iff_monotone_chain_condition`. It remains candidate evidence until the proof and
validation phases close its full boundary.

<a id="m0028-n-ring-regular"></a>
## M0028-N-RING-REGULAR

`IsNoetherianRing R` is Noetherianity of the regular module `R` over itself. This normalization
also aligns `Ideal R` definitionally with `Submodule R R`.

<a id="m0028-d-noetherian-class"></a>
## M0028-D-NOETHERIAN-CLASS

`isNoetherian_def` packages or projects the class field saying that every submodule is finitely
generated. Under the regular-module identification, those submodules are exactly ideals.

<a id="m0028-n-chain-iff"></a>
## M0028-N-CHAIN-IFF

The generic module chain theorem is specialized to the regular module. Its proof is split into
the Noetherian-to-well-founded and well-founded-to-eventual-equality packages below.

<a id="m0028-n-noetherian-wf"></a>
## M0028-N-NOETHERIAN-WF

`isNoetherian_iff'` identifies finite generation of every submodule with well-founded strict
descent in the complete submodule lattice. Its two material dependencies are explicit nodes.

<a id="m0028-l-fg-compact"></a>
## M0028-L-FG-COMPACT

`Submodule.fg_iff_compact` equates finite generation with compactness. Its visible proof expands a
finite span into a finite supremum and conversely extracts finitely many singleton spans from
compactness; it is not treated as a routine primitive.

<a id="m0028-c-lattice-wf"></a>
## M0028-C-LATTICE-WF

`CompleteLattice.wellFoundedGT_characterisations` relates well-founded strict descent to compact
generation properties of the complete lattice. It supplies the lattice engine used by
`isNoetherian_iff'`.

<a id="m0028-l-wf-chain"></a>
## M0028-L-WF-CHAIN

`wellFoundedGT_iff_monotone_chain_condition` upgrades the generic preorder condition to eventual
equality in a partial order. The preorder construction and equality conversion are kept separate.

<a id="m0028-l-preorder-chain"></a>
## M0028-L-PREORDER-CHAIN

The forward direction takes a well-founded minimum in the sequence range and rules out later
strict growth. The converse transforms an infinite strict descent into a monotone Nat sequence and
contradicts the no-strict-growth tail.

<a id="m0028-l-partial-equality"></a>
## M0028-L-PARTIAL-EQUALITY

For a later index `m`, monotonicity gives `a n <= a m`; rewriting strict order as
`<=` plus inequality converts the absence of strict growth into `a n = a m`. This is the precise
partial-order step behind eventual equality.

<a id="m0028-x-source"></a>
## M0028-X-SOURCE

The source status remains `H1`. Complete translation of Noether's nonunital setting to the modern
unital target, premise and proof-node crosswalks, errata work, and independent review are open.

<a id="m0028-x-provenance"></a>
## M0028-X-PROVENANCE

Pinned source blobs, terminal declarations, body text, authorship lineage, and the external Atlas
corroboration are inventoried. Complete transitive declaration and artifact provenance remains a
later gate.

<a id="m0028-x-trust"></a>
## M0028-X-TRUST

The phase uses the existing pinned shared cache as warm evidence. Cold offline replay, executable
and compiled-artifact identities, supply-chain closure, and independent verification remain open.

<a id="m0028-x-readable"></a>
## M0028-X-READABLE

This architecture ledger is not an independently reviewed mathematical proof reconstruction.
Short and long reader routes with node-specific primary-source mapping remain required for `R0`.

<a id="m0028-x-workflow"></a>
## M0028-X-WORKFLOW

This node binds proof installation, composition, validation, freshness, revocation, independent
verification, and release receipts. Workflow order cannot act as a mathematical premise.

## Status boundary

The frozen registry, typed graphs, and conditional compositions are self-tested worker artifacts
pending master acceptance. No proof is installed, no obligation is accepted closed, and no `H0`,
accepted `M0`, `R0`, complete trust/provenance, audit completion, theorem completion, release, or
master acceptance is claimed.
