# THM-M-0856 frozen obligation architecture

Item: `S56-M-0856-OBLIGATION_TREE`.

Registry version 1 freezes 56 canonical obligations before proof-phase closure credit.
The proof route follows the actual pinned `SimpleGraph.tutte` body through necessity, parity,
the maximal matching-free supergraph, universal-vertex clique and nonclique branches, the
near-matching symmetric-difference construction, and the exact local adapter. Source,
provenance, evidence, trust, documentation, and workflow edges are separately typed.

## Composition boundary

`ObligationTree.lean` checks only the root composition from the exact terminal adapter and
literal pinned terminal. Every internal source-body relation is recorded as an unverified
decomposition plan until an exact child-fingerprint composition harness is accepted. The
pinned candidate therefore remains M3/below E1 here, and no obligation is accepted closed.

## Proof route

```text
ROOT -> exact adapter + SimpleGraph.tutte
  necessity -> odd-component matched exits -> injection -> cardinal bound
  sufficiency by contraposition -> parity split
    odd order -> empty-set violator
    even order -> maximal matching-free supergraph -> universal-vertex deletion
      all residual components cliques -> representative/universal/internal matchings
      a residual component nonclique -> two near-matchings
        symmetric-difference cycles -> avoid/contain x branches -> alternating toggle
```

## Node ledger

### m0856-root

Every finite simple graph has a perfect matching exactly when every vertex deletion leaves at most as many odd components as deleted vertices.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `Stage1Instances.THM_M_0856.TutteOneFactorTarget`.

Formal target fingerprint: `sha256:ba4ff4695a846a4a0acbf1b08976c83039fb2ba111d42b8bdf561276cf26579d`.

Source locator: `Statement.lean; expression sha256 5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae`.

Required premises: `M0856-T-ADAPTER, M0856-T-UPSTREAM`.

Inference: Apply the checked terminal adapter to the pinned no-violator terminal without changing any binder, domain, or boundary case.

Output: The exact canonical universe-polymorphic proposition.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-s-target

Freeze the exact finite-simple-graph target and its expression fingerprint.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `Stage1Instances.THM_M_0856.TutteOneFactorTarget`.

Formal target fingerprint: `sha256:ba4ff4695a846a4a0acbf1b08976c83039fb2ba111d42b8bdf561276cf26579d`.

Source locator: `Statement.lean:27-31; statement.json canonical_formal_target`.

Required premises: `frozen-formal-context`.

Inference: Read the elaborated proposition and preserve its universe, graph, finiteness, existential matching, and universal deletion binders.

Output: The canonical target interface, counted only once at the root.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-s-domain

Fix V : Type u, G : SimpleGraph V, and [Finite V] with no connectedness, decidability, Fintype, or nonemptiness premise.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (G : SimpleGraph V), [Finite V] -> True`.

Formal target fingerprint: `sha256:cd0465ad2a37d1691a9bcf82982f4390a5a4a22e9a8c6d5b5988613fc2001cc8`.

Source locator: `Statement.lean:28-31; statement.json ordered_binders`.

Required premises: `frozen-formal-context`.

Inference: Propagate the original binder order and infer only local instances derivable from [Finite V].

Output: The exact domain and typeclass context used by every proof node.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-s-matching

Use a spanning matching subgraph as the perfect-matching witness.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (G : SimpleGraph V), (Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> (Exists fun M : G.Subgraph => M.IsPerfectMatching)`.

Formal target fingerprint: `sha256:db3540094abeeaca88a40d39444c9ae63379d5696747b377ab3f22d20eb1de01`.

Source locator: `Statement.lean:31; Mathlib/Combinatorics/SimpleGraph/Matching.lean`.

Required premises: `frozen-formal-context`.

Inference: Freeze the existential subgraph representation and its spanning and matching fields without asserting that every graph has such a witness; do not substitute an edge set or involution.

Output: A non-claiming interface identity that freezes the left side as `Exists fun M : G.Subgraph => M.IsPerfectMatching`.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-s-odd-condition

Count odd connected components of the induced graph after deleting an arbitrary vertex set U.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `Stage1Instances.THM_M_0856.OddComponentCondition`.

Formal target fingerprint: `sha256:3b6c1673c5c6b5e01b62f31b80d7933333d7983fa0c0b0690cd63c9ad15d78a8`.

Source locator: `Statement.lean:18-25`.

Required premises: `frozen-formal-context`.

Inference: Expand deleteVerts, oddComponents, and ncard only through the frozen definitions, retaining every U : Set V.

Output: The right side of the canonical equivalence.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-s-boundary

Retain empty carriers, odd carriers, isolated vertices, disconnected graphs, and empty or full deletion sets.

Formal target kind: `nonformal_record`.

Formal target/type/record: `statement.json#/degenerate_cases`.

Formal target fingerprint: `sha256:e06052732c07ec2fac0778d0a97d6337c39b30fde1548ef71b5697680fe193c2`.

Source locator: `statement.json degenerate_cases`.

Required premises: `frozen-formal-context`.

Inference: Check that each listed case remains admitted by the same target rather than being discharged by an added premise.

Output: No strengthened premise or omitted degenerate case.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-s-transport

Transport the deletion inequality to the absence of a strict IsTutteViolator in the direction used by mathlib.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `Stage1Instances.THM_M_0856.tutteOneFactorTarget_iff_noTutteViolatorTarget`.

Formal target fingerprint: `sha256:d8ea8421687617f5e362c776b34220f3944fefd10165fc20c81a003816894541`.

Source locator: `Statement.lean:46-57`.

Required premises: `frozen-formal-context`.

Inference: Unfold both violator predicates and use not_lt, preserving the complete Iff and all quantifiers.

