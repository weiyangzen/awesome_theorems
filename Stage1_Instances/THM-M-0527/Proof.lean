import Statement

/-!
# THM-M-0527 partial proof execution

This module closes the fiber-classification branch of the frozen target. The construction of a
connected cover realizing an arbitrary subgroup remains open and is not postulated here.
-/

namespace Stage1Instances.THM_M_0527

open Topology Filter Set Function

universe u v

noncomputable section

/-- Local homeomorphisms pull local path-connectedness back from their codomain. -/
theorem locPathConnectedSpace_of_isLocalHomeomorph
    {E : Type u} {X : Type v} [TopologicalSpace E] [TopologicalSpace X]
    [LocPathConnectedSpace X] {p : E -> X} (hp : IsLocalHomeomorph p) :
    LocPathConnectedSpace E := by
  refine LocPathConnectedSpace.of_bases
    (ι := Set E) (p := fun e U => U ∈ nhds e ∧ IsPathConnected U)
    (s := fun _ U => U) (fun e => ?_) (fun _ _ hU => hU.2)
  obtain ⟨h, he, rfl⟩ := hp e
  letI : LocPathConnectedSpace h.target := h.open_target.locPathConnectedSpace
  letI : LocPathConnectedSpace h.source :=
    h.toHomeomorphSourceTarget.isOpenEmbedding.locPathConnectedSpace
  have hsource :
      (Filter.map (fun z : h.source => (z : E))
        (nhds (⟨e, he⟩ : h.source))).HasBasis
        (fun U : Set h.source =>
          U ∈ nhds (⟨e, he⟩ : h.source) ∧ IsPathConnected U)
        (fun U => (Subtype.val : h.source -> E) '' U) := by
    simpa using
      (path_connected_basis (⟨e, he⟩ : h.source)).map
        (fun z : h.source => (z : E))
  rw [map_nhds_subtype_val, h.open_source.nhdsWithin_eq he] at hsource
  refine hsource.to_hasBasis ?_ ?_
  · intro U hU
    exact ⟨Subtype.val '' U,
      ⟨hsource.mem_of_mem hU, hU.2.image continuous_subtype_val⟩,
      subset_rfl⟩
  · intro U hU
    rcases hsource.mem_iff.mp hU.1 with ⟨V, hV, hVU⟩
    exact ⟨V, hV, hVU⟩

/-- The total space of a cover of a locally path-connected space is locally path-connected. -/
theorem covering_locPathConnectedSpace
    {E : Type u} {X : Type v} [TopologicalSpace E] [TopologicalSpace X]
    [LocPathConnectedSpace X] {p : E -> X} (hp : IsCoveringMap p) :
    LocPathConnectedSpace E :=
  locPathConnectedSpace_of_isLocalHomeomorph hp.isLocalHomeomorph

namespace PointedConnectedCover

/-- The subgroup-range lifting criterion specialized to two pointed connected covers. -/
theorem comparisonLift
    {X : Type u} [TopologicalSpace X] [LocPathConnectedSpace X] {x0 : X}
    (P Q : PointedConnectedCover X x0)
    (hrange : inducedSubgroup P ≤ inducedSubgroup Q) :
    ∃! f : C(P.E, Q.E), f P.e₀ = Q.e₀ ∧ Q.p ∘ f = P.p := by
  letI : LocPathConnectedSpace P.E := covering_locPathConnectedSpace P.covering_p
  rcases P with ⟨EP, tP, eP, pP, cpP, covP, connP, baseP⟩
  rcases Q with ⟨EQ, tQ, eQ, pQ, cpQ, covQ, connQ, baseQ⟩
  cases baseP
  dsimp only [inducedSubgroup, continuousMap] at hrange ⊢
  apply covQ.existsUnique_continuousMap_lifts_of_range_le
    (f := (⟨pP, cpP⟩ : C(EP, X))) (a₀ := eP) (e₀ := eQ) baseQ
  intro z hz
  rcases hz with ⟨a, rfl⟩
  obtain ⟨p, rfl⟩ := Path.Homotopic.Quotient.mk_surjective a
  apply hrange
  exact ⟨FundamentalGroup.fromPath (.mk p), by
    rw [FundamentalGroup.mapOfEq_apply, FundamentalGroup.map_apply]
    rfl⟩

