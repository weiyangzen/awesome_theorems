import Mathlib.Algebra.Quaternion
import Mathlib.Algebra.QuaternionBasis
import Mathlib.AlgebraicGeometry.Cover.Open
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Noetherian
import Mathlib.AlgebraicGeometry.Sites.Etale
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.NumberTheory.RamificationInertia.Ramification
import Mathlib.RingTheory.ClassGroup
import Mathlib.RingTheory.DedekindDomain.Factorization

/-!
# S1-M-084 / THM-M-0435: Shimura curves attached to quaternion algebras

This Stage1 artifact records a Lean 4 statement-shape boundary for the claim
"modular/Shimura curves attached to quaternion algebras".

The checked local content is deliberately modest: mathlib supplies quaternion
algebras, number-field rings of integers, affine base schemes, and basic
scheme-morphism predicates.  The arithmetic moduli problem, quaternionic orders,
level structures, and representability theorem are kept as explicit parameters.
-/

noncomputable section

open AlgebraicGeometry CategoryTheory Opposite
open ValuativeRel Valued.integer
open scoped NumberField nonZeroDivisors WithZero

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_084

/--
Arithmetic input for a quaternionic Shimura-curve statement.

The field is a number field, and `a b c` are the parameters used by mathlib's
`QuaternionAlgebra F a b c`.  More refined ramification and positivity data are
not yet fixed here; they belong in the future moduli predicate.
-/
structure QuaternionicArithmeticDatum where
  F : Type u
  instField : Field F
  instNumberField : NumberField F
  a : F
  b : F
  c : F

attribute [instance] QuaternionicArithmeticDatum.instField
attribute [instance] QuaternionicArithmeticDatum.instNumberField

namespace QuaternionicArithmeticDatum

/-- The quaternion algebra over the datum's number field. -/
abbrev algebra (D : QuaternionicArithmeticDatum.{u}) : Type u :=
  QuaternionAlgebra D.F D.a D.b D.c

/-- The arithmetic base scheme `Spec (𝓞 F)` for the datum. -/
abbrev baseScheme (D : QuaternionicArithmeticDatum.{u}) : Scheme.{u} :=
  Scheme.Spec.obj (op <| CommRingCat.of (𝓞 D.F))

/-- mathlib anchor: the standard four-element basis of the quaternion algebra. -/
def quaternionBasis (D : QuaternionicArithmeticDatum.{u}) :
    Module.Basis (Fin 4) D.F D.algebra :=
  QuaternionAlgebra.basisOneIJK D.a D.b D.c

end QuaternionicArithmeticDatum

/--
Abstract order-and-level data for the quaternionic moduli problem.

This is intentionally only a typed boundary.  A full formalization must replace
it by a concrete order, Eichler/level structure, and local ramification package.
-/
structure QuaternionicLevelDatum (D : QuaternionicArithmeticDatum.{u}) where
  Order : Type u
  instRing : Ring Order
  embedsInAlgebra : Nonempty (Order →+* D.algebra)
  levelCondition : Prop

attribute [instance] QuaternionicLevelDatum.instRing

/--
Which order package the eventual moduli problem is meant to use.

The constructors are only tags.  The actual order or Eichler-order axioms stay
as explicit fields of `QuaternionicModuliTarget`, because mathlib does not yet
provide the specialized quaternionic-order API needed for this Stage1 slot.
-/
inductive QuaternionicOrderKind where
  | quaternionicOrder
  | eichlerOrder
  deriving DecidableEq, Repr

/--
Ramification and splitting hypotheses for the quaternion algebra.

This is a typed boundary for the local/global arithmetic conditions: future
work should replace the abstract place carriers and proposition fields by
mathlib local-field, ideal, discriminant, and class-group data over `𝓞 F`.
-/
structure RamificationSplittingHypotheses (D : QuaternionicArithmeticDatum.{u}) where
  RamifiedPlace : Type u
  SplitPlace : Type u
  ramificationCondition : Prop
  splittingCondition : Prop
  archimedeanCondition : Prop

/-! ## PUB-04 order, ideal, class-group, and local-field audit boundary -/

namespace QuaternionicArithmeticDatum

/-- Checked mathlib anchor: the ring of integers of the datum's number field is Dedekind. -/
theorem ringOfIntegers_isDedekind (D : QuaternionicArithmeticDatum.{u}) :
    IsDedekindDomain (𝓞 D.F) := by
  infer_instance

/-- Finite primes of `𝓞 F`, represented by mathlib's height-one spectrum. -/
abbrev finitePrime (D : QuaternionicArithmeticDatum.{u}) : Type u :=
  IsDedekindDomain.HeightOneSpectrum (𝓞 D.F)

/-- The ideal class group of the base ring of integers. -/
abbrev idealClassGroup (D : QuaternionicArithmeticDatum.{u}) : Type u :=
  ClassGroup (𝓞 D.F)

/-- Checked mathlib anchor: the ideal class group of a number field is finite. -/
@[reducible]
def idealClassGroupFintype (D : QuaternionicArithmeticDatum.{u}) :
    Fintype (D.idealClassGroup) :=
  NumberField.RingOfIntegers.instFintypeClassGroup D.F

/--
Generic order carrier available from mathlib's `Subalgebra` API.

This is deliberately not called a completed quaternionic or Eichler order API:
it only proves that a subalgebra-shaped `𝓞 F`-order carrier over the quaternion
algebra can be typed locally.
-/
abbrev quaternionicOrderCarrierCandidate (D : QuaternionicArithmeticDatum.{u}) : Type u :=
  Subalgebra (𝓞 D.F) D.algebra

/-- Ideal of `𝓞 F` corresponding to a finite prime. -/
abbrev finitePrimeIdeal (D : QuaternionicArithmeticDatum.{u}) (v : D.finitePrime) :
    Ideal (𝓞 D.F) :=
  v.asIdeal

/-- Checked fractional-ideal valuation/count anchor at a finite prime of `𝓞 F`. -/
def fractionalIdealCountAnchor (D : QuaternionicArithmeticDatum.{u}) (v : D.finitePrime)
    (I : FractionalIdeal (𝓞 D.F)⁰ D.F) : ℤ :=
  FractionalIdeal.count D.F v I

end QuaternionicArithmeticDatum

/--
Abstract local-field substrate attached to a chosen finite prime.

The type `K` is kept explicit: the current mathlib substrate gives a strong
nonarchimedean-local-field interface, but this file does not construct the
completion of `F` at `v` or connect it to quaternionic splitting.
-/
structure FinitePrimeLocalFieldSubstrate
    (D : QuaternionicArithmeticDatum.{u}) (K : Type u)
    [Field K] [ValuativeRel K] [TopologicalSpace K] [IsNonarchimedeanLocalField K] where
  finitePrime : D.finitePrime
  integerDVR : IsDiscreteValuationRing 𝒪[K]
  residueFieldFinite : Finite 𝓀[K]
  valueGroupDiscrete : Nonempty (ValueGroupWithZero K ≃*o WithZero (Multiplicative ℤ))