Output: An exact checked bridge between canonical and pinned terminal interfaces.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-s-foundation

Account for propositional extensionality, classical choice, quotient soundness, Lean, mathlib, and the no-oracle computation policy.

Formal target kind: `nonformal_record`.

Formal target/type/record: `stage1-foundation-profile/1.0`.

Formal target fingerprint: `sha256:7e3193692b4f89ef8e391c9dc2675146277729ef483603d613158cdc9b1b45c9`.

Source locator: `anchor-audit.json immutable_environment and provenance_packet`.

Required premises: `frozen-formal-context`.

Inference: Compare machine-derived transitive dependencies with the selected foundation profile and reject any unknown trust path.

Output: A reviewed release-grade foundation and trust decision, not a theorem premise.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-n-finite-interfaces

Derive local Fintype and decidability interfaces from [Finite V] without adding a Nonempty V premise.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u}, [Finite V] -> Nonempty (Fintype V)`.

Formal target fingerprint: `sha256:911fd238a61084802bb295aae5bc4438cc2527c8840ace0a529a3073ccab0c34`.

Source locator: `Tutte.lean:126,272`.

Required premises: `frozen-formal-context`.

Inference: Obtain a local Fintype witness by classical choice and keep the empty carrier within the original [Finite V] context.

Output: Finite-cardinality APIs usable in the clique and maximal-graph branches.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-t-adapter

Convert the literal pinned no-violator theorem to the exact frozen inequality target.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter`.

Formal target fingerprint: `sha256:0954a4d4c5b9e79eeb1f3210c769e0437ae5ec84e2088395894abd237772afbd`.

Source locator: `ObligationTree.lean#terminal_adapter`.

Required premises: `frozen-formal-context`.

Inference: Simplify only the frozen target, odd-component condition, pinned violator predicate, and not_lt.

Output: MathlibTerminal implies TutteOneFactorTarget.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-t-upstream

Compose necessity and contraposed sufficiency into the pinned no-violator Iff.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `SimpleGraph.tutte`.

Formal target fingerprint: `sha256:49c6ef2ce7d08327c0e6ec61b8ae36983aa132ceedfc962a1315d2d05cc803a5`.

Source locator: `Tutte.lean:310-322`.

Required premises: `M0856-T-NECESSITY, M0856-T-SUFFICIENCY`.

Inference: Use the necessity declaration for the forward direction, then contrapose the reverse direction and split the finite carrier by parity.

Output: The literal MathlibTerminal proposition.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-t-necessity

A perfect matching prevents every vertex set from being a Tutte violator.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `SimpleGraph.not_isTutteViolator_of_isPerfectMatching`.

Formal target fingerprint: `sha256:e7445574cbdb037348a179caae13bc6f277b4ea005c651a6cc906937011f085b`.

Source locator: `Tutte.lean:140-149`.

Required premises: `M0856-L-ODD-MATCHES-OUTSIDE, M0856-C-ODD-TO-U-INJECTION, M0856-L-NCARD-INJECTION`.

Inference: Choose a matched exit from every odd component, prove the exit map injective, and compare finite cardinalities.

Output: For all U, not G.IsTutteViolator U.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-odd-matches-outside

Every odd component after deleting U has a matching edge to a vertex of U.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `ConnectedComponent.odd_matches_node_outside`.

Formal target fingerprint: `sha256:4fa3da578343dd88f14f894f3ff7fa43fcbb09136584d3b84f466b4379e9bd8d`.

Source locator: `Matching.lean:293-314`.

Required premises: `frozen-formal-context`.

Inference: Assume no matched exit, restrict the perfect matching to the component, derive even component cardinality, and contradict oddness.

Output: For each odd component, an incident matched vertex outside the deleted graph.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-odd-to-u-injection

Choose one supplied deleted endpoint for each odd component and construct an injection into U.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} [Finite V] {M : G.Subgraph} (hM : M.IsPerfectMatching) (U : Set V), (forall c : ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents, exists w, w ∈ U /\ exists v : ((⊤ : G.Subgraph).deleteVerts U).verts, M.Adj v w /\ v ∈ c.val.supp) -> exists f : ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents -> U, Function.Injective f`.

Formal target fingerprint: `sha256:2cb54d954d61cb7b09c6044a036b080e7d47a117e67742dc546f6a5d1923c0ea`.

Source locator: `Tutte.lean:144-147`.

Required premises: `frozen-formal-context`.

Inference: Consume the odd-exit family supplied by L-ODD-MATCHES-OUTSIDE, choose endpoints, then use matching uniqueness and common-component membership to show equal images force equal components.

Output: An injective map from odd components to U, conditional on the exact odd-component exit family.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-ncard-injection

Convert the component injection into the canonical odd-component ncard inequality.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} [Finite V] (U : Set V), (exists f : ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents -> U, Function.Injective f) -> ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents.ncard <= U.ncard`.

Formal target fingerprint: `sha256:45b466ab6dbc9d23aafd32d54e31c622c10ec992e90dc79f1227c5207b212f49`.

Source locator: `Tutte.lean:148-149`.

Required premises: `frozen-formal-context`.

Inference: Apply cardinal monotonicity to the subtype injection and normalize subtype cardinalities to Set.ncard.

Output: oddComponents.ncard <= U.ncard.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-t-sufficiency

If no vertex set violates Tutte's condition, a perfect matching exists.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (G : SimpleGraph V) [Finite V], (forall U : Set V, Not (G.IsTutteViolator U)) -> Exists fun M : G.Subgraph => M.IsPerfectMatching`.

Formal target fingerprint: `sha256:9d7b3968e9bf9c955b30e54556235ecead6de0c6e424c84876db0f4f809f2387`.

