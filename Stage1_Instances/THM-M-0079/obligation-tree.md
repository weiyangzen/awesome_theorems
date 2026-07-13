# THM-M-0079 frozen obligation architecture

## Freeze boundary

Registry `THM-M-0079-OBLIGATIONS-v1` freezes 39 obligations against the exact elaborated
`NielsenSchreierTarget` and the immutable anchor inventory. The machine denominator has 28 required
records: 27 mathematical proof nodes and the separate foundation certificate. The direct
`subgroupIsFreeOfIsFree` candidate is an informational bridge and cannot duplicate credit for its
action-groupoid, spanning-tree, end-equivalence, and freeness-transport bodies.

Any statement, eligibility, split, merge, risk, exclusion, or terminal-body change requires a new
registry version and append-only delta. No closure status was used to choose this denominator.
Recorded step budgets are architecture split thresholds, not verified logical-step counts; the
later R0 phase must supply substantive independently reviewed ledgers without changing this tree.

## Typed proof route

```text
M0079-ROOT
`-- M0079-T-ASSEMBLE
    |-- M0079-N-QUOTIENT-END-FREE
    |   |-- M0079-C-ACTION-CONNECTED
    |   |   |-- M0079-L-QUOTIENT-PRETRANSITIVE
    |   |   `-- M0079-C-QUOTIENT-NONEMPTY
    |   |-- M0079-C-ACTION-GROUPOID-FREE
    |   |   |-- M0079-C-ACTION-GENERATORS
    |   |   |-- M0079-C-SEMIDIRECT-LABELLING
    |   |   |-- M0079-L-AMBIENT-UNIQUE-LIFT
    |   |   |-- M0079-C-CURRY-UNCURRY
    |   |   `-- M0079-L-FUNCTOR-UNIQUENESS
    |   `-- M0079-L-CONNECTED-END-FREE
    |       |-- M0079-C-GEODESIC-TREE
    |       |   `-- M0079-C-ROOTED-CONNECTED
    |       |       |-- M0079-L-HOM-PATH
    |       |       |-- M0079-C-ACTION-CONNECTED
    |       |       `-- M0079-C-ACTION-GROUPOID-FREE
    |       |-- M0079-L-GEODESIC-ARBORESCENCE
    |       |   `-- M0079-C-ROOTED-CONNECTED
    |       |       |-- M0079-L-HOM-PATH
    |       |       |-- M0079-C-ACTION-CONNECTED
    |       |       `-- M0079-C-ACTION-GROUPOID-FREE
    |       `-- M0079-L-SPANNING-END-FREE
    |           |-- M0079-L-TREE-EDGE-IDENTITY
    |           |   `-- M0079-C-TREE-LOOPS
    |           |       `-- M0079-C-TREE-PATHS
    |           |-- M0079-C-FUNCTOR-END-HOM
    |           |   `-- M0079-C-TREE-LOOPS
    |           `-- M0079-C-COMPLEMENT-GENERATORS
    |-- M0079-C-END-SUBGROUP-EQUIV
    |   |-- M0079-C-STABILIZER-END
    |   `-- M0079-L-QUOTIENT-STABILIZER
    `-- M0079-T-MULEQUIV-FREENESS
