import ObligationTree
import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1029 proof-phase bodies

This module proves algebraic and conditional-moment consequences of the two
martingale hypotheses, the zero-elapsed increment case, Gaussian
identification from a characteristic function, and exact conditional
composition interfaces. It deliberately leaves the strict-positive-time
Gaussianity and independence argument as an explicit premise: the pinned
library has no continuous-martingale stochastic-calculus bridge that proves it.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1029.Proof

universe u

/-- Deterministic time, viewed as a process on any sample space. -/
def DeterministicTimeProcess {Omega : Type u} : RealProcess Omega :=
  fun t _ => (t : Real)

/-- A square process compensated by a candidate bracket process. -/
def BracketCompensated {Omega : Type u}
    (X A : RealProcess Omega) : RealProcess Omega :=
  fun t omega => X t omega ^ 2 - A t omega

/-- Compensation by deterministic time is the frozen quadratic compensation. -/
theorem bracketCompensated_deterministicTime_eq
    {Omega : Type u} (X : RealProcess Omega) :
    BracketCompensated X (DeterministicTimeProcess : RealProcess Omega) =
      QuadraticCompensated X := by
  rfl

/-- Deterministic time has continuous paths. -/
theorem deterministicTimeProcess_continuousPaths {Omega : Type u} :
    forall omega : Omega, Continuous fun t : Time =>
      (DeterministicTimeProcess : RealProcess Omega) t omega := by
  intro _
  exact continuous_subtype_val

/-- Deterministic time is pathwise monotone. -/
theorem deterministicTimeProcess_monotonePaths {Omega : Type u} :
    forall omega : Omega, Monotone fun t : Time =>
      (DeterministicTimeProcess : RealProcess Omega) t omega := by
  intro _ s t hst
  exact_mod_cast hst

/-- Deterministic time starts at zero almost everywhere. -/
theorem deterministicTimeProcess_startsAtZero {Omega : Type u}
    [MeasurableSpace Omega] (P : Measure Omega) :
    (DeterministicTimeProcess : RealProcess Omega) 0 =ᵐ[P] 0 := by
  rfl

/-- The quadratic-martingale hypothesis is deterministic-bracket compensation. -/
theorem bracketCompensated_martingale_of_quadratic
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega}
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega}
    (hquadratic : Martingale (QuadraticCompensated X) F P) :
    Martingale
      (BracketCompensated X (DeterministicTimeProcess : RealProcess Omega)) F P := by
  simpa [BracketCompensated, DeterministicTimeProcess, QuadraticCompensated] using hquadratic

/-- The compensated-square process is strongly adapted. -/
theorem quadraticCompensated_stronglyAdapted
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega}
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega}
    (hquadratic : Martingale (QuadraticCompensated X) F P) :
    StronglyAdapted F (QuadraticCompensated X) :=
  hquadratic.stronglyAdapted

/-- Squaring preserves strong adaptedness for the real martingale. -/
theorem square_stronglyAdapted
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega}
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega}
    (hmartingale : Martingale X F P) :
    StronglyAdapted F (fun t omega => X t omega ^ 2) := by
  simpa only [pow_two] using hmartingale.stronglyAdapted.mul hmartingale.stronglyAdapted

/-- The two hypotheses force deterministic time to be strongly adapted. -/
theorem deterministicTime_stronglyAdapted_of_martingales
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega}
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega}
    (hmartingale : Martingale X F P)
    (hquadratic : Martingale (QuadraticCompensated X) F P) :
    StronglyAdapted F (DeterministicTimeProcess : RealProcess Omega) := by
  have hdiff := (square_stronglyAdapted hmartingale).sub
    hquadratic.stronglyAdapted
  convert hdiff using 1
  funext t omega
  simp [DeterministicTimeProcess, QuadraticCompensated]