Source locator: `Tutte.lean:317-322`.

Required premises: `M0856-B-PARITY-SPLIT`.

Inference: Contrapose perfect-matching existence, then construct a violator in the odd-cardinality or even-cardinality branch.

Output: The reverse implication of the pinned terminal Iff.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-parity-split

Split Nat.card V into odd and not-odd cases and recompose exhaustively.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (G : SimpleGraph V) [Finite V], (forall M : G.Subgraph, Not M.IsPerfectMatching) -> (Odd (Nat.card V) -> Exists fun U : Set V => G.IsTutteViolator U) -> (Even (Nat.card V) -> Exists fun U : Set V => G.IsTutteViolator U) -> Exists fun U : Set V => G.IsTutteViolator U`.

Formal target fingerprint: `sha256:d97f4035b490f317cbb65d9526bf00c1ec7a809463d2a7af41f04bfb58948bd4`.

Source locator: `Tutte.lean:320-322`.

Required premises: `M0856-B-ODD-CARD, M0856-B-EVEN-CARD`.

Inference: Use the odd branch directly; in the complement convert not-odd to even before invoking the even-order theorem.

Output: A Tutte violator under the assumption that every subgraph matching is imperfect.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-odd-card

On an odd-order carrier, the empty deletion set is a Tutte violator.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} [Finite V], Odd (Nat.card V) -> exists U : Set V, U = ∅ /\ G.IsTutteViolator U`.

Formal target fingerprint: `sha256:728ce0e2275a0a8c10df2905efb99ac642f13362b96fdcc313cdb47b7a4c63a7`.

Source locator: `Tutte.lean:136-138,320-321`.

Required premises: `M0856-L-EMPTY-VIOLATOR`.

Inference: Relate odd total vertex count to a positive odd-component count after deleting no vertices.

Output: Exists U, G.IsTutteViolator U with U = empty.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-empty-violator

Odd total order implies strictly more than zero odd components after empty deletion.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `SimpleGraph.IsTutteViolator.empty`.

Formal target fingerprint: `sha256:90c1cd87b5cf0c96dd3f980c27c47c57dde1d8396b83361f51359eda7359d042`.

Source locator: `Tutte.lean:136-138`.

Required premises: `frozen-formal-context`.

Inference: Rewrite the empty-set cardinality and use odd_ncard_oddComponents to obtain positivity.

Output: G.IsTutteViolator empty.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-even-card

On an even-order matching-free graph, construct a Tutte violator.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} [Finite V], Even (Nat.card V) -> (forall M : G.Subgraph, Not M.IsPerfectMatching) -> exists U : Set V, G.IsTutteViolator U`.

Formal target fingerprint: `sha256:1702775bf34c3b491beaae8af85f76278c7b8ea1dce8381910a9d30a871f8d75`.

Source locator: `Tutte.lean:264-308,322`.

Required premises: `M0856-L-EXISTS-VIOLATOR`.

Inference: Invoke the maximal matching-free supergraph argument with the derived even cardinality witness.

Output: Exists U, G.IsTutteViolator U.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-exists-violator

Every finite even-order matching-free graph has a Tutte violator.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `SimpleGraph.exists_isTutteViolator`.

Formal target fingerprint: `sha256:00da48f7e1768b4e595105e31df0e43dbc05cc5db664120c8873c68a45231930`.

Source locator: `Tutte.lean:264-308`.

Required premises: `M0856-N-FINITE-INTERFACES, M0856-C-MAXIMAL-MATCHING-FREE, M0856-L-VIOLATOR-MONO, M0856-C-UNIVERSAL-DELETION, M0856-B-CLIQUE-SPLIT`.

Inference: Pass to an edge-maximal matching-free supergraph, delete its universal vertices, and split on whether all remaining components are cliques.

Output: A vertex set whose deletion leaves too many odd components.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-maximal-matching-free

Extend G to an edge-maximal matching-free supergraph Gmax.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `SimpleGraph.exists_maximal_isMatchingFree`.

Formal target fingerprint: `sha256:9267f5eb8ddcf8f1402687e378ac2d6b786f61052d7662f5143dfd62ca2315bd`.

Source locator: `Matching.lean:335-340; Tutte.lean:274`.

Required premises: `frozen-formal-context`.

Inference: Apply finite maximality to the matching-free property and retain both inclusion and strict-extension witnesses.

Output: G <= Gmax, Gmax matching-free, and every strict supergraph has a perfect matching.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-violator-mono

A violator for a supergraph remains a violator for a subgraph on the same vertices.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `SimpleGraph.IsTutteViolator.mono`.

Formal target fingerprint: `sha256:b15e1fd1e3d4bea75bc8828592e83ec542465f43d5b01bf101fa4630962bcb3e`.

Source locator: `Tutte.lean:60-65`.

Required premises: `frozen-formal-context`.

Inference: Use monotonicity of odd-component counts under edge deletion and discharge the strict cardinal inequality.

Output: Gmax violator U implies G violator U when G <= Gmax.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-universal-deletion

Choose Gmax.universalVerts as the candidate deletion set and expose the remaining connected components.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (Gmax : SimpleGraph V), Gmax.deleteUniversalVerts = (⊤ : Gmax.Subgraph).deleteVerts Gmax.universalVerts`.

Formal target fingerprint: `sha256:3816e0dcc9523cd7e099771a1dad1cba4bf742dfaeaad57461683ef111f15afa`.

Source locator: `Tutte.lean:275-278; UniversalVerts.lean:20-45`.

Required premises: `frozen-formal-context`.

Inference: Use the exact deleteUniversalVerts definition, then expose its connected-component type without assuming that a component exists.

