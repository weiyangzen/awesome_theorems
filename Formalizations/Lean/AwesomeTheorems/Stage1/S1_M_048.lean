import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass
import Mathlib.AlgebraicGeometry.EllipticCurve.Reduction
import Mathlib.NumberTheory.LSeries.Deriv
import Mathlib.NumberTheory.ModularForms.CongruenceSubgroups
import Mathlib.NumberTheory.ModularForms.QExpansion

/-!
# S1-M-048 / THM-M-0131 statement-shape artifact

This file records a Lean 4 statement-shape for the Shimura/Taniyama-Shimura
modularity correspondence between elliptic curves over `Q` and weight-two
modular forms. It is intentionally not a proof of modularity.
-/

noncomputable section

namespace Stage1.S1_M_048

open Matrix.SpecialLinearGroup

/-- A rational elliptic curve represented by mathlib's Weierstrass model API. -/
structure RationalWeierstrassEllipticCurve where
  W : WeierstrassCurve ℚ
  isElliptic : W.IsElliptic

/-- The `Γ₀(N)` congruence subgroup in the ambient group used by `CuspForm`. -/
abbrev Gamma0LevelSubgroup (N : ℕ) : Subgroup (GL (Fin 2) ℝ) :=
  CongruenceSubgroup.Gamma0 N

/-- The available mathlib target type for a weight-two cusp-form candidate at `Γ₀(N)`. -/
abbrev Gamma0LevelCuspFormTarget (N : ℕ) : Type :=
  CuspForm (Gamma0LevelSubgroup N) 2

/-- A weight-two cusp-form candidate with an explicit `Γ₀(N)` level target. -/
structure WeightTwoCuspFormCandidate (N : ℕ) where
  f : Gamma0LevelCuspFormTarget N

/--
Statement boundary for the missing modularity witness.

The three proposition fields are placeholders for the genuine theorem payload:
conductor/level compatibility, equality of Frobenius traces with q-expansion
coefficients, and compatibility of L-functions. They are kept explicit so later
work can replace them with concrete mathlib or pinned-upstream definitions.
-/
structure ModularityWitness (E : RationalWeierstrassEllipticCurve) where
  level : ℕ
  form : WeightTwoCuspFormCandidate level
  conductorLevelCompatible : Prop
  qExpansionMatchesFrobeniusTraces : Prop
  lSeriesCompatible : Prop

/--
Statement-shape only: every elliptic curve over `Q` should have a compatible
weight-two modular-form witness.
-/
def StatementShape : Prop :=
  ∀ E : RationalWeierstrassEllipticCurve,
    Nonempty { w : ModularityWitness E //
      w.conductorLevelCompatible ∧
      w.qExpansionMatchesFrobeniusTraces ∧
      w.lSeriesCompatible }

/-- Available target choices for `THM-M-0131-P03`. -/
inductive FinalTheoremTargetChoice where
  /-- Current repo-local target: a Weierstrass model over `ℚ`. -/
  | weierstrassModelOverQ
  /-- Future target: an elliptic curve as a scheme over `Spec ℚ`. -/
  | schemeOverSpecQ
  /-- Future bridge target between Weierstrass and scheme-level formulations. -/
  | equivalenceBridge
  deriving DecidableEq

/--
P03 decision record.

The final target for this Stage1 artifact is the Weierstrass-model statement over
`ℚ`, represented by `StatementShape`. A scheme-level statement over `Spec ℚ` is
not selected as the current target because this file has no repo-local
scheme-level elliptic-curve-over-`Spec ℚ` API anchor. The eventual scheme-level
formulation should be tracked as bridge work from this checked model statement.
-/
structure TheoremTargetDecision where
  selected : FinalTheoremTargetChoice
  currentTarget : Prop
  requiresSchemeBridge : Bool
  rationale : String

/-- Checked P03 decision: keep the current formal target as `StatementShape`. -/
def p03TheoremTargetDecision : TheoremTargetDecision where
  selected := .weierstrassModelOverQ
  currentTarget := StatementShape
  requiresSchemeBridge := true
  rationale :=
    "Use the Weierstrass-model statement over Q as the current Lean target; " ++
    "track scheme-over-Spec-Q and equivalence formulations as later bridge work."

theorem p03_selectsWeierstrassModelOverQ :
    p03TheoremTargetDecision.selected =
      FinalTheoremTargetChoice.weierstrassModelOverQ :=
  rfl

theorem p03_currentTarget_is_statementShape :
    p03TheoremTargetDecision.currentTarget = StatementShape :=
  rfl

theorem p03_requiresSchemeBridge :
    p03TheoremTargetDecision.requiresSchemeBridge = true :=
  rfl

/--
An integration-ready record for the conductor/level API audit requested by
`THM-M-0131-P04`. Rows with `missing` status document absent APIs rather than
pretending the global conductor bridge is already present.
-/
structure ConductorLevelAPIAuditRow where
  declaration : String
  moduleName : String
  repoLocalStatus : String
  role : String

