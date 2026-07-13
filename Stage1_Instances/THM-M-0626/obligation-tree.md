# THM-M-0626 frozen obligation architecture

Item: `S56-M-0626-OBLIGATION_TREE`.

Registry version 1 freezes 22 semantic obligations before proof-phase installation. Eligibility,
risk, and the denominator are derived from the exact connected-image claim and its open-set
pullback architecture, not from the audited candidate's availability. Any target correction,
split, merge, exclusion, risk change, or proof-body identity change requires registry version 2
and an append-only delta.

## Typed proof route

```text
M0626-ROOT [open H1/M3/R4]
`-- M0626-T-ASSEMBLE [checked conditional composition]
    |-- M0626-S-GLOBAL-LOCAL [checked narrow Continuous -> ContinuousOn transport]
    `-- M0626-A-ISCONNECTED-IMAGE [candidate-only IsConnected.image interface]

Deduplicated local body reconstruction (refinement route, not a second mandatory anchor child):

M0626-T-LOCAL-COMPOSE [checked conditional body reconstruction]
|-- M0626-L-IMAGE-NONEMPTY
`-- M0626-L-IMAGE-PRECONNECTED
    `-- M0626-N-SEPARATION-GOAL [checked conditional reduction]
        |-- M0626-C-RELATIVE-PREIMAGES
        |-- M0626-N-IMAGE-COVER-TO-SOURCE
        |-- M0626-N-WITNESS-PULLBACK
        |-- M0626-L-SOURCE-INTERSECTION
        `-- M0626-T-INTERSECTION-PUSHFORWARD
```

The six lowest nodes are explicit open packages. Their mathematical sequencing and shared use of
the relative-preimage construction are recorded in the refinement graph, while the reconstruction
proof graph is flattened to match the exact five-premise Lean composition certificate. The direct
pinned anchor and reconstructed local body are alternative, deduplicated routes: installing the
anchor does not falsely require reproving its internals. No visual source-code nesting is mistaken
for a checked parent composition.

## Node ledger

### m0626-root

The exact frozen global-continuity proposition, expression SHA-256
`5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231`.
It remains open `H1/M3/R4` with no accepted proof state.

### m0626-s-interface

The exact universes, carrier types, topology instances, subset, connectedness hypothesis, total
map, global continuity hypothesis, and direct-image conclusion. No separation axiom or injectivity
premise is introduced.

### m0626-s-connectedness

The checked expansion fixes `IsConnected s` as `s.Nonempty` together with `IsPreconnected s` on
both sides. This is a statement overlay and cannot earn duplicate proof credit.

### m0626-s-boundary

The empty source is excluded by ordinary connectedness. Singleton sources, constant and
noninjective maps, and arbitrary non-Hausdorff spaces remain included. These are statement
boundaries, not proof branches.

### m0626-s-global-local

The narrow package maps each global `Continuous f` premise to `ContinuousOn f s`. The Lean harness
checks this direction through `Continuous.continuousOn`; it claims no converse.

### m0626-s-foundation

This node owns the eventual accepted axiom, foundation, computation, direct-import, compiled
artifact, and transitive TCB report. The current candidate reports `propext`, `Classical.choice`,
and `Quot.sound`; release-grade closure remains open.

### m0626-n-image-cover-to-source

Given the two relative-preimage identities, rewrite `f '' s ⊆ u ∪ v` into
`s ⊆ u' ∪ v'` using `Set.image_subset_iff`, `Set.preimage_union`, and set identities.

### m0626-n-separation-goal

Unfold image preconnectedness into the arbitrary-open eliminator: open `u` and `v`, an image
cover, and nonempty image intersections must produce an image intersection witness. This is a
reduction, not a case split; the mandatory branch layer is provisionally not applicable.

### m0626-c-relative-preimages

Use `continuousOn_iff'` twice to construct source-open representatives `u'` and `v'` whose
intersections with `s` agree with the relative preimages of `u` and `v`.