/-- A pointed covering isomorphism identifies the two induced subgroups. -/
theorem inducedSubgroup_eq_of_isomorphic
    {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P Q : PointedConnectedCover X x₀) (hi : Isomorphic P Q) :
    inducedSubgroup P = inducedSubgroup Q := by
  rcases hi with ⟨h, he0, hover⟩
  apply Subgroup.ext
  intro g
  constructor
  · rintro ⟨a, rfl⟩
    rcases Path.Homotopic.Quotient.mk_surjective a with ⟨a, rfl⟩
    refine ⟨FundamentalGroup.fromPath
      (.mk ((a.map h.continuous).cast he0.symm he0.symm)), ?_⟩
    rw [FundamentalGroup.mapOfEq_apply, FundamentalGroup.mapOfEq_apply]
    congr 2
    apply Path.ext
    funext t
    exact hover (a t)
  · rintro ⟨a, rfl⟩
    rcases Path.Homotopic.Quotient.mk_surjective a with ⟨a, rfl⟩
    have he0symm : h.symm Q.e₀ = P.e₀ := by rw [← he0]; simp
    refine ⟨FundamentalGroup.fromPath
      (.mk ((a.map h.symm.continuous).cast he0symm.symm he0symm.symm)), ?_⟩
    rw [FundamentalGroup.mapOfEq_apply, FundamentalGroup.mapOfEq_apply]
    congr 2
    apply Path.ext
    funext t
    exact (hover (h.symm (a t))).symm.trans
      (congr_arg Q.p (h.apply_symm_apply (a t)))

/-- Projection commutation gives the corresponding equality of induced homomorphisms. -/
theorem inducedMap_naturality
    {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P Q : PointedConnectedCover X x₀) (h : P.E ≃ₜ Q.E)
    (he0 : h P.e₀ = Q.e₀) (hover : ∀ e, Q.p (h e) = P.p e) :
    (FundamentalGroup.mapOfEq Q.continuousMap Q.map_basepoint).comp
        (FundamentalGroup.mapOfEq
          (⟨h, h.continuous⟩ : C(P.E, Q.E)) he0) =
      FundamentalGroup.mapOfEq P.continuousMap P.map_basepoint := by
  apply MonoidHom.ext
  intro a
  rcases Path.Homotopic.Quotient.mk_surjective a with ⟨a, rfl⟩
  rw [MonoidHom.comp_apply, FundamentalGroup.mapOfEq_apply,
    FundamentalGroup.mapOfEq_apply, FundamentalGroup.mapOfEq_apply]
  congr 2
  apply Path.ext
  funext t
  exact hover (a t)

/-- A homeomorphism induces a surjection on fundamental groups, including the endpoint
transport in `mapOfEq`. -/
theorem inducedMap_surjective
    {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P Q : PointedConnectedCover X x₀) (h : P.E ≃ₜ Q.E)
    (he0 : h P.e₀ = Q.e₀) :
    Function.Surjective
      (FundamentalGroup.mapOfEq
        (⟨h, h.continuous⟩ : C(P.E, Q.E)) he0) := by
  intro a
  rcases Path.Homotopic.Quotient.mk_surjective a with ⟨a, rfl⟩
  have he0symm : h.symm Q.e₀ = P.e₀ := by rw [← he0]; simp
  refine ⟨FundamentalGroup.fromPath
    (.mk ((a.map h.symm.continuous).cast he0symm.symm he0symm.symm)), ?_⟩
  rw [FundamentalGroup.mapOfEq_apply]
  congr 2
  apply Path.ext
  funext t
  exact h.apply_symm_apply (a t)

/-- Precomposition by a surjective homomorphism does not change the range. -/
theorem range_eq_of_comp_eq_of_surjective
    {G H K : Type*} [Group G] [Group H] [Group K]
    (f : G →* H) (g : H →* K) (h : G →* K)
    (hcomp : g.comp f = h) (hf : Function.Surjective f) :
    g.range = h.range := by
  ext x
  constructor
  · rintro ⟨y, rfl⟩
    rcases hf y with ⟨z, rfl⟩
    exact ⟨z, (DFunLike.congr_fun hcomp z).symm⟩
  · rintro ⟨z, rfl⟩
    exact ⟨f z, DFunLike.congr_fun hcomp z⟩

/-- The naturality square and homeomorphism-induced surjection identify the subgroup ranges. -/
theorem inducedSubgroup_eq_of_naturality
    {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P Q : PointedConnectedCover X x₀) (h : P.E ≃ₜ Q.E)
    (he0 : h P.e₀ = Q.e₀)
    (hnatural :
      (FundamentalGroup.mapOfEq Q.continuousMap Q.map_basepoint).comp
          (FundamentalGroup.mapOfEq
            (⟨h, h.continuous⟩ : C(P.E, Q.E)) he0) =
        FundamentalGroup.mapOfEq P.continuousMap P.map_basepoint) :
    inducedSubgroup P = inducedSubgroup Q := by
  symm
  exact range_eq_of_comp_eq_of_surjective
    (FundamentalGroup.mapOfEq
      (⟨h, h.continuous⟩ : C(P.E, Q.E)) he0)
    (FundamentalGroup.mapOfEq Q.continuousMap Q.map_basepoint)
    (FundamentalGroup.mapOfEq P.continuousMap P.map_basepoint)
    hnatural
    (inducedMap_surjective P Q h he0)

/-- Naturality of induced maps proves the reverse fiber-classification implication. -/
theorem inducedSubgroup_eq_of_isomorphic_via_naturality
    {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P Q : PointedConnectedCover X x₀) (hi : Isomorphic P Q) :
    inducedSubgroup P = inducedSubgroup Q := by
  rcases hi with ⟨h, he0, hover⟩
  exact inducedSubgroup_eq_of_naturality P Q h he0
    (inducedMap_naturality P Q h he0 hover)

