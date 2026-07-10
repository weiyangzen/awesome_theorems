import Mathlib.Algebra.MonoidAlgebra.Basic
import Mathlib.Algebra.Lie.Character
import Mathlib.Algebra.Lie.Extension
import Mathlib.Algebra.Lie.Loop
import Mathlib.Algebra.Lie.Weights.Basic
import Mathlib.LinearAlgebra.RootSystem.WeylGroup
import Mathlib.RingTheory.HahnSeries.Basic

/-!
# Stage1 statement shape for S1-M-053 / THM-M-0137

This file is a conservative Stage1 artifact for the Kac-Peterson character formula for affine
Lie algebras.  It records a formalization boundary and checks the mathlib objects that are
currently close to the statement: loop Lie algebras, Lie characters, weight spaces, and Weyl
groups.  It is not a proof of the Kac-Peterson formula.
-/

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_053

universe u v w uι uR uM uN uS uG

/-- The untwisted polynomial loop algebra anchor available in mathlib. -/
abbrev UntwistedLoopAlgebra (R : Type u) (L : Type v)
    [CommRing R] [LieRing L] [LieAlgebra R L] : Type (max u v) :=
  LieAlgebra.loopAlgebra R ℤ L

/--
Canonical Stage1 target decision for the affine Kac-Moody algebra core.

The checked mathlib target is the untwisted polynomial loop algebra
`LieAlgebra.loopAlgebra R ℤ L`.  This is only the loop-algebra core of the usual untwisted
affine Kac-Moody construction; the central extension, degree derivation, affine Weyl action,
and positive-energy representation stack remain separate formalization targets.
-/
theorem untwistedLoopAlgebra_eq (R : Type u) (L : Type v)
    [CommRing R] [LieRing L] [LieAlgebra R L] :
    UntwistedLoopAlgebra R L = LieAlgebra.loopAlgebra R ℤ L :=
  rfl

/-! ## Character-ring and formal-series boundary for affine characters -/

/--
Finite formal characters over an additive weight lattice.

This is the checked mathlib object for finite support formal sums `∑ c_λ e^λ`.
It is a useful character-ring substrate, but it is too small for affine
highest-weight characters whose weight supports are usually infinite.
-/
abbrev FiniteFormalCharacterRing (Coeff : Type uR) (Weight : Type w)
    [Semiring Coeff] [AddMonoid Weight] : Type (max uR w) :=
  AddMonoidAlgebra Coeff Weight

/-- The finite formal-character ring is exactly mathlib's additive monoid algebra. -/
theorem finiteFormalCharacterRing_eq (Coeff : Type uR) (Weight : Type w)
    [Semiring Coeff] [AddMonoid Weight] :
    FiniteFormalCharacterRing Coeff Weight = AddMonoidAlgebra Coeff Weight :=
  rfl

/--
Hahn-series formal characters over an ordered weight lattice.

This gives a repo-local, checked infinite formal-series object with coefficient
function and partially well-ordered support.  A terminal Kac-Peterson
formalization still has to choose the affine weight order and prove that the
relevant character and denominator expansions satisfy the required support
conditions.
-/
abbrev HahnFormalCharacterSeries (Weight : Type w) (Coeff : Type uR)
    [PartialOrder Weight] [Zero Coeff] : Type (max w uR) :=
  HahnSeries Weight Coeff

/-- The Hahn formal-character series object is exactly mathlib's `HahnSeries`. -/
theorem hahnFormalCharacterSeries_eq (Weight : Type w) (Coeff : Type uR)
    [PartialOrder Weight] [Zero Coeff] :
    HahnFormalCharacterSeries Weight Coeff = HahnSeries Weight Coeff :=
  rfl

/-- The zero Hahn formal character has all coefficients equal to zero. -/
theorem hahnFormalCharacterSeries_coeff_zero {Weight : Type w} {Coeff : Type uR}
    [PartialOrder Weight] [Zero Coeff] (weight : Weight) :
    (0 : HahnFormalCharacterSeries Weight Coeff).coeff weight = 0 :=
  HahnSeries.coeff_zero

/--
Abstract interface for the affine formal-character series still needed by the
terminal Kac-Peterson statement.

The interface records the coefficient map, support predicate, and denominator
expansion predicate without claiming that the affine Kac-Moody order and
summability/support lemmas have been built.  Concrete future instances should
prefer `HahnFormalCharacterSeries` when a compatible affine weight order is
available.
-/
structure AffineFormalCharacterSeries (Weight : Type w) (Coeff : Type uR)
    (Series : Type uS) [Zero Coeff] [Semiring Series] where
  coeff : Series → Weight → Coeff
  coeff_zero : ∀ weight : Weight, coeff 0 weight = 0
  supportCondition : Series → Prop
  denominatorExpansionAllowed : Series → Prop

/-- Coefficient-zero projection for the affine formal-character interface. -/
theorem affineFormalCharacterSeries_coeff_zero {Weight : Type w} {Coeff : Type uR}
    {Series : Type uS} [Zero Coeff] [Semiring Series]
    (χ : AffineFormalCharacterSeries Weight Coeff Series) (weight : Weight) :
    χ.coeff 0 weight = 0 :=
  χ.coeff_zero weight