```

The proof graph stores every arrow twice: parent-to-child `proof_requires` and reciprocal
child-to-parent `composes`. The refinement graph separately stores the statement overlays and the
checked literal-carrier and basis-existence equivalences. Provenance, evidence, trust,
documentation, and workflow relations do not grant proof closure.

## Node ledger

### m0079-root

Exact universe-polymorphic claim: every subgroup of a group carrying an `IsFreeGroup` basis is
free. It has the expression fingerprint `bb109f77...a553` and consumes only exact assembly.

### m0079-s-exact

Freezes the binder-complete `NielsenSchreierTarget`; it is informational because it shares the
root's semantic identity.

### m0079-s-domain

Owns the universe, `Group G`, `IsFreeGroup G`, inherited subgroup group, and same-universe basis
contract.

### m0079-s-boundary

Includes bottom, top, trivial ambient, and infinite-rank subgroup instances. The route is uniform,
so the no-branch decision remains pending independent approval.

### m0079-s-literal-transport

The checked theorem `nielsenSchreierTarget_iff_literalFreeGroupTarget` relates the generic and
literal `FreeGroup X` formulations without duplicate proof credit.

### m0079-s-basis-transport

The checked theorem `nielsenSchreierTarget_iff_basisExistenceTarget` expands subgroup freeness to
existence of a `FreeGroupBasis`.

### m0079-s-foundation

Required assurance frontier node for the eventual transitive `propext`, `Classical.choice`, `Quot.sound`,
kernel, TCB, and symbolic-computation decision. It is not a mathematical proof premise.

### m0079-l-quotient-pretransitive

`MulAction.isPretransitive_quotient` supplies transitivity of the left action of `G` on `G/H`.

### m0079-c-quotient-nonempty

The identity coset supplies a nonempty quotient carrier.

### m0079-c-action-connected

Combines quotient pretransitivity and nonemptiness with the generic connectedness instance for the
action groupoid. The bundled local composition interface consumes the modeled children.

### m0079-c-action-generators

Owns the generating quiver and interpretation of ambient free generators as action-groupoid
morphisms inside `actionGroupoidIsFree`.

### m0079-c-semidirect-labelling

Owns the semidirect-product encoding used to label ambient free generators.

### m0079-l-ambient-unique-lift

Uses `IsFreeGroup.unique_lift` for existence and uniqueness of the homomorphism extending those
labels.

### m0079-c-curry-uncurry

Owns conversion between the semidirect homomorphism and an action-groupoid functor, including the
projection compatibility.

### m0079-l-functor-uniqueness

Owns equality of the lifted functor from curry equality and functor extensionality.

### m0079-c-action-groupoid-free

Assembles the preceding five semantic children into `IsFreeGroupoid (ActionCategory G A)`. Its
source body is shared by all five internal nodes, preventing body-count inflation.

### m0079-l-hom-path

`IsFreeGroupoid.path_nonempty_of_hom` converts a groupoid morphism into a path in the generating
quiver.

### m0079-c-rooted-connected

`IsFreeGroupoid.generators_connected` uses the hom-to-path engine in a connected free-groupoid
context to root the generating quiver.

### m0079-c-geodesic-tree

Chooses `Quiver.geodesicSubtree` at the selected root.

### m0079-l-geodesic-arborescence

Separately owns `Quiver.geodesicArborescence`, the invariant required to use the chosen subtree as
a spanning tree.

### m0079-c-tree-paths

`homOfPath` and `treeHom` turn unique tree paths into canonical root-to-vertex morphisms.

### m0079-c-tree-loops

`loopOfHom` conjugates arbitrary arrows along the tree paths to obtain loops at the root.

### m0079-l-tree-edge-identity

`loopOfHom_eq_id` proves that generator edges lying in the tree contribute the identity loop.

### m0079-c-functor-end-hom

`functorOfMonoidHom` extends a homomorphism on the root end group to a functor on the whole
groupoid.

### m0079-c-complement-generators

The complement of the spanning tree supplies the generator family and universal-property
labelling for the root end group.

### m0079-l-spanning-end-free

`IsFreeGroupoid.SpanningTree.endIsFree` assembles tree loops, the identity lemma, functor extension,
and complement generators into freeness of the root end group.

### m0079-l-connected-end-free

`IsFreeGroupoid.endIsFreeOfConnectedFree` chooses the geodesic spanning tree and applies the
spanning-tree result to any vertex of a connected free groupoid.

### m0079-n-quotient-end-free

The local `quotientVertexEndFree_of_components` specializes the generic result to the identity
coset, consuming action-groupoid freeness, quotient-action connectedness, and connected end
freeness.

### m0079-c-stabilizer-end

`ActionCategory.stabilizerIsoEnd` identifies the action stabilizer with the vertex end group.

### m0079-l-quotient-stabilizer

`MulAction.stabilizer_quotient` identifies the stabilizer of the identity coset with `H`.

### m0079-c-end-subgroup-equiv

`ActionCategory.endMulEquivSubgroup` composes the two identifications to produce
`End(identity coset) ≃* H`.

### m0079-t-mulequiv-freeness

`IsFreeGroup.ofMulEquiv` transports the free basis from the end group to the subgroup.

### m0079-t-assemble

`exactAssembly_of_end_packages` consumes the specialized end freeness, exact equivalence, and
transport interface to return the binder-complete root proposition.

### m0079-a-direct

`subgroupIsFreeOfIsFree` is the exact pinned `M0-W` candidate for the proof phase. It is a
deduplicated bridge, not accepted closure in this phase.

### m0079-x-source

Owns primary-source, definition, assumption, correction, and node-crosswalk work. Current H1 means
that an H0 packet and independent review remain open.

### m0079-x-provenance

Owns declaration/body/revision/source/license traversal. Every known body-bearing node maps here;
internal source regions share their enclosing terminal body identity.

### m0079-x-trust

Owns transitive axiom, compiled-artifact, executable, TCB, and supply-chain closure.

### m0079-x-documentation

Provides stable anchors for all nodes. This architecture ledger is not an independently reviewed
R0 reconstruction.

### m0079-x-workflow

Binds every obligation reciprocally to the authoritative task graph and preserves dependency,
freshness, invalidation, and revocation ordering.

## Composition boundary

Five graph-parent interfaces elaborate: quotient-action connectedness, end/subgroup equivalence,
quotient-end specialization, terminal assembly, and exact root identity. Nine deeper source parents
retain explicit planned child-to-parent harness status. The exact root has an elaborated-expression
fingerprint; non-root nodes have frozen planned-signature hashes, not elaborated Lean fingerprints.
The five local interfaces also carry explicit Lean type ascriptions. Imported declarations are
provenance anchors, not accepted composition receipts.

The mathematical architecture frontier has 13 nodes, and `M0079-S-FOUNDATION` is the separate
required machine-assurance frontier node. These are not claims that Blueprint section 6.6's
substantive leaf ledgers or verified step budgets are complete. Accepted closed obligations and
receipt IDs are empty. The root remains
`[H1, M3, R4]`; proof integration, H0, R0, full provenance/trust, hermetic and independent
validation, `AUDIT-Z`, `THEOREM-Z`, release, and master acceptance remain open.