/-- Public-backfill data for the P04 conductor/level audit. -/
def p04ConductorLevelAPIAudit : List ConductorLevelAPIAuditRow :=
  [ { declaration := "CongruenceSubgroup.Gamma0"
      moduleName := "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups"
      repoLocalStatus := "import-checked"
      role := "Gamma0 level subgroup, coercible to the ambient subgroup type used by CuspForm" },
    { declaration := "CongruenceSubgroup.Gamma0_mem"
      moduleName := "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups"
      repoLocalStatus := "import-checked"
      role := "membership criterion for lower-left entry congruent to zero modulo N" },
    { declaration := "CongruenceSubgroup.Gamma0_is_congruence"
      moduleName := "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups"
      repoLocalStatus := "wrapper-checked below for nonzero level"
      role := "Gamma0 is a congruence subgroup when N is nonzero" },
    { declaration := "CongruenceSubgroup.instFiniteIndexGamma0"
      moduleName := "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups"
      repoLocalStatus := "wrapper-checked below for nonzero level"
      role := "finite-index instance needed for arithmetic modular-form infrastructure" },
    { declaration := "CongruenceSubgroup.strictPeriods_Gamma0"
      moduleName := "Mathlib.NumberTheory.ModularForms.Cusps"
      repoLocalStatus := "wrapper-checked below"
      role := "q-expansion cusp-width normalization at infinity for Gamma0 N" },
    { declaration := "CongruenceSubgroup.strictWidthInfty_Gamma0"
      moduleName := "Mathlib.NumberTheory.ModularForms.Cusps"
      repoLocalStatus := "wrapper-checked below"
      role := "strict width at infinity is 1 for Gamma0 N" },
    { declaration := "WeierstrassCurve.IsMinimal"
      moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction"
      repoLocalStatus := "import-checked"
      role := "local minimal Weierstrass equation predicate over a DVR" },
    { declaration := "WeierstrassCurve.exists_isMinimal"
      moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction"
      repoLocalStatus := "wrapper-checked below"
      role := "existence of a local minimal Weierstrass model" },
    { declaration := "WeierstrassCurve.HasGoodReduction / HasMultiplicativeReduction / HasAdditiveReduction"
      moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction"
      repoLocalStatus := "wrapper-checked below"
      role := "local reduction-type API, useful substrate for conductor exponents" },
    { declaration := "elliptic-curve conductor over Q"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed global integer conductor N(E) for the final level equality" },
    { declaration := "conductor equals Gamma0 level theorem"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed bridge from E.conductor = N to the target CuspForm (Gamma0 N) 2" } ]

theorem gamma0LevelSubgroup_eq (N : ℕ) :
    Gamma0LevelSubgroup N =
      (CongruenceSubgroup.Gamma0 N : Subgroup (GL (Fin 2) ℝ)) :=
  rfl

theorem gamma0LevelCuspFormTarget_eq (N : ℕ) :
    Gamma0LevelCuspFormTarget N =
      CuspForm (CongruenceSubgroup.Gamma0 N : Subgroup (GL (Fin 2) ℝ)) 2 :=
  rfl

theorem p04_formTarget_is_Gamma0 (N : ℕ) (f : WeightTwoCuspFormCandidate N) :
    f.f ∈ (Set.univ : Set (Gamma0LevelCuspFormTarget N)) :=
  Set.mem_univ _

theorem gamma0StrictPeriodsAnchor (N : ℕ) :
    (Gamma0LevelSubgroup N).strictPeriods = AddSubgroup.zmultiples 1 :=
  CongruenceSubgroup.strictPeriods_Gamma0 N

theorem gamma0StrictWidthInftyAnchor (N : ℕ) :
    (Gamma0LevelSubgroup N).strictWidthInfty = 1 :=
  CongruenceSubgroup.strictWidthInfty_Gamma0 N

theorem gamma0CongruenceAnchor (N : ℕ) [NeZero N] :
    CongruenceSubgroup.IsCongruenceSubgroup (CongruenceSubgroup.Gamma0 N) :=
  CongruenceSubgroup.Gamma0_is_congruence N

theorem gamma0FiniteIndexAnchor (N : ℕ) [NeZero N] :
    (CongruenceSubgroup.Gamma0 N).FiniteIndex :=
  inferInstance

def MathlibMinimalModelExistenceAnchor : Prop :=
  ∀ (R K : Type*) [CommRing R] [IsDomain R] [IsDiscreteValuationRing R]
      [Field K] [Algebra R K] [IsFractionRing R K] (W : WeierstrassCurve K),
    ∃ C : WeierstrassCurve.VariableChange K, WeierstrassCurve.IsMinimal R (C • W)

theorem mathlibMinimalModelExistenceAnchor :
    MathlibMinimalModelExistenceAnchor :=
  fun R _K _ _ _ _ _ _ W => WeierstrassCurve.exists_isMinimal R W

def MathlibLocalReductionTrichotomyAnchor : Prop :=
  ∀ (R K : Type*) [CommRing R] [IsDomain R] [IsDiscreteValuationRing R]
      [Field K] [Algebra R K] [IsFractionRing R K] (W : WeierstrassCurve K)
      [WeierstrassCurve.IsMinimal R W],
    WeierstrassCurve.HasGoodReduction R W ∨
      WeierstrassCurve.HasMultiplicativeReduction R W ∨
      WeierstrassCurve.HasAdditiveReduction R W

theorem mathlibLocalReductionTrichotomyAnchor :
    MathlibLocalReductionTrichotomyAnchor :=
  fun R _K _ _ _ _ _ _ W _ =>
    WeierstrassCurve.hasGoodReduction_or_hasMultiplicativeReduction_or_hasAdditiveReduction R
      (W := W)

/-- Low-risk wrapper: mathlib exposes a Weierstrass-curve object model over `Q`. -/
def MathlibEllipticCurveModelAvailable : Prop :=
  Nonempty (WeierstrassCurve ℚ)

theorem mathlibEllipticCurveModelAvailable : MathlibEllipticCurveModelAvailable :=
  ⟨default⟩

/-- Low-risk wrapper: mathlib exposes the bundled type of weight-two cusp forms. -/
def MathlibCuspFormTypeAvailable : Prop :=
  ∀ Γ : Subgroup (GL (Fin 2) ℝ), CuspForm Γ 2 = CuspForm Γ 2

theorem mathlibCuspFormTypeAvailable : MathlibCuspFormTypeAvailable :=
  fun _ => rfl

/-- Thin wrapper around mathlib's q-expansion construction for cusp forms. -/
def cuspFormQExpansion
    (Γ : Subgroup (GL (Fin 2) ℝ)) (h : ℝ) (f : CuspForm Γ 2) : PowerSeries ℂ :=
  ModularFormClass.qExpansion h f

/--
An integration-ready record for the public mathlib anchor table requested by
`THM-M-0131-P02`. The strings are documentation data; the declarations below
are the typechecked anchors.
-/
structure MathlibAnchorTableRow where
  declaration : String
  moduleName : String
  repoLocalStatus : String
  role : String

/-- Public-backfill data for the exact P02 anchor list. -/
def p02MathlibAnchorTable : List MathlibAnchorTableRow :=
  [ { declaration := "WeierstrassCurve"
      moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass"
      repoLocalStatus := "import-checked"
      role := "Weierstrass model object for elliptic curves over Q" },
    { declaration := "WeierstrassCurve.IsElliptic"
      moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass"
      repoLocalStatus := "import-checked"
      role := "nonsingularity predicate on a Weierstrass curve" },
    { declaration := "CuspForm"
      moduleName := "Mathlib.NumberTheory.ModularForms.Basic"
      repoLocalStatus := "import-checked through QExpansion"
      role := "bundled cusp-form target type, currently over subgroups of GL(2,R)" },
    { declaration := "CongruenceSubgroup.Gamma0"
      moduleName := "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups"
      repoLocalStatus := "import-checked"
      role := "Gamma0 level subgroup of SL(2,Z)" },
    { declaration := "CongruenceSubgroup.Gamma1"
      moduleName := "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups"
      repoLocalStatus := "import-checked"
      role := "Gamma1 level subgroup of SL(2,Z)" },
    { declaration := "ModularFormClass.qExpansion"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "import-checked"
      role := "power-series q-expansion of a modular form" },
    { declaration := "qExpansion_coeff_unique"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "wrapper-checked below"
      role := "uniqueness theorem for q-expansion coefficients" } ]

/-- Typechecked anchor: mathlib exposes `WeierstrassCurve`. -/
def MathlibWeierstrassCurveAnchor : Prop :=
  Nonempty (WeierstrassCurve ℚ)

theorem mathlibWeierstrassCurveAnchor : MathlibWeierstrassCurveAnchor :=
  ⟨default⟩

/-- Typechecked anchor: mathlib exposes `WeierstrassCurve.IsElliptic`. -/
def MathlibWeierstrassCurveIsEllipticAnchor : Prop :=
  ∀ W : WeierstrassCurve ℚ, W.IsElliptic = W.IsElliptic

theorem mathlibWeierstrassCurveIsEllipticAnchor :
    MathlibWeierstrassCurveIsEllipticAnchor :=
  fun _ => rfl

/-- Typechecked anchor: mathlib exposes `CuspForm`. -/
def MathlibCuspFormAnchor : Prop :=
  ∀ Γ : Subgroup (GL (Fin 2) ℝ), CuspForm Γ 2 = CuspForm Γ 2

theorem mathlibCuspFormAnchor : MathlibCuspFormAnchor :=
  fun _ => rfl

/-- Typechecked anchor: mathlib exposes `CongruenceSubgroup.Gamma0`. -/
def MathlibGamma0Anchor : Prop :=
  ∀ N : ℕ, CongruenceSubgroup.Gamma0 N = CongruenceSubgroup.Gamma0 N

theorem mathlibGamma0Anchor : MathlibGamma0Anchor :=
  fun _ => rfl

/-- Typechecked anchor: mathlib exposes `CongruenceSubgroup.Gamma1`. -/
def MathlibGamma1Anchor : Prop :=
  ∀ N : ℕ, CongruenceSubgroup.Gamma1 N = CongruenceSubgroup.Gamma1 N

theorem mathlibGamma1Anchor : MathlibGamma1Anchor :=
  fun _ => rfl

/-- Typechecked anchor: mathlib exposes `ModularFormClass.qExpansion`. -/
def MathlibModularFormClassQExpansionAnchor : Prop :=
  ∀ (Γ : Subgroup (GL (Fin 2) ℝ)) (h : ℝ) (f : CuspForm Γ 2),
    ModularFormClass.qExpansion h f = ModularFormClass.qExpansion h f

theorem mathlibModularFormClassQExpansionAnchor :
    MathlibModularFormClassQExpansionAnchor :=
  fun _ _ _ => rfl

/-- Typechecked wrapper around mathlib's q-expansion coefficient uniqueness theorem. -/
theorem mathlibQExpansionCoeffUniqueAnchor
    {k : ℤ} {F : Type*} [FunLike F UpperHalfPlane ℂ]
    {Γ : Subgroup (GL (Fin 2) ℝ)} {h : ℝ} {c : ℕ → ℂ}
    (hh : 0 < h) (hΓ : h ∈ Γ.strictPeriods) {f : F} [ModularFormClass F Γ k]
    (hf : ∀ τ : UpperHalfPlane,
      HasSum (fun m ↦ c m • Function.Periodic.qParam h (τ : ℂ) ^ m) (f τ))
    (m : ℕ) :
    c m = (ModularFormClass.qExpansion h f).coeff m :=
  qExpansion_coeff_unique hh hΓ hf m

/--
Integration-ready audit row for `THM-M-0131-P05`.

This separates q-expansion coefficient facts that are checked in the pinned
mathlib snapshot from the Frobenius-trace/newform bridge names that are still
absent. Rows marked `missing` are intentionally strings, not theorem
declarations.
-/
structure QExpansionFrobeniusAPIAuditRow where
  declaration : String
  moduleName : String
  repoLocalStatus : String
  role : String

/--
Public-backfill data for q-expansion/Frobenius-trace compatibility blockers.

The checked q-expansion side is available for modular forms and cusp forms. The
elliptic-curve arithmetic side still lacks concrete declarations for Frobenius
trace, point-count normalization, normalized newforms/eigenvalues, and the final
good-prime coefficient equality.
-/
def p05QExpansionFrobeniusAPIAudit : List QExpansionFrobeniusAPIAuditRow :=
  [ { declaration := "ModularFormClass.qExpansion"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "import-checked"
      role := "PowerSeries-valued q-expansion for a modular form at a positive strict period" },
    { declaration := "qExpansion_coeff"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "wrapper-checked below"
      role := "identifies the m-th q-expansion coefficient with the Taylor coefficient of the cusp function" },
    { declaration := "qExpansion_coeff_zero"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "wrapper-checked below"
      role := "constant coefficient equals value at infinity under period hypotheses" },
    { declaration := "hasSum_qExpansion"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "wrapper-checked below"
      role := "q-expansion series sums to the modular form on the upper half-plane" },
    { declaration := "qExpansion_coeff_unique"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "wrapper-checked above"
      role := "coefficient uniqueness for q-expansions" },
    { declaration := "qExpansion_coeff_eq_intervalIntegral"
      moduleName := "Mathlib.NumberTheory.ModularForms.QExpansion"
      repoLocalStatus := "wrapper-checked below"
      role := "integral formula for q-expansion coefficients along a horizontal period interval" },
    { declaration := "CongruenceSubgroup.strictWidthInfty_Gamma0"
      moduleName := "Mathlib.NumberTheory.ModularForms.Cusps"
      repoLocalStatus := "wrapper-checked above"
      role := "normalizes the Gamma0 q-expansion period at infinity to 1" },
    { declaration := "WeierstrassCurve.HasGoodReduction"
      moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction"
      repoLocalStatus := "import-checked"
      role := "local good-reduction predicate, but not yet a finite-field point-count/Frobenius trace API" },
    { declaration := "WeierstrassCurve.hasGoodReduction_iff_isElliptic_reduction"
      moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction"
      repoLocalStatus := "wrapper-checked below"
      role := "connects good reduction to ellipticity of the reduced Weierstrass curve" },
    { declaration := "RationalWeierstrassEllipticCurve.goodPrimeFrobeniusTrace"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed definition of a_p(E) or trace(Frob_p | E) for good primes p" },
    { declaration := "RationalWeierstrassEllipticCurve.reductionCardinality_eq_prime_add_one_sub_frobeniusTrace"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed normalization theorem #E(F_p) = p + 1 - a_p(E)" },
    { declaration := "WeightTwoCuspFormCandidate.normalized_qExpansionCoeff_one"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed normalization for the associated weight-two eigenform/newform" },
    { declaration := "WeightTwoCuspFormCandidate.heckeEigenvalue_eq_qExpansionCoeff"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed bridge identifying Hecke eigenvalues with q-expansion coefficients" },
    { declaration := "ModularityWitness.qExpansionCoeff_eq_frobeniusTrace_at_good_prime"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "terminal good-prime compatibility a_p(f) = a_p(E)" },
    { declaration := "ModularityWitness.badPrimeLocalFactor_qExpansionCompatibility"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "ramified-prime compatibility needed before replacing the Prop field with local-factor data" } ]

/-- The Gamma0 q-expansion coefficient selected by the current statement shape. -/
def gamma0QExpansionCoeff (N m : ℕ) (f : WeightTwoCuspFormCandidate N) : ℂ :=
  (ModularFormClass.qExpansion (Gamma0LevelSubgroup N).strictWidthInfty f.f).coeff m

theorem gamma0QExpansionCoeff_eq (N m : ℕ) (f : WeightTwoCuspFormCandidate N) :
    gamma0QExpansionCoeff N m f =
      (ModularFormClass.qExpansion (Gamma0LevelSubgroup N).strictWidthInfty f.f).coeff m :=
  rfl

theorem gamma0QExpansionCoeff_widthOne_eq (N m : ℕ) (f : WeightTwoCuspFormCandidate N) :
    gamma0QExpansionCoeff N m f =
      (ModularFormClass.qExpansion 1 f.f).coeff m := by
  rw [gamma0QExpansionCoeff, gamma0StrictWidthInftyAnchor]

theorem mathlibQExpansionCoeffAnchor
    (Γ : Subgroup (GL (Fin 2) ℝ)) (h : ℝ) (f : CuspForm Γ 2) (m : ℕ) :
    (ModularFormClass.qExpansion h f).coeff m =
      (↑m.factorial)⁻¹ * iteratedDeriv m (SlashInvariantFormClass.cuspFunction h f) 0 :=
  ModularFormClass.qExpansion_coeff f m

theorem mathlibQExpansionCoeffZeroAnchor
    (Γ : Subgroup (GL (Fin 2) ℝ)) (h : ℝ) (f : CuspForm Γ 2)
    (hh : 0 < h) (hΓ : h ∈ Γ.strictPeriods) :
    (ModularFormClass.qExpansion h f).coeff 0 = UpperHalfPlane.valueAtInfty f :=
  ModularFormClass.qExpansion_coeff_zero f hh hΓ

theorem mathlibHasSumQExpansionAnchor
    (Γ : Subgroup (GL (Fin 2) ℝ)) (h : ℝ) (f : CuspForm Γ 2)
    (hh : 0 < h) (hΓ : h ∈ Γ.strictPeriods) (τ : UpperHalfPlane) :
    HasSum
      (fun m : ℕ => (ModularFormClass.qExpansion h f).coeff m •
        Function.Periodic.qParam h (τ : ℂ) ^ m)
      (f τ) :=
  ModularFormClass.hasSum_qExpansion f hh hΓ τ

theorem mathlibQExpansionCoeffIntervalIntegralAnchor
    (Γ : Subgroup (GL (Fin 2) ℝ)) (h : ℝ) (f : CuspForm Γ 2)
    (hh : 0 < h) (hΓ : h ∈ Γ.strictPeriods) (n : ℕ) {t : ℝ} (ht : 0 < t) :
    (ModularFormClass.qExpansion h f).coeff n =
      1 / h * ∫ u in 0..h,
        1 / Function.Periodic.qParam h (u + t * Complex.I) ^ n *
          f ⟨u + t * Complex.I, by simpa using ht⟩ :=
  ModularFormClass.qExpansion_coeff_eq_intervalIntegral f hh hΓ n ht

theorem mathlibGoodReductionEllipticReductionAnchor
    (R K : Type*) [CommRing R] [IsDomain R] [IsDiscreteValuationRing R]
    [Field K] [Algebra R K] [IsFractionRing R K] (W : WeierstrassCurve K)
    [WeierstrassCurve.IsMinimal R W] :
    WeierstrassCurve.HasGoodReduction R W ↔ (W.reduction R).IsElliptic :=
  WeierstrassCurve.hasGoodReduction_iff_isElliptic_reduction (R := R) (W := W)

/-- Exact missing declaration names proposed by the P05 audit. -/
def p05MissingQExpansionFrobeniusTheoremNames : List String :=
  [ "RationalWeierstrassEllipticCurve.goodPrimeFrobeniusTrace",
    "RationalWeierstrassEllipticCurve.reductionCardinality_eq_prime_add_one_sub_frobeniusTrace",
    "WeightTwoCuspFormCandidate.normalized_qExpansionCoeff_one",
    "WeightTwoCuspFormCandidate.heckeEigenvalue_eq_qExpansionCoeff",
    "ModularityWitness.qExpansionCoeff_eq_frobeniusTrace_at_good_prime",
    "ModularityWitness.badPrimeLocalFactor_qExpansionCompatibility" ]

/--
Integration-ready audit row for `THM-M-0131-P06`.

The checked declarations below come from `Mathlib.NumberTheory.LSeries.*`.
Rows marked `missing` are intentional blocker names for elliptic-curve and
newform L-series APIs that are not present in the audited local mathlib modules.
-/
structure LSeriesCompatibilityAPIAuditRow where
  declaration : String
  moduleName : String
  repoLocalStatus : String
  role : String

/--
Public-backfill data for L-series compatibility blockers.

Mathlib supplies a general Dirichlet/L-series substrate for coefficient
sequences, convergence, abscissae of absolute convergence, derivatives, and
analyticity on the half-plane of absolute convergence. The modularity theorem
needs substantially more arithmetic structure: elliptic-curve Hasse-Weil
coefficients, a newform/eigenform coefficient package, local Euler factors at
good and bad primes, completed L-functions with conductor/gamma factor, and
the theorem equating these data.
-/
def p06LSeriesCompatibilityAPIAudit : List LSeriesCompatibilityAPIAuditRow :=
  [ { declaration := "LSeries.term"
      moduleName := "Mathlib.NumberTheory.LSeries.Basic"
      repoLocalStatus := "wrapper-checked below"
      role := "n-th term f n / n^s of a coefficient-sequence L-series" },
    { declaration := "LSeries"
      moduleName := "Mathlib.NumberTheory.LSeries.Basic"
      repoLocalStatus := "wrapper-checked below"
      role := "generic complex-valued Dirichlet series attached to coefficients f : Nat -> Complex" },
    { declaration := "LSeriesSummable"
      moduleName := "Mathlib.NumberTheory.LSeries.Basic"
      repoLocalStatus := "wrapper-checked below"
      role := "absolute convergence predicate for the generic L-series" },
    { declaration := "LSeriesHasSum"
      moduleName := "Mathlib.NumberTheory.LSeries.Basic"
      repoLocalStatus := "wrapper-checked below"
      role := "sum predicate connecting the term series to a concrete complex value" },
    { declaration := "LSeries.abscissaOfAbsConv"
      moduleName := "Mathlib.NumberTheory.LSeries.Convergence"
      repoLocalStatus := "wrapper-checked below through Deriv import"
      role := "abscissa of absolute convergence for a coefficient-sequence L-series" },
    { declaration := "LSeries_analyticOn"
      moduleName := "Mathlib.NumberTheory.LSeries.Deriv"
      repoLocalStatus := "wrapper-checked below"
      role := "holomorphy of the generic L-series on its half-plane of absolute convergence" },
    { declaration := "LSeries_deriv"
      moduleName := "Mathlib.NumberTheory.LSeries.Deriv"
      repoLocalStatus := "wrapper-checked below"
      role := "derivative formula for a generic L-series in its absolute-convergence half-plane" },
    { declaration := "RationalWeierstrassEllipticCurve.lSeriesCoefficients"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed coefficients a_n(E) or Euler-product coefficients for the Hasse-Weil L-series of E/Q" },
    { declaration := "RationalWeierstrassEllipticCurve.lSeries"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed elliptic-curve L-series object specialized from the generic LSeries substrate" },
    { declaration := "RationalWeierstrassEllipticCurve.localEulerFactor"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed good-prime and bad-prime Euler factors, including conductor-dependent ramified factors" },
    { declaration := "WeightTwoCuspFormCandidate.newformLSeriesCoefficients"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed normalized newform/eigenform coefficient sequence compatible with q-expansion coefficients" },
    { declaration := "WeightTwoCuspFormCandidate.lSeries"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed modular-form L-series object for the associated weight-two newform" },
    { declaration := "WeightTwoCuspFormCandidate.localEulerFactor"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed Euler factors attached to Hecke eigenvalues at all primes" },
    { declaration := "ModularityWitness.lSeriesCoefficients_eq"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed global equality a_n(E) = a_n(f), not only good-prime trace equality" },
    { declaration := "ModularityWitness.localEulerFactor_eq"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "needed equality of every local Euler factor, including ramified primes" },
    { declaration := "ModularityWitness.lSeries_eq"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "terminal theorem replacing the abstract lSeriesCompatible Prop field" },
    { declaration := "ModularityWitness.completedLSeries_eq"
      moduleName := "missing from audited local mathlib modules"
      repoLocalStatus := "missing"
      role := "optional stronger completed-L-function equality with conductor and gamma-factor normalization" } ]

/-- The generic mathlib L-series attached to a complex coefficient sequence. -/
def genericCoefficientLSeries (a : ℕ → ℂ) : ℂ → ℂ :=
  LSeries a

theorem genericCoefficientLSeries_eq (a : ℕ → ℂ) (s : ℂ) :
    genericCoefficientLSeries a s = LSeries a s :=
  rfl

theorem mathlibLSeriesTermAnchor (a : ℕ → ℂ) (s : ℂ) (n : ℕ) :
    LSeries.term a s n = if n = 0 then 0 else a n / n ^ s :=
  LSeries.term_def a s n

theorem mathlibLSeriesSummableZeroAnchor (s : ℂ) :
    LSeriesSummable 0 s :=
  LSeriesSummable_zero

theorem mathlibLSeriesSummableMonotoneRealPartAnchor
    {a : ℕ → ℂ} {s s' : ℂ} (hss' : s.re ≤ s'.re)
    (hs : LSeriesSummable a s) :
    LSeriesSummable a s' :=
  hs.of_re_le_re hss'

theorem mathlibLSeriesHasSumValueAnchor
    {a : ℕ → ℂ} {s value : ℂ} (h : LSeriesHasSum a s value) :
    LSeries a s = value :=
  h.LSeries_eq

theorem mathlibLSeriesSummableOfAbscissaAnchor
    {a : ℕ → ℂ} {s : ℂ} (hs : LSeries.abscissaOfAbsConv a < s.re) :
    LSeriesSummable a s :=
  LSeriesSummable_of_abscissaOfAbsConv_lt_re hs

theorem mathlibLSeriesDerivAnchor
    {a : ℕ → ℂ} {s : ℂ} (hs : LSeries.abscissaOfAbsConv a < s.re) :
    deriv (LSeries a) s = -LSeries (LSeries.logMul a) s :=
  LSeries_deriv hs

theorem mathlibLSeriesAnalyticOnAnchor (a : ℕ → ℂ) :
    AnalyticOn ℂ (LSeries a) {s : ℂ | LSeries.abscissaOfAbsConv a < s.re} :=
  LSeries_analyticOn a

/-- Exact missing declaration names proposed by the P06 audit. -/
def p06MissingLSeriesCompatibilityTheoremNames : List String :=
  [ "RationalWeierstrassEllipticCurve.lSeriesCoefficients",
    "RationalWeierstrassEllipticCurve.lSeries",
    "RationalWeierstrassEllipticCurve.localEulerFactor",
    "WeightTwoCuspFormCandidate.newformLSeriesCoefficients",
    "WeightTwoCuspFormCandidate.lSeries",
    "WeightTwoCuspFormCandidate.localEulerFactor",
    "ModularityWitness.lSeriesCoefficients_eq",
    "ModularityWitness.localEulerFactor_eq",
    "ModularityWitness.lSeries_eq",
    "ModularityWitness.completedLSeries_eq" ]

/--
Integration-ready audit row for `THM-M-0131-P07`.

The rows record source-search facts as data. They deliberately distinguish
checked local dependency scans from the blocked authenticated GitHub code-search
step, because M0387-level bookkeeping does not allow anchor-only or
unauthenticated evidence to close an external-proof integration gate.
-/
structure ExternalLeanCodeSearchAuditRow where
  searchSurface : String
  exactQueryOrTerms : String
  observedResult : String
  implication : String

/-- Search terms required by the P07 external Lean-code audit. -/
def p07RequiredExternalSearchTerms : List String :=
  [ "Taniyama",
    "Shimura",
    "ModularityTheorem",
    "elliptic modularity",
    "elliptic curve modularity",
    "newform",
    "Gamma0",
    "WeierstrassCurve",
    "EllipticCurve" ]

/--
P07 external-code-search audit data.

The local Lake closure was scanned at the pinned revisions recorded in
`lake-manifest.json`: mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` and
`flt-regular` `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. GitHub's code-search
API returned `401 Requires authentication` and the local `gh` client reported no
logged-in GitHub host, so the requested authenticated global code search remains
an explicit process blocker rather than completion evidence.
-/
def p07ExternalLeanCodeSearchAudit : List ExternalLeanCodeSearchAuditRow :=
  [ { searchSurface := "repo-local Lake dependency closure"
      exactQueryOrTerms :=
        "Taniyama; Shimura; ModularityTheorem; elliptic modularity; " ++
          "elliptic curve modularity; newform; Gamma0; WeierstrassCurve; EllipticCurve"
      observedResult :=
        "mathlib/flt-regular scan found Gamma0, WeierstrassCurve, and elliptic-curve " ++
          "model APIs; it found no Taniyama, Shimura, ModularityTheorem, " ++
          "elliptic-curve modularity, or newform theorem candidate"
      implication :=
        "local dependency closure supplies substrate anchors only, not a terminal " ++
          "Shimura/Taniyama-Shimura modularity proof" },
    { searchSurface := "GitHub REST code search"
      exactQueryOrTerms := "Taniyama Shimura language:Lean"
      observedResult := "HTTP 401 with message Requires authentication"
      implication :=
        "authenticated primary-source global code search could not be completed in " ++
          "this worker environment" },
    { searchSurface := "GitHub CLI authentication"
      exactQueryOrTerms := "gh auth status"
      observedResult := "no logged-in GitHub hosts; no GH_TOKEN/GITHUB_TOKEN found"
      implication :=
        "P07 must remain open until an authenticated search is run, or credentials " ++
          "are supplied and the search is rerun" },
    { searchSurface := "GitHub REST repository search"
      exactQueryOrTerms := "Taniyama Shimura Lean"
      observedResult := "HTTP 200 with total_count 0"
      implication :=
        "unauthenticated repository-name/description search found no candidate, but " ++
          "this does not replace authenticated code search" },
    { searchSurface := "GitHub raw primary-source spot check"
      exactQueryOrTerms :=
        "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95 " ++
          "Mathlib/NumberTheory/ModularForms/CongruenceSubgroups.lean"
      observedResult :=
        "HTTP 200 source contains CongruenceSubgroup.Gamma0 and related subgroup APIs"
      implication :=
        "confirms a primary-source Gamma0 substrate anchor, not elliptic-curve " ++
          "modularity closure" } ]

/--
M0387 external-proof gate states for P07.

`authenticatedSearchBlocked` is intentionally non-completing: it records a
concrete process blocker for the search task itself, not an integration blocker
for a known proof-bearing repository.
-/
inductive P07ExternalLean4ProofGateStatus where
  /-- No exact proof candidate was found in the inspected local and public surfaces. -/
  | noCandidateFoundInInspectedSources
  /-- A proof candidate is pinned or vendored, imported, and checked locally. -/
  | pinnedImportedChecked
  /-- A proof candidate exists but has a concrete pin/import/check blocker. -/
  | candidateFoundConcreteIntegrationBlocker
  /-- The required authenticated global code search could not be completed. -/
  | authenticatedSearchBlocked
  /-- Only URL/name/source-note evidence exists; this cannot close the gate. -/
  | anchorOnlyUnresolved
  deriving DecidableEq, Repr

/-- Whether the P07 external-proof gate can be treated as resolved for audit bookkeeping. -/
def P07ExternalLean4ProofGateStatus.integrationGateResolved
    (status : P07ExternalLean4ProofGateStatus) : Bool :=
  match status with
  | .noCandidateFoundInInspectedSources => true
  | .pinnedImportedChecked => true
  | .candidateFoundConcreteIntegrationBlocker => true
  | .authenticatedSearchBlocked => false
  | .anchorOnlyUnresolved => false

/-- Whether the P07 status is repo-local theorem-completion evidence. -/
def P07ExternalLean4ProofGateStatus.repoLocalCompletionEvidence
    (status : P07ExternalLean4ProofGateStatus) : Bool :=
  match status with
  | .pinnedImportedChecked => true
  | .noCandidateFoundInInspectedSources => false
  | .candidateFoundConcreteIntegrationBlocker => false
  | .authenticatedSearchBlocked => false
  | .anchorOnlyUnresolved => false

/-- Current P07 status: the authenticated global search is blocked by missing credentials. -/
def p07CurrentExternalLean4ProofGateStatus : P07ExternalLean4ProofGateStatus :=
  .authenticatedSearchBlocked

theorem p07CurrentExternalLean4ProofGate_unresolved :
    p07CurrentExternalLean4ProofGateStatus.integrationGateResolved = false :=
  rfl

theorem p07CurrentExternalLean4ProofGate_not_completionEvidence :
    p07CurrentExternalLean4ProofGateStatus.repoLocalCompletionEvidence = false :=
  rfl

theorem p07AnchorOnlyExternalLean4ProofGate_unresolved :
    P07ExternalLean4ProofGateStatus.anchorOnlyUnresolved.integrationGateResolved = false :=
  rfl

theorem p07AnchorOnlyExternalLean4ProofGate_not_completionEvidence :
    P07ExternalLean4ProofGateStatus.anchorOnlyUnresolved.repoLocalCompletionEvidence = false :=
  rfl

/-- Exact missing execution condition before P07 can be publicly checked. -/
def p07AuthenticatedSearchBlocker : String :=
  "Run authenticated GitHub/primary-source Lean code search for the P07 terms; " ++
    "if an external proof candidate is found, record URL, revision, module, theorem, " ++
    "license/toolchain compatibility, then pin/import/check it or record a concrete " ++
    "integration blocker while keeping THM-M-0131 open."

/--
Integration-ready row for the `THM-M-0131-P08` `<=100` leaf ledger.

The rows are process data for public backfill. They are intentionally all
`unchecked`; none is a proof of the modularity theorem or a completed-status
upgrade.
-/
structure LocalLeafBudgetLedgerRow where
  leafId : String
  package : String
  leafTarget : String
  budget : String
  status : String

/-- Public-backfill data for the P08 `<=100` local leaf ledger. -/
def p08LocalLeafBudgetLedger : List LocalLeafBudgetLedgerRow :=
  [ { leafId := "S1-M-048-L001"
      package := "P01"
      leafTarget := "Verify statement namespace, imports, base field Q, and no hidden axioms/sorries."
      budget := "<= 25"
      status := "unchecked" },
    { leafId := "S1-M-048-L002"
      package := "P01"
      leafTarget :=
        "Decide whether final object should be Weierstrass model, scheme-level elliptic curve over Spec Q, or equivalence between them."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L003"
      package := "P02"
      leafTarget := "Import-check WeierstrassCurve, IsElliptic, j, point models, and reduction APIs."
      budget := "<= 60"
      status := "unchecked" },
    { leafId := "S1-M-048-L004"
      package := "P02"
      leafTarget :=
        "Import-check ModularForm, CuspForm, Gamma0, Gamma1, qExpansion, and modular group fundamental-domain APIs."
      budget := "<= 60"
      status := "unchecked" },
    { leafId := "S1-M-048-L005"
      package := "P03"
      leafTarget := "Define a first Lean statement for elliptic-curve conductor or record exact missing API blocker."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L006"
      package := "P03"
      leafTarget := "Replace abstract Gamma witness by Gamma0 level or a justified subgroup coercion path."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L007"
      package := "P04"
      leafTarget := "Define Frobenius trace/Euler-factor coefficient target for good primes, or document missing Galois/reduction APIs."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L008"
      package := "P04"
      leafTarget := "Connect q-expansion coefficient indexing to the Frobenius trace convention."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L009"
      package := "P05"
      leafTarget := "Choose L-series equality formulation and convergence domain using Mathlib.NumberTheory.LSeries.*."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L010"
      package := "P06"
      leafTarget := "Audit Hecke/newform APIs and identify missing declarations by theorem name."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L011"
      package := "P07"
      leafTarget := "Audit Galois representation and local Frobenius APIs for elliptic curves."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L012"
      package := "P08"
      leafTarget := "State modularity-lifting theorem boundary with explicit local conditions."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L013"
      package := "P08"
      leafTarget := "State deformation-ring/Hecke-algebra bridge boundary."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L014"
      package := "P09"
      leafTarget := "Define root theorem from the completed compatibility branches."
      budget := "<= 100"
      status := "unchecked" },
    { leafId := "S1-M-048-L015"
      package := "P10"
      leafTarget := "If an external proof is found, pin/import/check it or record an exact dependency blocker."
      budget := "<= 100"
      status := "unchecked" } ]

theorem p08LocalLeafBudgetLedger_length :
    p08LocalLeafBudgetLedger.length = 15 :=
  rfl

/-- P08 is public-process backfill data, not repo-local theorem completion evidence. -/
def p08LocalLeafBudgetLedgerIsCompletionEvidence : Bool :=
  false

theorem p08LocalLeafBudgetLedger_not_completionEvidence :
    p08LocalLeafBudgetLedgerIsCompletionEvidence = false :=
  rfl

end Stage1.S1_M_048
