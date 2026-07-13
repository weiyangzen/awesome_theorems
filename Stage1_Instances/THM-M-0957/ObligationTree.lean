import Mathlib.Combinatorics.Additive.AP.Three.Behrend
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0957 conditional obligation composition

This module fixes exact interfaces for the Behrend construction branch and the still-open sharp
parameter optimization. The imported `Behrend.bound_aux` theorem supplies only the quantitative
construction package. The historical coefficient is isolated in separate abstract premises and is
not derived from mathlib's weaker constant-four terminal bound.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0957_ObligationTree

namespace Canonical

/-- The exact frozen target, repeated in a nested namespace so this module remains independently
elaboratable before a target-local `Statement.olean` exists. -/
def Root : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
            Real.sqrt (Real.log (N : Real))) <
        (rothNumberNat (N + 1) : Real)

end Canonical

/-- The exact historical coefficient before the positive epsilon slack. -/
noncomputable def sharpConstant : Real :=
  2 * Real.sqrt (2 * Real.log 2)

/-- The lower expression occurring in the frozen historical target. -/
noncomputable def historicalLower (epsilon : Real) (N : Nat) : Real :=
  (N : Real) ^
    (1 - (sharpConstant + epsilon) / Real.sqrt (Real.log (N : Real)))

/-- A source-shaped dimension choice for the sharp optimization. -/
noncomputable def sharpDimension (N : Nat) : Nat :=
  ⌈Real.sqrt (2 * Real.log (N + 1) / Real.log 2)⌉₊