/-- Checked local-field anchor constructor for a chosen finite prime and local field. -/
def finitePrimeLocalFieldSubstrate
    (D : QuaternionicArithmeticDatum.{u}) (K : Type u)
    [Field K] [ValuativeRel K] [TopologicalSpace K] [IsNonarchimedeanLocalField K]
    (v : D.finitePrime) :
    FinitePrimeLocalFieldSubstrate D K :=
  {
    finitePrime := v
    integerDVR := inferInstance
    residueFieldFinite := inferInstance
    valueGroupDiscrete := ⟨IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt K⟩
  }

/--
One row in the `S1-M-084-PUB-04` audit of order/ideal/class-group/local-field
support over `𝓞 F`.
-/
structure ArithmeticSubstrateAuditRow where
  component : String
  checkedMathlibAnchors : String
  repoLocalBoundary : String
  missingShimuraCurveSpecialization : String
  deriving Repr

/--
PUB-04 verdict.

The result is intentionally partial: mathlib has the general arithmetic
substrate needed to type many carriers over `𝓞 F`, but the specialized
quaternionic/Eichler order and ramification/splitting package is still a
formalization leaf.
-/
def pub04OrderIdealClassLocalFieldVerdict : String :=
  "partial_substrate_only: mathlib supplies Dedekind-domain finite primes, ideals, \
fractional-ideal counts, class groups, finite-prime ramification-index API, and \
nonarchimedean local-field structure; it does not yet supply a specialized \
quaternionic/Eichler order package tying these APIs to QuaternionAlgebra, local \
maximal orders, discriminants, and split/ramified finite-place predicates over 𝓞 F."

/-- Integration-ready audit table for `S1-M-084-PUB-04`. -/
def pub04OrderIdealClassLocalFieldAudit : List ArithmeticSubstrateAuditRow := [
  {
    component := "base ring of integers and finite primes"
    checkedMathlibAnchors :=
      "NumberField.RingOfIntegers; IsDedekindDomain (𝓞 F); \
IsDedekindDomain.HeightOneSpectrum (𝓞 F)"
    repoLocalBoundary :=
      "QuaternionicArithmeticDatum.ringOfIntegers_isDedekind and \
QuaternionicArithmeticDatum.finitePrime type the Dedekind finite-prime base."
    missingShimuraCurveSpecialization :=
      "No completed finite-place package here chooses the quaternion algebra's \
ramified/split places or proves the needed global parity/discriminant facts."
  },
  {
    component := "ideals and fractional ideals"
    checkedMathlibAnchors :=
      "Ideal; FractionalIdeal; Ideal.finprod_heightOneSpectrum_factorization; \
FractionalIdeal.count; FractionalIdeal.finprod_heightOneSpectrum_factorization'"
    repoLocalBoundary :=
      "QuaternionicArithmeticDatum.finitePrimeIdeal and \
QuaternionicArithmeticDatum.fractionalIdealCountAnchor type finite-prime ideals \
and fractional-ideal exponents over 𝓞 F."
    missingShimuraCurveSpecialization :=
      "No checked reduced-discriminant, conductor, Eichler level, or \
quaternionic-order discriminant API is present in this Stage1 closure."
  },
  {
    component := "class group"
    checkedMathlibAnchors :=
      "ClassGroup (𝓞 F); NumberField.RingOfIntegers.instFintypeClassGroup"
    repoLocalBoundary :=
      "QuaternionicArithmeticDatum.idealClassGroup and idealClassGroupFintype \
expose the finite ideal-class-group carrier."
    missingShimuraCurveSpecialization :=
      "The class-group API is general commutative-algebra substrate; it does not \
construct the quaternionic moduli quotient or its adelic double-coset class set."
  },
  {
    component := "local fields"
    checkedMathlibAnchors :=
      "IsNonarchimedeanLocalField; 𝒪[K]; 𝓀[K]; \
IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt"
    repoLocalBoundary :=
      "FinitePrimeLocalFieldSubstrate records the DVR, finite residue field, and \
discrete value group available for an explicit local field K attached abstractly \
to a chosen finite prime."
    missingShimuraCurveSpecialization :=
      "This file does not construct F_v from v, does not identify the completed \
quaternion algebra, and does not prove split versus division at v."
  },
  {
    component := "quaternionic and Eichler orders"
    checkedMathlibAnchors :=
      "QuaternionAlgebra; generic Subalgebra (𝓞 F) D.algebra"
    repoLocalBoundary :=
      "QuaternionicArithmeticDatum.quaternionicOrderCarrierCandidate types only \
a generic subalgebra-shaped carrier."
    missingShimuraCurveSpecialization :=
      "No mathlib-local specialized QuaternionicOrder, EichlerOrder, local \
maximal order, reduced norm/order discriminant, or ramification package is \
available in this repo-local closure."
  }
]

/--
Polarization data for the abelian-variety side of the quaternionic moduli
problem.

The `RosatiCompatible` field is intentionally a predicate on the chosen
polarization objects; replacing it by genuine abelian-variety and Rosati API is
one of the remaining formalization leaves.
-/
structure QuaternionicPolarizationDatum (D : QuaternionicArithmeticDatum.{u}) where
  Polarization : Type u
  RosatiCompatible : Polarization → Prop
  polarizationCondition : Prop

/--
Arithmetic moduli target for the Shimura-curve statement.

This structure is the repo-local answer to the PUB-03 statement-shape gap: it
names the quaternionic order or Eichler order, level structure, ramification and
splitting hypotheses, polarization data, chosen topology, and the moduli functor
whose representing object is expected to be the Shimura curve.
-/
structure QuaternionicModuliTarget (D : QuaternionicArithmeticDatum.{u}) where
  orderKind : QuaternionicOrderKind
  Order : Type u
  instOrderRing : Ring Order
  embedsInAlgebra : Nonempty (Order →+* D.algebra)
  orderCondition : Prop
  eichlerCondition : Prop
  LevelStructure : Type u
  levelCondition : LevelStructure → Prop
  ramificationSplitting : RamificationSplittingHypotheses D
  polarizationData : QuaternionicPolarizationDatum D
  chosenTopology : GrothendieckTopology Scheme.{u}
  ModuliObject : (S : Scheme.{u}) → (S ⟶ D.baseScheme) → Type u
  moduliSheafCondition : Prop