Output: The candidate deletion subgraph is definitionally the top subgraph with universal vertices removed.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-clique-split

Split whether every component after deleting universal vertices is a clique and recompose the two contradiction handlers.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (Gmax : SimpleGraph V) [Finite V], Gmax.IsMatchingFree -> Even (Nat.card V) -> (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Not (Gmax.IsTutteViolator Gmax.universalVerts) -> ((forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False) -> (Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False) -> False`.

Formal target fingerprint: `sha256:7a7d3356dc9284008954076fc57f71e699d03c9509b6ec52be098513e9ff45a3`.

Source locator: `Tutte.lean:278-308`.

Required premises: `M0856-B-ALL-CLIQUES, M0856-B-NONCLIQUE`.

Inference: Use classical case analysis on the componentwise clique predicate and invoke exactly the matching branch handler; neither child may be ignored.

Output: A contradiction from either exhaustive clique-status branch, with the maximal-graph context retained.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-all-cliques

If all deleted components are cliques and universalVerts is not a violator, derive a perfect matching of Gmax.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {Gmax : SimpleGraph V} [Finite V], Gmax.IsMatchingFree -> Even (Nat.card V) -> Not (Gmax.IsTutteViolator Gmax.universalVerts) -> (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False`.

Formal target fingerprint: `sha256:5bf1c31b962fe0ad319fd815d89f11c2539c9767d08c3551083a282d8c31625f`.

Source locator: `Tutte.lean:280-286`.

Required premises: `M0856-T-CLIQUE-PERFECT`.

Inference: Normalize the nonviolator cardinal bound and invoke the clique-support perfect-matching construction.

Output: A contradiction to Gmax being matching-free.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-t-clique-perfect

Build a perfect matching when universal-vertex deletion decomposes into cliques and the count bound holds.

Formal target kind: `exact_lean_type`.

Formal target/type/record: `SimpleGraph.Subgraph.IsPerfectMatching.exists_of_isClique_supp`.

Formal target fingerprint: `sha256:b7c70d3c35f6ea582461165ddd71f3bd092f4097c8139b68c287e38d5ed7b11e`.

Source locator: `Tutte.lean:118-134`.

Required premises: `M0856-N-FINITE-INTERFACES, M0856-C-NEAR-COVER-MATCHING, M0856-C-COMPLEMENT-MATCHING, M0856-C-SUP-PERFECT`.

Inference: Combine a near-covering matching with a matching on its uncovered universal-vertex complement.

Output: Exists M : Subgraph Gmax, M.IsPerfectMatching.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-near-cover-matching

Construct a matching covering every non-universal vertex and possibly leaving universal vertices uncovered.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (G : SimpleGraph V) [Finite V], Not (G.IsTutteViolator G.universalVerts) -> (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> exists M : G.Subgraph, M.IsMatching /\ M.vertsᶜ ⊆ G.universalVerts`.

Formal target fingerprint: `sha256:d918f2d721ac5690029ed1e0eee3d6b761ae2c9f61998f049c699b78b074a2e7`.

Source locator: `Tutte.lean:67-116`.

Required premises: `M0856-C-ODD-REPRESENTATIVES, M0856-C-MATCH-REPS-UNIVERSALS, M0856-C-INTERNAL-COMPONENT-MATCHINGS, M0856-C-ISUP-DISJOINT-MATCHING, M0856-L-UNCOVERED-SUBSET`.

Inference: Match odd-component representatives to universal vertices, match remaining component vertices internally, and take the disjoint supremum.

Output: M.IsMatching and M.verts complement subset universalVerts.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-odd-representatives

Choose one representative in each odd component and derive the disjointness and cardinal bound needed to match them to universal vertices.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (G : SimpleGraph V) [Finite V], Not (G.IsTutteViolator G.universalVerts) -> let reps : Set G.deleteUniversalVerts.verts := Quot.out '' G.deleteUniversalVerts.coe.oddComponents; ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents /\ reps.ncard = G.deleteUniversalVerts.coe.oddComponents.ncard /\ Disjoint G.universalVerts (Subtype.val '' reps) /\ (Subtype.val '' reps).ncard <= G.universalVerts.ncard`.

Formal target fingerprint: `sha256:eedef3bab4f130aecafc8edb8e6c6f88c39464276138265c20fe0609fb047ed7`.

Source locator: `Tutte.lean:79-84; Connectivity/Represents.lean:39-44,67-68; UniversalVerts.lean:59-62`.

Required premises: `frozen-formal-context`.

Inference: Use image_out and ncard_eq, lift representatives through Subtype.val, prove universal-vertex disjointness, and normalize the nonviolator inequality to the image ncard bound.

Output: A representative set with exact count, disjointness from universal vertices, and the nonviolator cardinal bound.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-match-reps-universals

Match odd-component representatives injectively to universal vertices using the derived nonviolator bound.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} [Finite V] {reps : Set G.deleteUniversalVerts.verts}, ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents -> Disjoint G.universalVerts (Subtype.val '' reps) -> (Subtype.val '' reps).ncard <= G.universalVerts.ncard -> exists t : Set V, t ⊆ G.universalVerts /\ exists M1 : G.Subgraph, M1.verts = Subtype.val '' reps ∪ t /\ M1.IsMatching`.

Formal target fingerprint: `sha256:00c3d5a831ed98b9d69e4e4813601c6eada788a56a4e9892ebbd7d9103e7a2fc`.

Source locator: `Tutte.lean:81-84; UniversalVerts.lean:48-58`.

Required premises: `frozen-formal-context`.

Inference: Apply exists_of_universalVerts to the derived disjointness and ncard bound, retaining t, its subset proof, the exact vertex equation, and matching property for downstream parity.

Output: A selected universal set t and matching M1 whose vertices are exactly the representatives and t.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-internal-component-matchings

For each deleted component, derive evenness of the unused vertices and match them inside its clique.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} [Finite V] {reps : Set G.deleteUniversalVerts.verts} {t : Set V} {M1 : G.Subgraph}, (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents -> t ⊆ G.universalVerts -> M1.verts = Subtype.val '' reps ∪ t -> M1.IsMatching -> exists complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph, forall K, (complMatch K).verts = Subtype.val '' K.supp \ M1.verts /\ (complMatch K).IsMatching`.

Formal target fingerprint: `sha256:a698d3b08ba96a95e0314189f9cd0f409fe2acc1472634e5f521ce5d48860cda`.

Source locator: `Tutte.lean:85-92; UniversalVerts.lean:69-77; Matching.lean:260-275`.

Required premises: `frozen-formal-context`.

Inference: Use the representative parity lemma to prove each residual set even, inherit the clique property, and apply the finite clique matching equivalence before choosing the family.

Output: A component-indexed family of matchings covering exactly the vertices not used by M1.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-isup-disjoint-matching

Take the supremum of the component-local matchings and derive both matching and M1-disjointness invariants.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} {M1 : G.Subgraph} (complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph), M1.IsMatching -> (forall K, (complMatch K).verts = Subtype.val '' K.supp \ M1.verts /\ (complMatch K).IsMatching) -> let M2 := iSup complMatch; M2.IsMatching /\ Disjoint M1.support M2.support`.

Formal target fingerprint: `sha256:42c5b0e60a8e2337d168e5b9125aeb1bc9d26f556c92fcdd5040127276417c2e`.

Source locator: `Tutte.lean:93-104; Matching.lean:128-142`.

Required premises: `frozen-formal-context`.

Inference: Derive pairwise support disjointness from distinct connected-component supports, apply matching closure under iSup, and lift the exact residual-vertex equations to M1 support disjointness.

Output: A global matching M2 together with the required disjointness from M1.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-uncovered-subset

Show every vertex left uncovered by M1 and the component-local supremum is universal.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} (M1 : G.Subgraph) (complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph), (forall K, (complMatch K).verts = Subtype.val '' K.supp \ M1.verts) -> let M2 := iSup complMatch; (M1.verts ∪ M2.verts)ᶜ ⊆ G.universalVerts`.

Formal target fingerprint: `sha256:859bcf04f6b7a59de6f534616424b65f76d9e8db695b73bff37ef7c37164d925`.

Source locator: `Tutte.lean:105-116`.

Required premises: `frozen-formal-context`.

Inference: For a non-universal vertex, choose its component in deleteUniversalVerts; if it is not in M1, the exact component-local vertex equation places it in the supremum.

Output: The exact near-cover property needed for the supremum matching.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-complement-matching

Derive evenness of the uncovered universal vertices and match them.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} [Finite V] (M : G.Subgraph), Even (Nat.card V) -> M.IsMatching -> M.vertsᶜ ⊆ G.universalVerts -> exists M' : G.Subgraph, M'.verts = M.vertsᶜ /\ M'.IsMatching`.