/-! ## Highest-weight and integrability predicate boundary -/

/--
Abstract predicate data for affine highest-weight representations.

The fields are deliberately interface-level hooks.  They describe the predicates needed by the
Kac-Peterson statement without claiming that mathlib already supplies a completed affine
Kac-Moody representation package.  Future refinements should replace these hooks by concrete
central-extension, degree-derivation, affine-root, and weight-space APIs.
-/
structure AffineRepresentationPredicateData (Rep : Type v) (Weight : Type w)
    (SimpleRoot : Type uι) where
  isWeightVector : Rep → Weight → Prop
  positiveRootActionVanishes : Rep → Prop
  generatesModule : Rep → Prop
  simpleRootActionLocallyFinite : SimpleRoot → Prop
  level : Weight → ℤ
  energy : Weight → ℤ
  simpleCorootPairing : SimpleRoot → Weight → ℤ

/-- A vector is highest-weight of weight `λ` when it is a weight vector killed by positive roots. -/
def IsHighestWeightVector {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    (D : AffineRepresentationPredicateData Rep Weight SimpleRoot) (v : Rep)
    (highestWeight : Weight) : Prop :=
  D.isWeightVector v highestWeight ∧ D.positiveRootActionVanishes v

/-- A representation is highest-weight of weight `λ` if it is generated by a highest-weight vector. -/
def IsHighestWeightModule {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    (D : AffineRepresentationPredicateData Rep Weight SimpleRoot)
    (highestWeight : Weight) : Prop :=
  ∃ v : Rep, IsHighestWeightVector D v highestWeight ∧ D.generatesModule v

/--
Interface-level integrability predicate: each simple-root `sl₂` direction is locally finite.

The actual local-finiteness theorem for affine Kac-Moody root operators is still a future
formalization target; this predicate records the exact slot it must occupy.
-/
def IsIntegrableRepresentation {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    (D : AffineRepresentationPredicateData Rep Weight SimpleRoot) : Prop :=
  ∀ i : SimpleRoot, D.simpleRootActionLocallyFinite i

/-- The highest weight has level `k`. -/
def HasLevel {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    (D : AffineRepresentationPredicateData Rep Weight SimpleRoot)
    (highestWeight : Weight) (k : ℤ) : Prop :=
  D.level highestWeight = k

/-- Nonnegative affine level for a highest weight. -/
def IsPositiveLevelWeight {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    (D : AffineRepresentationPredicateData Rep Weight SimpleRoot)
    (highestWeight : Weight) : Prop :=
  0 ≤ D.level highestWeight

/-- Positive-energy boundary: the chosen highest weight has nonnegative energy degree. -/
def IsPositiveEnergyWeight {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    (D : AffineRepresentationPredicateData Rep Weight SimpleRoot)
    (highestWeight : Weight) : Prop :=
  0 ≤ D.energy highestWeight

/-- Dominant-integral boundary: all simple coroot pairings of the weight are nonnegative integers. -/
def IsDominantIntegralWeight {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    (D : AffineRepresentationPredicateData Rep Weight SimpleRoot)
    (highestWeight : Weight) : Prop :=
  ∀ i : SimpleRoot, 0 ≤ D.simpleCorootPairing i highestWeight

/--
Combined predicate package for the integrable positive-energy dominant-integral highest-weight
input expected by a future Kac-Peterson character formula statement.
-/
def IsIntegrablePositiveEnergyDominantHighestWeightModule {Rep : Type v} {Weight : Type w}
    {SimpleRoot : Type uι} (D : AffineRepresentationPredicateData Rep Weight SimpleRoot)
    (highestWeight : Weight) : Prop :=
  IsHighestWeightModule D highestWeight ∧
    IsIntegrableRepresentation D ∧
    IsPositiveLevelWeight D highestWeight ∧
    IsPositiveEnergyWeight D highestWeight ∧
    IsDominantIntegralWeight D highestWeight

/-- Projection from the combined predicate package to the highest-weight predicate. -/
theorem integrablePositiveEnergyDominantHighestWeightModule_highestWeight
    {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    {D : AffineRepresentationPredicateData Rep Weight SimpleRoot} {highestWeight : Weight}
    (h : IsIntegrablePositiveEnergyDominantHighestWeightModule D highestWeight) :
    IsHighestWeightModule D highestWeight :=
  h.1

/-- Projection from the combined predicate package to integrability. -/
theorem integrablePositiveEnergyDominantHighestWeightModule_integrable
    {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    {D : AffineRepresentationPredicateData Rep Weight SimpleRoot} {highestWeight : Weight}
    (h : IsIntegrablePositiveEnergyDominantHighestWeightModule D highestWeight) :
    IsIntegrableRepresentation D :=
  h.2.1

/-- Projection from the combined predicate package to nonnegative level. -/
theorem integrablePositiveEnergyDominantHighestWeightModule_positiveLevel
    {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    {D : AffineRepresentationPredicateData Rep Weight SimpleRoot} {highestWeight : Weight}
    (h : IsIntegrablePositiveEnergyDominantHighestWeightModule D highestWeight) :
    IsPositiveLevelWeight D highestWeight :=
  h.2.2.1

/-- Projection from the combined predicate package to positive energy. -/
theorem integrablePositiveEnergyDominantHighestWeightModule_positiveEnergy
    {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    {D : AffineRepresentationPredicateData Rep Weight SimpleRoot} {highestWeight : Weight}
    (h : IsIntegrablePositiveEnergyDominantHighestWeightModule D highestWeight) :
    IsPositiveEnergyWeight D highestWeight :=
  h.2.2.2.1

/-- Projection from the combined predicate package to dominant-integrality. -/
theorem integrablePositiveEnergyDominantHighestWeightModule_dominantIntegral
    {Rep : Type v} {Weight : Type w} {SimpleRoot : Type uι}
    {D : AffineRepresentationPredicateData Rep Weight SimpleRoot} {highestWeight : Weight}
    (h : IsIntegrablePositiveEnergyDominantHighestWeightModule D highestWeight) :
    IsDominantIntegralWeight D highestWeight :=
  h.2.2.2.2

/-! ## Finite-to-affine Weyl action and dot-action boundary -/

/--
Abstract bridge from a checked finite Weyl group to a future affine Weyl group action.

For the Kac-Peterson formula the Weyl sum uses the affine Weyl dot action
`w • (λ + ρ) - ρ`.  Mathlib currently supplies the finite `RootPairing.weylGroup` API, while
the affine Weyl group and its action on affine weights still have to be built or imported.
This structure records exactly the missing map and compatibility condition without treating
the finite API as an affine proof.
-/
structure FiniteToAffineWeylDotActionBridge
    (FiniteWeylGroup : Type uG) (AffineWeylGroup : Type uS) (Weight : Type w)
    [Group FiniteWeylGroup] [Group AffineWeylGroup] [AddCommGroup Weight] where
  finiteToAffine : FiniteWeylGroup →* AffineWeylGroup
  finiteAction : FiniteWeylGroup →* Weight ≃+ Weight
  affineAction : AffineWeylGroup →* Weight ≃+ Weight
  finiteAction_compatible : finiteAction = affineAction.comp finiteToAffine
  rho : Weight

namespace FiniteToAffineWeylDotActionBridge

variable {FiniteWeylGroup : Type uG} {AffineWeylGroup : Type uS} {Weight : Type w}
variable [Group FiniteWeylGroup] [Group AffineWeylGroup] [AddCommGroup Weight]

/-- Affine Weyl dot action with respect to the bridge's chosen `ρ`. -/
def affineDotAction
    (D : FiniteToAffineWeylDotActionBridge FiniteWeylGroup AffineWeylGroup Weight)
    (w : AffineWeylGroup) (weight : Weight) : Weight :=
  D.affineAction w (weight + D.rho) - D.rho

/-- Finite Weyl dot action transported through the finite-to-affine bridge. -/
def finiteDotActionViaAffine
    (D : FiniteToAffineWeylDotActionBridge FiniteWeylGroup AffineWeylGroup Weight)
    (w : FiniteWeylGroup) (weight : Weight) : Weight :=
  D.affineDotAction (D.finiteToAffine w) weight

/-- Compatibility of the finite action with the affine action after applying the bridge map. -/
theorem finiteAction_apply_eq_affineAction
    (D : FiniteToAffineWeylDotActionBridge FiniteWeylGroup AffineWeylGroup Weight)
    (w : FiniteWeylGroup) (weight : Weight) :
    D.finiteAction w weight = D.affineAction (D.finiteToAffine w) weight := by
  have h :=
    congrArg (fun f : FiniteWeylGroup →* Weight ≃+ Weight => f w)
      D.finiteAction_compatible
  exact congrArg (fun e : Weight ≃+ Weight => e weight) h

/-- The transported finite dot action is the finite action applied to `λ + ρ`, then shifted back. -/
theorem finiteDotActionViaAffine_eq_finiteAction
    (D : FiniteToAffineWeylDotActionBridge FiniteWeylGroup AffineWeylGroup Weight)
    (w : FiniteWeylGroup) (weight : Weight) :
    D.finiteDotActionViaAffine w weight = D.finiteAction w (weight + D.rho) - D.rho := by
  simp [finiteDotActionViaAffine, affineDotAction, finiteAction_apply_eq_affineAction]

end FiniteToAffineWeylDotActionBridge

/-- The checked finite Weyl action from mathlib's `RootPairing.weylGroup` API. -/
noncomputable def rootPairingFiniteWeylAction {ι : Type uι} {R : Type uR} {M : Type uM}
    {N : Type uN}
    [CommRing R] [AddCommGroup M] [Module R M] [AddCommGroup N] [Module R N]
    (P : RootPairing ι R M N) (w : P.weylGroup) (weight : M) : M :=
  w • weight

/--
Finite Weyl dot-action shape attached to `RootPairing.weylGroup`.

This is the finite-root-system part of the bridge.  It is not the affine Weyl group action
needed by the Kac-Peterson formula until a concrete affine Weyl group, affine weight lattice,
and compatibility map are supplied.
-/
noncomputable def rootPairingFiniteDotAction {ι : Type uι} {R : Type uR} {M : Type uM}
    {N : Type uN}
    [CommRing R] [AddCommGroup M] [Module R M] [AddCommGroup N] [Module R N]
    (P : RootPairing ι R M N) (rho : M) (w : P.weylGroup) (weight : M) : M :=
  rootPairingFiniteWeylAction P w (weight + rho) - rho

/-- The simple-reflection generator of the finite dot action is the mathlib root reflection. -/
theorem rootPairingFiniteDotAction_ofIdx {ι : Type uι} {R : Type uR} {M : Type uM}
    {N : Type uN} [CommRing R] [AddCommGroup M] [Module R M] [AddCommGroup N]
    [Module R N] (P : RootPairing ι R M N) (rho weight : M) (i : ι) :
    rootPairingFiniteDotAction P rho (RootPairing.weylGroup.ofIdx P i) weight =
      P.reflection i (weight + rho) - rho := by
  simp [rootPairingFiniteDotAction, rootPairingFiniteWeylAction]

/--
Data needed before a faithful Lean statement of the Kac-Peterson character formula can be
written.  The fields intentionally keep the unavailable pieces as propositions, rather than
pretending that mathlib already contains the full affine Kac-Moody representation stack.
-/
structure KacPetersonCharacterFormulaInput where
  AffineLieAlgebra : Type u
  HighestWeightModule : Type v
  WeightLattice : Type w
  SimpleRootIndex : Type uι
  AffineWeylGroup : Type uι
  CharacterRing : Type uR
  character : CharacterRing
  kacPetersonSeries : CharacterRing
  highestWeight : WeightLattice
  IsAffineKacMoody : Prop
  IsHighestWeightRepresentation : Prop
  IsIntegrableRepresentation : Prop
  IsPositiveEnergyRepresentation : Prop
  IsPositiveLevelRepresentation : Prop
  IsDominantIntegralHighestWeight : Prop
  IsIntegrableHighestWeightModule : Prop
  AffineWeylActionAvailable : Prop
  DotActionWellFormed : Prop
  CharacterRingModelsAffineFormalSeries : Prop
  WeylKacDenominatorAvailable : Prop
  CharacterFormulaWellFormed : Prop
  CharacterEqualsKacPetersonFormula : Prop

/--
Stage1 statement shape: once the affine Kac-Moody object, the integrable highest-weight module,
the denominator/formal-character infrastructure, and the formula expression are all available,
the module character equals the Kac-Peterson series.
-/
def StatementShape : Prop :=
  ∀ X : KacPetersonCharacterFormulaInput.{u, v, w, uι, uR},
    X.IsAffineKacMoody →
    X.IsHighestWeightRepresentation →
    X.IsIntegrableRepresentation →
    X.IsPositiveEnergyRepresentation →
    X.IsPositiveLevelRepresentation →
    X.IsDominantIntegralHighestWeight →
    X.IsIntegrableHighestWeightModule →
    X.AffineWeylActionAvailable →
    X.DotActionWellFormed →
    X.CharacterRingModelsAffineFormalSeries →
    X.WeylKacDenominatorAvailable →
    X.CharacterFormulaWellFormed →
    X.CharacterEqualsKacPetersonFormula

/-- Local wrapper for the current mathlib Lie-character bracket vanishing anchor. -/
theorem lieCharacter_bracket_vanishes {R : Type u} {L : Type v}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    (χ : LieAlgebra.LieCharacter R L) (x y : L) :
    χ ⁅x, y⁆ = 0 :=
  LieAlgebra.lieCharacter_apply_lie χ x y

/-- Local wrapper for the current mathlib weight-space membership anchor. -/
theorem mem_weightSpace_iff {R : Type u} {L : Type v} {M : Type w}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    [AddCommGroup M] [Module R M] [LieRingModule L M] [LieModule R L M]
    (χ : L → R) (m : M) :
    m ∈ LieModule.weightSpace M χ ↔ ∀ x : L, ⁅x, m⁆ = χ x • m :=
  LieModule.mem_weightSpace χ m

/-- Local wrapper for the current mathlib Weyl-group generator anchor. -/
theorem reflection_mem_weylGroup {ι : Type uι} {R : Type uR} {M : Type uM} {N : Type uN}
    [CommRing R] [AddCommGroup M] [Module R M] [AddCommGroup N] [Module R N]
    (P : RootPairing ι R M N) (i : ι) :
    RootPairing.Equiv.reflection P i ∈ P.weylGroup :=
  RootPairing.reflection_mem_weylGroup P i

/--
The central-extension-adjacent 2-cocycle supplied by `Mathlib.Algebra.Lie.Loop`.

This alias keeps the Stage1 audit tied to the actual mathlib object: an invariant symmetric
bilinear form on the base Lie algebra gives a two-cocycle on the loop algebra with trivial
coefficients.  Building the affine Kac-Moody central extension from this cocycle remains a
separate integration target.
-/
noncomputable abbrev LoopCentralExtensionCocycle (R : Type u) (A : Type v) (L : Type w)
    [CommRing R] [LieRing L] [LieAlgebra R L]
    [CommRing A] [IsAddTorsionFree R] [Algebra A R]
    (Φ : LinearMap.BilinForm R L)
    (hΦ : LinearMap.BilinForm.lieInvariant L Φ) (hΦs : Φ.IsSymm) :
    LieModule.Cohomology.twoCocycle R (LieAlgebra.loopAlgebra R A L)
      (TrivialLieModule R (LieAlgebra.loopAlgebra R A L) R) :=
  LieAlgebra.LoopAlgebra.twoCocycleOfBilinear R A L Φ hΦ hΦs

/-- Local wrapper for the residue-pairing formula underlying the loop-algebra 2-cochain. -/
theorem loop_twoCochainOfBilinear_apply_apply {R : Type u} {A : Type v} {L : Type w}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    [CommRing A] [IsAddTorsionFree R] [Algebra A R]
    (Φ : LinearMap.BilinForm R L) (hΦs : Φ.IsSymm)
    (x y : LieAlgebra.loopAlgebra R A L) :
    LieAlgebra.LoopAlgebra.twoCochainOfBilinear R A L Φ hΦs x y =
      (TrivialLieModule.equiv R (LieAlgebra.loopAlgebra R A L) R).symm
        (LieAlgebra.LoopAlgebra.residuePairing R A L Φ x y) :=
  LieAlgebra.LoopAlgebra.twoCochainOfBilinear_apply_apply R A L Φ hΦs x y

/-- The loop-algebra cocycle is bundled from the corresponding residue 2-cochain. -/
theorem loop_twoCocycleOfBilinear_val {R : Type u} {A : Type v} {L : Type w}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    [CommRing A] [IsAddTorsionFree R] [Algebra A R]
    (Φ : LinearMap.BilinForm R L)
    (hΦ : LinearMap.BilinForm.lieInvariant L Φ) (hΦs : Φ.IsSymm) :
    (LieAlgebra.LoopAlgebra.twoCocycleOfBilinear R A L Φ hΦ hΦs).val =
      LieAlgebra.LoopAlgebra.twoCochainOfBilinear R A L Φ hΦs :=
  rfl

/-! ## Audit constants retained for Stage1 repair bookkeeping -/

/-- The statement-shape identity used by audit tooling. -/
theorem statementShape_iff :
    StatementShape.{u, v, w, uι, uR} ↔
      ∀ X : KacPetersonCharacterFormulaInput.{u, v, w, uι, uR},
        X.IsAffineKacMoody →
        X.IsHighestWeightRepresentation →
        X.IsIntegrableRepresentation →
        X.IsPositiveEnergyRepresentation →
        X.IsPositiveLevelRepresentation →
        X.IsDominantIntegralHighestWeight →
        X.IsIntegrableHighestWeightModule →
        X.AffineWeylActionAvailable →
        X.DotActionWellFormed →
        X.CharacterRingModelsAffineFormalSeries →
        X.WeylKacDenominatorAvailable →
        X.CharacterFormulaWellFormed →
        X.CharacterEqualsKacPetersonFormula :=
  Iff.rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.MonoidAlgebra.Basic",
  "Mathlib.Algebra.Lie.Character",
  "Mathlib.Algebra.Lie.Extension",
  "Mathlib.Algebra.Lie.Loop",
  "Mathlib.Algebra.Lie.Weights.Basic",
  "Mathlib.LinearAlgebra.RootSystem.WeylGroup",
  "Mathlib.RingTheory.HahnSeries.Basic"
]

/-- Pinned theorem or definition names used by this local artifact. -/
def repoLocalAnchorNames : List String := [
  "AddMonoidAlgebra",
  "HahnSeries",
  "HahnSeries.coeff",
  "HahnSeries.coeff_zero",
  "FiniteFormalCharacterRing",
  "HahnFormalCharacterSeries",
  "AffineFormalCharacterSeries",
  "AffineRepresentationPredicateData",
  "IsHighestWeightVector",
  "IsHighestWeightModule",
  "IsIntegrableRepresentation",
  "HasLevel",
  "IsPositiveLevelWeight",
  "IsPositiveEnergyWeight",
  "IsDominantIntegralWeight",
  "IsIntegrablePositiveEnergyDominantHighestWeightModule",
  "FiniteToAffineWeylDotActionBridge",
  "FiniteToAffineWeylDotActionBridge.affineDotAction",
  "FiniteToAffineWeylDotActionBridge.finiteDotActionViaAffine",
  "rootPairingFiniteWeylAction",
  "rootPairingFiniteDotAction",
  "LieAlgebra.loopAlgebra",
  "LieAlgebra.loopAlgebraEquivLaurent",
  "LieAlgebra.LoopAlgebra.toFinsupp",
  "LieAlgebra.LoopAlgebra.residuePairing",
  "LieAlgebra.LoopAlgebra.twoCochainOfBilinear",
  "LieAlgebra.LoopAlgebra.twoCochainOfBilinear_apply_apply",
  "LieAlgebra.LoopAlgebra.twoCocycleOfBilinear",
  "LieAlgebra.Extension.ofTwoCocycle",
  "LieAlgebra.LieCharacter",
  "LieAlgebra.lieCharacter_apply_lie",
  "LieModule.weightSpace",
  "LieModule.mem_weightSpace",
  "RootPairing.weylGroup",
  "RootPairing.Equiv.reflection",
  "RootPairing.reflection_mem_weylGroup"
]

/-- Public Stage1 note text proposed for the S1-M-053 blueprint backfill. -/
def publicStage1BackfillNote : String :=
  "Repo-local Lean artifact `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_053.lean` " ++
  "compiles as a Stage1 statement-shape and anchor audit only.  It checks mathlib anchors for " ++
  "`AddMonoidAlgebra`, `HahnSeries`, and `LieAlgebra.loopAlgebra`, chooses " ++
  "`LieAlgebra.loopAlgebra R ℤ L` as the canonical " ++
  "Lean target for the untwisted affine loop-algebra core, and checks loop-algebra " ++
  "residue/cochain/cocycle APIs, Lie characters, weight spaces, finite formal " ++
  "character rings, Hahn-series formal characters, interface-level highest-weight, " ++
  "integrable, positive-level, positive-energy, dominant-integral predicates, and finite " ++
  "`RootPairing.weylGroup` action/dot-action bridge boundaries; it is not a repo-local proof " ++
  "of the Kac-Peterson character " ++
  "formula, and the public status remains open/partial until an affine Kac-Moody " ++
  "character theorem is imported or proved and locally validated."

/-- Audit decision for the formal character object in this Stage1 slot. -/
def formalCharacterSeriesObjectAudit : String :=
  "Use `AddMonoidAlgebra Coeff Weight` as the checked finite formal-character ring and " ++
  "`HahnSeries Weight Coeff` as the checked infinite formal-series substrate once an affine " ++
  "weight order is chosen.  The local `AffineFormalCharacterSeries` interface records the " ++
  "coefficient map plus support and denominator-expansion predicates, but terminal closure " ++
  "still requires proving the Kac-Peterson character and denominator series satisfy the " ++
  "selected affine support conditions."

/-- Audit decision for highest-weight and integrability predicates in this Stage1 slot. -/
def representationPredicateAudit : String :=
  "`AffineRepresentationPredicateData` records the checked predicate boundary for affine " ++
  "highest-weight representations: weight-vector membership, positive-root annihilation, " ++
  "generation by a highest-weight vector, simple-root local finiteness, integral level, " ++
  "energy degree, and simple-coroot pairings.  The derived predicates " ++
  "`IsHighestWeightModule`, `IsIntegrableRepresentation`, `IsPositiveLevelWeight`, " ++
  "`IsPositiveEnergyWeight`, and `IsDominantIntegralWeight` are statement-shape " ++
  "infrastructure only; terminal closure still requires replacing these hooks by concrete " ++
  "affine Kac-Moody module and root-operator APIs."

/-- Audit decision for finite-to-affine Weyl action and dot action in this Stage1 slot. -/
def finiteToAffineWeylDotActionAudit : String :=
  "`RootPairing.weylGroup` supplies checked finite Weyl-group generators and the local file " ++
  "records the finite dot-action shape `w • (lambda + rho) - rho`.  The new " ++
  "`FiniteToAffineWeylDotActionBridge` interface records the required map from a finite Weyl " ++
  "group into a future affine Weyl group, the compatible affine action on weights, and the " ++
  "affine dot action.  This is a bridge contract, not terminal affine Weyl closure: a concrete " ++
  "affine root datum, translation lattice, affine weight action, and compatibility proof are " ++
  "still required."

/-- Audit decision for the canonical affine Kac-Moody Lean target in this Stage1 slot. -/
def canonicalAffineKacMoodyTargetAudit : String :=
  "Use `LieAlgebra.loopAlgebra R ℤ L` as the canonical repo-local target for the " ++
  "untwisted affine Kac-Moody loop-algebra core.  Mathlib documents this as the classical " ++
  "loop algebra and provides residue/cochain/cocycle APIs.  Do not treat this as the full " ++
  "affine Kac-Moody algebra: mathlib still leaves central-extension construction, " ++
  "degree derivation, affine Weyl action, and positive-energy representation theory outside " ++
  "the closed local artifact."

/-- Audit result for the loop-algebra central-extension-adjacent APIs currently in mathlib. -/
def loopAlgebraCentralExtensionAudit : String :=
  "Mathlib.Algebra.Lie.Loop provides residuePairing, twoCochainOfBilinear, and " ++
  "twoCocycleOfBilinear for loop algebras.  These APIs construct the invariant-form " ++
  "2-cocycle with trivial coefficients; Mathlib.Algebra.Lie.Extension separately provides " ++
  "Extension.ofTwoCocycle for extensions from 2-cocycles.  The Loop module TODO still lists " ++
  "construction of central extensions from invariant forms and positive-energy representations, " ++
  "so these anchors are adjacent infrastructure rather than closure of the Kac-Peterson formula."

/-- Audit result for the available bridge from cocycles to bundled Lie-algebra extensions. -/
def loopAlgebraCocycleToExtensionBridgeAudit : String :=
  "Mathlib.Algebra.Lie.Extension exposes LieAlgebra.Extension.ofTwoCocycle, but the current " ++
  "Stage1 artifact does not instantiate a completed affine Kac-Moody central extension from " ++
  "Loop.twoCocycleOfBilinear.  The remaining bridge is to package the loop cocycle with the " ++
  "needed kernel Lie-algebra/trivial-action instances and then add the degree derivation, " ++
  "affine root datum, Weyl action, and representation/character infrastructure."

/-- Search terms used in the local mathlib tree for the Kac-Peterson anchor audit. -/
def mathlibAuditSearchTerms : List String := [
  "Kac-Peterson",
  "Kac Peterson",
  "affine Lie algebra character",
  "affine Kac-Moody character",
  "Weyl-Kac character formula",
  "loopAlgebra",
  "central extension",
  "twoCocycleOfBilinear",
  "LieCharacter",
  "weightSpace",
  "AddMonoidAlgebra",
  "HahnSeries",
  "formal character",
  "highest weight",
  "integrable highest weight",
  "positive energy",
  "level",
  "dominant integral",
  "weylGroup",
  "dot action",
  "affine Weyl action"
]

/-- C007 external Lean 4 code-search terms requested for the Kac-Peterson audit. -/
def c007ExternalLeanCodeSearchTerms : List String := [
  "Kac-Peterson",
  "Kac Peterson",
  "Weyl-Kac character",
  "Weyl Kac character",
  "affine Kac-Moody character",
  "affine Kac Moody character",
  "Kac-Peterson character formula",
  "Weyl-Kac character formula"
]

/--
C007 local pinned-source search result.

The pinned mathlib checkout at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains adjacent affine Kac-Moody infrastructure, including `LieAlgebra.loopAlgebra`
and `LoopAlgebra.twoCocycleOfBilinear`, but no terminal Lean declaration for a
Kac-Peterson or Weyl-Kac character formula.
-/
def c007PinnedMathlibSearchResult : String :=
  "pinned mathlib source checked; adjacent loop-algebra and Kac-Moody anchors found, " ++
  "but no terminal Lean 4 Kac-Peterson or Weyl-Kac character formula theorem found"

/--
C007 authenticated primary-source code-search gate.

The local GitHub CLI is not authenticated and no `GH_TOKEN`/`GITHUB_TOKEN` style
environment variable is available in this execution environment.  Therefore this
artifact records an integration blocker instead of claiming a completed authenticated
external-code audit.
-/
def c007AuthenticatedPrimarySourceCodeSearchGate : String :=
  "blocked: gh auth status reports no authenticated GitHub host, no token environment " ++
  "variable is present, and gh api /search/code cannot run without authentication"

/-- Machine proof debt classification for this Stage1 slot. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration-debt gate for this repair pass.

No complete Lean 4 Kac-Peterson character formula proof was found in the
current Lake dependency closure.  This artifact is therefore not a completed
wrapper and carries no completed state with repo-local integration debt.
-/
def repoLocalIntegrationDebtGate : String :=
  "not completed; no completed state retains repo_local_integration_debt"

/-!
## C008 public-status guard

This child task is public-document integration work.  The checked data below records the
noncompletion guard that a serial integrator can merge into public status surfaces later.
-/

/--
C008 public status guard rows.

These rows are synchronization metadata only.  They do not edit public documents and do not
close the Kac-Peterson character formula.
-/
structure PublicStatusSurfaceGuard where
  surface : String
  requiredWording : String
  currentAudit : String
  terminalTheoremRepoLocalClosed : Bool
  mayClaimCompletionBeforeTerminalClosure : Bool

/--
C008 guard for public status surfaces that must remain open or partial.

The terminal theorem is not repo-local closed: the local file checks only statement-shape
infrastructure and adjacent mathlib anchors, not a proof-bearing affine Kac-Moody character
formula theorem or pinned external dependency.
-/
def c008PublicStatusSurfaceGuards : List PublicStatusSurfaceGuard :=
  [ { surface := "Docs/Stage1_Blueprint.md",
      requiredWording := "open / partial statement-shape only",
      currentAudit := "S1-M-053 checklist row remains unchecked; this child supplies merge-ready wording only",
      terminalTheoremRepoLocalClosed := false,
      mayClaimCompletionBeforeTerminalClosure := false },
    { surface := "Docs/todos_20260430.md",
      requiredWording := "open / partial statement-shape only",
      currentAudit := "serial public-doc integration may add the status note, but not a completion claim",
      terminalTheoremRepoLocalClosed := false,
      mayClaimCompletionBeforeTerminalClosure := false },
    { surface := "README.md",
      requiredWording := "open / partial statement-shape only",
      currentAudit := "README or summary text must not call Kac-Peterson repo-local closed from this anchor audit",
      terminalTheoremRepoLocalClosed := false,
      mayClaimCompletionBeforeTerminalClosure := false } ]

/-- C008 covers the three public surfaces normally synchronized by Stage1 status backfill. -/
theorem c008PublicStatusSurfaceGuards_length :
    c008PublicStatusSurfaceGuards.length = 3 :=
  rfl

/-- C008 records that no listed public surface has terminal repo-local closure yet. -/
theorem c008PublicStatusSurfaceGuards_not_repoLocalClosed :
    c008PublicStatusSurfaceGuards.map
      PublicStatusSurfaceGuard.terminalTheoremRepoLocalClosed =
      [false, false, false] :=
  rfl

/-- C008 public surfaces must not claim completion before terminal repo-local closure. -/
theorem c008PublicStatusSurfaceGuards_no_premature_completion :
    c008PublicStatusSurfaceGuards.map
      PublicStatusSurfaceGuard.mayClaimCompletionBeforeTerminalClosure =
      [false, false, false] :=
  rfl

/-- C008 diagnosis for the child task. -/
def c008PublicStatusDiagnosis : String :=
  "public_doc_integration_guard; keep S1-M-053 open/partial until a terminal Kac-Peterson theorem is repo-local closed"

/-- C008 repo-local integration-debt gate result for the current noncompletion state. -/
def c008RepoLocalIntegrationDebtGate : String :=
  "passes_for_noncompletion_state: no completed claim and no completed-state repo_local_integration_debt"

#check LieAlgebra.loopAlgebra
#check AddMonoidAlgebra
#check HahnSeries
#check HahnSeries.coeff
#check HahnSeries.coeff_zero
#check LieAlgebra.loopAlgebraEquivLaurent
#check LieAlgebra.LoopAlgebra.toFinsupp
#check LieAlgebra.LoopAlgebra.residuePairing
#check LieAlgebra.LoopAlgebra.twoCochainOfBilinear
#check LieAlgebra.LoopAlgebra.twoCochainOfBilinear_apply_apply
#check LieAlgebra.LoopAlgebra.twoCocycleOfBilinear
#check LieAlgebra.Extension.ofTwoCocycle
#check LieAlgebra.LieCharacter
#check LieAlgebra.lieCharacter_apply_lie
#check LieModule.weightSpace
#check LieModule.mem_weightSpace
#check RootPairing.weylGroup
#check RootPairing.Equiv.reflection
#check RootPairing.reflection_mem_weylGroup
#check UntwistedLoopAlgebra
#check untwistedLoopAlgebra_eq
#check FiniteFormalCharacterRing
#check finiteFormalCharacterRing_eq
#check HahnFormalCharacterSeries
#check hahnFormalCharacterSeries_eq
#check hahnFormalCharacterSeries_coeff_zero
#check AffineFormalCharacterSeries
#check affineFormalCharacterSeries_coeff_zero
#check AffineRepresentationPredicateData
#check IsHighestWeightVector
#check IsHighestWeightModule
#check IsIntegrableRepresentation
#check HasLevel
#check IsPositiveLevelWeight
#check IsPositiveEnergyWeight
#check IsDominantIntegralWeight
#check IsIntegrablePositiveEnergyDominantHighestWeightModule
#check integrablePositiveEnergyDominantHighestWeightModule_highestWeight
#check integrablePositiveEnergyDominantHighestWeightModule_integrable
#check integrablePositiveEnergyDominantHighestWeightModule_positiveLevel
#check integrablePositiveEnergyDominantHighestWeightModule_positiveEnergy
#check integrablePositiveEnergyDominantHighestWeightModule_dominantIntegral
#check FiniteToAffineWeylDotActionBridge
#check FiniteToAffineWeylDotActionBridge.affineDotAction
#check FiniteToAffineWeylDotActionBridge.finiteDotActionViaAffine
#check FiniteToAffineWeylDotActionBridge.finiteAction_apply_eq_affineAction
#check FiniteToAffineWeylDotActionBridge.finiteDotActionViaAffine_eq_finiteAction
#check rootPairingFiniteWeylAction
#check rootPairingFiniteDotAction
#check rootPairingFiniteDotAction_ofIdx
#check KacPetersonCharacterFormulaInput
#check StatementShape
#check lieCharacter_bracket_vanishes
#check mem_weightSpace_iff
#check reflection_mem_weylGroup
#check LoopCentralExtensionCocycle
#check loop_twoCochainOfBilinear_apply_apply
#check loop_twoCocycleOfBilinear_val
#check statementShape_iff
#check publicStage1BackfillNote
#check formalCharacterSeriesObjectAudit
#check representationPredicateAudit
#check finiteToAffineWeylDotActionAudit
#check canonicalAffineKacMoodyTargetAudit
#check loopAlgebraCentralExtensionAudit
#check loopAlgebraCocycleToExtensionBridgeAudit
#check c007ExternalLeanCodeSearchTerms
#check c007PinnedMathlibSearchResult
#check c007AuthenticatedPrimarySourceCodeSearchGate
#check PublicStatusSurfaceGuard
#check c008PublicStatusSurfaceGuards
#check c008PublicStatusSurfaceGuards_length
#check c008PublicStatusSurfaceGuards_not_repoLocalClosed
#check c008PublicStatusSurfaceGuards_no_premature_completion
#check c008PublicStatusDiagnosis
#check c008RepoLocalIntegrationDebtGate

end S1_M_053
end Stage1
end AwesomeTheorems
