import ObligationTree
import Mathlib.Probability.IdentDistribIndep
import Mathlib.Probability.Independence.ZeroOne
import Mathlib.Probability.ProductMeasure
import Mathlib.MeasureTheory.Measure.SeparableMeasure
import Mathlib.MeasureTheory.Measure.MeasuredSets
import Mathlib.GroupTheory.Perm.Fin
import Mathlib.Logic.Equiv.Fin.Basic

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal MeasureTheory ProbabilityTheory symmDiff

namespace M1008Search

universe u

/-- The finite-prefix block swap: exchange `0..N` with `N+1..2N+1`, fix the rest. -/
def prefixBlockSwap (N : Nat) : Equiv.Perm Nat :=
  Equiv.Perm.viaFintypeEmbedding (finAddFlip (m := N + 1) (n := N + 1)) Fin.valEmbedding

lemma prefixBlockSwap_apply_left (N : Nat) (i : Nat) (hi : i ≤ N) :
    prefixBlockSwap N i = (N + 1) + i := by
  let f : Fin ((N + 1) + (N + 1)) ↪ Nat := Fin.valEmbedding
  have hi' : i < (N + 1) + (N + 1) := by omega
  let x : Fin ((N + 1) + (N + 1)) := ⟨i, hi'⟩
  have hx : f x = i := by rfl
  rw [show prefixBlockSwap N i = prefixBlockSwap N (f x) by rw [hx], prefixBlockSwap]
  change Equiv.Perm.viaFintypeEmbedding _ Fin.valEmbedding (Fin.valEmbedding x) = _
  exact (Equiv.Perm.viaFintypeEmbedding_apply_image
    (finAddFlip (m := N + 1) (n := N + 1)) Fin.valEmbedding x).trans (by
      change ((finAddFlip (m := N + 1) (n := N + 1)) x : Nat) = _
      rw [finAddFlip_apply_mk_left (by omega)])

lemma prefixBlockSwap_apply_right (N : Nat) (i : Nat)
    (hlo : N + 1 ≤ i) (hhi : i ≤ 2 * N + 1) :
    prefixBlockSwap N i = i - (N + 1) := by
  let f : Fin ((N + 1) + (N + 1)) ↪ Nat := Fin.valEmbedding
  have hi' : i < (N + 1) + (N + 1) := by omega
  let x : Fin ((N + 1) + (N + 1)) := ⟨i, hi'⟩
  have hx : f x = i := by rfl
  rw [show prefixBlockSwap N i = prefixBlockSwap N (f x) by rw [hx], prefixBlockSwap]
  change Equiv.Perm.viaFintypeEmbedding _ Fin.valEmbedding (Fin.valEmbedding x) = _
  exact (Equiv.Perm.viaFintypeEmbedding_apply_image
    (finAddFlip (m := N + 1) (n := N + 1)) Fin.valEmbedding x).trans (by
      change ((finAddFlip (m := N + 1) (n := N + 1)) x : Nat) = _
      rw [finAddFlip_apply_mk_right hlo])

lemma prefixBlockSwap_apply_outside (N : Nat) (i : Nat) (hi : 2 * N + 1 < i) :
    prefixBlockSwap N i = i := by
  rw [prefixBlockSwap, Equiv.Perm.viaFintypeEmbedding_apply_notMem_range]
  intro h
  obtain ⟨x, hx⟩ := h
  have : (x : Nat) < 2 * (N + 1) := by omega
  simp only [Fin.valEmbedding_apply] at hx
  omega

lemma prefixBlockSwap_hasFiniteSupport (N : Nat) :
    Set.Finite {i | prefixBlockSwap N i ≠ i} := by
  apply Set.Finite.subset (Set.finite_Iic (2 * N + 1))
  intro i hi
  simp only [Set.mem_setOf_eq] at hi
  exact not_lt.mp fun h => hi (prefixBlockSwap_apply_outside N i h)

lemma prefixBlockSwap_image_prefix (N : Nat) :
    prefixBlockSwap N '' Set.Iic N = Set.Icc (N + 1) (2 * N + 1) := by
  ext j
  constructor
  · rintro ⟨i, hi, rfl⟩
    simp only [Set.mem_Iic] at hi
    rw [prefixBlockSwap_apply_left N i hi]
    constructor <;> omega
  · intro hj
    simp only [Set.mem_Icc] at hj
    refine ⟨j - (N + 1), by simp only [Set.mem_Iic]; omega, ?_⟩
    rw [prefixBlockSwap_apply_left N (j - (N + 1)) (by omega)]
    omega