### m0626-n-witness-pullback

Destructure the two image-intersection witnesses and rewrite them through the relative-preimage
identities to obtain witnesses in `s ∩ u'` and `s ∩ v'`.

### m0626-l-source-intersection

Apply the supplied `IsPreconnected s` eliminator to the source-open representatives, source cover,
and pulled-back witnesses. The output is a witness in `s ∩ (u' ∩ v')`.

### m0626-t-intersection-pushforward

Rewrite the source overlap through both relative-preimage identities and send its witness through
`f`, producing a point of `f '' s ∩ (u ∩ v)`.

### m0626-l-image-preconnected

Re-abstract the checked separation engine as `IsPreconnected (f '' s)`. This is the substantive
body of pinned `IsPreconnected.image`, not an independent wrapper proof.

### m0626-l-image-nonempty

Map a source witness through `f` using `Set.image_nonempty.mpr` after extracting it with
`IsConnected.nonempty`.

### m0626-a-isconnected-image

The exact `ContinuousOn` interface of pinned `IsConnected.image`. Its source body pairs the two
reconstruction outputs, but those nodes form a deduplicated alternative route rather than mandatory
children of the imported candidate. Its accepted node debt remains `M3`; a separate field records
the provisional `M0-W` candidate classification. No proof-phase installation or accepted credit
occurs here.

### m0626-t-local-compose

`localConnectedImage_of_components` conditionally reconstructs the terminal body's two branches.
It shares the candidate's semantic conclusion and is explicitly deduplicated from the imported
body in unique-body and coverage metrics.

### m0626-t-assemble

`exactAssembly_of_packages` consumes the narrow global-to-local transport and local connected-image
package. `root_of_exactAssembly` checks that its output is the complete canonical root, not a
weaker local theorem.

All worker-checked interfaces retain accepted machine debt `M3`; their separate candidate fields
record worker-local `M0-L` potential pending master acceptance. No `M0-*` node status is asserted
by this architecture packet.

### m0626-x-source

Pinpoint primary-source identity, assumptions, proof-step mapping, errata, and independent review
remain open. The modern Stacks Project source lead does not yet establish `H0`.

### m0626-x-provenance

The terminal declaration/body graph, source slices, import closure, revisions, licenses, and
duplicate wrapper identities remain release-open. This support node grants no proof credit.

### m0626-x-trust

Transitive declarations, compiled artifacts, axioms, TCB, unsafe/oracle boundaries, supply chain,
and replay remain open despite the direct candidate audit.

### m0626-x-readable

A complete independently reviewed reader-facing reconstruction remains open. This architecture
ledger is not `R0`.

### m0626-x-workflow

Proof installation, validation, independent verification, release, freshness, and revocation
receipts remain downstream and cannot be replaced by this worker packet.

## Freeze boundary

`typed-graphs.json` keeps proof, refinement, provenance, evidence, trust, documentation, and
workflow edges separate. The workflow graph snapshots the seven authoritative task nodes and their
dependency chain. All proof nonleaves have exact conditional Lean certificates, but every
substantive leaf remains an explicit premise and no obligation is accepted closed. The immediate
machine proof cut is `M0626-A-ISCONNECTED-IMAGE`; the registry separately exposes the six open
reconstruction leaves so the cut does not imply their closure. The theorem-completion cut additionally
includes source, foundation/TCB, provenance, readability, and workflow gates. Primary-source H0,
foundation/TCB acceptance,
provenance, readable R0, proof installation, hermetic replay, independent validation, `AUDIT-Z`,
and theorem completion remain open.

The node validation recipes are structural: their `covered_declarations` lists are deliberately
empty. The separate scoped Lean command recorded in the receipt is the only kernel evidence for
the conditional composition declarations in this phase; downstream validation must not infer
kernel coverage from a structural Python recipe.
