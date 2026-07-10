import Mathlib.Algebra.MonoidAlgebra.Basic
import Mathlib.Algebra.Ring.NegOnePow
import Mathlib.GroupTheory.Coxeter.Length
import Mathlib.LinearAlgebra.RootSystem.WeylGroup

namespace AwesomeTheorems.Stage1.S1_M_051

universe u v w

/-
Statement normalization for THM-M-0135.

The classical Macdonald identities are affine-root-system denominator
identities.  This Stage1 artifact deliberately records only the statement
boundary that can be checked repo-locally today:

* `AffineRootDatum` is the local affine-root wrapper chosen for this Stage1
  slot.  It keeps real roots, imaginary roots, and multiplicities explicit
  instead of pretending that mathlib's current finite `RootPairing` API is
  already an affine denominator-identity model.
* `AffineMacdonaldData` packages an `AffineRootDatum`-shaped payload together
  with the two sides of the identity that a future precise statement must
  specialize.
* `ExpressionRing` is currently `AddMonoidAlgebra Z Weight`.  This gives a
  concrete checked ring of finite-support weight expressions and a usable
  monomial API, but it is not yet a completed infinite product or formal
  series target.
* `StatementShape D` is only the normalized equality shape
  `D.denominatorProduct = D.alternatingSum`.  The file does not assert that
  every `AffineMacdonaldData` satisfies this equality and does not prove the
  Macdonald identity.
-/

/--
Current finite-support expression ring for normalized weight expressions.

This is intentionally conservative.  A terminal Macdonald-identity
formalization may need to replace it with `HahnSeries`, `MvPowerSeries`, or a
custom completed formal-series model carrying support and summability proofs.
-/
abbrev ExpressionRing (Weight : Type u) [AddCommGroup Weight] : Type u :=
  AddMonoidAlgebra ℤ Weight

/--
Expression-ring target selected for the current Stage1 statement shape.

The selected target is finite-support `AddMonoidAlgebra`.  This discharges only
finite-support bookkeeping for already-materialized expressions; it does not
encode the completed infinite products appearing in the full Macdonald
identities.
-/
inductive ExpressionTargetChoice where
  | addMonoidAlgebraFiniteSupport

/-- Current expression-target decision for this Stage1 artifact. -/
def selectedExpressionTarget : ExpressionTargetChoice :=
  .addMonoidAlgebraFiniteSupport

/-- The finite support of an expression in the selected `AddMonoidAlgebra` target. -/
def expressionSupport {Weight : Type u} [AddCommGroup Weight]
    (x : ExpressionRing Weight) : Finset Weight :=
  x.support

/-- Membership in the selected expression support is exactly nonzero coefficient support. -/
theorem expressionSupport_spec {Weight : Type u} [AddCommGroup Weight]
    (x : ExpressionRing Weight) (lambda : Weight) :
    lambda ∈ expressionSupport x ↔ x lambda ≠ 0 := by
  exact Finsupp.mem_support_iff

/--
Support obligations discharged by choosing `AddMonoidAlgebra`.

Every expression has a finite `Finset` support and the support is extensionally
the set of weights with nonzero coefficient.
-/
structure AddMonoidAlgebraSupportObligations {Weight : Type u} [AddCommGroup Weight]
    (x : ExpressionRing Weight) where
  support : Finset Weight
  support_spec : ∀ lambda, lambda ∈ support ↔ x lambda ≠ 0

/-- Checked support witness for any expression in the selected finite-support target. -/
def expressionSupportObligations {Weight : Type u} [AddCommGroup Weight]
    (x : ExpressionRing Weight) : AddMonoidAlgebraSupportObligations x where
  support := expressionSupport x
  support_spec := expressionSupport_spec x

/--
Finite-summation obligations for the selected `AddMonoidAlgebra` target.

This is intentionally a finite-support substitute for a true infinite
summability theorem.  A terminal Macdonald-identity formalization must replace
or extend it when the denominator product is represented as a completed formal
series.
-/
structure AddMonoidAlgebraSummabilityObligations {Weight : Type u} [AddCommGroup Weight]
    (x : ExpressionRing Weight) where
  summationSupport : Finset Weight
  coefficientOutsideSupport : ∀ lambda, lambda ∉ summationSupport -> x lambda = 0

