import ExternalInvoke
import Statement

open Filter Function MeasureTheory
open scoped BigOperators Matrix.Norms.L2Operator

noncomputable section

universe u v

namespace Stage1Instances.THM_M_1056

abbrev Euclid (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E] := EuclideanSpace Real (Fin (dE (E := E)))

/-- The exact remaining bridge: measurable coordinate projections for a
measurable internal direct sum.  Its output is everywhere measurable, while
the algebraic laws are only required on the conull internal-sum set. -/
def MeasurableObliqueProjectionPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E]
    (mu : Measure Omega) (k : Nat)
    (V : Fin k -> Omega -> Submodule Real (Euclid E)),
    (forall i, ErgodicTheory.MeasurableSubspace (fun omega => V i omega)) ->
    (∀ᵐ omega ∂mu, DirectSum.IsInternal (fun i => V i omega)) ->
    exists P : Omega -> Fin k -> Euclid E →L[Real] Euclid E,
      (forall i, StronglyMeasurable (fun omega => P omega i)) /\
      ∀ᵐ omega ∂mu,
        (forall i y, P omega i y ∈ V i omega) /\
        (forall i y, y ∈ V i omega -> P omega i y = y) /\
        (forall i j, i ≠ j ->
          (P omega i).comp (P omega j) = 0) /\
        (∑ i, P omega i) = ContinuousLinearMap.id Real (Euclid E)