/-- The compensated-square martingale makes every coordinate square integrable. -/
theorem quadratic_coordinate_integrable
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega}
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega} [IsFiniteMeasure P]
    (hquadratic : Martingale (QuadraticCompensated X) F P) (t : Time) :
    Integrable (fun omega => X t omega ^ 2) P := by
  have hsum : Integrable
      (fun omega => QuadraticCompensated X t omega + (t : Real)) P :=
    (hquadratic.integrable t).add (integrable_const (t : Real))
  convert hsum using 1
  funext omega
  simp [QuadraticCompensated]

/-- Every process coordinate belongs to L2. -/
theorem coordinate_memLp_two
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} [IsFiniteMeasure P]
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega}
    (hmartingale : Martingale X F P)
    (hquadratic : Martingale (QuadraticCompensated X) F P) (t : Time) :
    MemLp (X t) 2 P := by
  refine (memLp_two_iff_integrable_sq ?_).2 ?_
  · exact (hmartingale.integrable t).aestronglyMeasurable
  · exact quadratic_coordinate_integrable hquadratic t

/-- Every increment belongs to L2. -/
theorem increment_memLp_two
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} [IsFiniteMeasure P]
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega}
    (hmartingale : Martingale X F P)
    (hquadratic : Martingale (QuadraticCompensated X) F P) (s t : Time) :
    MemLp (fun omega => X t omega - X s omega) 2 P := by
  exact (coordinate_memLp_two hmartingale hquadratic t).sub
    (coordinate_memLp_two hmartingale hquadratic s)

/-- Every squared increment is integrable. -/
theorem increment_square_integrable
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} [IsFiniteMeasure P]
    {F : Filtration Time (inferInstance : MeasurableSpace Omega)}
    {X : RealProcess Omega}
    (hmartingale : Martingale X F P)
    (hquadratic : Martingale (QuadraticCompensated X) F P) (s t : Time) :
    Integrable (fun omega => (X t omega - X s omega) ^ 2) P := by
  exact (memLp_two_iff_integrable_sq
    ((hmartingale.integrable t).sub (hmartingale.integrable s)).aestronglyMeasurable).1
      (increment_memLp_two hmartingale hquadratic s t)

/-- Every future increment has conditional mean zero given the past. -/
theorem increment_condExp_eq_zero
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega) (hmartingale : Martingale X F P)
    {s t : Time} (hst : s <= t) :
    P[fun omega => X t omega - X s omega | F s] =ᵐ[P] 0 := by
  have hsub := condExp_sub
    (hmartingale.integrable t) (hmartingale.integrable s) (F s)
  have hxt := hmartingale.condExp_ae_eq hst
  have hxs : P[X s | F s] = X s :=
    condExp_of_stronglyMeasurable (F.le s)
      (hmartingale.stronglyMeasurable s) (hmartingale.integrable s)
  filter_upwards [hsub, hxt] with omega hsubo hxto
  simp only [Pi.sub_apply] at hsubo
  change P[X t - X s | F s] omega = (0 : Omega -> Real) omega
  rw [hsubo, hxto, hxs]
  simp