/-- Checked finite-summation witness for any expression in the selected target. -/
def expressionSummabilityObligations {Weight : Type u} [AddCommGroup Weight]
    (x : ExpressionRing Weight) : AddMonoidAlgebraSummabilityObligations x where
  summationSupport := expressionSupport x
  coefficientOutsideSupport := by
    intro lambda hnot
    by_contra hcoeff
    exact hnot ((expressionSupport_spec x lambda).2 hcoeff)

/--
Local affine-root datum selected for the Macdonald-identity statement shape.

Mathlib's `RootPairing` API remains a useful finite-root-system anchor, but the
affine Macdonald identities need real roots, imaginary roots, and root
multiplicities as first-class fields.  This wrapper is intentionally local until
an upstream affine/Kac-Moody root datum with denominator identities is found or
implemented.
-/
structure AffineRootDatum where
  Weight : Type u
  [weightAddCommGroup : AddCommGroup Weight]
  Simple : Type v
  coxeterMatrix : CoxeterMatrix Simple
  WeylGroup : Type w
  [weylGroupInst : Group WeylGroup]
  coxeterSystem : CoxeterSystem coxeterMatrix WeylGroup
  positiveRealRoots : Set Weight
  positiveImaginaryRoots : Set Weight
  rootMultiplicity : Weight -> Nat
  rho : Weight
  weylAction : WeylGroup -> Weight ≃+ Weight

attribute [instance] AffineRootDatum.weightAddCommGroup
attribute [instance] AffineRootDatum.weylGroupInst

/--
Minimal expression data for a Macdonald-type affine-root-system identity.

This is a Stage1 statement-shape boundary, not a proof of the Macdonald
identity.  It records the pieces that a later integrator must replace by a
specific affine root datum, completed product side, and completed alternating
Weyl-sum side.
-/
structure AffineMacdonaldData where
  Weight : Type u
  [weightAddCommGroup : AddCommGroup Weight]
  Simple : Type v
  coxeterMatrix : CoxeterMatrix Simple
  WeylGroup : Type w
  [weylGroupInst : Group WeylGroup]
  coxeterSystem : CoxeterSystem coxeterMatrix WeylGroup
  positiveRealRoots : Set Weight
  positiveImaginaryRoots : Set Weight
  rootMultiplicity : Weight -> Nat
  rho : Weight
  weylAction : WeylGroup -> Weight ≃+ Weight
  denominatorProduct : ExpressionRing Weight
  alternatingSum : ExpressionRing Weight

attribute [instance] AffineMacdonaldData.weightAddCommGroup
attribute [instance] AffineMacdonaldData.weylGroupInst

/--
Projection from the statement-shape carrier to the local affine-root wrapper.

This records the child-task model decision repo-locally: use a local
`AffineRootDatum` with explicit real/imaginary root data and multiplicities,
while treating mathlib `RootPairing` as adjacent finite-root infrastructure.
-/
def AffineMacdonaldData.toAffineRootDatum (D : AffineMacdonaldData.{u, v, w}) :
    AffineRootDatum.{u, v, w} where
  Weight := D.Weight
  weightAddCommGroup := D.weightAddCommGroup
  Simple := D.Simple
  coxeterMatrix := D.coxeterMatrix
  WeylGroup := D.WeylGroup
  weylGroupInst := D.weylGroupInst
  coxeterSystem := D.coxeterSystem
  positiveRealRoots := D.positiveRealRoots
  positiveImaginaryRoots := D.positiveImaginaryRoots
  rootMultiplicity := D.rootMultiplicity
  rho := D.rho
  weylAction := D.weylAction

/-- Statement-shape candidate: the denominator product equals the alternating Weyl sum. -/
def StatementShape (D : AffineMacdonaldData.{u, v, w}) : Prop :=
  D.denominatorProduct = D.alternatingSum

/-- Universal closure of the Stage1 statement shape, kept separate from any proof claim. -/
def UniversalStatementShape : Prop :=
  ∀ D : AffineMacdonaldData.{u, v, w}, StatementShape D

/-- A checked mathlib ingredient for Weyl-sign bookkeeping via Coxeter length parity. -/
def CoxeterLengthParityAnchorStatement : Prop :=
  ∀ {B W : Type*} [Group W] {M : CoxeterMatrix B}
    (cs : CoxeterSystem M W) (w₁ w₂ : W),
      cs.length (w₁ * w₂) % 2 = (cs.length w₁ + cs.length w₂) % 2

/-- Direct wrapper around `CoxeterSystem.length_mul_mod_two`. -/
theorem coxeterLengthParityAnchor : CoxeterLengthParityAnchorStatement := by
  intro B W _ M cs w₁ w₂
  exact CoxeterSystem.length_mul_mod_two cs w₁ w₂