variable {Omega : Type u} [MeasurableSpace Omega]
variable {mu : Measure Omega} [IsProbabilityMeasure mu]
variable {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
variable [FiniteDimensional Real E]

noncomputable def pullbackProjection
    (Q : Euclid E →L[Real] Euclid E) : E →L[Real] E :=
  (coordEquiv (E := E)).symm.toContinuousLinearMap.comp
    (Q.comp (coordEquiv (E := E)).toContinuousLinearMap)

theorem pullbackProjection_apply (Q : Euclid E →L[Real] Euclid E) (x : E) :
    pullbackProjection Q x =
      (coordEquiv (E := E)).symm (Q (coordEquiv (E := E) x)) := by
  rfl

theorem pullbackProjection_comp (Q R : Euclid E →L[Real] Euclid E) :
    (pullbackProjection Q).comp (pullbackProjection R) =
      pullbackProjection (Q.comp R) := by
  ext x
  simp [pullbackProjection]

theorem pullbackProjection_zero :
    pullbackProjection (0 : Euclid E →L[Real] Euclid E) = 0 := by
  ext x
  simp [pullbackProjection]

theorem pullbackProjection_id :
    pullbackProjection (ContinuousLinearMap.id Real (Euclid E)) =
      ContinuousLinearMap.id Real E := by
  ext x
  simp [pullbackProjection]

theorem pullbackProjection_sum {k : Nat} (Q : Fin k -> Euclid E →L[Real] Euclid E) :
    pullbackProjection (∑ i, Q i) = ∑ i, pullbackProjection (Q i) := by
  ext x
  simp [pullbackProjection, map_sum]

theorem stronglyMeasurable_pullbackProjection
    {F : Omega -> Euclid E →L[Real] Euclid E}
    (hF : StronglyMeasurable F) :
    StronglyMeasurable (fun omega => pullbackProjection (F omega)) := by
  let post : (Euclid E →L[Real] Euclid E) →L[Real]
      Euclid E →L[Real] E :=
    (ContinuousLinearMap.compL Real (Euclid E) (Euclid E) E)
      (coordEquiv (E := E)).symm.toContinuousLinearMap
  let pre : (Euclid E →L[Real] E) →L[Real] E →L[Real] E :=
    (ContinuousLinearMap.compL Real E (Euclid E) E).flip
      (coordEquiv (E := E)).toContinuousLinearMap
  have hp := post.continuous.comp_stronglyMeasurable hF
  have hq := pre.continuous.comp_stronglyMeasurable hp
  simpa only [post, pre, ContinuousLinearMap.compL_apply,
    ContinuousLinearMap.flip_apply, pullbackProjection] using hq

theorem external_cocycle_eq_matrixCocycle
    (B : Omega -> Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real)
    (T : Omega -> Omega) (n : Nat) (omega : Omega) :
    ErgodicTheory.cocycle B T n omega = matrixCocycle (E := E) B T n omega := by
  induction n generalizing omega with
  | zero => rfl
  | succ n ih =>
      rw [ErgodicTheory.cocycle_succ, matrixCocycle_succ, ih]

theorem target_cocycleVector_eq
    (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E)
    (n : Nat) (omega : Omega) (x : E) :
    Stage1Instances.THM_M_1056.cocycleVector T A n omega x =
      bridgeCocycleVector T A n omega x := by
  induction n generalizing omega x with
  | zero => rfl
  | succ n ih =>
      rw [Stage1Instances.THM_M_1056.cocycleVector, bridgeCocycleVector]
      rw [ih]

theorem equivariance_of_ranges
    {k : Nat} (T : Omega → Omega) (A : Omega → E ≃L[Real] E)
    (V : Fin k → Omega → Submodule Real (Euclid E))
    (P : Omega → Fin k → Euclid E →L[Real] Euclid E)
    (omega : Omega)
    (hrange : ∀ (i : Fin k) (y : Euclid E), P omega i y ∈ V i omega)
    (hfixT : ∀ (i : Fin k) (y : Euclid E),
      y ∈ V i (T omega) → P (T omega) i y = y)
    (hdisjT : ∀ (i j : Fin k), i ≠ j →
      (P (T omega) i).comp (P (T omega) j) = 0)
    (hsum : (∑ i, P omega i) = ContinuousLinearMap.id Real (Euclid E))
    (hmap : ∀ i, Submodule.map
      (Matrix.toEuclideanCLM (𝕜 := Real) (matrixGenerator A omega)).toLinearMap
        (V i omega) = V i (T omega)) :
    ∀ i,
      (Matrix.toEuclideanCLM (𝕜 := Real) (matrixGenerator A omega)).comp (P omega i) =
        (P (T omega) i).comp
          (Matrix.toEuclideanCLM (𝕜 := Real) (matrixGenerator A omega)) := by
  intro i
  let L := Matrix.toEuclideanCLM (𝕜 := Real) (matrixGenerator A omega)
  apply ContinuousLinearMap.ext
  intro y
  have hdecomp : y = ∑ j, P omega j y := by
    have := congrArg (fun Q : Euclid E →L[Real] Euclid E => Q y) hsum
    simpa using this.symm
  change L (P omega i y) = P (T omega) i (L y)
  symm
  calc
    P (T omega) i (L y) =
        P (T omega) i (L (∑ j, P omega j y)) := by rw [← hdecomp]
    _ = ∑ j, P (T omega) i (L (P omega j y)) := by simp
    _ = P (T omega) i (L (P omega i y)) := by
      rw [Finset.sum_eq_single i]
      · intro j _ hji
        have hjmem : L (P omega j y) ∈ V j (T omega) := by
          rw [← hmap j]
          exact ⟨P omega j y, hrange j y, rfl⟩
        have hjfix := hfixT j _ hjmem
        have hc := congrArg (fun Q : Euclid E →L[Real] Euclid E => Q (L (P omega j y)))
          (hdisjT i j hji.symm)
        simpa [hjfix] using hc
      · simp
    _ = L (P omega i y) := by
      apply hfixT i
      rw [← hmap i]
      exact ⟨P omega i y, hrange i y, rfl⟩

theorem count_pos_of_internal_nonzero
    {k : Nat} (V : Fin k → Omega → Submodule Real (Euclid E))
    (hE : 0 < Module.finrank Real E)
    (hgood : ∀ᵐ omega ∂mu,
      DirectSum.IsInternal (fun i => V i omega) ∧
      (∀ i, V i omega ≠ ⊥)) :
    0 < k := by
  by_contra hk
  have hk0 : k = 0 := Nat.eq_zero_of_not_pos hk
  obtain ⟨omega, hinternal, _⟩ := hgood.exists
  subst k
  have htop : (⊥ : Submodule Real (Euclid E)) = ⊤ := by
    letI : IsEmpty (Fin 0) := ⟨Fin.elim0⟩
    simpa only [iSup_of_empty] using hinternal.submodule_iSup_eq_top
  have hEuclid : 0 < Module.finrank Real (Euclid E) := by
    simpa [Euclid, dE] using hE
  letI : Nontrivial (Euclid E) := Module.nontrivial_of_finrank_pos hEuclid
  exact bot_ne_top htop

theorem pullbackProjection_idempotent_of_range_fix
    (Q : Euclid E →L[Real] Euclid E) (V : Submodule Real (Euclid E))
    (hrange : ∀ y, Q y ∈ V) (hfix : ∀ y, y ∈ V → Q y = y) :
    (pullbackProjection Q).comp (pullbackProjection Q) = pullbackProjection Q := by
  rw [pullbackProjection_comp]
  congr 1
  apply ContinuousLinearMap.ext
  intro y
  exact hfix _ (hrange y)

theorem pullbackProjection_disjoint_of_disjoint
    (Q R : Euclid E →L[Real] Euclid E) (h : Q.comp R = 0) :
    (pullbackProjection Q).comp (pullbackProjection R) = 0 := by
  rw [pullbackProjection_comp, h, pullbackProjection_zero]

theorem pullbackProjection_nonzero_of_submodule
    (Q : Euclid E →L[Real] Euclid E) (V : Submodule Real (Euclid E))
    (hfix : ∀ y, y ∈ V → Q y = y) (hV : V ≠ ⊥) :
    pullbackProjection Q ≠ 0 := by
  obtain ⟨y, hyV, hy0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hV
  intro hzero
  have happ := congrArg (fun L : E →L[Real] E => L ((coordEquiv (E := E)).symm y)) hzero
  simp only [pullbackProjection_apply, ContinuousLinearMap.zero_apply,
    (coordEquiv (E := E)).apply_symm_apply, hfix y hyV] at happ
  apply hy0
  apply (coordEquiv (E := E)).symm.injective
  simpa using happ

theorem pullbackProjection_sum_eq_id
    {k : Nat} (Q : Fin k → Euclid E →L[Real] Euclid E)
    (hsum : (∑ i, Q i) = ContinuousLinearMap.id Real (Euclid E)) :
    (∑ i, pullbackProjection (Q i)) = ContinuousLinearMap.id Real E := by
  rw [← pullbackProjection_sum, hsum, pullbackProjection_id]

theorem oseledets_target_of_projection_package
    (hproj : MeasurableObliqueProjectionPackage.{u, v}) :
    Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget.{u, v} := by
  intro Omega _ mu _ E _ _ _ _ _ hE T hT A hA hint hint'
  have hintS : Integrable (fun omega => bridgeLogPlus ‖(A omega).toContinuousLinearMap‖) mu := by
    simpa only [Stage1Instances.THM_M_1056.logPlus, bridgeLogPlus] using hint
  have hintS' : Integrable (fun omega => bridgeLogPlus ‖(A omega).symm.toContinuousLinearMap‖) mu := by
    simpa only [Stage1Instances.THM_M_1056.logPlus, bridgeLogPlus] using hint'
  obtain ⟨k, lambda, V, hlambda, hVmeas, hsplit⟩ :=
    external_oseledets_on_arbitrary_fiber_coordinates T hT A hA hintS hintS'
  have hinternal : ∀ᵐ omega ∂mu, DirectSum.IsInternal (fun i => V i omega) :=
    hsplit.mono fun _ h => h.1
  obtain ⟨P, hPmeas, hPlaws⟩ := hproj Omega E mu k V hVmeas hinternal
  let projection : Omega -> Fin k -> E →L[Real] E :=
    fun omega i => pullbackProjection (P omega i)
  refine ⟨{
    count := k
    count_pos := count_pos_of_internal_nonzero V hE (hsplit.mono fun _ h => ⟨h.1, h.2.1⟩)
    exponent := lambda
    exponent_strict := hlambda
    projection := projection
    projection_measurable := fun i => stronglyMeasurable_pullbackProjection (hPmeas i)
    projection_idempotent := ?_
    projection_disjoint := ?_
    projection_sum := ?_
    projection_nonzero := ?_
    equivariant := ?_
    growth := ?_
  }⟩
  · filter_upwards [hPlaws] with omega hP
    intro i
    exact pullbackProjection_idempotent_of_range_fix
      (P omega i) (V i omega) (hP.1 i) (hP.2.1 i)
  · filter_upwards [hPlaws] with omega hP
    intro i j hij
    exact pullbackProjection_disjoint_of_disjoint _ _ (hP.2.2.1 i j hij)
  · filter_upwards [hPlaws] with omega hP
    exact pullbackProjection_sum_eq_id (fun i => P omega i) hP.2.2.2
  · filter_upwards [hPlaws, hsplit] with omega hP hs
    intro i
    exact pullbackProjection_nonzero_of_submodule
      (P omega i) (V i omega) (hP.2.1 i) (hs.2.1 i)
  · have hsplitT : ∀ᵐ omega ∂mu,
        DirectSum.IsInternal (fun i => V i (T omega)) := by
      exact hT.toMeasurePreserving.quasiMeasurePreserving.tendsto_ae.eventually hinternal
    filter_upwards [hPlaws, hsplit, hPlaws.filter_mono
      hT.toMeasurePreserving.quasiMeasurePreserving.tendsto_ae, hsplitT]
      with omega hP hs hPT _
    intro i
    have hcoord := equivariance_of_ranges T A V P omega
      hP.1 hPT.2.1 hPT.2.2.1 hP.2.2.2
      hs.2.2.1 i
    apply ContinuousLinearMap.ext
    intro x
    apply (coordEquiv (E := E)).injective
    simpa [projection, pullbackProjection, matrixGenerator,
      toEuclideanCLM_matrixOfCLM, conjugateCLM_apply] using
      congrArg (fun L : Euclid E →L[Real] Euclid E => L (coordEquiv (E := E) x)) hcoord
  · filter_upwards [hPlaws, hsplit] with omega hP hs
    intro i x hx hfix
    have hcoordfix : P omega i (coordEquiv (E := E) x) = coordEquiv (E := E) x := by
      apply (coordEquiv (E := E)).symm.injective
      simpa [projection, pullbackProjection] using hfix
    have hxV : coordEquiv (E := E) x ∈ V i omega := by
      rw [← hcoordfix]
      exact hP.1 i _
    have hcoordne : coordEquiv (E := E) x ≠ 0 := by
      intro hzero
      apply hx
      apply (coordEquiv (E := E)).injective
      simpa using hzero
    have hgrowth := (hs.2.2.2 i (coordEquiv (E := E) x) hxV
      hcoordne).1
    have hgrowth' : Tendsto
        (fun n : Nat => (n : Real)⁻¹ *
          Real.log ‖Matrix.toEuclideanCLM (𝕜 := Real)
            (matrixCocycle (matrixGenerator A) T n omega)
            (coordEquiv (E := E) x)‖)
        atTop (nhds (lambda i)) := by
      simpa only [external_cocycle_eq_matrixCocycle] using hgrowth
    have htarget := (tendsto_growth_coordinate_iff T A omega x hx (lambda i)).mp hgrowth'
    simpa only [target_cocycleVector_eq] using htarget

end Stage1Instances.THM_M_1056