attribute [instance] QuaternionicModuliTarget.instOrderRing

namespace QuaternionicModuliTarget

/-- Forget the detailed moduli target to the earlier order/level placeholder. -/
def toLevelDatum {D : QuaternionicArithmeticDatum.{u}} (T : QuaternionicModuliTarget D) :
    QuaternionicLevelDatum D :=
  {
    Order := T.Order
    instRing := T.instOrderRing
    embedsInAlgebra := T.embedsInAlgebra
    levelCondition := ∃ level : T.LevelStructure, T.levelCondition level
  }

/-- The chosen Grothendieck topology carried by the moduli target. -/
def topology {D : QuaternionicArithmeticDatum.{u}} (T : QuaternionicModuliTarget D) :
    GrothendieckTopology Scheme.{u} :=
  T.chosenTopology

end QuaternionicModuliTarget

/--
Geometric properties expected of the structural map of an integral
Shimura-curve model.

PUB-05 strengthens the package with the currently checkable scheme-geometry
surface: properness, finite type in mathlib's `LocallyOfFiniteType` form,
separatedness, smooth relative dimension one, smoothness, and local
noetherianity of the total space.  The relative-dimension field is deliberately
`SmoothOfRelativeDimension 1`; this file does not claim a general arbitrary
fiber-dimension API or a construction of the Shimura curve.
-/
def ArithmeticCurvePackage (D : QuaternionicArithmeticDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  IsProper π ∧ LocallyOfFiniteType π ∧ IsSeparated π ∧
    SmoothOfRelativeDimension 1 π ∧ Smooth π ∧ IsLocallyNoetherian X

/--
Representing object for a fully specified quaternionic moduli target.

The final field is still a proposition rather than a theorem: the current file
records the target shape and verifies that it is well typed, without claiming
the representability theorem.
-/
structure QuaternionicRepresentingObject
    (D : QuaternionicArithmeticDatum.{u}) (T : QuaternionicModuliTarget D) where
  X : Scheme.{u}
  π : X ⟶ D.baseScheme
  curvePackage : ArithmeticCurvePackage D X π
  representsModuliObject : Prop

/--
Statement-shape candidate for Shimura curves on quaternion algebras.

`RepresentsQuaternionicModuli D N X π` is the missing arithmetic geometry
payload: it should say that `X` represents the moduli problem determined by the
quaternion algebra, order, level, and ramification data.  Keeping it as a
parameter prevents the checked substrate anchors from being misread as a proof
of the terminal theorem.
-/
def StatementShape
    (RepresentsQuaternionicModuli :
      (D : QuaternionicArithmeticDatum.{u}) → QuaternionicLevelDatum D →
        (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop) :
    Prop :=
  ∀ (D : QuaternionicArithmeticDatum.{u}) (N : QuaternionicLevelDatum D),
    ∃ X : Scheme.{u}, ∃ π : X ⟶ D.baseScheme,
      ArithmeticCurvePackage D X π ∧ RepresentsQuaternionicModuli D N X π

/- The exact boundary exposed for later public backfill and integrator review. -/
theorem statementShape_unfold
    (RepresentsQuaternionicModuli :
      (D : QuaternionicArithmeticDatum.{u}) → QuaternionicLevelDatum D →
        (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop) :
    StatementShape RepresentsQuaternionicModuli ↔
      ∀ (D : QuaternionicArithmeticDatum.{u}) (N : QuaternionicLevelDatum D),
        ∃ X : Scheme.{u}, ∃ π : X ⟶ D.baseScheme,
          ArithmeticCurvePackage D X π ∧ RepresentsQuaternionicModuli D N X π :=
  Iff.rfl

/--
Statement-shape candidate after PUB-03 has fixed the arithmetic moduli target
as an explicit structure.
-/
def TargetStatementShape
    (RepresentsQuaternionicModuliTarget :
      (D : QuaternionicArithmeticDatum.{u}) → QuaternionicModuliTarget D →
        (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop) :
    Prop :=
  ∀ (D : QuaternionicArithmeticDatum.{u}) (T : QuaternionicModuliTarget D),
    ∃ R : QuaternionicRepresentingObject D T,
      RepresentsQuaternionicModuliTarget D T R.X R.π

/- The PUB-03 boundary exposed for later public backfill and integrator review. -/
theorem targetStatementShape_unfold
    (RepresentsQuaternionicModuliTarget :
      (D : QuaternionicArithmeticDatum.{u}) → QuaternionicModuliTarget D →
        (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop) :
    TargetStatementShape RepresentsQuaternionicModuliTarget ↔
      ∀ (D : QuaternionicArithmeticDatum.{u}) (T : QuaternionicModuliTarget D),
        ∃ R : QuaternionicRepresentingObject D T,
          RepresentsQuaternionicModuliTarget D T R.X R.π :=
  Iff.rfl

/-! ## Checked mathlib substrate wrappers -/

/-- Projection wrapper for the properness component of the geometric package. -/
theorem properProjectionAnchor {D : QuaternionicArithmeticDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : ArithmeticCurvePackage D X π) : IsProper π :=
  h.1

/-- Projection wrapper for the finite-type component of the geometric package. -/
theorem locallyOfFiniteTypeProjectionAnchor
    {D : QuaternionicArithmeticDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : ArithmeticCurvePackage D X π) : LocallyOfFiniteType π :=
  h.2.1

/-- Projection wrapper for the separatedness component of the geometric package. -/
theorem separatedProjectionAnchor {D : QuaternionicArithmeticDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : ArithmeticCurvePackage D X π) : IsSeparated π :=
  h.2.2.1

/-- Projection wrapper for the relative-dimension-one component of the geometric package. -/
theorem relativeDimensionOneProjectionAnchor
    {D : QuaternionicArithmeticDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : ArithmeticCurvePackage D X π) :
    SmoothOfRelativeDimension 1 π :=
  h.2.2.2.1

/-- Projection wrapper for the smoothness component of the geometric package. -/
theorem smoothProjectionAnchor {D : QuaternionicArithmeticDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : ArithmeticCurvePackage D X π) : Smooth π :=
  h.2.2.2.2.1

/-- Projection wrapper for the locally noetherian component of the geometric package. -/
theorem locallyNoetherianProjectionAnchor {D : QuaternionicArithmeticDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : ArithmeticCurvePackage D X π) : IsLocallyNoetherian X :=
  h.2.2.2.2.2

/-- mathlib anchor: affine open covers of schemes are available. -/
def affineOpenCoverAnchor (X : Scheme.{u}) : X.OpenCover :=
  X.affineCover

/-- mathlib anchor: the big etale topology on schemes is available. -/
def etaleTopologyAnchor : GrothendieckTopology Scheme.{u} :=
  Scheme.etaleTopology

/-! ## Checked arithmetic moduli-target boundary wrappers -/

/-- Projection wrapper for the order tag in the arithmetic moduli target. -/
def moduliTargetOrderKind {D : QuaternionicArithmeticDatum.{u}} (T : QuaternionicModuliTarget D) :
    QuaternionicOrderKind :=
  T.orderKind

/-- Projection wrapper for the chosen topology in the arithmetic moduli target. -/
def moduliTargetTopology {D : QuaternionicArithmeticDatum.{u}} (T : QuaternionicModuliTarget D) :
    GrothendieckTopology Scheme.{u} :=
  T.topology

/-- Projection wrapper for the ramification/splitting package. -/
def moduliTargetRamificationSplitting
    {D : QuaternionicArithmeticDatum.{u}} (T : QuaternionicModuliTarget D) :
    RamificationSplittingHypotheses D :=
  T.ramificationSplitting

/-- Projection wrapper for the polarization package. -/
def moduliTargetPolarization
    {D : QuaternionicArithmeticDatum.{u}} (T : QuaternionicModuliTarget D) :
    QuaternionicPolarizationDatum D :=
  T.polarizationData

/-- Projection wrapper for the curve package carried by a representing object. -/
theorem representingObjectCurvePackage
    {D : QuaternionicArithmeticDatum.{u}} {T : QuaternionicModuliTarget D}
    (R : QuaternionicRepresentingObject D T) : ArithmeticCurvePackage D R.X R.π :=
  R.curvePackage

/--
One row in the public mathlib anchor table for `S1-M-084-PUB-02`.

The rows are checked repo-local metadata: the declarations named here are also
exercised by the typed wrappers and `#check` probes in this file.  They are
substrate anchors only, not a construction of a Shimura curve or its moduli
interpretation.
-/
structure MathlibAnchorRow where
  requestedName : String
  importModule : String
  pinnedRevision : String
  repoLocalEvidence : String
  completionBoundary : String
  deriving Repr

/-!
## PUB-05 scheme-geometry audit boundary

The current mathlib snapshot is strong enough to make the curve package more
precise in three low-risk directions: finite type, separatedness, and smooth
relative dimension one.  It is not yet a terminal Shimura-curve theorem because
this file still lacks the arithmetic moduli construction and a proof that the
representing object satisfies these properties.
-/

/--
One row in the `S1-M-084-PUB-05` audit of scheme-geometry support for the
geometric package.
-/
structure SchemeGeometryAuditRow where
  requestedStrengthening : String
  checkedMathlibAnchors : String
  repoLocalEvidence : String
  remainingBoundary : String
  deriving Repr

/-! ## Audit constants -/

/-- The mathlib revision used for the public anchor audit in this Stage1 slot. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Public mathlib anchor table for `S1-M-084-PUB-02`. -/
def publicMathlibAnchorTable : List MathlibAnchorRow := [
  {
    requestedName := "QuaternionAlgebra",
    importModule := "Mathlib.Algebra.Quaternion",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by QuaternionicArithmeticDatum.algebra",
    completionBoundary := "quaternion-algebra type anchor only; no quaternionic order or moduli theorem"
  },
  {
    requestedName := "QuaternionAlgebra.basisOneIJK",
    importModule := "Mathlib.Algebra.QuaternionBasis",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by QuaternionicArithmeticDatum.quaternionBasis",
    completionBoundary := "basis anchor only; no Eichler-order or level-structure package"
  },
  {
    requestedName := "NumberField",
    importModule := "Mathlib.NumberTheory.NumberField.Basic",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by QuaternionicArithmeticDatum.instNumberField",
    completionBoundary := "number-field class anchor only; no arithmetic moduli construction"
  },
  {
    requestedName := "NumberField.RingOfIntegers",
    importModule := "Mathlib.NumberTheory.NumberField.Basic",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by QuaternionicArithmeticDatum.baseScheme through 𝓞 D.F",
    completionBoundary := "ring-of-integers anchor only; no order/ideal/class-group ramification package"
  },
  {
    requestedName := "Scheme.Spec",
    importModule := "Mathlib.AlgebraicGeometry.Scheme",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by QuaternionicArithmeticDatum.baseScheme",
    completionBoundary := "affine base-scheme anchor only; no representing Shimura curve"
  },
  {
    requestedName := "IsProper",
    importModule := "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ArithmeticCurvePackage and properProjectionAnchor",
    completionBoundary := "geometric predicate anchor only; no constructed proper structural map"
  },
  {
    requestedName := "Smooth",
    importModule := "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ArithmeticCurvePackage and smoothProjectionAnchor",
    completionBoundary := "geometric predicate anchor only; no constructed smooth structural map"
  },
  {
    requestedName := "IsLocallyNoetherian",
    importModule := "Mathlib.AlgebraicGeometry.Noetherian",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ArithmeticCurvePackage and locallyNoetherianProjectionAnchor",
    completionBoundary := "scheme predicate anchor only; no noetherian model proof"
  },
  {
    requestedName := "Scheme.etaleTopology",
    importModule := "Mathlib.AlgebraicGeometry.Sites.Etale",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by etaleTopologyAnchor",
    completionBoundary := "site anchor only; no etale-sheaf representability/descent theorem"
  }
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Quaternion",
  "Mathlib.Algebra.QuaternionBasis",
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Cover.Open",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Noetherian",
  "Mathlib.AlgebraicGeometry.Sites.Etale"
]

/-- Additional mathlib modules checked for the `S1-M-084-PUB-04` arithmetic-substrate audit. -/
def mathlibPub04AuditModules : List String := [
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.NumberTheory.NumberField.ClassNumber",
  "Mathlib.NumberTheory.RamificationInertia.Ramification",
  "Mathlib.RingTheory.ClassGroup",
  "Mathlib.RingTheory.DedekindDomain.Factorization"
]

/-- Additional mathlib modules checked for the `S1-M-084-PUB-05` scheme-geometry audit. -/
def mathlibPub05AuditModules : List String := [
  "Mathlib.AlgebraicGeometry.Morphisms.FiniteType",
  "Mathlib.AlgebraicGeometry.Morphisms.Separated",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Noetherian",
  "Mathlib.AlgebraicGeometry.Artinian",
  "Mathlib.RingTheory.KrullDimension.Basic",
  "Mathlib.RingTheory.RingHom.StandardSmooth"
]

/--
PUB-05 verdict.

The result is partial but usable: the Stage1 package can now require finite
type as `LocallyOfFiniteType`, separatedness as `IsSeparated`, and relative
dimension one as `SmoothOfRelativeDimension 1`.  The unavailable part is a
general scheme-morphism dimension-one/fiber-dimension theorem for arbitrary
arithmetic curves and, more importantly, a proof that a constructed
quaternionic moduli space satisfies the package.
-/
def pub05SchemeGeometryVerdict : String :=
  "strengthened_statement_shape_only: mathlib supplies LocallyOfFiniteType, \
IsSeparated, IsProper extending both, and SmoothOfRelativeDimension 1; the \
repo-local ArithmeticCurvePackage now records these fields explicitly, but no \
Shimura-curve representing object or general arbitrary-fiber dimension-one \
theory is proved here."

/-- Integration-ready audit table for `S1-M-084-PUB-05`. -/
def pub05SchemeGeometryAudit : List SchemeGeometryAuditRow := [
  {
    requestedStrengthening := "finite type over Spec(𝓞 F)"
    checkedMathlibAnchors :=
      "LocallyOfFiniteType; IsProper extends LocallyOfFiniteType"
    repoLocalEvidence :=
      "ArithmeticCurvePackage includes LocallyOfFiniteType π, and \
locallyOfFiniteTypeProjectionAnchor projects it."
    remainingBoundary :=
      "This is a predicate on a supplied structural map π; no representing \
Shimura curve has been constructed or proved finite type."
  },
  {
    requestedStrengthening := "separatedness over Spec(𝓞 F)"
    checkedMathlibAnchors :=
      "IsSeparated; IsProper extends IsSeparated; separated morphisms are \
stable under composition and base change"
    repoLocalEvidence :=
      "ArithmeticCurvePackage includes IsSeparated π, and \
separatedProjectionAnchor projects it."
    remainingBoundary :=
      "This records the separatedness requirement; it does not prove the \
diagonal of a quaternionic moduli object is a closed immersion."
  },
  {
    requestedStrengthening := "relative dimension one"
    checkedMathlibAnchors :=
      "SmoothOfRelativeDimension n; SmoothOfRelativeDimension.smooth; \
standard-smooth relative-dimension ring-hom anchors"
    repoLocalEvidence :=
      "ArithmeticCurvePackage includes SmoothOfRelativeDimension 1 π, and \
relativeDimensionOneProjectionAnchor projects it."
    remainingBoundary :=
      "The checked boundary is smooth relative dimension one.  This file does \
not provide a general non-smooth fiber-dimension-one API or prove that the \
Shimura moduli object has one-dimensional fibers."
  },
  {
    requestedStrengthening := "locally noetherian total space"
    checkedMathlibAnchors :=
      "IsLocallyNoetherian; LocallyOfFiniteType.isLocallyNoetherian for \
locally finite type morphisms over locally noetherian bases"
    repoLocalEvidence :=
      "ArithmeticCurvePackage retains IsLocallyNoetherian X, and \
locallyNoetherianProjectionAnchor projects it."
    remainingBoundary :=
      "The package records local noetherianity of X directly; it does not yet \
derive it from a constructed finite-type model over Spec(𝓞 F)."
  }
]

/-- Search terms that did not locate a terminal Shimura-curve theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "ShimuraCurve",
  "Shimura curve",
  "ModularCurve",
  "Eichler",
  "quaternionic moduli",
  "RepresentsQuaternionicModuli"
]

/-! ## PUB-06 external Lean 4 anchor audit boundary -/

/--
One row in the `S1-M-084-PUB-06` primary-source Lean 4 external search.

This is metadata only.  A row can record a useful adjacent repository or a
search blocker, but it is not proof evidence unless `proofClosureStatus` says a
specific theorem is closed and `lakeCompatibility` says the dependency is in the
repo-local Lake closure.
-/
structure ExternalLean4AuditRow where
  searchTerms : String
  repositoryUrl : String
  commit : String
  module : String
  theoremOrDeclarationNames : String
  proofClosureStatus : String
  lakeCompatibility : String
  deriving Repr

/--
PUB-06 authenticated-search gate.

The local worker had no authenticated GitHub session, and unauthenticated GitHub
REST code search was rate-limited.  Therefore this audit records direct
primary-source repository checks only; it must not be read as a globally
complete authenticated code-search absence certificate.
-/
def pub06AuthenticatedSearchGate : String :=
  "blocked_for_global_authenticated_code_search: gh auth status reports not \
logged in, and unauthenticated GitHub REST code search returned API rate-limit \
exhaustion; direct primary-source checks were still run against the local \
mathlib dependency and the ImperialCollegeLondon/FLT Lean 4 repository."

/--
PUB-06 external Lean 4 audit table.

The only source hit with substantial adjacent `QuaternionAlgebra` material was
the ImperialCollegeLondon/FLT Lean 4 project.  It contains automorphic forms on
totally definite quaternion algebras and Hecke-operator scaffolding, but no
`ShimuraCurve`, `ModularCurve`, or `Eichler` source hit in the checked clone, and
its relevant quaternion-algebra files still contain proof placeholders.  No row supplies a
terminal Shimura-curve theorem that can be pinned as completion evidence.
-/
def pub06ExternalLean4Audit : List ExternalLean4AuditRow := [
  {
    searchTerms := "ShimuraCurve; Shimura curve; Shimura; ModularCurve; Eichler"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := mathlibAnchorRevision
    module := "Mathlib/Algebra/Quaternion.lean; Mathlib/Algebra/QuaternionBasis.lean"
    theoremOrDeclarationNames :=
      "QuaternionAlgebra; QuaternionAlgebra.basisOneIJK; \
QuaternionAlgebra.coe_basisOneIJK_repr"
    proofClosureStatus :=
      "substrate_only: checked quaternion-algebra declarations; no \
ShimuraCurve, ModularCurve, Eichler, or Shimura-curve representability theorem \
found in the pinned local mathlib checkout"
    lakeCompatibility :=
      "already in repo-local Lake closure through pinned mathlib revision \
8a178386ffc0f5fef0b77738bb5449d50efeea95"
  },
  {
    searchTerms := "QuaternionAlgebra; Shimura; ModularCurve; Eichler"
    repositoryUrl := "https://github.com/ImperialCollegeLondon/FLT"
    commit := "2f4325e3b3e647225890f143d4f2dbf1315d4ebd"
    module :=
      "FLT/Mathlib/Algebra/IsQuaternionAlgebra.lean; \
FLT/QuaternionAlgebra/NumberField.lean; \
FLT/AutomorphicForm/QuaternionAlgebra/Defs.lean; \
FLT/AutomorphicForm/QuaternionAlgebra/FiniteDimensional.lean; \
FLT/AutomorphicForm/QuaternionAlgebra/HeckeOperators/Abstract.lean; \
FLT/AutomorphicForm/QuaternionAlgebra/HeckeOperators/Concrete.lean; \
FLT/AutomorphicForm/QuaternionAlgebra/HeckeOperators/Local.lean"
    theoremOrDeclarationNames :=
      "IsQuaternionAlgebra; IsQuaternionAlgebra.IsTotallyDefinite; \
IsQuaternionAlgebra.NumberField.Rigidification; \
IsQuaternionAlgebra.NumberField.IsUnramified; \
TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicForm; \
TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicForm.finiteDimensional; \
TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicForm.HeckeOperator.T; \
TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicForm.HeckeOperator.U"
    proofClosureStatus :=
      "adjacent_not_terminal: no checked ShimuraCurve, ModularCurve, Eichler, \
or Shimura-curve representability theorem found; relevant quaternion-algebra \
files include proof placeholders, so this is not a closed external proof"
    lakeCompatibility :=
      "not compatible as a completion dependency for this repo-local slot: FLT \
uses Lean v4.30.0-rc2 and mathlib 244d9a4c3071a109aa54a41242317594d3c83fb4, \
while this repository is pinned to mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; \
also no terminal theorem is present to import"
  }
]

/-! ## Stage1 audit status -/

/-- Current repo-local machine status for this Stage1 slot. -/
def machineCheckedStatus : String := "not_repo_local_closed"

/-- Current machine proof debt classification for this Stage1 slot. -/
def machineProofDebtClassification : String := "formalization_debt"

/-- Repo-local integration-debt gate for the current non-completed artifact. -/
def repoLocalIntegrationDebtGate : String :=
  "not completed; no completed state retains repo_local_integration_debt"

/--
External Lean 4 closure status from the repair audit.

No terminal theorem for Shimura curves attached to quaternion algebras is imported
or pinned in this repository.  A future exact external proof must be integrated
through Lake or recorded with a concrete integration blocker before completion.
-/
def externalLean4ClosureStatus : String :=
  "no pinned external Lean 4 terminal Shimura-curve proof in repo-local closure"

/-! ## PUB-07 pin/import/check integration gate -/

/--
Repo-local decision for `S1-M-084-PUB-07`.

This is deliberately separate from the PUB-06 search table.  PUB-06 records
which source surfaces were audited; PUB-07 records whether any found external
proof can be used as completion evidence in this repository.  The current
answer is negative: the audit found adjacent substrate only, so there is no
dependency to pin and no terminal theorem for a local wrapper.
-/
structure Pub07IntegrationDecision where
  terminalExternalProofFound : Bool
  pinnedDependencyAdded : Bool
  vendoredProofBodyAdded : Bool
  concreteBlockerForFoundProofRecorded : Bool
  anchorOnlyEvidenceAcceptedAsCompletion : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  currentMachineStatus : String
  currentDebtClassification : String
  currentAction : String
  nextAllowedOutcomes : List String
  deriving Repr

/--
Current PUB-07 decision.

No terminal external Lean 4 Shimura-curve proof was found by PUB-06, so this
worker does not add a Lake dependency or vendor a proof body.  If a later audit
does find an exact closed theorem, the allowed outcomes are a validated pin, a
validated vendored/local wrapper, or a concrete blocker while keeping the item
open.
-/
def pub07IntegrationDecision : Pub07IntegrationDecision where
  terminalExternalProofFound := false
  pinnedDependencyAdded := false
  vendoredProofBodyAdded := false
  concreteBlockerForFoundProofRecorded := false
  anchorOnlyEvidenceAcceptedAsCompletion := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  currentMachineStatus := machineCheckedStatus
  currentDebtClassification := machineProofDebtClassification
  currentAction :=
    "no pin/import/check target: PUB-06 found no terminal external Lean 4 \
Shimura-curve proof; keep S1-M-084 open as formalization_debt/not_repo_local_closed"
  nextAllowedOutcomes := [
    "external_upstream_pinned after an exact closed theorem is pinned/imported \
and validated by lake env lean in this repository",
    "local_wrapper_upstream_* after a compatible upstream theorem is imported \
and wrapped by a repo-local checked theorem",
    "integration_blocker if an exact external proof is found but toolchain, \
dependency, namespace, proof-placeholder, or license constraints block \
immediate pin/import/check"
  ]

/-- PUB-07 found no terminal external proof available for pin/import/check. -/
theorem pub07IntegrationDecision_no_terminalExternalProof :
    pub07IntegrationDecision.terminalExternalProofFound = false := by
  rfl

/-- PUB-07 does not accept anchor-only evidence as completion evidence. -/
theorem pub07IntegrationDecision_no_anchorOnlyCompletion :
    pub07IntegrationDecision.anchorOnlyEvidenceAcceptedAsCompletion = false := by
  rfl

/-- PUB-07 leaves no completed-state repo-local integration debt. -/
theorem pub07IntegrationDecision_no_completedStateRepoLocalIntegrationDebt :
    pub07IntegrationDecision.completedStateRetainsRepoLocalIntegrationDebt = false := by
  rfl

/-- PUB-07 keeps the current machine status non-completed. -/
theorem pub07IntegrationDecision_not_repoLocalClosed :
    pub07IntegrationDecision.currentMachineStatus = "not_repo_local_closed" := by
  rfl

/-! ## PUB-08 unchecked leaf-budget ledger expansion -/

/--
One independent M0387-level `<=100` step ledger for an unchecked parent leaf.

The rows below are proof-planning metadata.  They split the parent leaves
`S1-M-084-L13` through `S1-M-084-L21` into bounded local ledgers, but every row
remains unchecked formalization debt until a future worker supplies actual proof
terms, imports, or a concrete integration blocker.
-/
structure Pub08LeafBudgetLedgerRow where
  leafId : String
  parentPackage : String
  localLedgerTitle : String
  upstreamInputs : String
  downstreamOutput : String
  subledger : List String
  proposedMaxSteps : Nat
  status : String
  completionBoundary : String
  deriving Repr

namespace Pub08LeafBudgetLedgerRow

/-- Boolean budget check used by the PUB-08 metadata guard. -/
def withinM0387BudgetBool (row : Pub08LeafBudgetLedgerRow) : Bool :=
  if row.proposedMaxSteps <= 100 then true else false

/-- Boolean non-completion check used by the PUB-08 metadata guard. -/
def notCompletionEvidenceBool (row : Pub08LeafBudgetLedgerRow) : Bool :=
  row.status == "unchecked_formalization_debt"

end Pub08LeafBudgetLedgerRow

/--
Expanded independent `<=100` step ledgers for the previously unchecked leaves
`S1-M-084-L13` through `S1-M-084-L21`.
-/
def pub08UncheckedLeafBudgetLedger : List Pub08LeafBudgetLedgerRow := [
  {
    leafId := "S1-M-084-L13"
    parentPackage := "P02.quaternion_algebra_object_model"
    localLedgerTitle := "Quaternionic or Eichler order carrier"
    upstreamInputs :=
      "QuaternionicArithmeticDatum, QuaternionAlgebra, ring of integers O_F, \
generic Subalgebra carrier"
    downstreamOutput :=
      "A concrete order/Eichler-order API target replacing the generic \
QuaternionicLevelDatum.Order placeholder"
    subledger := [
      "Fix whether the first implementation target is a full quaternionic order \
or an Eichler order",
      "Choose the carrier over O_F and its embedding into D.algebra",
      "State finiteness and spanning conditions needed for an O_F-order",
      "State multiplicative closure and one-containment requirements",
      "Isolate the conductor/level field required for the Eichler case",
      "Record which facts are generic Subalgebra substrate and which are missing \
specialized order facts",
      "Expose projection wrappers for the order carrier, embedding, and level \
condition",
      "Keep the row unchecked until the specialized API is proved or imported"
    ]
    proposedMaxSteps := 80
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "No specialized QuaternionicOrder or EichlerOrder theorem is proved here."
  },
  {
    leafId := "S1-M-084-L14"
    parentPackage := "P02.quaternion_algebra_object_model"
    localLedgerTitle := "Local ramification and splitting hypotheses"
    upstreamInputs :=
      "finitePrime, finitePrimeIdeal, local-field substrate, ramification index \
anchors"
    downstreamOutput :=
      "A typed finite-place ramified/split predicate package for D.algebra"
    subledger := [
      "Choose the finite-place carrier used by the statement",
      "Separate finite ramification, finite splitting, and archimedean conditions",
      "Specify the completion or local-field parameter K for each finite place",
      "State the split matrix-algebra branch and the division-algebra branch",
      "Connect finite-prime ideals to the local condition interface",
      "Record discriminant/parity data required by the global quaternion algebra",
      "Expose a wrapper returning RamificationSplittingHypotheses D",
      "Keep the row unchecked until completion/splitting theorems are available"
    ]
    proposedMaxSteps := 90
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "No theorem identifies completed quaternion algebras as split or ramified."
  },
  {
    leafId := "S1-M-084-L15"
    parentPackage := "P03.arithmetic_base_package"
    localLedgerTitle := "Noetherian and finite-type base properties"
    upstreamInputs :=
      "NumberField.RingOfIntegers, IsDedekindDomain O_F, Scheme.Spec"
    downstreamOutput :=
      "A checked base package for Spec(O_F) supporting finite-type arithmetic \
geometry statements"
    subledger := [
      "Project the Dedekind-domain instance for O_F",
      "Identify the noetherian-ring fact needed for Spec(O_F)",
      "State the locally noetherian base-scheme target",
      "State the finite-type-over-base target for structural morphisms",
      "Separate base facts from properties of a future representing object X",
      "Add projection wrappers only after the exact mathlib names are fixed",
      "Record any missing bridge from commutative algebra to scheme geometry",
      "Keep the row unchecked until the base-scheme facts are proved locally"
    ]
    proposedMaxSteps := 75
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "The current file records substrate anchors but not a complete base package."
  },
  {
    leafId := "S1-M-084-L16"
    parentPackage := "P04.curve_geometry_package"
    localLedgerTitle := "Separated, finite-type, relative-dimension-one curve package"
    upstreamInputs :=
      "ArithmeticCurvePackage, IsProper, LocallyOfFiniteType, IsSeparated, \
SmoothOfRelativeDimension 1"
    downstreamOutput :=
      "A stronger geometric package for the structural map of the Shimura curve"
    subledger := [
      "Keep IsProper as the properness requirement",
      "Keep LocallyOfFiniteType as the finite-type proxy available in mathlib",
      "Keep IsSeparated as an explicit structural-map requirement",
      "Use SmoothOfRelativeDimension 1 for the smooth curve branch",
      "Retain Smooth and IsLocallyNoetherian projections for existing callers",
      "Record the nonsmooth/singular integral-model boundary separately",
      "Expose all projections as wrappers from ArithmeticCurvePackage",
      "Keep the row unchecked until a constructed X is proved to satisfy them"
    ]
    proposedMaxSteps := 70
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "The package is typed, but no Shimura-curve structural map is constructed."
  },
  {
    leafId := "S1-M-084-L17"
    parentPackage := "P05.moduli_problem_package"
    localLedgerTitle := "Concrete order, level, and polarization data"
    upstreamInputs :=
      "QuaternionicModuliTarget, QuaternionicOrderKind, \
QuaternionicPolarizationDatum"
    downstreamOutput :=
      "A non-placeholder moduli datum carrying order action, level structure, \
and polarization constraints"
    subledger := [
      "Select the moduli objects, such as abelian varieties or abelian surfaces",
      "Specify the order action by the chosen quaternionic or Eichler order",
      "Specify the level structure and its admissibility predicate",
      "Specify polarization objects and the Rosati-compatibility condition",
      "Specify the base morphism S -> Spec(O_F) for families",
      "Separate coarse moduli, fine moduli, and stack-level variants",
      "Expose a conversion to the older QuaternionicLevelDatum interface",
      "Keep the row unchecked until the placeholder Type/Prop fields are removed"
    ]
    proposedMaxSteps := 95
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "QuaternionicModuliTarget is a typed boundary, not a concrete moduli theory."
  },
  {
    leafId := "S1-M-084-L18"
    parentPackage := "P05.moduli_problem_package"
    localLedgerTitle := "Representability predicate without placeholders"
    upstreamInputs :=
      "QuaternionicModuliTarget, chosen topology, ModuliObject functor"
    downstreamOutput :=
      "A precise RepresentsQuaternionicModuliTarget predicate over schemes"
    subledger := [
      "Fix whether representability is fine, coarse, stacky, or a rigidified \
fine moduli statement",
      "Define the functor on test schemes over D.baseScheme",
      "Define morphisms of moduli objects and isomorphism classes if needed",
      "State naturality of pullback along test-scheme morphisms",
      "State the universal object or universal property expected of X",
      "Tie the chosen topology to sheafification or descent requirements",
      "Replace representsModuliObject : Prop by an explicit universal property",
      "Keep the row unchecked until no placeholder predicate remains"
    ]
    proposedMaxSteps := 95
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "The current representing-object field is still an abstract proposition."
  },
  {
    leafId := "S1-M-084-L19"
    parentPackage := "P06.representability_package"
    localLedgerTitle := "Sheaf and descent package for the moduli functor"
    upstreamInputs :=
      "chosen Grothendieck topology, ModuliObject, pullback/naturality data"
    downstreamOutput :=
      "A sheaf/descent theorem usable by the representability proof"
    subledger := [
      "Choose the topology used for descent, initially the etale topology",
      "State the presheaf or fibered-category object to be sheafified",
      "Prove or import compatibility of moduli objects with base change",
      "Prove local gluing of objects under covering families",
      "Prove uniqueness/effectivity of descent data",
      "Separate automorphism issues from fine representability",
      "Expose the descent result as an input to the representability package",
      "Keep the row unchecked until a checked sheaf/descent theorem exists"
    ]
    proposedMaxSteps := 100
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "No sheaf/descent theorem for quaternionic moduli objects is proved here."
  },
  {
    leafId := "S1-M-084-L20"
    parentPackage := "P06.representability_package"
    localLedgerTitle := "Representability by a scheme and curve identification"
    upstreamInputs :=
      "concrete moduli predicate, sheaf/descent package, curve geometry package"
    downstreamOutput :=
      "A representing scheme X with ArithmeticCurvePackage and Shimura-curve \
identification"
    subledger := [
      "Choose the representability theorem source: local proof, mathlib wrapper, \
or pinned external proof",
      "Construct or import the candidate scheme X",
      "Construct the structural map X -> D.baseScheme",
      "Prove the universal property for the moduli target",
      "Prove properness, finite type, separatedness, and local noetherianity",
      "Prove the relative-dimension-one or curve property",
      "Identify the result as the required Shimura curve statement",
      "Keep the row unchecked until the theorem is kernel-checked in this repo"
    ]
    proposedMaxSteps := 100
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "No representing scheme or terminal Shimura-curve theorem is present."
  },
  {
    leafId := "S1-M-084-L21"
    parentPackage := "P07.repo_local_closure_gate"
    localLedgerTitle := "External proof pin/import/check or concrete blocker"
    upstreamInputs :=
      "PUB-06 external audit, PUB-07 integration decision, Lake dependency \
closure"
    downstreamOutput :=
      "A validated dependency/wrapper outcome or a precise non-completion blocker"
    subledger := [
      "Rerun authenticated primary-source search if no exact theorem is known",
      "For a candidate proof, record repository URL, commit, module, and theorem \
names",
      "Audit the candidate for proof placeholders and license constraints",
      "Compare Lean toolchain and mathlib revisions with this repository",
      "Either pin/import/check the dependency or vendor a compatible proof body",
      "Add a repo-local wrapper theorem only after the imported theorem validates",
      "If integration fails, record the concrete toolchain/dependency/blocker",
      "Keep the parent open unless local validation of the terminal theorem passes"
    ]
    proposedMaxSteps := 85
    status := "unchecked_formalization_debt"
    completionBoundary :=
      "PUB-07 found no terminal external proof, so there is no current pin target."
  }
]

/-- PUB-08 expands exactly the nine parent leaves L13 through L21. -/
theorem pub08UncheckedLeafBudgetLedger_length :
    pub08UncheckedLeafBudgetLedger.length = 9 := by
  rfl

/-- Every PUB-08 row proposes a local budget of at most 100 steps. -/
theorem pub08UncheckedLeafBudgetLedger_withinM0387Budget :
    pub08UncheckedLeafBudgetLedger.all Pub08LeafBudgetLedgerRow.withinM0387BudgetBool = true := by
  native_decide

/-- PUB-08 rows are all explicitly non-completion evidence. -/
theorem pub08UncheckedLeafBudgetLedger_notCompletionEvidence :
    pub08UncheckedLeafBudgetLedger.all Pub08LeafBudgetLedgerRow.notCompletionEvidenceBool = true := by
  native_decide

/- PUB-08 keeps the parent open; it is a ledger expansion, not theorem closure. -/
def pub08CompletionClaimAllowed : Bool := false

/-- PUB-08 does not authorize a theorem-completion claim. -/
theorem pub08CompletionClaimAllowed_eq_false :
    pub08CompletionClaimAllowed = false := by
  rfl

/-! ## Audit probes -/

#check QuaternionAlgebra
#check QuaternionAlgebra.basisOneIJK
#check NumberField
#check NumberField.RingOfIntegers
#check Scheme.Spec
#check IsProper
#check LocallyOfFiniteType
#check IsSeparated
#check SmoothOfRelativeDimension
#check Smooth
#check IsLocallyNoetherian
#check Scheme.etaleTopology
#check mathlibAnchorRevision
#check publicMathlibAnchorTable
#check StatementShape
#check QuaternionicModuliTarget
#check QuaternionicRepresentingObject
#check TargetStatementShape
#check QuaternionicArithmeticDatum.ringOfIntegers_isDedekind
#check QuaternionicArithmeticDatum.finitePrime
#check QuaternionicArithmeticDatum.idealClassGroup
#check QuaternionicArithmeticDatum.idealClassGroupFintype
#check QuaternionicArithmeticDatum.quaternionicOrderCarrierCandidate
#check QuaternionicArithmeticDatum.finitePrimeIdeal
#check QuaternionicArithmeticDatum.fractionalIdealCountAnchor
#check FinitePrimeLocalFieldSubstrate
#check finitePrimeLocalFieldSubstrate
#check IsDedekindDomain.HeightOneSpectrum
#check FractionalIdeal.count
#check ClassGroup
#check Ideal.ramificationIdx
#check IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt
#check pub04OrderIdealClassLocalFieldVerdict
#check pub04OrderIdealClassLocalFieldAudit
#check mathlibPub04AuditModules
#check locallyOfFiniteTypeProjectionAnchor
#check separatedProjectionAnchor
#check relativeDimensionOneProjectionAnchor
#check pub05SchemeGeometryVerdict
#check pub05SchemeGeometryAudit
#check mathlibPub05AuditModules
#check ExternalLean4AuditRow
#check pub06AuthenticatedSearchGate
#check pub06ExternalLean4Audit
#check Pub07IntegrationDecision
#check pub07IntegrationDecision
#check pub07IntegrationDecision_no_terminalExternalProof
#check pub07IntegrationDecision_no_anchorOnlyCompletion
#check pub07IntegrationDecision_no_completedStateRepoLocalIntegrationDebt
#check pub07IntegrationDecision_not_repoLocalClosed
#check Pub08LeafBudgetLedgerRow
#check pub08UncheckedLeafBudgetLedger
#check pub08UncheckedLeafBudgetLedger_length
#check pub08UncheckedLeafBudgetLedger_withinM0387Budget
#check pub08UncheckedLeafBudgetLedger_notCompletionEvidence
#check pub08CompletionClaimAllowed
#check pub08CompletionClaimAllowed_eq_false
#check machineCheckedStatus
#check machineProofDebtClassification

end S1_M_084
end Stage1
end AwesomeTheorems