/--
Parity equality for natural exponents induces equality of the corresponding
integer unit signs.
-/
theorem negOnePow_natCast_eq_of_mod_two_eq {m n : Nat} (h : m % 2 = n % 2) :
    Int.negOnePow (m : Int) = Int.negOnePow (n : Int) := by
  rw [Int.negOnePow_eq_iff, Int.even_sub, Int.even_coe_nat, Int.even_coe_nat,
    Nat.even_iff, Nat.even_iff]
  constructor
  · intro hm
    rwa [← h]
  · intro hn
    rwa [h]

/--
The Coxeter length sign character `w ↦ (-1) ^ length(w)`.

The multiplicativity proof is exactly the checked parity anchor
`CoxeterSystem.length_mul_mod_two`, transported to the unit group `ℤˣ`.
-/
noncomputable def coxeterLengthSign {B : Type u} {W : Type v} [Group W]
    {M : CoxeterMatrix B} (cs : CoxeterSystem M W) : W →* ℤˣ where
  toFun w := Int.negOnePow (cs.length w : Int)
  map_one' := by
    simp [CoxeterSystem.length_one]
  map_mul' w₁ w₂ := by
    rw [← Int.negOnePow_add]
    exact negOnePow_natCast_eq_of_mod_two_eq
      (CoxeterSystem.length_mul_mod_two cs w₁ w₂)

@[simp]
theorem coxeterLengthSign_apply {B : Type u} {W : Type v} [Group W]
    {M : CoxeterMatrix B} (cs : CoxeterSystem M W) (w : W) :
    coxeterLengthSign cs w = Int.negOnePow (cs.length w : Int) := rfl

@[simp]
theorem coxeterLengthSign_coe {B : Type u} {W : Type v} [Group W]
    {M : CoxeterMatrix B} (cs : CoxeterSystem M W) (w : W) :
    ((coxeterLengthSign cs w : ℤˣ) : ℤ) = (-1 : ℤ) ^ cs.length w := by
  exact Int.coe_negOnePow_natCast (cs.length w)

theorem coxeterLengthSign_eq_one_iff {B : Type u} {W : Type v} [Group W]
    {M : CoxeterMatrix B} (cs : CoxeterSystem M W) (w : W) :
    coxeterLengthSign cs w = 1 ↔ Even (cs.length w) := by
  simp [Int.negOnePow_eq_one_iff, Int.even_coe_nat]

theorem coxeterLengthSign_eq_neg_one_iff {B : Type u} {W : Type v} [Group W]
    {M : CoxeterMatrix B} (cs : CoxeterSystem M W) (w : W) :
    coxeterLengthSign cs w = -1 ↔ Odd (cs.length w) := by
  simp [Int.negOnePow_eq_neg_one_iff, Int.odd_coe_nat]

/-- Macdonald-data-specialized Weyl sign character for the alternating Weyl sum. -/
noncomputable def AffineMacdonaldData.weylSign (D : AffineMacdonaldData.{u, v, w}) :
    D.WeylGroup →* ℤˣ :=
  coxeterLengthSign D.coxeterSystem

@[simp]
theorem AffineMacdonaldData.weylSign_apply (D : AffineMacdonaldData.{u, v, w})
    (g : D.WeylGroup) :
    D.weylSign g = Int.negOnePow (D.coxeterSystem.length g : Int) := rfl

/-- A checked mathlib ingredient locating the finite root-pairing Weyl-group API. -/
def RootPairingWeylGroupAnchorStatement : Prop :=
  ∀ {ι R M N : Type*} [CommRing R] [AddCommGroup M] [Module R M]
    [AddCommGroup N] [Module R N] (P : RootPairing ι R M N),
      P.weylGroup ≤ P.weylGroup

/-- Direct wrapper around `RootPairing.weylGroup`; this is not an affine denominator identity. -/
theorem rootPairingWeylGroupAnchor : RootPairingWeylGroupAnchorStatement := by
  intro ι R M N _ _ _ _ _ P
  exact le_rfl

/-- A checked expression-ring anchor for monomials in a weight lattice. -/
noncomputable def weightMonomial (D : AffineMacdonaldData.{u, v, w}) (lambda : D.Weight) :
    AddMonoidAlgebra ℤ D.Weight :=
  AddMonoidAlgebra.single lambda 1

end AwesomeTheorems.Stage1.S1_M_051