Formal target fingerprint: `sha256:d09ad936c624884039338e25521a03b883cda7734f9c8ab9567e343d06282e16`.

Source locator: `Tutte.lean:126-130`.

Required premises: `frozen-formal-context`.

Inference: Combine even total order with the matching's even vertex count to derive complement parity, inherit the universal-vertex clique, and apply the finite clique matching equivalence.

Output: A matching M' with vertices exactly M.verts complement, with complement parity derived rather than assumed.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-sup-perfect

Take the disjoint supremum of the near-covering and complement matchings.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} {M M' : G.Subgraph}, M.IsMatching -> M'.IsMatching -> M'.verts = M.vertsᶜ -> (M ⊔ M').IsPerfectMatching`.

Formal target fingerprint: `sha256:58aee41c3ad4657b0b7c8900803b42b2087a5d14d965af9054eecb8b1f1b16fd`.

Source locator: `Tutte.lean:131-134`.

Required premises: `frozen-formal-context`.

Inference: Prove support disjointness from complementary vertex sets and prove the supremum vertices equal the universe.

Output: A spanning matching, hence a perfect matching.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-nonclique

If one deleted component is not a clique, use maximality to obtain two near-perfect matchings and combine them.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (Gmax : SimpleGraph V) [Finite V], Gmax.IsMatchingFree -> (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False`.

Formal target fingerprint: `sha256:6c123074c446b1dd878b52b627027f593a3741aada5f0302d433e7b5ea25144f`.

Source locator: `Tutte.lean:287-308`.

Required premises: `M0856-C-NONCLIQUE-WITNESS, M0856-L-SHORTEST-PATH-TRIPLE, M0856-C-EDGE-AUGMENTATIONS, M0856-C-NEAR-MATCHINGS, M0856-T-NEAR-TO-PERFECT`.

Inference: Extract a shortest-path three-vertex pattern, add two missing edges separately, and invoke the near-matching composition.

Output: A perfect matching of Gmax, contradicting matching-freedom.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-nonclique-witness

