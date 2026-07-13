import ObligationTree

set_option autoImplicit false

/-! Generated exact-declaration probes and planned proposition signatures for THM-M-0856. -/

namespace Stage1Instances.THM_M_0856.ObligationSignatures

universe u v

open SimpleGraph
open scoped symmDiff

#check (rfl : @Stage1Instances.THM_M_0856.TutteOneFactorTarget.{u} = (forall {V : Type u} (G : SimpleGraph V), [Finite V] -> ((Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> Stage1Instances.THM_M_0856.OddComponentCondition G)))
/-- Frozen planned interface for `M0856-S-DOMAIN`; this definition grants no proof closure. -/
def M0856_S_DOMAIN : Prop := forall {V : Type u} (G : SimpleGraph V), [Finite V] -> True

/-- Frozen planned interface for `M0856-S-MATCHING`; this definition grants no proof closure. -/
def M0856_S_MATCHING : Prop := forall {V : Type u} (G : SimpleGraph V), (Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> (Exists fun M : G.Subgraph => M.IsPerfectMatching)

#check (@Stage1Instances.THM_M_0856.OddComponentCondition : forall {V : Type u} (G : SimpleGraph V), Prop)
#check (@Stage1Instances.THM_M_0856.tutteOneFactorTarget_iff_noTutteViolatorTarget : Stage1Instances.THM_M_0856.TutteOneFactorTarget <-> Stage1Instances.THM_M_0856.NoTutteViolatorTarget)
/-- Frozen planned interface for `M0856-N-FINITE-INTERFACES`; this definition grants no proof closure. -/
def M0856_N_FINITE_INTERFACES : Prop := forall {V : Type u}, [Finite V] -> Nonempty (Fintype V)

#check (@Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter : Stage1Instances.THM_M_0856.ObligationTree.MathlibTerminal -> Stage1Instances.THM_M_0856.TutteOneFactorTarget)
#check (@SimpleGraph.tutte : forall {V : Type u} {G : SimpleGraph V} [Finite V], (Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> forall U : Set V, Not (G.IsTutteViolator U))
#check (@SimpleGraph.not_isTutteViolator_of_isPerfectMatching : forall {V : Type u} {G : SimpleGraph V} [Finite V] {M : G.Subgraph}, M.IsPerfectMatching -> forall U : Set V, Not (G.IsTutteViolator U))
#check (@SimpleGraph.ConnectedComponent.odd_matches_node_outside : forall {V : Type u} {G : SimpleGraph V} {M : G.Subgraph} [Finite V] {U : Set V}, M.IsPerfectMatching -> forall c : ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents, exists w, w ∈ U /\ exists v : ((⊤ : G.Subgraph).deleteVerts U).verts, M.Adj v w /\ v ∈ c.val.supp)
/-- Frozen planned interface for `M0856-C-ODD-TO-U-INJECTION`; this definition grants no proof closure. -/
def M0856_C_ODD_TO_U_INJECTION : Prop := forall {V : Type u} {G : SimpleGraph V} [Finite V] {M : G.Subgraph} (hM : M.IsPerfectMatching) (U : Set V), (forall c : ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents, exists w, w ∈ U /\ exists v : ((⊤ : G.Subgraph).deleteVerts U).verts, M.Adj v w /\ v ∈ c.val.supp) -> exists f : ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents -> U, Function.Injective f

/-- Frozen planned interface for `M0856-L-NCARD-INJECTION`; this definition grants no proof closure. -/
def M0856_L_NCARD_INJECTION : Prop := forall {V : Type u} {G : SimpleGraph V} [Finite V] (U : Set V), (exists f : ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents -> U, Function.Injective f) -> ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents.ncard <= U.ncard

/-- Frozen planned interface for `M0856-T-SUFFICIENCY`; this definition grants no proof closure. -/
def M0856_T_SUFFICIENCY : Prop := forall {V : Type u} (G : SimpleGraph V) [Finite V], (forall U : Set V, Not (G.IsTutteViolator U)) -> Exists fun M : G.Subgraph => M.IsPerfectMatching

/-- Frozen planned interface for `M0856-B-PARITY-SPLIT`; this definition grants no proof closure. -/
def M0856_B_PARITY_SPLIT : Prop := forall {V : Type u} (G : SimpleGraph V) [Finite V], (forall M : G.Subgraph, Not M.IsPerfectMatching) -> (Odd (Nat.card V) -> Exists fun U : Set V => G.IsTutteViolator U) -> (Even (Nat.card V) -> Exists fun U : Set V => G.IsTutteViolator U) -> Exists fun U : Set V => G.IsTutteViolator U

/-- Frozen planned interface for `M0856-B-ODD-CARD`; this definition grants no proof closure. -/
def M0856_B_ODD_CARD : Prop := forall {V : Type u} {G : SimpleGraph V} [Finite V], Odd (Nat.card V) -> exists U : Set V, U = ∅ /\ G.IsTutteViolator U

#check (@SimpleGraph.IsTutteViolator.empty : forall {V : Type u} {G : SimpleGraph V} [Finite V], Odd (Nat.card V) -> G.IsTutteViolator (∅ : Set V))
/-- Frozen planned interface for `M0856-B-EVEN-CARD`; this definition grants no proof closure. -/
def M0856_B_EVEN_CARD : Prop := forall {V : Type u} {G : SimpleGraph V} [Finite V], Even (Nat.card V) -> (forall M : G.Subgraph, Not M.IsPerfectMatching) -> exists U : Set V, G.IsTutteViolator U

#check (@SimpleGraph.exists_isTutteViolator : forall {V : Type u} {G : SimpleGraph V} [Finite V], (forall M : G.Subgraph, Not M.IsPerfectMatching) -> Even (Nat.card V) -> exists U, G.IsTutteViolator U)
#check (@SimpleGraph.exists_maximal_isMatchingFree : forall {V : Type u} {G : SimpleGraph V} [Finite V], G.IsMatchingFree -> exists Gmax, G <= Gmax /\ Gmax.IsMatchingFree /\ forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching)
#check (@SimpleGraph.IsTutteViolator.mono : forall {V : Type u} {G G' : SimpleGraph V} [Finite V] {U : Set V}, G <= G' -> G'.IsTutteViolator U -> G.IsTutteViolator U)
/-- Frozen planned interface for `M0856-C-UNIVERSAL-DELETION`; this definition grants no proof closure. -/
def M0856_C_UNIVERSAL_DELETION : Prop := forall {V : Type u} (Gmax : SimpleGraph V), Gmax.deleteUniversalVerts = (⊤ : Gmax.Subgraph).deleteVerts Gmax.universalVerts

/-- Frozen planned interface for `M0856-B-CLIQUE-SPLIT`; this definition grants no proof closure. -/
def M0856_B_CLIQUE_SPLIT : Prop := forall {V : Type u} (Gmax : SimpleGraph V) [Finite V], Gmax.IsMatchingFree -> Even (Nat.card V) -> (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Not (Gmax.IsTutteViolator Gmax.universalVerts) -> ((forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False) -> (Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False) -> False

/-- Frozen planned interface for `M0856-B-ALL-CLIQUES`; this definition grants no proof closure. -/
def M0856_B_ALL_CLIQUES : Prop := forall {V : Type u} {Gmax : SimpleGraph V} [Finite V], Gmax.IsMatchingFree -> Even (Nat.card V) -> Not (Gmax.IsTutteViolator Gmax.universalVerts) -> (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False

#check (@SimpleGraph.Subgraph.IsPerfectMatching.exists_of_isClique_supp : forall {V : Type u} {G : SimpleGraph V} [Finite V], Even (Nat.card V) -> Not (G.IsTutteViolator G.universalVerts) -> (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> exists M : G.Subgraph, M.IsPerfectMatching)
/-- Frozen planned interface for `M0856-C-NEAR-COVER-MATCHING`; this definition grants no proof closure. -/
def M0856_C_NEAR_COVER_MATCHING : Prop := forall {V : Type u} (G : SimpleGraph V) [Finite V], Not (G.IsTutteViolator G.universalVerts) -> (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> exists M : G.Subgraph, M.IsMatching /\ M.vertsᶜ ⊆ G.universalVerts

/-- Frozen planned interface for `M0856-C-ODD-REPRESENTATIVES`; this definition grants no proof closure. -/
def M0856_C_ODD_REPRESENTATIVES : Prop := forall {V : Type u} (G : SimpleGraph V) [Finite V], Not (G.IsTutteViolator G.universalVerts) -> let reps : Set G.deleteUniversalVerts.verts := Quot.out '' G.deleteUniversalVerts.coe.oddComponents; ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents /\ reps.ncard = G.deleteUniversalVerts.coe.oddComponents.ncard /\ Disjoint G.universalVerts (Subtype.val '' reps) /\ (Subtype.val '' reps).ncard <= G.universalVerts.ncard

/-- Frozen planned interface for `M0856-C-MATCH-REPS-UNIVERSALS`; this definition grants no proof closure. -/
def M0856_C_MATCH_REPS_UNIVERSALS : Prop := forall {V : Type u} {G : SimpleGraph V} [Finite V] {reps : Set G.deleteUniversalVerts.verts}, ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents -> Disjoint G.universalVerts (Subtype.val '' reps) -> (Subtype.val '' reps).ncard <= G.universalVerts.ncard -> exists t : Set V, t ⊆ G.universalVerts /\ exists M1 : G.Subgraph, M1.verts = Subtype.val '' reps ∪ t /\ M1.IsMatching

/-- Frozen planned interface for `M0856-C-INTERNAL-COMPONENT-MATCHINGS`; this definition grants no proof closure. -/
def M0856_C_INTERNAL_COMPONENT_MATCHINGS : Prop := forall {V : Type u} {G : SimpleGraph V} [Finite V] {reps : Set G.deleteUniversalVerts.verts} {t : Set V} {M1 : G.Subgraph}, (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents -> t ⊆ G.universalVerts -> M1.verts = Subtype.val '' reps ∪ t -> M1.IsMatching -> exists complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph, forall K, (complMatch K).verts = Subtype.val '' K.supp \ M1.verts /\ (complMatch K).IsMatching

/-- Frozen planned interface for `M0856-C-ISUP-DISJOINT-MATCHING`; this definition grants no proof closure. -/
def M0856_C_ISUP_DISJOINT_MATCHING : Prop := forall {V : Type u} {G : SimpleGraph V} {M1 : G.Subgraph} (complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph), M1.IsMatching -> (forall K, (complMatch K).verts = Subtype.val '' K.supp \ M1.verts /\ (complMatch K).IsMatching) -> let M2 := iSup complMatch; M2.IsMatching /\ Disjoint M1.support M2.support

/-- Frozen planned interface for `M0856-L-UNCOVERED-SUBSET`; this definition grants no proof closure. -/
def M0856_L_UNCOVERED_SUBSET : Prop := forall {V : Type u} {G : SimpleGraph V} (M1 : G.Subgraph) (complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph), (forall K, (complMatch K).verts = Subtype.val '' K.supp \ M1.verts) -> let M2 := iSup complMatch; (M1.verts ∪ M2.verts)ᶜ ⊆ G.universalVerts

/-- Frozen planned interface for `M0856-C-COMPLEMENT-MATCHING`; this definition grants no proof closure. -/
def M0856_C_COMPLEMENT_MATCHING : Prop := forall {V : Type u} {G : SimpleGraph V} [Finite V] (M : G.Subgraph), Even (Nat.card V) -> M.IsMatching -> M.vertsᶜ ⊆ G.universalVerts -> exists M' : G.Subgraph, M'.verts = M.vertsᶜ /\ M'.IsMatching

/-- Frozen planned interface for `M0856-C-SUP-PERFECT`; this definition grants no proof closure. -/
def M0856_C_SUP_PERFECT : Prop := forall {V : Type u} {G : SimpleGraph V} {M M' : G.Subgraph}, M.IsMatching -> M'.IsMatching -> M'.verts = M.vertsᶜ -> (M ⊔ M').IsPerfectMatching

/-- Frozen planned interface for `M0856-B-NONCLIQUE`; this definition grants no proof closure. -/
def M0856_B_NONCLIQUE : Prop := forall {V : Type u} (Gmax : SimpleGraph V) [Finite V], Gmax.IsMatchingFree -> (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False

/-- Frozen planned interface for `M0856-C-NONCLIQUE-WITNESS`; this definition grants no proof closure. -/
def M0856_C_NONCLIQUE_WITNESS : Prop := forall {V : Type u} (Gmax : SimpleGraph V), Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> exists K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, exists x y : K, x ≠ y /\ Not (K.toSimpleGraph.Adj x y) /\ exists p : K.toSimpleGraph.Walk x y, p.IsPath /\ p.length = K.toSimpleGraph.dist x y /\ 1 < K.toSimpleGraph.dist x y

/-- Frozen planned interface for `M0856-L-SHORTEST-PATH-TRIPLE`; this definition grants no proof closure. -/
def M0856_L_SHORTEST_PATH_TRIPLE : Prop := forall {V : Type u} (Gmax : SimpleGraph V) {K : Gmax.deleteUniversalVerts.coe.ConnectedComponent} {v w : K} {p : K.toSimpleGraph.Walk v w}, p.length = K.toSimpleGraph.dist v w -> 1 < K.toSimpleGraph.dist v w -> exists x a b : V, Gmax.Adj x a /\ Gmax.Adj a b /\ Not (Gmax.Adj x b) /\ x ≠ b /\ a ∉ Gmax.universalVerts

/-- Frozen planned interface for `M0856-C-EDGE-AUGMENTATIONS`; this definition grants no proof closure. -/
def M0856_C_EDGE_AUGMENTATIONS : Prop := forall {V : Type u} (Gmax : SimpleGraph V) (x a b : V), Gmax.Adj x a -> Gmax.Adj a b -> x ≠ b -> Not (Gmax.Adj x b) -> a ∉ Gmax.universalVerts -> exists c : V, a ≠ c /\ x ≠ c /\ b ≠ c /\ Not (Gmax.Adj c a) /\ Gmax < Gmax ⊔ SimpleGraph.edge x b /\ Gmax < Gmax ⊔ SimpleGraph.edge a c

/-- Frozen planned interface for `M0856-C-NEAR-MATCHINGS`; this definition grants no proof closure. -/
def M0856_C_NEAR_MATCHINGS : Prop := forall {V : Type u} (Gmax : SimpleGraph V) (x a b c : V), (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Gmax < Gmax ⊔ SimpleGraph.edge x b -> Gmax < Gmax ⊔ SimpleGraph.edge a c -> (exists M1 : (Gmax ⊔ SimpleGraph.edge x b).Subgraph, M1.IsPerfectMatching) /\ (exists M2 : (Gmax ⊔ SimpleGraph.edge a c).Subgraph, M2.IsPerfectMatching)

/-- Frozen planned interface for `M0856-T-NEAR-TO-PERFECT`; this definition grants no proof closure. -/
def M0856_T_NEAR_TO_PERFECT : Prop := forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> exists M : G.Subgraph, M.IsPerfectMatching

/-- Frozen planned interface for `M0856-B-FIRST-EXTRA-ABSENT`; this definition grants no proof closure. -/
def M0856_B_FIRST_EXTRA_ABSENT : Prop := forall {V : Type u} {G : SimpleGraph V} {x b : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph}, M1.IsPerfectMatching -> Not (M1.Adj x b) -> exists M : G.Subgraph, M.IsPerfectMatching

/-- Frozen planned interface for `M0856-B-SECOND-EXTRA-ABSENT`; this definition grants no proof closure. -/
def M0856_B_SECOND_EXTRA_ABSENT : Prop := forall {V : Type u} {G : SimpleGraph V} {a c : V} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, M2.IsPerfectMatching -> Not (M2.Adj a c) -> exists M : G.Subgraph, M.IsPerfectMatching

/-- Frozen planned interface for `M0856-B-BOTH-EXTRA-PRESENT`; this definition grants no proof closure. -/
def M0856_B_BOTH_EXTRA_PRESENT : Prop := forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> exists M : G.Subgraph, M.IsPerfectMatching

/-- Frozen planned interface for `M0856-C-SYMDIFF-CYCLES`; this definition grants no proof closure. -/
def M0856_C_SYMDIFF_CYCLES : Prop := forall {V : Type u} {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> let cycles := M1.spanningCoe ∆ M2.spanningCoe; cycles.IsAlternating M2.spanningCoe /\ cycles.IsCycles /\ cycles.Adj a c /\ ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b

/-- Frozen planned interface for `M0856-B-CYCLE-SUPPORT-SPLIT`; this definition grants no proof closure. -/
def M0856_B_CYCLE_SUPPORT_SPLIT : Prop := forall {V : Type u} {G cycles : SimpleGraph V} {x b a c : V} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph}, (x ∉ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c) -> (x ∈ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c) -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c

/-- Frozen planned interface for `M0856-B-CYCLE-AVOIDS-X`; this definition grants no proof closure. -/
def M0856_B_CYCLE_AVOIDS_X : Prop := forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe ∆ M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b -> x ∉ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c

/-- Frozen planned interface for `M0856-B-CYCLE-CONTAINS-X`; this definition grants no proof closure. -/
def M0856_B_CYCLE_CONTAINS_X : Prop := forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe ∆ M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b -> x ∈ (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\ G'.IsCycles /\ Not (G'.Adj x b) /\ G'.Adj a c /\ G' ≤ G ⊔ SimpleGraph.edge a c

/-- Frozen planned interface for `M0856-C-TRUNCATED-PATH`; this definition grants no proof closure. -/
def M0856_C_TRUNCATED_PATH : Prop := forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G ⊔ SimpleGraph.edge x b).Subgraph} {M2 : (G ⊔ SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe ∆ M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe ≤ (G ⊔ SimpleGraph.edge a c) ⊔ SimpleGraph.edge x b -> x ∈ (cycles.connectedComponentMk c).supp -> exists x' : V, (x' = x \/ x' = b) /\ exists p : cycles.Walk a x', p.IsPath /\ p.toSubgraph.Adj a c /\ Not (p.toSubgraph.Adj x b) /\ p.toSubgraph.spanningCoe ≤ G ⊔ SimpleGraph.edge a c /\ forall c' : V, c' ≠ a -> p.toSubgraph.Adj c' x' -> M2.Adj c' x'

/-- Frozen planned interface for `M0856-L-ALTERNATING-CYCLE-AUGMENT`; this definition grants no proof closure. -/
def M0856_L_ALTERNATING_CYCLE_AUGMENT : Prop := forall {V : Type u} {G G' : SimpleGraph V} {x b a c : V} {M : (G ⊔ SimpleGraph.edge a c).Subgraph} (p : G'.Walk a x), p.IsPath -> G'.IsAlternating M.spanningCoe -> Not (M.Adj x a) -> p.toSubgraph.Adj a c -> Not (p.toSubgraph.Adj x b) -> M.Adj a c -> G.Adj x a -> x ≠ c -> a ≠ b -> p.toSubgraph.spanningCoe ≤ G ⊔ SimpleGraph.edge a c -> ((c' : V) -> c' ≠ a -> p.toSubgraph.Adj c' x -> M.Adj c' x) -> exists G'', G''.IsAlternating M.spanningCoe /\ G''.IsCycles /\ Not (G''.Adj x b) /\ G''.Adj a c /\ G'' ≤ G ⊔ SimpleGraph.edge a c

/-- Frozen planned interface for `M0856-L-SYMDIFF-PRESERVES-PERFECT`; this definition grants no proof closure. -/
def M0856_L_SYMDIFF_PRESERVES_PERFECT : Prop := forall {V : Type u} {G G' : SimpleGraph V} {a c : V} {M : (G ⊔ SimpleGraph.edge a c).Subgraph}, M.IsPerfectMatching -> G'.IsAlternating M.spanningCoe -> G'.IsCycles -> G'.Adj a c -> M.Adj a c -> G' ≤ G ⊔ SimpleGraph.edge a c -> exists hle : M.spanningCoe ∆ G' ≤ G, (G.toSubgraph (M.spanningCoe ∆ G') hle).IsPerfectMatching


end Stage1Instances.THM_M_0856.ObligationSignatures