/-- Every future increment has conditional second moment equal to elapsed time. -/
theorem increment_condExp_sq
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega)
    (hmartingale : Martingale X F P)
    (hquadratic : Martingale (QuadraticCompensated X) F P)
    {s t : Time} (hst : s <= t) :
    P[fun omega => (X t omega - X s omega) ^ 2 | F s] =ᵐ[P]
      fun _ => ((t - s : Time) : Real) := by
  have hsq (r : Time) : Integrable (fun omega => X r omega ^ 2) P :=
    quadratic_coordinate_integrable hquadratic r
  have hlp (r : Time) : MemLp (X r) 2 P :=
    coordinate_memLp_two hmartingale hquadratic r
  have hcross : Integrable (X t * X s) P := (hlp t).integrable_mul (hlp s)
  have hcross2 : Integrable (fun omega => 2 * (X t * X s) omega) P :=
    hcross.const_mul 2
  have hsplit := condExp_sub (hsq t) (integrable_const (t : Real)) (F s)
  have hq := hquadratic.condExp_ae_eq hst
  have hxt := hmartingale.condExp_ae_eq hst
  have hmul := condExp_mul_of_stronglyMeasurable_right
    (hmartingale.stronglyMeasurable s) hcross (hmartingale.integrable t)
  have hmain1 := condExp_add ((hsq t).sub hcross2) (hsq s) (F s)
  have hmain2 := condExp_sub (hsq t) hcross2 (F s)
  have hscalar := condExp_smul (μ := P) (m := F s) (2 : Real) (X t * X s)
  filter_upwards [hq, hsplit, hxt, hmul, hmain1, hmain2, hscalar] with
    omega hqo hsplito hxto hmulo hm1o hm2o hscalo
  simp only [QuadraticCompensated, Pi.sub_apply, Pi.mul_apply,
    condExp_const (F.le s)] at hqo hsplito hxto hmulo hm1o hm2o hscalo
  simp only [Pi.smul_apply, smul_eq_mul] at hscalo
  rw [show (fun omega => (X t omega - X s omega) ^ 2) =
      ((fun omega => X t omega ^ 2) - (fun omega => 2 * (X t * X s) omega) +
        (fun omega => X s omega ^ 2)) by
        funext omega
        change (X t omega - X s omega) ^ 2 =
          X t omega ^ 2 - 2 * (X t omega * X s omega) + X s omega ^ 2
        ring]
  change P[((fun omega => X t omega ^ 2) -
      (fun omega => 2 * (X t omega * X s omega)) +
      (fun omega => X s omega ^ 2)) | F s] omega = _
  rw [hm1o]
  simp only [Pi.add_apply]
  rw [hm2o]
  change P[fun omega => X t omega ^ 2 | F s] omega -
      P[(2 : Real) • (X t * X s) | F s] omega +
      P[fun omega => X s omega ^ 2 | F s] omega = _
  rw [hscalo, hmulo, hxto]
  have hss : P[fun omega => X s omega ^ 2 | F s] =
      fun omega => X s omega ^ 2 :=
    condExp_of_stronglyMeasurable (F.le s)
      ((hmartingale.stronglyMeasurable s).pow 2) (hsq s)
  rw [hss]
  have ht2 : P[fun omega => X t omega ^ 2 | F s] omega =
      X s omega ^ 2 + (t : Real) - (s : Real) := by
    have hconst : P[fun _ : Omega => (t : Real) | F s] omega = (t : Real) := by
      rw [condExp_const (F.le s)]
    change P[fun omega => X t omega ^ 2 - (t : Real) | F s] omega =
      X s omega ^ 2 - (s : Real) at hqo
    have hsubpoint : P[fun omega => X t omega ^ 2 - (t : Real) | F s] omega =
        P[(fun omega => X t omega ^ 2) -
          (fun _ : Omega => (t : Real)) | F s] omega := rfl
    calc
      P[fun omega => X t omega ^ 2 | F s] omega =
          P[fun omega => X t omega ^ 2 - (t : Real) | F s] omega +
            (t : Real) := by
              rw [hsubpoint, hsplito]
              ring
      _ = X s omega ^ 2 + (t : Real) - (s : Real) := by rw [hqo]; ring
  rw [ht2]
  rw [NNReal.coe_sub hst]
  ring

/-- A zero-start martingale has zero mean at every time. -/
theorem integral_process_eq_zero
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega) (hzero : X 0 =ᵐ[P] 0)
    (hmartingale : Martingale X F P) (t : Time) : P[X t] = 0 := by
  have hset := hmartingale.setIntegral_eq
    (show (0 : Time) <= t by exact bot_le)
    (show MeasurableSet[F 0] Set.univ from MeasurableSet.univ)
  simp only [Measure.restrict_univ] at hset
  have hzero_int : P[X 0] = 0 := by
    rw [integral_congr_ae hzero]
    simp
  exact hset.symm.trans hzero_int