lemma prefixBlockSwap_prefix_disjoint (N : Nat) :
    Disjoint (Set.Iic N) (prefixBlockSwap N '' Set.Iic N) := by
  rw [prefixBlockSwap_image_prefix]
  exact Set.Iic_disjoint_Ici.mpr (by omega) |>.mono_right Set.Icc_subset_Ici_self

variable {E : Type u} [MeasurableSpace E]

def reindex (σ : Equiv.Perm Nat) (x : Nat → E) : Nat → E := fun n => x (σ n)

lemma measurable_reindex (σ : Equiv.Perm Nat) : Measurable (reindex (E := E) σ) := by
  exact measurable_pi_lambda _ fun i => measurable_pi_apply (σ i)

omit [MeasurableSpace E] in
lemma cylinder_reindex_preimage (σ : Equiv.Perm Nat) {I : Finset Nat}
    {S : Set (I → E)} :
    reindex (E := E) σ ⁻¹' cylinder I S =
      cylinder (I.preimage σ.symm σ.symm.injective.injOn)
        (((σ.symm.restrictPreimageFinset I).piCongrLeft (fun _ : I => E)) ⁻¹' S) := by
  ext x
  change I.restrict (reindex σ x) ∈ S ↔
    (σ.symm.restrictPreimageFinset I).piCongrLeft (fun _ : I => E)
      ((I.preimage σ.symm σ.symm.injective.injOn).restrict x) ∈ S
  apply iff_of_eq
  congr 1
  funext i
  have hmem : σ i ∈ I.preimage σ.symm σ.symm.injective.injOn := by simp
  have heq : (σ.symm.restrictPreimageFinset I) ⟨σ i, hmem⟩ = i := by
    apply Subtype.ext
    simp
  rw [← heq, Equiv.piCongrLeft_apply_apply]
  simp [Finset.restrict, reindex]

lemma measurableCylinders_reindex_preimage (σ : Equiv.Perm Nat)
    {A : Set (Nat → E)} (hA : A ∈ measurableCylinders (fun _ : Nat => E)) :
    reindex (E := E) σ ⁻¹' A ∈ measurableCylinders (fun _ : Nat => E) := by
  obtain ⟨I, S, hS, rfl⟩ := (mem_measurableCylinders _).1 hA
  rw [cylinder_reindex_preimage]
  exact cylinder_mem_measurableCylinders _ _ (hS.preimage (by fun_prop))

lemma measurableCylinders_measureDense (ν : Measure (Nat → E)) [IsFiniteMeasure ν] :
    ν.MeasureDense (measurableCylinders (fun _ : Nat => E)) := by
  refine Measure.MeasureDense.of_generateFrom_isSetAlgebra_finite ν
    isSetAlgebra_measurableCylinders ?_
  exact generateFrom_measurableCylinders.symm

end M1008Search

namespace M1008Search

variable {E : Type u} [MeasurableSpace E]

/-- Every measurable path event has an initial-cylinder approximation in real measure. -/
lemma exists_initialCylinder_real_symmDiff_lt
    (ν : Measure (Nat → E)) [IsProbabilityMeasure ν]
    {A : Set (Nat → E)} (hA : MeasurableSet A)
    {ε : ℝ} (hε : 0 < ε) :
    ∃ N B, MeasurableSet B ∧ ν.real (A ∆ cylinder (Finset.Iic N) B) < ε := by
  have hεe : 0 < ENNReal.ofReal ε := ENNReal.ofReal_pos.mpr hε
  obtain ⟨C, hC, hAC⟩ := exists_measure_symmDiff_lt_of_generateFrom_isSetRing
    (μ := ν) (C := measurableCylinders (fun _ : Nat => E))
    (isSetRing_measurableCylinders (α := fun _ : Nat => E))
    (by
      refine ⟨{Set.univ}, Set.countable_singleton _, ?_, ?_⟩
      · simpa using univ_mem_measurableCylinders (fun _ : Nat => E)
      · simp)
    generateFrom_measurableCylinders.symm hA hεe
  rw [measurableCylinders_nat] at hC
  simp only [Set.mem_iUnion, Set.mem_singleton_iff] at hC
  obtain ⟨N, B, hB, rfl⟩ := hC
  refine ⟨N, B, hB, ?_⟩
  rw [measureReal_def]
  have hmeasure : ν (A ∆ cylinder (Finset.Iic N) B) < ENNReal.ofReal ε := by
    simpa [symmDiff_comm] using hAC
  have hreal := ENNReal.toReal_lt_toReal (by finiteness) ENNReal.ofReal_ne_top |>.2 hmeasure
  simpa [ENNReal.toReal_ofReal hε.le] using hreal

end M1008Search

namespace M1008Search

variable {Omega : Type*} [MeasurableSpace Omega]

/-- Intersections are Lipschitz for symmetric-difference measure. -/
lemma measureReal_inter_symmDiff_le
    (mu : Measure Omega) [IsFiniteMeasure mu] (s s' t t' : Set Omega)
    (hs : NullMeasurableSet s mu) (hs' : NullMeasurableSet s' mu)
    (ht : NullMeasurableSet t mu) (ht' : NullMeasurableSet t' mu) :
    |mu.real (s ∩ t) - mu.real (s' ∩ t')| ≤
      mu.real (s ∆ s') + mu.real (t ∆ t') := by
  apply (abs_measureReal_sub_le_measureReal_symmDiff
    (hs.inter ht) (hs'.inter ht')).trans
  apply (measureReal_mono ?_ (by finiteness)).trans (measureReal_union_le _ _)
  intro x hx
  simp only [Set.mem_symmDiff, Set.mem_inter_iff, Set.mem_union] at hx ⊢
  rcases hx with ⟨hx, hnot⟩ | ⟨hx, hnot⟩
  · rcases hx with ⟨hsx, htx⟩
    by_cases hs'x : x ∈ s'
    · right; left
      exact ⟨htx, fun ht'x => hnot ⟨hs'x, ht'x⟩⟩
    · left; left
      exact ⟨hsx, hs'x⟩
  · rcases hx with ⟨hs'x, ht'x⟩
    by_cases hsx : x ∈ s
    · right; right
      exact ⟨ht'x, fun htx => hnot ⟨hsx, htx⟩⟩
    · left; right
      exact ⟨hs'x, hsx⟩

/-- Quantitative comparison between a set and two independent approximants. -/
lemma abs_measureReal_sub_square_le
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    {A C D : Set Omega}
    (hA : NullMeasurableSet A mu)
    (hC : NullMeasurableSet C mu) (hD : NullMeasurableSet D mu)
    (hfactor : mu (C ∩ D) = mu C * mu D)
    (hequal : mu C = mu D) :
    |mu.real A - mu.real A * mu.real A| ≤
      mu.real (A ∆ C) + mu.real (A ∆ D) + 2 * mu.real (A ∆ C) := by
  have hinter := measureReal_inter_symmDiff_le mu A C A D hA hC hA hD
  have hproduct : mu.real (C ∩ D) = mu.real C * mu.real D := by
    rw [measureReal_def, hfactor, ENNReal.toReal_mul, measureReal_def, measureReal_def]
  calc
    |mu.real A - mu.real A * mu.real A|
        ≤ |mu.real A - mu.real (C ∩ D)| +
            |mu.real (C ∩ D) - mu.real A * mu.real A| := by
          simpa [Real.dist_eq] using dist_triangle (mu.real A)
            (mu.real (C ∩ D)) (mu.real A * mu.real A)
    _ ≤ (mu.real (A ∆ C) + mu.real (A ∆ D)) + 2 * mu.real (A ∆ C) := by
      gcongr
      · simpa only [Set.inter_self] using hinter
      · rw [hproduct]
        have hreal : mu.real D = mu.real C := by
          simpa only [measureReal_def] using congrArg ENNReal.toReal hequal.symm
        rw [hreal, abs_sub_comm, mul_self_sub_mul_self]
        calc
          |(mu.real A + mu.real C) * (mu.real A - mu.real C)|
              = |mu.real A + mu.real C| * |mu.real A - mu.real C| := abs_mul _ _
          _ ≤ 2 * mu.real (A ∆ C) := by
            rw [abs_of_nonneg (add_nonneg measureReal_nonneg measureReal_nonneg)]
            have hsum : mu.real A + mu.real C ≤ 2 := by
              have hA1 : mu.real A ≤ 1 := measureReal_le_one
              have hC1 : mu.real C ≤ 1 := measureReal_le_one
              linarith
            have hdiff : |mu.real A - mu.real C| ≤ mu.real (A ∆ C) :=
              abs_measureReal_sub_le_measureReal_symmDiff hA hC
            calc
              (mu.real A + mu.real C) * |mu.real A - mu.real C|
                  ≤ 2 * |mu.real A - mu.real C| :=
                    mul_le_mul_of_nonneg_right hsum (abs_nonneg _)
              _ ≤ 2 * mu.real (A ∆ C) :=
                mul_le_mul_of_nonneg_left hdiff (by norm_num)
    _ = _ := by ring

end M1008Search

namespace M1008Search

variable {Omega : Type*} [MeasurableSpace Omega]
variable {E : Type u} [MeasurableSpace E]

/-- Cylinder factorization pulled back to the original sample space. -/
lemma cylinder_pullback_factorization
    {mu : Measure Omega} {X : Nat → Omega → E}
    (hX : iIndepFun X mu) (hXm : ∀ i, AEMeasurable (X i) mu)
    {I J : Finset Nat} (hIJ : Disjoint I J)
    {A : Set (I → E)} {B : Set (J → E)}
    (hA : MeasurableSet A) (hB : MeasurableSet B) :
    mu ((fun omega => I.restrict (fun i => X i omega)) ⁻¹' A ∩
        (fun omega => J.restrict (fun i => X i omega)) ⁻¹' B) =
      mu ((fun omega => I.restrict (fun i => X i omega)) ⁻¹' A) *
        mu ((fun omega => J.restrict (fun i => X i omega)) ⁻¹' B) := by
  exact (iIndepFun.indepFun_finset₀ I J hIJ hX hXm).measure_inter_preimage_eq_mul
    A B hA hB

/-- An iid process has the same probability for a measurable event after reindexing. -/
lemma reindex_preimage_measure_eq
    {mu : Measure Omega} {X : Nat → Omega → E}
    (hX : iIndepFun X mu)
    (hiid : ∀ i j, IdentDistrib (X i) (X j) mu mu)
    (sigma : Equiv.Perm Nat) {A : Set (Nat → E)} (hA : MeasurableSet A) :
    mu ((fun omega => reindex (E := E) sigma (fun i => X i omega)) ⁻¹' A) =
      mu ((fun omega i => X i omega) ⁻¹' A) := by
  have hid : IdentDistrib (fun omega i => X i omega)
      (fun omega i => X (sigma i) omega) mu mu :=
    IdentDistrib.pi (fun i => hiid i (sigma i)) hX (hX.precomp sigma.injective)
  exact (hid.measure_preimage_eq hA).symm

/-- An initial cylinder and its block-swapped copy factorize under an iid path. -/
lemma initialCylinder_pullback_factorization
    {mu : Measure Omega} {X : Nat → Omega → E}
    (hX : iIndepFun X mu) (hXm : ∀ i, AEMeasurable (X i) mu)
    {N : Nat} {B : Set (Finset.Iic N → E)} (hB : MeasurableSet B) :
    mu ((fun omega i => X i omega) ⁻¹' cylinder (Finset.Iic N) B ∩
        (fun omega i => X i omega) ⁻¹'
          (reindex (E := E) (prefixBlockSwap N) ⁻¹' cylinder (Finset.Iic N) B)) =
      mu ((fun omega i => X i omega) ⁻¹' cylinder (Finset.Iic N) B) *
        mu ((fun omega i => X i omega) ⁻¹'
          (reindex (E := E) (prefixBlockSwap N) ⁻¹' cylinder (Finset.Iic N) B)) := by
  let I := Finset.Iic N
  let sigma := prefixBlockSwap N
  let J := I.preimage sigma.symm sigma.symm.injective.injOn
  let movedBase :=
    ((sigma.symm.restrictPreimageFinset I).piCongrLeft (fun _ : I => E)) ⁻¹' B
  have hJ : Disjoint I J := by
    rw [Finset.disjoint_left]
    intro i hi hj
    have hiN : i ≤ N := by simpa [I] using hi
    have hsymmI : sigma.symm i ∈ I := by simpa [J] using hj
    have hs := prefixBlockSwap_apply_left N (sigma.symm i) (by simpa [I] using hsymmI)
    rw [sigma.apply_symm_apply] at hs
    omega
  have hmove : reindex (E := E) sigma ⁻¹' cylinder I B = cylinder J movedBase :=
    cylinder_reindex_preimage sigma
  rw [hmove]
  change mu ((fun omega => I.restrict (fun i => X i omega)) ⁻¹' B ∩
      (fun omega => J.restrict (fun i => X i omega)) ⁻¹' movedBase) = _
  exact cylinder_pullback_factorization hX hXm hJ hB (hB.preimage (by fun_prop))

omit [MeasurableSpace E] in
/-- Symmetry makes a path event equal to its pullback by a supported reindexing. -/
lemma symmetric_reindex_preimage_eq
    {A : Set (Nat → E)}
    (hsymm : ∀ sigma : Equiv.Perm Nat, Set.Finite {i | sigma i ≠ i} →
      ∀ x, x ∈ A ↔ reindex (E := E) sigma x ∈ A)
    (sigma : Equiv.Perm Nat) (hsigma : Set.Finite {i | sigma i ≠ i}) :
    reindex (E := E) sigma ⁻¹' A = A := by
  ext x
  simpa only [Set.mem_preimage] using (hsymm sigma hsigma x).symm

end M1008Search

namespace M1008Search

variable {Omega : Type*} [MeasurableSpace Omega]
variable {E : Type u} [MeasurableSpace E]

/-- The quantitative approximation argument forces idempotence of event probability. -/
lemma symmetric_path_measureReal_factorization
    {mu : Measure Omega} [IsProbabilityMeasure mu]
    {X : Nat → Omega → E}
    (hX : iIndepFun X mu)
    (hiid : ∀ i j, IdentDistrib (X i) (X j) mu mu)
    {A : Set (Nat → E)} (hA : MeasurableSet A)
    (hsymm : ∀ sigma : Equiv.Perm Nat, Set.Finite {i | sigma i ≠ i} →
      ∀ x, x ∈ A ↔ reindex (E := E) sigma x ∈ A) :
    mu.real ((fun omega i => X i omega) ⁻¹' A) =
      mu.real ((fun omega i => X i omega) ⁻¹' A) *
        mu.real ((fun omega i => X i omega) ⁻¹' A) := by
  let path : Omega → Nat → E := fun omega i => X i omega
  let eventPreimage := path ⁻¹' A
  have hXm : ∀ i, AEMeasurable (X i) mu := fun i => (hiid i i).aemeasurable_fst
  have hpath : AEMeasurable path mu := aemeasurable_pi_iff.2 hXm
  have hnull : NullMeasurableSet eventPreimage mu :=
    hpath.nullMeasurableSet_preimage hA
  let nu := mu.map path
  letI : IsProbabilityMeasure nu := Measure.isProbabilityMeasure_map hpath
  apply eq_of_sub_eq_zero
  apply abs_eq_zero.mp
  apply le_antisymm ?_ (abs_nonneg _)
  apply le_of_forall_pos_le_add
  intro epsilon hepsilon
  obtain ⟨N, B, hB, hBA⟩ :=
    exists_initialCylinder_real_symmDiff_lt nu hA (show 0 < epsilon / 4 by positivity)
  let sigma := prefixBlockSwap N
  let cylinderEvent := path ⁻¹' cylinder (Finset.Iic N) B
  let movedCylinder := path ⁻¹' (reindex (E := E) sigma ⁻¹' cylinder (Finset.Iic N) B)
  have hcylMeas : MeasurableSet (cylinder (α := fun _ : Nat => E) (Finset.Iic N) B) :=
    hB.cylinder (Finset.Iic N)
  have hmovedMeas : MeasurableSet
      (reindex (E := E) sigma ⁻¹' cylinder (Finset.Iic N) B) :=
    hcylMeas.preimage (measurable_reindex sigma)
  have hcylNull : NullMeasurableSet cylinderEvent mu :=
    hpath.nullMeasurableSet_preimage hcylMeas
  have hmovedNull : NullMeasurableSet movedCylinder mu :=
    hpath.nullMeasurableSet_preimage hmovedMeas
  have hfactor : mu (cylinderEvent ∩ movedCylinder) =
      mu cylinderEvent * mu movedCylinder :=
    initialCylinder_pullback_factorization hX hXm hB
  have hequal : mu cylinderEvent = mu movedCylinder := by
    symm
    exact reindex_preimage_measure_eq hX hiid sigma hcylMeas
  have hsigma : Set.Finite {i | sigma i ≠ i} := prefixBlockSwap_hasFiniteSupport N
  have hAinv : reindex (E := E) sigma ⁻¹' A = A :=
    symmetric_reindex_preimage_eq hsymm sigma hsigma
  have hCerror : mu.real (eventPreimage ∆ cylinderEvent) < epsilon / 4 := by
    have hmap : nu.real (A ∆ cylinder (Finset.Iic N) B) =
        mu.real (eventPreimage ∆ cylinderEvent) := by
      rw [Measure.real, Measure.real, Measure.map_apply_of_aemeasurable hpath
        (hA.symmDiff hcylMeas)]
      rfl
    rwa [← hmap]
  have hDerror : mu.real (eventPreimage ∆ movedCylinder) < epsilon / 4 := by
    have hset : eventPreimage ∆ movedCylinder =
        path ⁻¹' (reindex (E := E) sigma ⁻¹'
          (A ∆ cylinder (Finset.Iic N) B)) := by
      ext omega
      simp only [Set.mem_symmDiff, Set.mem_preimage]
      have hinv := hsymm sigma hsigma (path omega)
      tauto
    rw [hset, Measure.real]
    have heqMeasure : mu (path ⁻¹' (reindex (E := E) sigma ⁻¹'
        (A ∆ cylinder (Finset.Iic N) B))) =
        mu (path ⁻¹' (A ∆ cylinder (Finset.Iic N) B)) := by
      simpa [path, Set.preimage_preimage] using
        (reindex_preimage_measure_eq hX hiid sigma (hA.symmDiff hcylMeas))
    rw [heqMeasure]
    have hmap : mu (path ⁻¹' (A ∆ cylinder (Finset.Iic N) B)) =
        nu (A ∆ cylinder (Finset.Iic N) B) :=
      (Measure.map_apply_of_aemeasurable hpath (hA.symmDiff hcylMeas)).symm
    rw [hmap]
    exact hBA
  have hbound := abs_measureReal_sub_square_le mu hnull hcylNull hmovedNull hfactor hequal
  have hsmall :
      mu.real (eventPreimage ∆ cylinderEvent) +
          mu.real (eventPreimage ∆ movedCylinder) +
            2 * mu.real (eventPreimage ∆ cylinderEvent) < epsilon := by
    linarith
  have hlt : |mu.real eventPreimage - mu.real eventPreimage * mu.real eventPreimage| < epsilon :=
    hbound.trans_lt hsmall
  have hfinal : |mu.real eventPreimage - mu.real eventPreimage * mu.real eventPreimage| ≤
      0 + epsilon := by simpa using hlt.le
  simpa [eventPreimage, path] using hfinal

end M1008Search

namespace Stage1Instances.THM_M_1008

open M1008Search

/-- Hewitt-Savage zero-one law for measurable finite-permutation-invariant iid path events. -/
theorem hewittSavageZeroOneTarget : HewittSavageZeroOneTarget := by
  intro Omega E _ _ mu _ X event hX hiid hA hsymm
  have hidem := symmetric_path_measureReal_factorization hX hiid hA
    (fun sigma hsigma x => hsymm sigma hsigma x)
  have hcases : mu.real (processPath X ⁻¹' event) = 0 ∨
      mu.real (processPath X ⁻¹' event) = 1 := by
    apply eq_zero_or_one_of_sq_eq_self
    simpa [pow_two] using hidem.symm
  rcases hcases with hzero | hone
  · left
    have hfinite : mu (processPath X ⁻¹' event) ≠ ∞ := by finiteness
    simpa [measureReal_def, ENNReal.toReal_eq_zero_iff, hfinite] using hzero
  · right
    simpa [measureReal_def] using
      (ENNReal.toReal_eq_one_iff (mu (processPath X ⁻¹' event))).mp
        (by simpa [measureReal_def] using hone)

#print axioms hewittSavageZeroOneTarget

end Stage1Instances.THM_M_1008
