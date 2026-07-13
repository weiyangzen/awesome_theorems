import Mathlib.Data.Finite.Card
import Mathlib.Data.Set.Card

/-!
# THM-M-0812: Konig's matching-cover statement

This module freezes the finite bipartite multigraph statement from the
inspected translation of Konig's 1931 paper. Edges are an independently
finite type with endpoint maps into two vertex-side types, so parallel edges
are represented rather than silently erased. This file contains statement
transports, structural mutations, and boundary checks, but no proof of the
general theorem.
-/

namespace Stage1Instances.THM_M_0812

universe uL uR uE

/-- A set of edges is a matching when neither endpoint map identifies two
selected edges. -/
def IsEdgeMatching {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (M : Set E) : Prop :=
  Set.InjOn left M ∧ Set.InjOn right M

/-- A pair of vertex subsets covers every edge when each edge has at least one
endpoint in the corresponding subset. -/
def IsBipartiteVertexCover {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (CLeft : Set L) (CRight : Set R) : Prop :=
  ∀ e : E, left e ∈ CLeft ∨ right e ∈ CRight

/-- `k` is the maximum matching edge cardinality. The witness and universal
bound make "maximum" explicit rather than merely inclusion-maximal. -/
def HasMatchingNumber {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (k : Nat) : Prop :=
  (∃ M : Set E, IsEdgeMatching left right M ∧ M.ncard = k) ∧
    ∀ M : Set E, IsEdgeMatching left right M -> M.ncard ≤ k

/-- `k` is the minimum number of vertices in a cover. The cardinality counts
the two typed side occurrences as the tagged disjoint union `L ⊕ R`, even
when `L` and `R` happen to be the same Lean type. -/
def HasVertexCoverNumber {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (k : Nat) : Prop :=
  (∃ CLeft : Set L, ∃ CRight : Set R,
      IsBipartiteVertexCover left right CLeft CRight ∧
        CLeft.ncard + CRight.ncard = k) ∧
    ∀ (CLeft : Set L) (CRight : Set R),
      IsBipartiteVertexCover left right CLeft CRight ->
        k ≤ CLeft.ncard + CRight.ncard

/-- The exact finite bipartite matching-cover equality selected by this
statement phase from the human claim frozen at intake.

The independently finite edge type preserves possible parallel edges in the
source convention. Isolated vertices remain in `L` or `R`, and `E` may be
empty. The conclusion gives one natural number which is both the attained
maximum matching size and the attained minimum vertex-cover size.
-/
def KonigMatchingCoverTarget : Prop :=
  ∀ (L : Type uL) (R : Type uR) (E : Type uE)
    [Finite L] [Finite R] [Finite E]
    (left : E -> L) (right : E -> R),
      ∃ k : Nat,
        HasMatchingNumber left right k ∧
          HasVertexCoverNumber left right k

/-- Direct binder-complete expansion of the canonical target. -/
def ExpandedKonigMatchingCoverTarget : Prop :=
  ∀ (L : Type uL) (R : Type uR) (E : Type uE)
    [Finite L] [Finite R] [Finite E]
    (left : E -> L) (right : E -> R),
      ∃ k : Nat,
        ((∃ M : Set E,
            (Set.InjOn left M ∧ Set.InjOn right M) ∧ M.ncard = k) ∧
          ∀ M : Set E,
            (Set.InjOn left M ∧ Set.InjOn right M) -> M.ncard ≤ k) ∧
        ((∃ CLeft : Set L, ∃ CRight : Set R,
            (∀ e : E, left e ∈ CLeft ∨ right e ∈ CRight) ∧
              CLeft.ncard + CRight.ncard = k) ∧
          ∀ (CLeft : Set L) (CRight : Set R),
            (∀ e : E, left e ∈ CLeft ∨ right e ∈ CRight) ->
              k ≤ CLeft.ncard + CRight.ncard)

/-- Checked identity between the named and fully expanded encodings. -/
theorem konigMatchingCoverTarget_iff_expanded :
    KonigMatchingCoverTarget.{uL, uR, uE} ↔
      ExpandedKonigMatchingCoverTarget.{uL, uR, uE} := by
  rfl

/-! ## Checked simple-relation transport

The following declarations show that parallel-edge identity does not change
either extremum. This bridges the source's unresolved simple-versus-parallel
convention rather than silently choosing one side of it.
-/

/-- A representative edge for each occupied endpoint pair. -/
noncomputable def endpointRepresentative {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R)
    (p : {q : L × R // ∃ e, (left e, right e) = q}) : E :=
  p.property.choose

lemma endpointRepresentative_spec {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R)
    (p : {q : L × R // ∃ e, (left e, right e) = q}) :
    (left (endpointRepresentative left right p),
      right (endpointRepresentative left right p)) = p.1 :=
  p.property.choose_spec

lemma endpointRepresentative_injective {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) :
    Function.Injective (endpointRepresentative left right) := by
  intro p q h
  apply Subtype.ext
  rw [← endpointRepresentative_spec left right p,
    ← endpointRepresentative_spec left right q, h]

lemma left_endpointRepresentative {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R)
    (p : {q : L × R // ∃ e, (left e, right e) = q}) :
    left (endpointRepresentative left right p) = p.1.1 := by
  exact congrArg Prod.fst (endpointRepresentative_spec left right p)

lemma right_endpointRepresentative {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R)
    (p : {q : L × R // ∃ e, (left e, right e) = q}) :
    right (endpointRepresentative left right p) = p.1.2 := by
  exact congrArg Prod.snd (endpointRepresentative_spec left right p)

lemma isEdgeMatching_endpointRepresentative_iff
    {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R)
    (M : Set {q : L × R // ∃ e, (left e, right e) = q}) :
    IsEdgeMatching
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.1)
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.2) M ↔
      IsEdgeMatching left right (endpointRepresentative left right '' M) := by
  rw [IsEdgeMatching, IsEdgeMatching]
  constructor
  · rintro ⟨hl, hr⟩
    constructor
    · rintro _ ⟨p, hp, rfl⟩ _ ⟨q, hq, rfl⟩ heq
      congr 1
      apply hl hp hq
      simpa only [left_endpointRepresentative] using heq
    · rintro _ ⟨p, hp, rfl⟩ _ ⟨q, hq, rfl⟩ heq
      congr 1
      apply hr hp hq
      simpa only [right_endpointRepresentative] using heq
  · rintro ⟨hl, hr⟩
    constructor
    · intro p hp q hq heq
      apply endpointRepresentative_injective left right
      apply hl (Set.mem_image _ _ _ |>.mpr ⟨p, hp, rfl⟩)
        (Set.mem_image _ _ _ |>.mpr ⟨q, hq, rfl⟩)
      simpa only [left_endpointRepresentative, heq]
    · intro p hp q hq heq
      apply endpointRepresentative_injective left right
      apply hr (Set.mem_image _ _ _ |>.mpr ⟨p, hp, rfl⟩)
        (Set.mem_image _ _ _ |>.mpr ⟨q, hq, rfl⟩)
      simpa only [right_endpointRepresentative, heq]

lemma ncard_image_endpointRepresentative
    {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R)
    (M : Set {q : L × R // ∃ e, (left e, right e) = q}) :
    (endpointRepresentative left right '' M).ncard = M.ncard := by
  exact Set.ncard_image_of_injective M (endpointRepresentative_injective left right)

lemma hasMatchingNumber_simple_of_incidence
    {L : Type uL} {R : Type uR} {E : Type uE} [Finite E]
    (left : E -> L) (right : E -> R) (k : Nat)
    (h : HasMatchingNumber left right k) :
    HasMatchingNumber
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.1)
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.2) k := by
  rcases h with ⟨⟨M, hM, hk⟩, hmax⟩
  constructor
  · let f : E -> {q : L × R // ∃ e, (left e, right e) = q} :=
      fun e => ⟨(left e, right e), e, rfl⟩
    let MS : Set {q : L × R // ∃ e, (left e, right e) = q} := f '' M
    have hfM : Set.InjOn f M := by
      intro e he e' he' hp
      apply hM.1 he he'
      exact congrArg (fun p => p.1.1) hp
    refine ⟨MS, ?_, ?_⟩
    · constructor
      · rintro _ ⟨e, he, rfl⟩ _ ⟨e', he', rfl⟩ hleft
        congr 1
        exact hM.1 he he' hleft
      · rintro _ ⟨e, he, rfl⟩ _ ⟨e', he', rfl⟩ hright
        congr 1
        exact hM.2 he he' hright
    · rw [Set.InjOn.ncard_image hfM, hk]
  · intro N hN
    rw [← ncard_image_endpointRepresentative left right N]
    exact hmax _ ((isEdgeMatching_endpointRepresentative_iff left right N).mp hN)

lemma hasVertexCoverNumber_simple_iff_incidence
    {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (k : Nat) :
    HasVertexCoverNumber
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.1)
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.2) k ↔
      HasVertexCoverNumber left right k := by
  constructor
  · rintro ⟨⟨CLeft, CRight, hcover, hk⟩, hmin⟩
    constructor
    · exact ⟨CLeft, CRight,
        fun e => hcover ⟨(left e, right e), e, rfl⟩, hk⟩
    · intro CLeft CRight hcover
      apply hmin CLeft CRight
      rintro ⟨p, e, he⟩
      simpa [← he] using hcover e
  · rintro ⟨⟨CLeft, CRight, hcover, hk⟩, hmin⟩
    constructor
    · refine ⟨CLeft, CRight, ?_, hk⟩
      rintro ⟨p, e, he⟩
      simpa [← he] using hcover e
    · intro CLeft CRight hcover
      apply hmin CLeft CRight
      intro e
      exact hcover ⟨(left e, right e), e, rfl⟩

lemma hasMatchingNumber_incidence_of_simple
    {L : Type uL} {R : Type uR} {E : Type uE} [Finite E]
    (left : E -> L) (right : E -> R) (k : Nat)
    (h : HasMatchingNumber
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.1)
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.2) k) :
    HasMatchingNumber left right k := by
  rcases h with ⟨⟨N, hN, hk⟩, hmax⟩
  constructor
  · refine ⟨endpointRepresentative left right '' N,
      (isEdgeMatching_endpointRepresentative_iff left right N).mp hN, ?_⟩
    rw [ncard_image_endpointRepresentative left right N, hk]
  · intro M hM
    let f : E -> {q : L × R // ∃ e, (left e, right e) = q} :=
      fun e => ⟨(left e, right e), e, rfl⟩
    let MS : Set {q : L × R // ∃ e, (left e, right e) = q} := f '' M
    have hfM : Set.InjOn f M := by
      intro e he e' he' hp
      exact hM.1 he he' (congrArg (fun p => p.1.1) hp)
    have hMS : IsEdgeMatching
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.1)
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.2) MS := by
      constructor
      · rintro _ ⟨e, he, rfl⟩ _ ⟨e', he', rfl⟩ hleft
        congr 1
        exact hM.1 he he' hleft
      · rintro _ ⟨e, he, rfl⟩ _ ⟨e', he', rfl⟩ hright
        congr 1
        exact hM.2 he he' hright
    rw [← Set.InjOn.ncard_image hfM]
    exact hmax MS hMS

lemma hasMatchingNumber_simple_iff_incidence
    {L : Type uL} {R : Type uR} {E : Type uE} [Finite E]
    (left : E -> L) (right : E -> R) (k : Nat) :
    HasMatchingNumber
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.1)
        (fun p : {q : L × R // ∃ e, (left e, right e) = q} => p.1.2) k ↔
      HasMatchingNumber left right k :=
  ⟨hasMatchingNumber_incidence_of_simple left right k,
    hasMatchingNumber_simple_of_incidence left right k⟩

lemma isEdgeMatching_equiv_image_iff
    {L : Type uL} {R : Type uR} {E : Type uE} {E' : Type*}
    (e : E ≃ E') (left : E' -> L) (right : E' -> R) (M : Set E) :
    IsEdgeMatching (left ∘ e) (right ∘ e) M ↔
      IsEdgeMatching left right (e '' M) := by
  rw [IsEdgeMatching, IsEdgeMatching]
  constructor
  · rintro ⟨hl, hr⟩
    constructor
    · rintro _ ⟨x, hx, rfl⟩ _ ⟨y, hy, rfl⟩ h
      exact congrArg e (hl hx hy h)
    · rintro _ ⟨x, hx, rfl⟩ _ ⟨y, hy, rfl⟩ h
      exact congrArg e (hr hx hy h)
  · rintro ⟨hl, hr⟩
    constructor
    · intro x hx y hy h
      apply e.injective
      exact hl (Set.mem_image _ _ _ |>.mpr ⟨x, hx, rfl⟩)
        (Set.mem_image _ _ _ |>.mpr ⟨y, hy, rfl⟩) h
    · intro x hx y hy h
      apply e.injective
      exact hr (Set.mem_image _ _ _ |>.mpr ⟨x, hx, rfl⟩)
        (Set.mem_image _ _ _ |>.mpr ⟨y, hy, rfl⟩) h

lemma ncard_equiv_image {E : Type uE} {E' : Type*}
    (e : E ≃ E') (M : Set E) : (e '' M).ncard = M.ncard := by
  exact Set.ncard_image_of_injective M e.injective

lemma hasMatchingNumber_equiv_iff
    {L : Type uL} {R : Type uR} {E : Type uE} {E' : Type*}
    (e : E ≃ E') (left : E' -> L) (right : E' -> R) (k : Nat) :
    HasMatchingNumber (left ∘ e) (right ∘ e) k ↔
      HasMatchingNumber left right k := by
  constructor
  · rintro ⟨⟨M, hM, hk⟩, hmax⟩
    constructor
    · refine ⟨e '' M,
        (isEdgeMatching_equiv_image_iff e left right M).mp hM, ?_⟩
      rw [ncard_equiv_image e M, hk]
    · intro N hN
      let M : Set E := e ⁻¹' N
      have hMN : e '' M = N := by
        ext y
        simp [M]
      rw [← hMN, ncard_equiv_image e M]
      apply hmax M
      exact (isEdgeMatching_equiv_image_iff e left right M).mpr (hMN ▸ hN)
  · rintro ⟨⟨N, hN, hk⟩, hmax⟩
    let M : Set E := e ⁻¹' N
    have hMN : e '' M = N := by
      ext y
      simp [M]
    constructor
    · refine ⟨M,
        (isEdgeMatching_equiv_image_iff e left right M).mpr (hMN ▸ hN), ?_⟩
      rw [← ncard_equiv_image e M, hMN, hk]
    · intro M' hM'
      rw [← ncard_equiv_image e M']
      exact hmax _ ((isEdgeMatching_equiv_image_iff e left right M').mp hM')

lemma hasVertexCoverNumber_equiv_iff
    {L : Type uL} {R : Type uR} {E : Type uE} {E' : Type*}
    (e : E ≃ E') (left : E' -> L) (right : E' -> R) (k : Nat) :
    HasVertexCoverNumber (left ∘ e) (right ∘ e) k ↔
      HasVertexCoverNumber left right k := by
  constructor
  · rintro ⟨⟨CLeft, CRight, hcover, hk⟩, hmin⟩
    constructor
    · refine ⟨CLeft, CRight, ?_, hk⟩
      intro x
      simpa only [Function.comp_apply, e.apply_symm_apply] using hcover (e.symm x)
    · intro CLeft CRight hcover
      apply hmin CLeft CRight
      intro x
      exact hcover (e x)
  · rintro ⟨⟨CLeft, CRight, hcover, hk⟩, hmin⟩
    constructor
    · refine ⟨CLeft, CRight, ?_, hk⟩
      intro x
      exact hcover (e x)
    · intro CLeft CRight hcover
      apply hmin CLeft CRight
      intro x
      simpa only [Function.comp_apply, e.apply_symm_apply] using hcover (e.symm x)

/-- The simple bipartite-relation formulation obtained by retaining one edge
for each occupied endpoint pair. -/
def SimpleRelationKonigTarget : Prop :=
  ∀ (L : Type uL) (R : Type uR) [Finite L] [Finite R]
    (adj : L -> R -> Prop),
      ∃ k : Nat,
        HasMatchingNumber
            (fun e : {p : L × R // adj p.1 p.2} => e.1.1)
            (fun e : {p : L × R // adj p.1 p.2} => e.1.2) k ∧
          HasVertexCoverNumber
            (fun e : {p : L × R // adj p.1 p.2} => e.1.1)
            (fun e : {p : L × R // adj p.1 p.2} => e.1.2) k

/-- Parallel-edge erasure preserves the theorem. The enlarged edge universe
allows the relation's endpoint-pair subtype to be lifted without restricting
the vertex universes. -/
theorem konigMatchingCoverTarget_iff_simpleRelationKonigTarget :
    KonigMatchingCoverTarget.{uL, uR, uE} ↔
      SimpleRelationKonigTarget.{uL, uR} := by
  constructor
  · intro h L R _ _ adj
    let S := {p : L × R // adj p.1 p.2}
    letI : Finite (L × R) := Finite.of_surjective
      (fun i : Fin (Nat.card L) × Fin (Nat.card R) =>
        ((Finite.equivFin L).symm i.1, (Finite.equivFin R).symm i.2))
      (fun p => ⟨((Finite.equivFin L) p.1, (Finite.equivFin R) p.2), by simp⟩)
    letI : Finite S := Finite.of_injective Subtype.val Subtype.val_injective
    let edgeEquiv : ULift.{uE} (Fin (Nat.card S)) ≃ S :=
      Equiv.ulift.trans (Finite.equivFin S).symm
    let leftS : S -> L := fun e => e.1.1
    let rightS : S -> R := fun e => e.1.2
    rcases h L R (ULift.{uE} (Fin (Nat.card S)))
      (leftS ∘ edgeEquiv) (rightS ∘ edgeEquiv) with
      ⟨k, hmatching, hcover⟩
    refine ⟨k, ?_, ?_⟩
    · exact (hasMatchingNumber_equiv_iff edgeEquiv
        leftS rightS k).mp hmatching
    · exact (hasVertexCoverNumber_equiv_iff edgeEquiv
        leftS rightS k).mp hcover
  · intro h L R E _ _ _ left right
    let adj : L -> R -> Prop := fun l r => ∃ e, (left e, right e) = (l, r)
    rcases h L R adj with ⟨k, hmatching, hcover⟩
    refine ⟨k, ?_, ?_⟩
    · exact (hasMatchingNumber_simple_iff_incidence left right k).mp hmatching
    · exact (hasVertexCoverNumber_simple_iff_incidence left right k).mp hcover

/-! Structural statement mutations. -/

/-- Removed-hypothesis mutation: the edge type need not be finite. -/
def mutationRemovedFiniteEdges : Prop :=
  ∀ (L : Type uL) (R : Type uR) (E : Type uE)
    [Finite L] [Finite R]
    (left : E -> L) (right : E -> R),
      ∃ k : Nat,
        HasMatchingNumber left right k ∧
          HasVertexCoverNumber left right k

/-- Changed-domain mutation: matching size counts incident vertices rather
than edges, which doubles every nonempty matching cardinality. -/
def mutationCountsMatchingVertices : Prop :=
  ∀ (L : Type uL) (R : Type uR) (E : Type uE)
    [Finite L] [Finite R] [Finite E]
    (left : E -> L) (right : E -> R),
      ∃ k : Nat,
        ((∃ M : Set E, IsEdgeMatching left right M ∧ 2 * M.ncard = k) ∧
          ∀ M : Set E, IsEdgeMatching left right M -> 2 * M.ncard ≤ k) ∧
            HasVertexCoverNumber left right k

/-- Changed-scope mutation: one extremal value must work for all endpoint maps
on fixed side and edge types. -/
def mutationChangedEndpointBinderScope : Prop :=
  ∀ (L : Type uL) (R : Type uR) (E : Type uE)
    [Finite L] [Finite R] [Finite E],
      ∃ k : Nat, ∀ (left : E -> L) (right : E -> R),
        HasMatchingNumber left right k ∧
          HasVertexCoverNumber left right k

/-- Boundary mutation: edgeless graphs are excluded. -/
def mutationExcludesEdgelessGraph : Prop :=
  ∀ (L : Type uL) (R : Type uR) (E : Type uE)
    [Finite L] [Finite R] [Finite E] [Nonempty E]
    (left : E -> L) (right : E -> R),
      ∃ k : Nat,
        HasMatchingNumber left right k ∧
          HasVertexCoverNumber left right k

#check_failure
  (rfl : KonigMatchingCoverTarget.{uL, uR, uE} =
    mutationRemovedFiniteEdges.{uL, uR, uE})
#check_failure
  (rfl : KonigMatchingCoverTarget.{uL, uR, uE} =
    mutationCountsMatchingVertices.{uL, uR, uE})
#check_failure
  (rfl : KonigMatchingCoverTarget.{uL, uR, uE} =
    mutationChangedEndpointBinderScope.{uL, uR, uE})
#check_failure
  (rfl : KonigMatchingCoverTarget.{uL, uR, uE} =
    mutationExcludesEdgelessGraph.{uL, uR, uE})

/-- Edgeless graphs, including graphs with isolated vertices on either side,
have matching and vertex-cover number zero. -/
theorem edgelessBoundary
    (L : Type uL) (R : Type uR) [Finite L] [Finite R]
    (left : Empty -> L) (right : Empty -> R) :
    HasMatchingNumber left right 0 ∧ HasVertexCoverNumber left right 0 := by
  constructor
  · constructor
    · exact ⟨∅, by simp [IsEdgeMatching]⟩
    · intro M _
      have hM : M = ∅ := Set.eq_empty_iff_forall_notMem.mpr fun e => nomatch e
      simp [hM]
  · constructor
    · exact ⟨∅, ∅, by simp [IsBipartiteVertexCover]⟩
    · intro CLeft CRight _
      exact Nat.zero_le _

/-- A single edge has matching and vertex-cover number one. -/
theorem singleEdgeBoundary :
    HasMatchingNumber (fun _ : Unit => ()) (fun _ : Unit => ()) 1 ∧
      HasVertexCoverNumber (fun _ : Unit => ()) (fun _ : Unit => ()) 1 := by
  constructor
  · constructor
    · refine ⟨Set.univ, ?_, by simp⟩
      constructor <;> intro a _ b _ _ <;> exact Subsingleton.elim a b
    · intro M _
      simpa using Set.ncard_le_one_of_subsingleton M
  · constructor
    · exact ⟨Set.univ, ∅, by simp [IsBipartiteVertexCover]⟩
    · intro CLeft CRight hCover
      rcases hCover () with hLeft | hRight
      · exact (Nat.one_le_iff_ne_zero.mpr (Set.ncard_ne_zero_of_mem hLeft)).trans
          (Nat.le_add_right _ _)
      · exact (Nat.one_le_iff_ne_zero.mpr (Set.ncard_ne_zero_of_mem hRight)).trans
          (Nat.le_add_left _ _)

#print axioms konigMatchingCoverTarget_iff_expanded
#print axioms konigMatchingCoverTarget_iff_simpleRelationKonigTarget
#print axioms edgelessBoundary
#print axioms singleEdgeBoundary

end Stage1Instances.THM_M_0812

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0812.KonigMatchingCoverTarget