/-- Uniqueness of pointed lifts makes the two comparison maps mutual inverses. -/
theorem comparisonMaps_mutualInverse
    {X : Type u} [TopologicalSpace X] {x0 : X}
    (P Q : PointedConnectedCover X x0)
    (f : C(P.E, Q.E)) (g : C(Q.E, P.E))
    (hf0 : f P.e₀ = Q.e₀) (hg0 : g Q.e₀ = P.e₀)
    (hf : Q.p ∘ f = P.p) (hg : P.p ∘ g = Q.p) :
    Function.LeftInverse g f ∧ Function.RightInverse g f := by
  constructor
  · intro e
    apply congrFun (P.covering_p.eq_of_comp_eq
      (g.continuous.comp f.continuous) continuous_id ?_ P.e₀ ?_) e
    · funext z
      exact (congrFun hg (f z)).trans (congrFun hf z)
    · simp [hf0, hg0]
  · intro e
    apply congrFun (Q.covering_p.eq_of_comp_eq
      (f.continuous.comp g.continuous) continuous_id ?_ Q.e₀ ?_) e
    · funext z
      exact (congrFun hf (g z)).trans (congrFun hg z)
    · simp [hf0, hg0]

/-- Continuous mutual inverses assemble to a homeomorphism. -/
noncomputable def comparisonHomeomorph
    {X : Type u} [TopologicalSpace X] {x0 : X}
    (P Q : PointedConnectedCover X x0)
    (f : C(P.E, Q.E)) (g : C(Q.E, P.E))
    (hgf : Function.LeftInverse g f) (hfg : Function.RightInverse g f) :
    P.E ≃ₜ Q.E :=
  Homeomorph.mk ⟨f, g, hgf, hfg⟩ f.continuous g.continuous

/-- The comparison homeomorphism is a pointed isomorphism over the base. -/
theorem isomorphic_of_comparisonMaps
    {X : Type u} [TopologicalSpace X] {x0 : X}
    (P Q : PointedConnectedCover X x0)
    (f : C(P.E, Q.E)) (g : C(Q.E, P.E))
    (hf0 : f P.e₀ = Q.e₀) (hg0 : g Q.e₀ = P.e₀)
    (hf : Q.p ∘ f = P.p) (hg : P.p ∘ g = Q.p) : Isomorphic P Q := by
  rcases comparisonMaps_mutualInverse P Q f g hf0 hg0 hf hg with ⟨hgf, hfg⟩
  exact ⟨comparisonHomeomorph P Q f g hgf hfg, hf0, congrFun hf⟩

/-- Equal induced subgroups produce a pointed covering isomorphism. -/
theorem isomorphic_of_inducedSubgroup_eq
    {X : Type u} [TopologicalSpace X] [LocPathConnectedSpace X] {x0 : X}
    (P Q : PointedConnectedCover X x0)
    (hrange : inducedSubgroup P = inducedSubgroup Q) : Isomorphic P Q := by
  rcases comparisonLift P Q hrange.le with ⟨f, ⟨hf0, hf⟩, _⟩
  rcases comparisonLift Q P hrange.ge with ⟨g, ⟨hg0, hg⟩, _⟩
  exact isomorphic_of_comparisonMaps P Q f g hf0 hg0 hf hg

/-- Exact fiber criterion used by the second conjunct of the frozen root target. -/
theorem inducedSubgroup_eq_iff_isomorphic
    {X : Type u} [TopologicalSpace X] [LocPathConnectedSpace X] {x0 : X}
    (P Q : PointedConnectedCover X x0) :
    inducedSubgroup P = inducedSubgroup Q ↔ Isomorphic P Q :=
  ⟨isomorphic_of_inducedSubgroup_eq P Q,
    inducedSubgroup_eq_of_isomorphic_via_naturality P Q⟩

end PointedConnectedCover

#print axioms locPathConnectedSpace_of_isLocalHomeomorph
#print axioms covering_locPathConnectedSpace
#print axioms PointedConnectedCover.comparisonLift
#print axioms PointedConnectedCover.inducedSubgroup_eq_of_isomorphic
#print axioms PointedConnectedCover.inducedMap_naturality
#print axioms PointedConnectedCover.inducedMap_surjective
#print axioms PointedConnectedCover.range_eq_of_comp_eq_of_surjective
#print axioms PointedConnectedCover.inducedSubgroup_eq_of_naturality
#print axioms PointedConnectedCover.inducedSubgroup_eq_of_isomorphic_via_naturality
#print axioms PointedConnectedCover.comparisonMaps_mutualInverse
#print axioms PointedConnectedCover.comparisonHomeomorph
#print axioms PointedConnectedCover.isomorphic_of_comparisonMaps
#print axioms PointedConnectedCover.isomorphic_of_inducedSubgroup_eq
#print axioms PointedConnectedCover.inducedSubgroup_eq_iff_isomorphic

end


end Stage1Instances.THM_M_0527