/-- The second moment of each coordinate is deterministic time. -/
theorem integral_process_sq_eq_time
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega) (hzero : X 0 =ᵐ[P] 0)
    (hmartingale : Martingale X F P)
    (hquadratic : Martingale (QuadraticCompensated X) F P)
    (t : Time) : P[fun omega => X t omega ^ 2] = (t : Real) := by
  have hL2 := coordinate_memLp_two hmartingale hquadratic t
  have hcomp_set := hquadratic.setIntegral_eq
    (show (0 : Time) <= t by exact bot_le)
    (show MeasurableSet[F 0] Set.univ from MeasurableSet.univ)
  simp only [Measure.restrict_univ] at hcomp_set
  have hzero_comp : P[QuadraticCompensated X 0] = 0 := by
    have hzero_sq : QuadraticCompensated X 0 =ᵐ[P] (0 : Omega -> Real) := by
      filter_upwards [hzero] with omega homega
      simp [QuadraticCompensated, homega]
    rw [integral_congr_ae hzero_sq]
    simp
  have heq : P[QuadraticCompensated X t] =
      P[fun omega => X t omega ^ 2] - (t : Real) := by
    rw [show QuadraticCompensated X t =
        fun omega => X t omega ^ 2 - (t : Real) from rfl,
      integral_sub hL2.integrable_sq (integrable_const (t : Real)),
      integral_const, probReal_univ, smul_eq_mul, one_mul]
  rw [hzero_comp, heq] at hcomp_set
  exact sub_eq_zero.mp hcomp_set.symm

/-- Each coordinate has variance equal to time. -/
theorem variance_process_eq_time
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega) (hzero : X 0 =ᵐ[P] 0)
    (hmartingale : Martingale X F P)
    (hquadratic : Martingale (QuadraticCompensated X) F P)
    (t : Time) : Var[X t; P] = (t : Real) := by
  have hL2 := coordinate_memLp_two hmartingale hquadratic t
  rw [variance_eq_sub hL2,
    integral_process_eq_zero P F X hzero hmartingale t]
  norm_num
  exact integral_process_sq_eq_time P F X hzero hmartingale hquadratic t

/-- The zero-elapsed increment is independent of the past and Gaussian. -/
theorem zeroElapsedIncrement
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega) (t : Time) :
    Indep (F t)
        (MeasurableSpace.comap (fun omega => X t omega - X t omega) (borel Real)) P /\
    HasLaw (fun omega => X t omega - X t omega)
        (gaussianReal 0 (t - t)) P := by
  constructor
  · have hbot : Indep (F t) (⊥ : MeasurableSpace Omega) P :=
      indep_bot_right (μ := P) (F t)
    simpa only [sub_self, MeasurableSpace.comap_const] using hbot
  · constructor
    · simpa only [sub_self] using
        (aemeasurable_const : AEMeasurable (fun _ : Omega => (0 : Real)) P)
    · simp [Measure.map_const]

/-- The pinned characteristic-function uniqueness theorem identifies the Gaussian law. -/
theorem hasLaw_gaussianReal_of_charFun
    {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} [IsProbabilityMeasure P]
    {Y : Omega -> Real} {v : NNReal}
    (hY : AEMeasurable Y P)
    (hchar : forall z : Real,
      charFun (P.map Y) z = Complex.exp (-(v : Real) * z ^ 2 / 2)) :
    HasLaw Y (gaussianReal 0 v) P := by
  refine ⟨hY, Measure.ext_of_charFun (funext fun z => ?_)⟩
  rw [hchar z, charFun_gaussianReal]
  push_cast
  ring