Choose a nonclique component, two nonadjacent vertices, and a shortest path between them inside that component.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (Gmax : SimpleGraph V), Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> exists K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, exists x y : K, x ≠ y /\ Not (K.toSimpleGraph.Adj x y) /\ exists p : K.toSimpleGraph.Walk x y, p.IsPath /\ p.length = K.toSimpleGraph.dist x y /\ 1 < K.toSimpleGraph.dist x y`.

Formal target fingerprint: `sha256:5176663c08f02cd8ec261eea34531f24a3663c1a8bcc99cd28d8d5c6b1f1e97c`.

Source locator: `Tutte.lean:288-292; Metric.lean:242-247,337-340`.

Required premises: `frozen-formal-context`.

Inference: Negate the componentwise clique condition to choose K and its nonadjacent supported vertices, then use connectedness of K.toSimpleGraph to obtain a distance-realizing path and strict distance bound.

Output: A chosen nonclique component, nonadjacent distinct pair, and distance-realizing path of length greater than one.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-shortest-path-triple

Extract adjacent x-a-b along the component shortest path and normalize them to ambient vertices.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (Gmax : SimpleGraph V) {K : Gmax.deleteUniversalVerts.coe.ConnectedComponent} {v w : K} {p : K.toSimpleGraph.Walk v w}, p.length = K.toSimpleGraph.dist v w -> 1 < K.toSimpleGraph.dist v w -> exists x a b : V, Gmax.Adj x a /\ Gmax.Adj a b /\ Not (Gmax.Adj x b) /\ x ≠ b /\ a ∉ Gmax.universalVerts`.

Formal target fingerprint: `sha256:b168024076ca171361820e3395181e60ee4bdc8fcafba777e315d4712606c3cd`.

Source locator: `Metric.lean:378-389; Tutte.lean:290-298`.

Required premises: `frozen-formal-context`.

Inference: Apply exists_adj_adj_not_adj_ne in K.toSimpleGraph, then unfold the induced deleted-component graph and subtype coercions to preserve adjacency, nonadjacency, distinctness, and membership outside universalVerts.

Output: Ambient vertices x, a, b with two path edges, a missing chord, x distinct from b, and a non-universal.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-edge-augmentations

Choose c nonadjacent to a and form the two strict supergraphs adding x-b and a-c.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (Gmax : SimpleGraph V) (x a b : V), Gmax.Adj x a -> Gmax.Adj a b -> x ≠ b -> Not (Gmax.Adj x b) -> a ∉ Gmax.universalVerts -> exists c : V, a ≠ c /\ x ≠ c /\ b ≠ c /\ Not (Gmax.Adj c a) /\ Gmax < Gmax ⊔ SimpleGraph.edge x b /\ Gmax < Gmax ⊔ SimpleGraph.edge a c`.

Formal target fingerprint: `sha256:623f39abcd241fe269748909f9950d539fc5b2e0fc97d1a63bdf1a9e13b48935`.

Source locator: `Tutte.lean:297-305`.

Required premises: `frozen-formal-context`.

Inference: Use non-universality of a for c; derive b != c and x != c from the two retained Gmax adjacencies and a-c nonadjacency; then prove both missing-edge strictness conditions.

Output: Two strict edge extensions of Gmax plus every distinctness fact required by the near-matching theorem.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-near-matchings

Use edge-maximal matching-freedom to obtain perfect matchings in both one-edge extensions.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} (Gmax : SimpleGraph V) (x a b c : V), (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Gmax < Gmax ⊔ SimpleGraph.edge x b -> Gmax < Gmax ⊔ SimpleGraph.edge a c -> (exists M1 : (Gmax ⊔ SimpleGraph.edge x b).Subgraph, M1.IsPerfectMatching) /\ (exists M2 : (Gmax ⊔ SimpleGraph.edge a c).Subgraph, M2.IsPerfectMatching)`.

Formal target fingerprint: `sha256:499382d744f523a93c805928da2ab27a8d75a30cf3efe527d0348b57f4e58ed5`.

Source locator: `Tutte.lean:300-306`.

Required premises: `frozen-formal-context`.

Inference: Apply the maximality certificate to each strict supergraph and preserve which artificial edge belongs to which graph.

Output: Perfect matchings M1 and M2 on the two augmented graphs.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-t-near-to-perfect

Combine perfect matchings from the two one-edge extensions into a perfect matching of the original graph.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> exists M : G.Subgraph, M.IsPerfectMatching`.

Formal target fingerprint: `sha256:090c672ce2d6e5459440ec3060a6a246404a4daee3ec9c68ca29e0bfc2f3461a`.

Source locator: `Tutte.lean:153-262`.

Required premises: `M0856-B-FIRST-EXTRA-ABSENT, M0856-B-SECOND-EXTRA-ABSENT, M0856-B-BOTH-EXTRA-PRESENT`.

Inference: Return an extension matching directly when it omits its added edge; otherwise use an alternating cycle in the symmetric difference and toggle it.

Output: Exists M : Subgraph Gmax, M.IsPerfectMatching.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-first-extra-absent

If M1 omits the artificial edge x-b, restrict M1 to Gmax.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} {x b : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph}, M1.IsPerfectMatching -> Not (M1.Adj x b) -> exists M : G.Subgraph, M.IsPerfectMatching`.

Formal target fingerprint: `sha256:a324ca6881e9262eb38a621c19ef216bc81b2fd83aa80be9213fb621dab53243`.

Source locator: `Tutte.lean:160-163`.

Required premises: `frozen-formal-context`.

Inference: Use toSubgraph with the spanning-coefficient inclusion and transport perfect matching across the restriction.

Output: A perfect matching of the original graph.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-second-extra-absent

If M2 omits the artificial edge a-c, restrict M2 to Gmax.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} {a c : V} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, M2.IsPerfectMatching -> Not (M2.Adj a c) -> exists M : G.Subgraph, M.IsPerfectMatching`.

Formal target fingerprint: `sha256:4ee0dc3a65d6575ca1a33f6366b181a7436514b84ef4754bb10f21cf594c2f27`.

Source locator: `Tutte.lean:164-166`.

Required premises: `frozen-formal-context`.

Inference: Use the symmetric restriction argument for the second augmented graph.

Output: A perfect matching of the original graph.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-both-extra-present

When both augmented perfect matchings contain their artificial edges, splice them with an alternating symmetric-difference cycle.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> exists M : G.Subgraph, M.IsPerfectMatching`.