/-- A source-shaped radix choice compatible with an ambient interval of size `N + 1`. -/
noncomputable def sharpRadix (N : Nat) : Nat :=
  ⌊((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ / 2⌋₊

/-- The real value immediately below the floor used for the selected radix. -/
noncomputable def radixProxy (N : Nat) : Real :=
  ((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ / 2 - 1

/-- The rounded dimension properties consumed by the optimal-exponent calculation. -/
def DimensionControlAt (N : Nat) : Prop :=
  2 <= sharpDimension N /\
    |(sharpDimension N : Real) -
      Real.sqrt (2 * Real.log (N + 1 : Nat) / Real.log 2)| <= 1

/-- The root interface used by all composition declarations below. -/
abbrev Root : Prop := Canonical.Root

/-- The exact implicit quantitative package supplied by the sphere/digit construction. -/
def QuantitativeConstructionPackage : Prop :=
  forall n d : Nat, d ≠ 0 -> 2 <= n ->
    (d : Real) ^ (n - 2) / (n : Real) <=
      (rothNumberNat ((2 * d - 1) ^ n) : Real)

/-- Eventual nondegeneracy of the selected dimension and radix. -/
def ParameterAdmissibilityPackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N ->
    sharpRadix N ≠ 0 /\ 2 <= sharpDimension N

/-- Eventual control of the rounded dimension selected above. -/
def DimensionControlPackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N -> DimensionControlAt N

/-- Eventual nonzeroness of the rounded radix. -/
def RadixNonzeroPackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N -> sharpRadix N ≠ 0

/-- Eventual containment of the digit image in the inclusive source interval. -/
def AmbientFitPackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N ->
    (2 * sharpRadix N - 1) ^ sharpDimension N <= N + 1

/-- The exact floor-loss comparison used to replace the real proxy by the natural radix. -/
def RadixFloorPackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N ->
    0 <= radixProxy N /\ radixProxy N <= (sharpRadix N : Real)

/-- Eventual normalization of real powers into the exponential loss expression. -/
def RpowNormalizationPackage : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      historicalLower epsilon N <=
        Real.exp
          (Real.log (N : Real) -
            (sharpConstant + epsilon) * Real.sqrt (Real.log (N : Real)))

/-- The central sharp-constant calculation, conditional on the explicitly separated rounded
dimension facts. Its four exact analytic children are declared below. -/
def OptimalExponentBridgePackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        Real.exp
            (Real.log (N : Real) -
              (sharpConstant + delta) * Real.sqrt (Real.log (N : Real))) <
          radixProxy N ^ (sharpDimension N - 2) /
            (sharpDimension N : Real)

/-- Eventual positivity and logarithmic retention for the floored-radix proxy. -/
def ProxyLogLowerPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        0 < radixProxy N /\
          Real.log (N : Real) / (sharpDimension N : Real) - Real.log 2 - delta / 4 <=
            Real.log (radixProxy N)

/-- Exact exponential form of the real value immediately above the proxy. -/
def ProxyRpowIdentityPackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N ->
    DimensionControlAt N ->
      radixProxy N + 1 =
        Real.exp
          (Real.log (((N + 1 : Nat) : Real)) /
            (sharpDimension N : Real) - Real.log 2)

/-- Eventual slack needed to absorb the subtraction by one in the proxy. -/
def ProxySlackAbsorptionPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        Real.exp
              (Real.log (N : Real) / (sharpDimension N : Real) -
                Real.log 2 - delta / 4) + 1 <=
          Real.exp
            (Real.log (((N + 1 : Nat) : Real)) /
              (sharpDimension N : Real) - Real.log 2)

/-- Eventual control of the reciprocal-dimension half of the balanced exponent. -/
def ReciprocalDimensionLossPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        2 * Real.log (N : Real) / (sharpDimension N : Real) <=
          (Real.sqrt (2 * Real.log 2) + delta / 8) *
            Real.sqrt (Real.log (N : Real))

/-- The no-slack reciprocal half of the balanced exponent estimate. -/
def ReciprocalBalancedCorePackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N ->
    DimensionControlAt N ->
      2 * Real.log (N : Real) / (sharpDimension N : Real) <=
        Real.sqrt (2 * Real.log 2) * Real.sqrt (Real.log (N : Real))

/-- Eventual control of the linear-dimension half of the balanced exponent. -/
def LinearDimensionLossPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        (sharpDimension N : Real) * Real.log 2 <=
          (Real.sqrt (2 * Real.log 2) + delta / 8) *
            Real.sqrt (Real.log (N : Real))

/-- Ceiling control before absorbing the `N + 1` and fixed additive losses. -/
def LinearCeilingPackage : Prop :=
  exists N0 : Nat, forall N : Nat, N0 <= N ->
    DimensionControlAt N ->
      (sharpDimension N : Real) * Real.log 2 <=
        Real.sqrt
            (2 * Real.log (((N + 1 : Nat) : Real)) * Real.log 2) +
          Real.log 2

/-- Eventual absorption of the `N + 1` increment and ceiling error. -/
def LinearIncrementAbsorptionPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      Real.sqrt
            (2 * Real.log (((N + 1 : Nat) : Real)) * Real.log 2) +
          Real.log 2 <=
        (Real.sqrt (2 * Real.log 2) + delta / 8) *
          Real.sqrt (Real.log (N : Real))

/-- Eventual absorption of floor slack, denominator, and fixed logarithmic losses. -/
def SubleadingLossPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        delta / 4 * ((sharpDimension N - 2 : Nat) : Real) +
            Real.log (sharpDimension N : Real) - 2 * Real.log 2 <
          3 * delta / 4 * Real.sqrt (Real.log (N : Real))

/-- Eventual absorption of the dimension multiple of the allocated slack. -/
def DimensionSlackPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        delta / 4 * ((sharpDimension N - 2 : Nat) : Real) <=
          delta / 2 * Real.sqrt (Real.log (N : Real))

/-- Eventual absorption of the logarithmic dimension and fixed factor. -/
def LogDimensionLossPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      DimensionControlAt N ->
        Real.log (sharpDimension N : Real) - 2 * Real.log 2 <
          delta / 4 * Real.sqrt (Real.log (N : Real))

/-- The sharp asymptotic estimate at the real radix proxy. -/
def ProxyAsymptoticPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      Real.exp
          (Real.log (N : Real) -
            (sharpConstant + delta) * Real.sqrt (Real.log (N : Real))) <
        radixProxy N ^ (sharpDimension N - 2) /
          (sharpDimension N : Real)

/-- The genuinely open sharp asymptotic estimate for the selected rounded parameters. -/
def RatioAsymptoticPackage : Prop :=
  forall delta : Real, 0 < delta ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      Real.exp
          (Real.log (N : Real) -
            (sharpConstant + delta) * Real.sqrt (Real.log (N : Real))) <
        (sharpRadix N : Real) ^ (sharpDimension N - 2) /
          (sharpDimension N : Real)

/-- The exact lower-expression comparison needed by the root assembly. -/
def SharpEstimatePackage : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      historicalLower epsilon N <
        (sharpRadix N : Real) ^ (sharpDimension N - 2) /
          (sharpDimension N : Real)

/-- All sharp parameter facts, sharing one sufficiently-large threshold. -/
def SharpParameterPackage : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      sharpRadix N ≠ 0 /\
      2 <= sharpDimension N /\
      (2 * sharpRadix N - 1) ^ sharpDimension N <= N + 1 /\
      historicalLower epsilon N <
        (sharpRadix N : Real) ^ (sharpDimension N - 2) /
          (sharpDimension N : Real)

/-- Monotonicity transport from the constructed digit interval into the inclusive source
interval. -/
def IndexMonotonicityPackage : Prop :=
  forall n d N : Nat, (2 * d - 1) ^ n <= N + 1 ->
    (rothNumberNat ((2 * d - 1) ^ n) : Real) <=
      (rothNumberNat (N + 1) : Real)

/-- The three exact proof packages consumed by the final root composition. -/
def ExactAssembly : Prop :=
  QuantitativeConstructionPackage /\
    SharpParameterPackage /\
      IndexMonotonicityPackage

/-- Checked adapter to the pinned construction package, not to the historical root. -/
theorem pinnedQuantitativeConstruction : QuantitativeConstructionPackage := by
  intro n d hd hn
  exact Behrend.bound_aux hd hn

/-- Checked inclusive-index transport. -/
theorem pinnedIndexMonotonicity : IndexMonotonicityPackage := by
  intro n d N hfit
  exact_mod_cast rothNumberNat.mono hfit

/-- Checked threshold merge for dimension and radix admissibility. -/
theorem parameterAdmissibility_of_dimension_and_radix
    (dimension : DimensionControlPackage)
    (radix : RadixNonzeroPackage) : ParameterAdmissibilityPackage := by
  obtain ⟨Ndimension, hdimension⟩ := dimension
  obtain ⟨Nradix, hradix⟩ := radix
  refine ⟨max Ndimension Nradix, ?_⟩
  intro N hN
  have hdimensionN : Ndimension <= N := (Nat.le_max_left _ _).trans hN
  have hradixN : Nradix <= N := (Nat.le_max_right _ _).trans hN
  exact ⟨hradix N hradixN, (hdimension N hdimensionN).1⟩

/-- Checked composition of the proxy identity and subtraction-by-one slack. -/
theorem proxyLogLower_of_identity_and_slack
    (identity : ProxyRpowIdentityPackage)
    (slack : ProxySlackAbsorptionPackage) : ProxyLogLowerPackage := by
  intro delta hdelta
  obtain ⟨Nidentity, hidentity⟩ := identity
  obtain ⟨Nslack, hslack⟩ := slack delta hdelta
  refine ⟨max Nidentity Nslack, ?_⟩
  intro N hN hdimension
  have hidentityN : Nidentity <= N := (Nat.le_max_left _ _).trans hN
  have hslackN : Nslack <= N := (Nat.le_max_right _ _).trans hN
  let lower : Real :=
    Real.log (N : Real) / (sharpDimension N : Real) - Real.log 2 - delta / 4
  have hcomparison := hslack N hslackN hdimension
  rw [← hidentity N hidentityN hdimension] at hcomparison
  have hexp : Real.exp lower <= radixProxy N := by
    dsimp only [lower]
    linarith
  have hproxy : 0 < radixProxy N := (Real.exp_pos lower).trans_le hexp
  exact ⟨hproxy, (Real.le_log_iff_exp_le hproxy).2 hexp⟩

/-- Checked addition of the allocated positive slack to the reciprocal core. -/
theorem reciprocalLoss_of_balanced_core
    (core : ReciprocalBalancedCorePackage) : ReciprocalDimensionLossPackage := by
  obtain ⟨N0, hcore⟩ := core
  intro delta hdelta
  refine ⟨N0, ?_⟩
  intro N hN hdimension
  exact (hcore N hN hdimension).trans <|
    mul_le_mul_of_nonneg_right
      (le_add_of_nonneg_right (by positivity : 0 <= delta / 8))
      (Real.sqrt_nonneg _)

/-- Checked composition of ceiling control and increment absorption. -/
theorem linearLoss_of_ceiling_and_increment
    (ceiling : LinearCeilingPackage)
    (increment : LinearIncrementAbsorptionPackage) : LinearDimensionLossPackage := by
  obtain ⟨Nceiling, hceiling⟩ := ceiling
  intro delta hdelta
  obtain ⟨Nincrement, hincrement⟩ := increment delta hdelta
  refine ⟨max Nceiling Nincrement, ?_⟩
  intro N hN hdimension
  exact (hceiling N ((Nat.le_max_left _ _).trans hN) hdimension).trans
    (hincrement N ((Nat.le_max_right _ _).trans hN))

/-- Checked recombination of the dimension and logarithmic subleading losses. -/
theorem subleadingLoss_of_dimension_and_log
    (dimension : DimensionSlackPackage)
    (logarithmic : LogDimensionLossPackage) : SubleadingLossPackage := by
  intro delta hdelta
  obtain ⟨Ndimension, hdimension⟩ := dimension delta hdelta
  obtain ⟨Nlogarithmic, hlogarithmic⟩ := logarithmic delta hdelta
  refine ⟨max Ndimension Nlogarithmic, ?_⟩
  intro N hN hcontrol
  have hd := hdimension N ((Nat.le_max_left _ _).trans hN) hcontrol
  have hl := hlogarithmic N ((Nat.le_max_right _ _).trans hN) hcontrol
  nlinarith

/-- Checked assembly of the four explicit sharp-exponent leaves. -/
theorem optimalExponent_of_components
    (proxy : ProxyLogLowerPackage)
    (reciprocal : ReciprocalDimensionLossPackage)
    (linear : LinearDimensionLossPackage)
    (subleading : SubleadingLossPackage) : OptimalExponentBridgePackage := by
  intro delta hdelta
  obtain ⟨Nproxy, hproxy⟩ := proxy delta hdelta
  obtain ⟨Nreciprocal, hreciprocal⟩ := reciprocal delta hdelta
  obtain ⟨Nlinear, hlinear⟩ := linear delta hdelta
  obtain ⟨Nsubleading, hsubleading⟩ := subleading delta hdelta
  refine ⟨max Nproxy (max Nreciprocal (max Nlinear Nsubleading)), ?_⟩
  intro N hN hdimension
  have hproxyN : Nproxy <= N := (Nat.le_max_left _ _).trans hN
  have hreciprocalN : Nreciprocal <= N :=
    (Nat.le_max_left _ _).trans ((Nat.le_max_right _ _).trans hN)
  have hlinearN : Nlinear <= N :=
    (Nat.le_max_left _ _).trans
      ((Nat.le_max_right _ _).trans ((Nat.le_max_right _ _).trans hN))
  have hsubleadingN : Nsubleading <= N :=
    (Nat.le_max_right _ _).trans
      ((Nat.le_max_right _ _).trans ((Nat.le_max_right _ _).trans hN))
  have hp := hproxy N hproxyN hdimension
  have hr := hreciprocal N hreciprocalN hdimension
  have hl := hlinear N hlinearN hdimension
  have hs := hsubleading N hsubleadingN hdimension
  let n : Nat := sharpDimension N
  let q : Real := radixProxy N
  let L : Real := Real.log (N : Real)
  let S : Real := Real.sqrt L
  have hn : 2 <= n := hdimension.1
  have hnpos : 0 < (n : Real) := by
    exact_mod_cast (lt_of_lt_of_le (by decide) hn)
  have hcastsub : ((n - 2 : Nat) : Real) = (n : Real) - 2 := by
    rw [Nat.cast_sub hn]
    norm_num
  have hp' :
      0 < q /\
        L / (n : Real) - Real.log 2 - delta / 4 <= Real.log q := by
    simpa only [n, q, L] using hp
  have hr' :
      2 * L / (n : Real) <=
        (Real.sqrt (2 * Real.log 2) + delta / 8) * S := by
    simpa only [n, L, S] using hr
  have hl' :
      (n : Real) * Real.log 2 <=
        (Real.sqrt (2 * Real.log 2) + delta / 8) * S := by
    simpa only [n, L, S] using hl
  have hs' :
      delta / 4 * ((n - 2 : Nat) : Real) +
          Real.log (n : Real) - 2 * Real.log 2 <
        3 * delta / 4 * S := by
    simpa only [n, L, S] using hs
  have hloss :
      2 * L / (n : Real) + (n : Real) * Real.log 2 +
          (delta / 4 * ((n - 2 : Nat) : Real) +
            Real.log (n : Real) - 2 * Real.log 2) <
        (2 * Real.sqrt (2 * Real.log 2) + delta) * S := by
    nlinarith [hr', hl', hs']
  have hrewrite :
      ((n - 2 : Nat) : Real) *
            (L / (n : Real) - Real.log 2 - delta / 4) - Real.log (n : Real) =
        L -
          (2 * L / (n : Real) + (n : Real) * Real.log 2 +
            (delta / 4 * ((n - 2 : Nat) : Real) +
              Real.log (n : Real) - 2 * Real.log 2)) := by
    rw [hcastsub]
    field_simp [hnpos.ne']
    ring
  have hbalanced :
      L - (sharpConstant + delta) * S <
        ((n - 2 : Nat) : Real) *
            (L / (n : Real) - Real.log 2 - delta / 4) - Real.log (n : Real) := by
    rw [hrewrite]
    dsimp only [sharpConstant]
    exact sub_lt_sub_left hloss L
  have hlog :
      L - (sharpConstant + delta) * S <
        ((n - 2 : Nat) : Real) * Real.log q - Real.log (n : Real) := by
    exact hbalanced.trans_le <| sub_le_sub_right
      (mul_le_mul_of_nonneg_left hp'.2 (Nat.cast_nonneg _)) _
  change Real.exp (L - (sharpConstant + delta) * S) < q ^ (n - 2) / (n : Real)
  calc
    Real.exp (L - (sharpConstant + delta) * S) <
        Real.exp (((n - 2 : Nat) : Real) * Real.log q - Real.log (n : Real)) :=
      Real.exp_lt_exp.mpr hlog
    _ = Real.exp (((n - 2 : Nat) : Real) * Real.log q) /
        Real.exp (Real.log (n : Real)) := by rw [Real.exp_sub]
    _ = q ^ (n - 2) / (n : Real) := by
      rw [Real.exp_nat_mul, Real.exp_log hp'.1, Real.exp_log hnpos]

/-- Checked use of the central optimal-exponent bridge after rounded dimension control. -/
theorem proxyAsymptotic_of_dimension_and_bridge
    (dimension : DimensionControlPackage)
    (bridge : OptimalExponentBridgePackage) : ProxyAsymptoticPackage := by
  intro delta hdelta
  obtain ⟨Ndimension, hdimension⟩ := dimension
  obtain ⟨Nbridge, hbridge⟩ := bridge delta hdelta
  refine ⟨max Ndimension Nbridge, ?_⟩
  intro N hN
  have hdimensionN : Ndimension <= N := (Nat.le_max_left _ _).trans hN
  have hbridgeN : Nbridge <= N := (Nat.le_max_right _ _).trans hN
  exact hbridge N hbridgeN (hdimension N hdimensionN)

/-- Checked replacement of the real radix proxy by the selected floored natural radix. -/
theorem ratioAsymptotic_of_proxy_floor_and_dimension
    (proxy : ProxyAsymptoticPackage)
    (floor : RadixFloorPackage)
    (dimension : DimensionControlPackage) : RatioAsymptoticPackage := by
  intro delta hdelta
  obtain ⟨Nproxy, hproxy⟩ := proxy delta hdelta
  obtain ⟨Nfloor, hfloor⟩ := floor
  obtain ⟨Ndimension, hdimension⟩ := dimension
  refine ⟨max Nproxy (max Nfloor Ndimension), ?_⟩
  intro N hN
  have hproxyN : Nproxy <= N := (Nat.le_max_left _ _).trans hN
  have hfloorN : Nfloor <= N :=
    (Nat.le_max_left _ _).trans ((Nat.le_max_right _ _).trans hN)
  have hdimensionN : Ndimension <= N :=
    (Nat.le_max_right _ _).trans ((Nat.le_max_right _ _).trans hN)
  have hfloorAt := hfloor N hfloorN
  have hpower :
      radixProxy N ^ (sharpDimension N - 2) <=
        (sharpRadix N : Real) ^ (sharpDimension N - 2) := by
    exact pow_le_pow_left₀ hfloorAt.1 hfloorAt.2 _
  have hdimensionPos : 0 < (sharpDimension N : Real) := by
    exact_mod_cast (show 0 < sharpDimension N from
      lt_of_lt_of_le (by decide) (hdimension N hdimensionN).1)
  exact (hproxy N hproxyN).trans_le
    (div_le_div_of_nonneg_right hpower hdimensionPos.le)

/-- Checked composition of power normalization and the sharper half-epsilon ratio estimate. -/
theorem sharpEstimate_of_normalization_and_ratio
    (normalization : RpowNormalizationPackage)
    (ratio : RatioAsymptoticPackage) : SharpEstimatePackage := by
  intro epsilon hepsilon
  obtain ⟨Nnormalization, hnormalization⟩ := normalization epsilon hepsilon
  obtain ⟨Nratio, hratio⟩ := ratio (epsilon / 2) (half_pos hepsilon)
  refine ⟨max 2 (max Nnormalization Nratio), ?_⟩
  intro N hN
  have htwo : 2 <= N := (Nat.le_max_left 2 (max Nnormalization Nratio)).trans hN
  have hnormalizationN : Nnormalization <= N :=
    (Nat.le_max_left Nnormalization Nratio).trans
      ((Nat.le_max_right 2 (max Nnormalization Nratio)).trans hN)
  have hratioN : Nratio <= N :=
    (Nat.le_max_right Nnormalization Nratio).trans
      ((Nat.le_max_right 2 (max Nnormalization Nratio)).trans hN)
  have hNreal : (1 : Real) < (N : Real) := by
    exact_mod_cast (show 1 < N from lt_of_lt_of_le (by decide) htwo)
  have hsqrt : 0 < Real.sqrt (Real.log (N : Real)) :=
    Real.sqrt_pos.2 (Real.log_pos hNreal)
  have hslack :
      Real.exp
          (Real.log (N : Real) -
            (sharpConstant + epsilon) * Real.sqrt (Real.log (N : Real))) <
        Real.exp
          (Real.log (N : Real) -
            (sharpConstant + epsilon / 2) * Real.sqrt (Real.log (N : Real))) := by
    rw [Real.exp_lt_exp]
    nlinarith
  exact (hnormalization N hnormalizationN).trans_lt
    (hslack.trans (hratio N hratioN))

/-- Checked threshold merge for all parameter-side children. -/
theorem sharpParameters_of_components
    (admissibility : ParameterAdmissibilityPackage)
    (ambient : AmbientFitPackage)
    (estimate : SharpEstimatePackage) : SharpParameterPackage := by
  obtain ⟨Nadmissibility, hadmissibility⟩ := admissibility
  obtain ⟨Nambient, hambient⟩ := ambient
  intro epsilon hepsilon
  obtain ⟨Nestimate, hestimate⟩ := estimate epsilon hepsilon
  refine ⟨max Nadmissibility (max Nambient Nestimate), ?_⟩
  intro N hN
  have hadmissibilityN : Nadmissibility <= N :=
    (Nat.le_max_left Nadmissibility (max Nambient Nestimate)).trans hN
  have hambientN : Nambient <= N :=
    (Nat.le_max_left Nambient Nestimate).trans
      ((Nat.le_max_right Nadmissibility (max Nambient Nestimate)).trans hN)
  have hestimateN : Nestimate <= N :=
    (Nat.le_max_right Nambient Nestimate).trans
      ((Nat.le_max_right Nadmissibility (max Nambient Nestimate)).trans hN)
  exact ⟨(hadmissibility N hadmissibilityN).1,
    (hadmissibility N hadmissibilityN).2,
    hambient N hambientN,
    hestimate N hestimateN⟩

/-- Checked three-child assembly without importing any child as an accepted proof. -/
theorem exactAssembly_of_children
    (construction : QuantitativeConstructionPackage)
    (parameters : SharpParameterPackage)
    (index : IndexMonotonicityPackage) : ExactAssembly :=
  ⟨construction, parameters, index⟩

/-- Checked child-to-root composition for the exact historical statement. -/
theorem root_of_quantitative_and_parameters
    (construction : QuantitativeConstructionPackage)
    (parameters : SharpParameterPackage)
    (index : IndexMonotonicityPackage) : Root := by
  intro epsilon hepsilon
  obtain ⟨N0, hN0⟩ := parameters epsilon hepsilon
  refine ⟨N0, ?_⟩
  intro N hN
  obtain ⟨hradix, hdimension, hambient, hlower⟩ := hN0 N hN
  have hconstruction := construction (sharpDimension N) (sharpRadix N) hradix hdimension
  simpa only [historicalLower, sharpConstant] using
    hlower.trans_le (hconstruction.trans
      (index (sharpDimension N) (sharpRadix N) N hambient))

/-- Checked assembly-to-root wrapper, retaining the exact three package premises. -/
theorem root_of_exactAssembly (assembly : ExactAssembly) : Root :=
  root_of_quantitative_and_parameters assembly.1 assembly.2.1 assembly.2.2

assert_no_sorry pinnedQuantitativeConstruction
assert_no_sorry pinnedIndexMonotonicity
assert_no_sorry parameterAdmissibility_of_dimension_and_radix
assert_no_sorry proxyLogLower_of_identity_and_slack
assert_no_sorry reciprocalLoss_of_balanced_core
assert_no_sorry linearLoss_of_ceiling_and_increment
assert_no_sorry subleadingLoss_of_dimension_and_log
assert_no_sorry optimalExponent_of_components
assert_no_sorry proxyAsymptotic_of_dimension_and_bridge
assert_no_sorry ratioAsymptotic_of_proxy_floor_and_dimension
assert_no_sorry sharpEstimate_of_normalization_and_ratio
assert_no_sorry sharpParameters_of_components
assert_no_sorry exactAssembly_of_children
assert_no_sorry root_of_quantitative_and_parameters
assert_no_sorry root_of_exactAssembly

#print sorries pinnedQuantitativeConstruction
#print sorries pinnedIndexMonotonicity
#print sorries parameterAdmissibility_of_dimension_and_radix
#print sorries proxyLogLower_of_identity_and_slack
#print sorries reciprocalLoss_of_balanced_core
#print sorries linearLoss_of_ceiling_and_increment
#print sorries subleadingLoss_of_dimension_and_log
#print sorries optimalExponent_of_components
#print sorries proxyAsymptotic_of_dimension_and_bridge
#print sorries ratioAsymptotic_of_proxy_floor_and_dimension
#print sorries sharpEstimate_of_normalization_and_ratio
#print sorries sharpParameters_of_components
#print sorries exactAssembly_of_children
#print sorries root_of_quantitative_and_parameters
#print sorries root_of_exactAssembly

#print axioms pinnedQuantitativeConstruction
#print axioms pinnedIndexMonotonicity
#print axioms parameterAdmissibility_of_dimension_and_radix
#print axioms proxyLogLower_of_identity_and_slack
#print axioms reciprocalLoss_of_balanced_core
#print axioms linearLoss_of_ceiling_and_increment
#print axioms subleadingLoss_of_dimension_and_log
#print axioms optimalExponent_of_components
#print axioms proxyAsymptotic_of_dimension_and_bridge
#print axioms ratioAsymptotic_of_proxy_floor_and_dimension
#print axioms sharpEstimate_of_normalization_and_ratio
#print axioms sharpParameters_of_components
#print axioms exactAssembly_of_children
#print axioms root_of_quantitative_and_parameters
#print axioms root_of_exactAssembly

open Lean Elab Command in
elab "#print_obligation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0957_ObligationTree.pinnedQuantitativeConstruction,
    ``Stage1Instances.THM_M_0957_ObligationTree.pinnedIndexMonotonicity,
    ``Stage1Instances.THM_M_0957_ObligationTree.parameterAdmissibility_of_dimension_and_radix,
    ``Stage1Instances.THM_M_0957_ObligationTree.proxyLogLower_of_identity_and_slack,
    ``Stage1Instances.THM_M_0957_ObligationTree.reciprocalLoss_of_balanced_core,
    ``Stage1Instances.THM_M_0957_ObligationTree.linearLoss_of_ceiling_and_increment,
    ``Stage1Instances.THM_M_0957_ObligationTree.subleadingLoss_of_dimension_and_log,
    ``Stage1Instances.THM_M_0957_ObligationTree.optimalExponent_of_components,
    ``Stage1Instances.THM_M_0957_ObligationTree.proxyAsymptotic_of_dimension_and_bridge,
    ``Stage1Instances.THM_M_0957_ObligationTree.ratioAsymptotic_of_proxy_floor_and_dimension,
    ``Stage1Instances.THM_M_0957_ObligationTree.sharpEstimate_of_normalization_and_ratio,
    ``Stage1Instances.THM_M_0957_ObligationTree.sharpParameters_of_components,
    ``Stage1Instances.THM_M_0957_ObligationTree.exactAssembly_of_children,
    ``Stage1Instances.THM_M_0957_ObligationTree.root_of_quantitative_and_parameters,
    ``Stage1Instances.THM_M_0957_ObligationTree.root_of_exactAssembly
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
  logInfo m!"OBLIGATION_CLOSURE declarations={closure.size}"
  logInfo m!"OBLIGATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"OBLIGATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"OBLIGATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_obligation_closure

set_option pp.universes true in
set_option pp.explicit true in
#print Root

end Stage1Instances.THM_M_0957_ObligationTree