/-- The constant-zero random variable has centered zero-variance Gaussian law. -/
theorem hasLaw_gaussianReal_zero
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P] :
    HasLaw (fun _ : Omega => (0 : Real)) (gaussianReal 0 0) P := by
  constructor
  · exact aemeasurable_const
  · simp [Measure.map_const]

/-- Gaussian laws for all increments, separated from independence. -/
def GaussianIncrementLawPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega),
      Martingale X F P ->
      Martingale (QuadraticCompensated X) F P ->
      forall {s t : Time}, s <= t ->
        HasLaw (fun omega => X t omega - X s omega)
          (gaussianReal 0 (t - s)) P

/-- Independence from the past for all increments, separated from their laws. -/
def IncrementIndependencePackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega),
      Martingale X F P ->
      Martingale (QuadraticCompensated X) F P ->
      forall {s t : Time}, s <= t ->
        Indep (F s)
          (MeasurableSpace.comap (fun omega => X t omega - X s omega) (borel Real)) P

/-- Combine the exact law and independence components into the frozen package. -/
theorem incrementLawPackage_of_components
    (gaussian : GaussianIncrementLawPackage.{u})
    (independent : IncrementIndependencePackage.{u}) :
    Stage1Instances.THM_M_1029.IncrementLawPackage.{u} := by
  intro Omega _ P _ F X hmartingale hquadratic s t hst
  exact ⟨independent Omega P F X hmartingale hquadratic hst,
    gaussian Omega P F X hmartingale hquadratic hst⟩

/-- The still-open strict-positive-time increment package. -/
def StrictIncrementLawPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega),
      Martingale X F P ->
      Martingale (QuadraticCompensated X) F P ->
      forall {s t : Time}, s < t ->
        Indep (F s)
            (MeasurableSpace.comap
              (fun omega => X t omega - X s omega) (borel Real)) P /\
          HasLaw (fun omega => X t omega - X s omega)
            (gaussianReal 0 (t - s)) P

/-- Reduce the frozen non-strict package to strict time using the closed boundary case. -/
theorem incrementLawPackage_of_strict
    (hstrict : StrictIncrementLawPackage.{u}) :
    IncrementLawPackage.{u} := by
  intro Omega _ P _ F X hmartingale hquadratic s t hst
  rcases hst.eq_or_lt with rfl | hlt
  · exact zeroElapsedIncrement P F X s
  · exact hstrict Omega P F X hmartingale hquadratic hlt

/-- Exact root composition from the two still-open increment components. -/
theorem root_of_assumedIncrementComponents
    (gaussian : GaussianIncrementLawPackage.{u})
    (independent : IncrementIndependencePackage.{u}) :
    LevyMartingaleCharacterizationTarget.{u} :=
  root_of_incrementLawPackage
    (incrementLawPackage_of_components gaussian independent)

#print axioms bracketCompensated_deterministicTime_eq
#print axioms deterministicTimeProcess_continuousPaths
#print axioms deterministicTimeProcess_monotonePaths
#print axioms deterministicTimeProcess_startsAtZero
#print axioms bracketCompensated_martingale_of_quadratic
#print axioms quadraticCompensated_stronglyAdapted
#print axioms square_stronglyAdapted
#print axioms deterministicTime_stronglyAdapted_of_martingales
#print axioms quadratic_coordinate_integrable
#print axioms coordinate_memLp_two
#print axioms increment_memLp_two
#print axioms increment_square_integrable
#print axioms increment_condExp_eq_zero
#print axioms increment_condExp_sq
#print axioms integral_process_eq_zero
#print axioms integral_process_sq_eq_time
#print axioms variance_process_eq_time
#print axioms zeroElapsedIncrement
#print axioms hasLaw_gaussianReal_of_charFun
#print axioms hasLaw_gaussianReal_zero
#print axioms incrementLawPackage_of_components
#print axioms incrementLawPackage_of_strict
#print axioms root_of_assumedIncrementComponents

end Stage1Instances.THM_M_1029.Proof