Formal target fingerprint: `sha256:95dd47ea73ad29c9c49dcd50e668b25ebeb2276df920839f77c2c57035039f07`.

Source locator: `Tutte.lean:167-262`.

Required premises: `M0856-C-SYMDIFF-CYCLES, M0856-B-CYCLE-SUPPORT-SPLIT, M0856-L-SYMDIFF-PRESERVES-PERFECT`.

Inference: Establish the symmetric-difference invariants, split whether its c-component contains x, and toggle M2 along the resulting alternating cycle.

Output: A perfect matching of the original graph after the cycle-support subcase.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-symdiff-cycles

When both artificial edges occur, form the symmetric difference of the two perfect matchings as alternating cycles.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> let cycles := M1.spanningCoe ∆ M2.spanningCoe; cycles.IsAlternating M2.spanningCoe /\ cycles.IsCycles /\ cycles.Adj a c /\ ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b`.

Formal target fingerprint: `sha256:e5e70f89c044a40189ff4f34adccd102482c12116a948bb8f3ca402f14985bd3`.

Source locator: `Tutte.lean:167-194; Matching.lean:413-429 and isAlternating_symmDiff_right`.

Required premises: `frozen-formal-context`.

Inference: Derive that M1 omits a-c, prove alternation and the cycles property, expose a-c in the symmetric difference, and retain the component inclusion used by both support branches.

Output: The symmetric-difference cycles are alternating with respect to M2, contain a-c, and place c's component inside the two-edge ambient graph.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-cycle-support-split

Split whether x lies in the support of the symmetric-difference component containing c and recompose the common alternating-cycle contract.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G cycles : SimpleGraph V} {x b a c : V} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, (x ∉ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c) -> (x ∈ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c) -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c`.

Formal target fingerprint: `sha256:5885d86a03c8940e401a99704f54fb4ccdd5cd85ca260fa15e81306cbf9bce0b`.

Source locator: `Tutte.lean:195-262`.

Required premises: `M0856-B-CYCLE-AVOIDS-X, M0856-B-CYCLE-CONTAINS-X`.

Inference: Use classical case analysis on support membership, invoke exactly one child branch, and return its full common contract rather than only the excluded-middle proposition.

Output: An alternating cycles graph satisfying the identical inclusion and edge-incidence contract in either exhaustive support subcase.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-cycle-avoids-x

If the symmetric-difference component containing c avoids x, use that component cycle directly.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe ∆ M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b -> x ∉ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c`.

Formal target fingerprint: `sha256:baf253b7607f28eab114e927d3c91dd8a142ef73d7313157b00f8ab6bfb6b4d7`.

Source locator: `Tutte.lean:195-206`.

Required premises: `frozen-formal-context`.

Inference: Restrict to the connected component, inherit alternation and the cycles property, use a-c to retain the component, and remove the only extra x-b edge using x's absence from the support.

Output: The c-component yields an alternating cycles graph containing a-c, avoiding x-b, and lying in G sup edge a c.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-b-cycle-contains-x

If that component contains x, cut a cycle path before an occurrence of x or b and close it with x-a.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe ∆ M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b -> x ∈ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c`.

Formal target fingerprint: `sha256:b5ee7e8679bff9efa0786ccb4d98bd3eb81299fdc83e5dd6e56551c2e75b83e5`.

Source locator: `Tutte.lean:207-262`.

Required premises: `M0856-C-TRUNCATED-PATH, M0856-L-ALTERNATING-CYCLE-AUGMENT`.

Inference: Use finite local finiteness, extract and truncate the component cycle, prove the terminal matching edge, then invoke the alternating-cycle augmentation in the x or b endpoint subcase.

Output: The truncated-path construction yields the same full alternating cycles contract as the avoid-x branch.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-c-truncated-path

Construct a path from a to x or b that contains a-c, omits x-b, lies in the second augmentation, and ends with the required M2 edge.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe ∆ M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b -> x ∈ (cycles.connectedComponentMk c).supp -> exists x' : V, (x' = x \/ x' = b) /\ exists p : cycles.Walk a x', p.IsPath /\ p.toSubgraph.Adj a c /\ Not (p.toSubgraph.Adj x b) /\ p.toSubgraph.spanningCoe ≤ G ⊔ SimpleGraph.edge a c /\ forall c' : V, c' ≠ a -> p.toSubgraph.Adj c' x' -> M2.Adj c' x'`.

Formal target fingerprint: `sha256:8d43a3420ce7307b1e225b1bf076dd32e00dd3d289f0f1f4cb8e3772af9af542`.

Source locator: `Tutte.lean:207-253`.

Required premises: `frozen-formal-context`.

Inference: Select and truncate the component cycle, prove the path inclusion after deleting x-b, and use matching uniqueness at x or b to derive the terminal M2 edge needed by the augmentation lemma.

Output: A simple path whose endpoint, a-c edge, x-b exclusion, ambient inclusion, and terminal M2-edge contract are all explicit.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-alternating-cycle-augment

Close the truncated alternating path with edge x-a while preserving cycle and edge-exclusion invariants.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G G' : SimpleGraph V} {x b a c : V} {M : (G ⊔ SimpleGraph.edge a c).Subgraph} (p : G'.Walk a x), p.IsPath -> G'.IsAlternating M.spanningCoe -> Not (M.Adj x a) -> p.toSubgraph.Adj a c -> Not (p.toSubgraph.Adj x b) -> M.Adj a c -> G.Adj x a -> x ≠ c -> a ≠ b -> p.toSubgraph.spanningCoe ≤ G ⊔ SimpleGraph.edge a c -> ((c' : V) -> c' ≠ a -> p.toSubgraph.Adj c' x -> M.Adj c' x) -> exists G'', G''.IsAlternating M.spanningCoe /\ G''.IsCycles /\ Not (G''.Adj x b) /\ G''.Adj a c /\ G'' ≤ G ⊔ SimpleGraph.edge a c`.

Formal target fingerprint: `sha256:c03ccae832466b1f9b7ef96568a16b9f7baf3b07ca64e90015f26eb2cba369bc`.

Source locator: `Tutte.lean:39-56,254-262`.

Required premises: `frozen-formal-context`.

Inference: Take the path spanning graph sup the closing edge, prove degree two, alternating parity, and the required graph inclusion.

Output: An alternating cycles graph containing a-c, excluding x-b, and lying in G sup edge a c.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-l-symdiff-preserves-perfect

Derive that toggling the second augmented matching along the selected alternating cycles graph lies in G, then transport perfectness.

Formal target kind: `planned_lean_signature`.

Formal target/type/record: `forall {V : Type u} {G G' : SimpleGraph V} {a c : V} {M : (G ⊔ SimpleGraph.edge a c).Subgraph}, M.IsPerfectMatching -> G'.IsAlternating M.spanningCoe -> G'.IsCycles -> G'.Adj a c -> M.Adj a c -> G' ≤ G ⊔ SimpleGraph.edge a c -> exists hle : M.spanningCoe ∆ G' ≤ G, (G.toSubgraph (M.spanningCoe ∆ G') hle).IsPerfectMatching`.

Formal target fingerprint: `sha256:69decbdfe7d62c38151f6ed9b25c23389fba42582934ee94ae42ee738dc5d9ec`.

Source locator: `Matching.lean:576-604; Tutte.lean:173-181`.

Required premises: `frozen-formal-context`.

Inference: Derive the inclusion from the augmented-graph bounds and cancellation of the artificial a-c edge present in both M and G'; then apply symmetric-difference preservation and transport the exact graph through G.toSubgraph.

Output: A derived inclusion and the corresponding explicit symmetric-difference perfect matching in G.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-x-source

Map every material mathematical node to a pinpoint primary proof source, incorporated definitions, assumptions, and corrections.

Formal target kind: `nonformal_record`.

Formal target/type/record: `stage1-source-crosswalk-record/1.0`.

Formal target fingerprint: `sha256:7dcf8dc2a47f7d125cbf1c9da2a3bae903c3ee7af37167b2405d1df237296c18`.

Source locator: `source-statement-crosswalk.md; primary 1947 article lead`.

Required premises: `frozen-formal-context`.

Inference: Preserve an admitted edition and map each source transition to the frozen nodes; a bibliographic identity alone does not close this obligation.

Output: An independently reviewed H0 crosswalk for the complete route.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-x-provenance

Bind local wrappers, the single exact terminal body, support declarations, private source segments, hashes, origin, license, and transitive dependencies.

Formal target kind: `nonformal_record`.

Formal target/type/record: `stage1-provenance-closure-record/1.0`.

Formal target fingerprint: `sha256:40e27f3f1605a129a934338ae188436d8ea9a69d2621de82980161b37cfc6576`.

Source locator: `anchor-audit.json provenance_packet`.

Required premises: `frozen-formal-context`.

Inference: Traverse actual declaration bodies and deduplicate the local adapter and Atlas wrapper from the sole SimpleGraph.tutte terminal body.

Output: Release-grade proof-body provenance without duplicate root credit.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-x-trust

Close the transitive axiom, unsafe-code, compiled-artifact, executable, dependency, and TCB inventory.

Formal target kind: `nonformal_record`.

Formal target/type/record: `stage1-trust-closure-record/1.0`.

Formal target fingerprint: `sha256:fbb331661461981ff8e40d8183a28b1510fc266b695fd26f0ae0b5d07586e335`.

Source locator: `anchor-audit.json trust_boundary`.

Required premises: `frozen-formal-context`.

Inference: Hash and classify every trusted element, then perform cold offline and independent replay; unknown trust fails closed.

Output: Accepted trust closure under the selected foundation policy.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-x-documentation

Provide a stable reader-facing entry and exact formal/source boundary for every readable obligation.

Formal target kind: `nonformal_record`.

Formal target/type/record: `stage1-readable-crosswalk-record/1.0`.

Formal target fingerprint: `sha256:2987d8ccb0409eb52d96f94c3f9b5bf4257878cd98562733633fa558a1b1f3e4`.

Source locator: `obligation-tree.md`.

Required premises: `frozen-formal-context`.

Inference: Reconstruct the accepted proof route in graph-theory language while keeping architecture plans distinct from completed proof claims.

Output: Node-specific readable records and independent R0 review receipts.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.

### m0856-x-workflow

Enforce dependency legality from anchor acceptance through proof, validation, release, invalidation, and revocation.

Formal target kind: `nonformal_record`.

Formal target/type/record: `stage1-workflow-state-record/1.0`.

Formal target fingerprint: `sha256:143e68b8b89d8007636a0a3fea49d465955670bdda658eed75bee870730fbe2e`.

Source locator: `Docs/Stage1_Execution_DAG_rev-5.6.json; task-dag.json`.

Required premises: `frozen-formal-context`.

Inference: Bind task-to-obligation links and reject any downstream acceptance before its prerequisites and receipts are accepted.

Output: Only dependency-legal provisional or accepted execution states.

Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit
completion, and theorem completion remain open.
