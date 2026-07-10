import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic
import Mathlib.NumberTheory.FunctionField
import Mathlib.NumberTheory.ClassNumber.FunctionField
import Mathlib.RepresentationTheory.Basic
import Mathlib.RingTheory.DedekindDomain.FiniteAdeleRing
import Mathlib.RingTheory.Frobenius

/-!
# S1-M-061 / THM-M-0433: Laurent Lafforgue theorem

Stage1 statement-shape artifact for Laurent Lafforgue's global Langlands
correspondence for `GL n` over function fields.

The local mathlib checkout has useful adjacent APIs for function fields, class
groups, absolute Galois groups, ordinary representations, and arithmetic
Frobenius elements.  It does not contain the automorphic representation, adelic
`GL n`, compatible system, Satake parameter, or L-function object model needed
for a terminal theorem.  The declarations below therefore keep the formal
boundary explicit and compile without proof placeholders.
-/

noncomputable section

open scoped Polynomial

namespace AwesomeTheorems.Stage1.S1_M_061

universe uFq uF uE uV uPlace uAuto uRank uSatake uCentral uWeil

/-- A plain representation of the absolute Galois group, using currently available mathlib APIs. -/
abbrev AbsoluteGaloisRepresentation
    (F : Type uF) (E : Type uE) (V : Type uV)
    [Field F] [Semiring E] [AddCommMonoid V] [Module E V] :
    Type (max uF uV) :=
  Representation E (Field.absoluteGaloisGroup F) V

/--
Abstract local-place data for a one-variable global function field.

This is intentionally not identified with a final curve/place API: the audited
mathlib snapshot exposes function fields and arithmetic Frobenius elements, but
not the full place-indexed local Langlands/Satake interface required by
Lafforgue's theorem.
-/
structure FunctionFieldPlaceData (F : Type uF) : Type (max uF (uPlace + 1)) where
  Place : Type uPlace
  isUnramified : Place -> Prop
  residueCardinality : Place -> Nat

/--
Concrete finite-place type currently available for a separable global function
field: height-one primes of the function-field ring of integers.

This captures the finite places coming from the affine model
`FunctionField.ringOfIntegers Fq F`; the place at infinity and a theorem-level
ramification/Frobenius API still have to be integrated separately.
-/
abbrev FunctionFieldFinitePlace
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F] :
    Type uF :=
  IsDedekindDomain.HeightOneSpectrum (FunctionField.ringOfIntegers Fq F)

/-- Residue field at a finite function-field place. -/
abbrev FunctionFieldResidueField
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (v : FunctionFieldFinitePlace Fq F) : Type uF :=
  FunctionField.ringOfIntegers Fq F ⧸ v.asIdeal

/--
Finite adeles of the affine function-field model, specialized from mathlib's
Dedekind-domain restricted product.

This is a concrete checked anchor for the finite-adelic substrate only.  It is
not yet the full function-field adele ring needed by Laurent Lafforgue, because
the final API must also account for the places above infinity and the automorphic
quotient.
-/
abbrev FunctionFieldFiniteAdeleRing
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F] : Type uF :=
  IsDedekindDomain.FiniteAdeleRing (FunctionField.ringOfIntegers Fq F) F

/-- The `GL_n(R)` substrate currently available from mathlib. -/
abbrev GLn (ι : Type uRank) (R : Type uF)
    [Fintype ι] [DecidableEq ι] [Semiring R] : Type (max uRank uF) :=
  Matrix.GeneralLinearGroup ι R

/--
The checked finite-adelic `GL_n` anchor for a function field.

This is still weaker than the terminal automorphic object model: it gives
`GL_n` over the finite restricted product, but not the full adelic quotient,
smoothness, admissibility, cuspidality, central characters, or Satake
parameters.
-/
abbrev FunctionFieldFiniteAdeleGLn
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (ι : Type uRank) [Fintype ι] [DecidableEq ι] :
    Type (max uRank uF) :=
  GLn ι (FunctionFieldFiniteAdeleRing Fq F)

/--
Instantiate the abstract Stage1 place data with mathlib's concrete
height-one-spectrum API for finite places of `FunctionField.ringOfIntegers`.

The unramified predicate is still an explicit input because this mathlib slice
does not yet provide the Lafforgue-level ramification and Frobenius interface.
-/
noncomputable def functionFieldPlaceDataOfHeightOneSpectrum
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (isUnramified : FunctionFieldFinitePlace Fq F -> Prop) :
    FunctionFieldPlaceData F where
  Place := FunctionFieldFinitePlace Fq F
  isUnramified := isUnramified
  residueCardinality := fun v => Nat.card (FunctionFieldResidueField Fq F v)

@[simp]
theorem functionFieldPlaceDataOfHeightOneSpectrum_isUnramified
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (isUnramified : FunctionFieldFinitePlace Fq F -> Prop)
    (v : FunctionFieldFinitePlace Fq F) :
    (functionFieldPlaceDataOfHeightOneSpectrum Fq F isUnramified).isUnramified v =
      isUnramified v :=
  rfl

/-- Residue-cardinality theorem for the concrete height-one-spectrum instantiation. -/
@[simp]
theorem functionFieldPlaceDataOfHeightOneSpectrum_residueCardinality
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (isUnramified : FunctionFieldFinitePlace Fq F -> Prop)
    (v : FunctionFieldFinitePlace Fq F) :
    (functionFieldPlaceDataOfHeightOneSpectrum Fq F isUnramified).residueCardinality v =
      Nat.card (FunctionFieldResidueField Fq F v) :=
  rfl

/--
When the residue field has a `Fintype` instance, the Stage1 cardinality field is
the usual finite-cardinality expression.
-/
theorem functionFieldPlaceDataOfHeightOneSpectrum_residueCardinality_eq_fintype_card
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (isUnramified : FunctionFieldFinitePlace Fq F -> Prop)
    (v : FunctionFieldFinitePlace Fq F) [Fintype (FunctionFieldResidueField Fq F v)] :
    (functionFieldPlaceDataOfHeightOneSpectrum Fq F isUnramified).residueCardinality v =
      Fintype.card (FunctionFieldResidueField Fq F v) := by
  rw [functionFieldPlaceDataOfHeightOneSpectrum_residueCardinality,
    Nat.card_eq_fintype_card]

/--
Galois-side statement data for a future formal Laurent Lafforgue theorem.

The theorem should eventually replace these predicates by concrete `l`-adic
representation, ramification, purity, and determinant conditions.
-/
structure LafforgueGaloisParameter
    (F : Type uF) (E : Type uE) (V : Type uV)
    [Field F] [Semiring E] [AddCommMonoid V] [Module E V] :
    Type (max uF uE uV) where
  representation : AbsoluteGaloisRepresentation F E V
  rank : Nat
  continuous : Prop
  irreducible : Prop
  unramifiedOutsideFiniteSet : Prop
  determinantFiniteOrderAfterTwist : Prop

/--
Abstract Weil-group and Frobenius-polynomial data for the Galois side.

The final Laurent Lafforgue formalization should replace this by a concrete
global-function-field Weil group, inertia/decomposition groups, and a checked
characteristic-polynomial construction for unramified Frobenius elements.
-/
structure GaloisWeilFrobeniusData
    (F : Type uF) (E : Type uE) [Field F] [Semiring E]
    (places : FunctionFieldPlaceData.{uF, uPlace} F) :
    Type (max uF uE uPlace (uWeil + 1)) where
  WeilGroup : Type uWeil
  toAbsoluteGalois : WeilGroup -> Field.absoluteGaloisGroup F
  arithmeticFrobeniusAt : (v : places.Place) -> places.isUnramified v -> WeilGroup
  frobeniusCharacteristicPolynomial :
    (v : places.Place) -> places.isUnramified v -> Polynomial E

/--
Galois/Weil-side design package for the Laurent Lafforgue statement.

This child isolates the source-side hypotheses requested by the public task:
continuous `l`-adic parameters, finite ramification, irreducibility,
determinant/twist hypotheses, and Frobenius characteristic polynomials.  The
fields remain abstract because the audited local mathlib API does not yet
provide the terminal function-field Weil-group and ramification interface.
-/
structure LafforgueGaloisWeilSide
    (F : Type uF) (E : Type uE) (V : Type uV)
    [Field F] [Field E] [AddCommGroup V] [Module E V]
    (places : FunctionFieldPlaceData.{uF, uPlace} F) :
    Type (max uF uE uV uPlace (uWeil + 1)) where
  coefficientPrime : Nat
  coefficientPrimeDifferentFromCharacteristic : Prop
  lAdicContinuous : LafforgueGaloisParameter F E V -> Prop
  finitelyRamified : LafforgueGaloisParameter F E V -> Prop
  irreducibleParameter : LafforgueGaloisParameter F E V -> Prop
  determinantTwistHypothesis : LafforgueGaloisParameter F E V -> Prop
  predicateMatchesStatementShape :
    ∀ rho : LafforgueGaloisParameter F E V,
      (lAdicContinuous rho ↔ rho.continuous) ∧
        (finitelyRamified rho ↔ rho.unramifiedOutsideFiniteSet) ∧
        (irreducibleParameter rho ↔ rho.irreducible) ∧
        (determinantTwistHypothesis rho ↔ rho.determinantFiniteOrderAfterTwist)
  frobeniusData :
    GaloisWeilFrobeniusData.{uF, uE, uPlace, uWeil} F E places

namespace LafforgueGaloisWeilSide

theorem lAdicContinuous_iff_continuous
    {F : Type uF} {E : Type uE} {V : Type uV}
    [Field F] [Field E] [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueGaloisWeilSide F E V places)
    (rho : LafforgueGaloisParameter F E V) :
    side.lAdicContinuous rho ↔ rho.continuous :=
  (side.predicateMatchesStatementShape rho).1

theorem finitelyRamified_iff_unramifiedOutsideFiniteSet
    {F : Type uF} {E : Type uE} {V : Type uV}
    [Field F] [Field E] [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueGaloisWeilSide F E V places)
    (rho : LafforgueGaloisParameter F E V) :
    side.finitelyRamified rho ↔ rho.unramifiedOutsideFiniteSet :=
  (side.predicateMatchesStatementShape rho).2.1

theorem irreducibleParameter_iff_irreducible
    {F : Type uF} {E : Type uE} {V : Type uV}
    [Field F] [Field E] [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueGaloisWeilSide F E V places)
    (rho : LafforgueGaloisParameter F E V) :
    side.irreducibleParameter rho ↔ rho.irreducible :=
  (side.predicateMatchesStatementShape rho).2.2.1

theorem determinantTwistHypothesis_iff_statementShape
    {F : Type uF} {E : Type uE} {V : Type uV}
    [Field F] [Field E] [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueGaloisWeilSide F E V places)
    (rho : LafforgueGaloisParameter F E V) :
    side.determinantTwistHypothesis rho ↔ rho.determinantFiniteOrderAfterTwist :=
  (side.predicateMatchesStatementShape rho).2.2.2

/-- Frobenius characteristic polynomial supplied by the abstract Galois/Weil side. -/
def frobeniusCharacteristicPolynomial
    {F : Type uF} {E : Type uE} {V : Type uV}
    [Field F] [Field E] [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueGaloisWeilSide F E V places)
    (v : places.Place) (hv : places.isUnramified v) : Polynomial E :=
  side.frobeniusData.frobeniusCharacteristicPolynomial v hv

/-- Arithmetic Frobenius element supplied by the abstract Galois/Weil side. -/
def arithmeticFrobeniusAt
    {F : Type uF} {E : Type uE} {V : Type uV}
    [Field F] [Field E] [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueGaloisWeilSide F E V places)
    (v : places.Place) (hv : places.isUnramified v) : side.frobeniusData.WeilGroup :=
  side.frobeniusData.arithmeticFrobeniusAt v hv

end LafforgueGaloisWeilSide

/--
Abstract central-character data for the automorphic side.

The terminal object should replace `Source` by the idele class group or the
center of `GL_n` over the function-field adeles, and `character` by the checked
character API used by the automorphic representation library.
-/
structure AutomorphicCentralCharacter
    (Fq : Type uFq) (F : Type uF) (E : Type uE) [Semiring E] :
    Type (max uFq uF uE (uCentral + 1)) where
  Source : Type uCentral
  character : Source -> E
  finiteOrder : Prop

/--
Abstract Satake-parameter package indexed by the Stage1 place data.

The terminal theorem should replace `Parameter` by semisimple conjugacy classes
or the chosen local dual-group object, and `heckePolynomial` by the checked
Hecke/Satake polynomial attached to the automorphic representation at an
unramified place.
-/
structure AutomorphicSatakeParameters
    (F : Type uF) (E : Type uE) [Semiring E]
    (places : FunctionFieldPlaceData.{uF, uPlace} F) :
    Type (max uF uE uPlace (uSatake + 1)) where
  Parameter : Type uSatake
  parameterAt : places.Place -> Parameter
  heckePolynomial : places.Place -> Polynomial E
  definedAtUnramified : ∀ v : places.Place, places.isUnramified v -> Nonempty Parameter

/--
Automorphic-side design package for the Laurent Lafforgue statement.

It separates the concrete finite-adelic `GL_n` anchor from the abstract
automorphic representation API still missing from mathlib: full function-field
adeles, quotient by `GL_n(F)`, cuspidality, central characters, and Satake data.
-/
structure LafforgueAutomorphicSide
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (E : Type uE) [Field E]
    (places : FunctionFieldPlaceData.{uF, uPlace} F) :
    Type (max uFq uF uE uPlace (uRank + 1) (uAuto + 1) (uCentral + 1) (uSatake + 1)) where
  RankIndex : Type uRank
  rankIndexFintype : Fintype RankIndex
  rankIndexDecidableEq : DecidableEq RankIndex
  AutomorphicRepresentation : Type uAuto
  finiteAdeleGLnAnchor :
    Nonempty (FunctionFieldFiniteAdeleGLn Fq F RankIndex)
  isFullFunctionFieldAdeleGLn : AutomorphicRepresentation -> Prop
  cuspidal : AutomorphicRepresentation -> Prop
  centralCharacter :
    AutomorphicRepresentation -> AutomorphicCentralCharacter.{uFq, uF, uE, uCentral} Fq F E
  satakeParameters :
    AutomorphicRepresentation -> AutomorphicSatakeParameters.{uF, uE, uPlace, uSatake} F E places

attribute [instance] LafforgueAutomorphicSide.rankIndexFintype
attribute [instance] LafforgueAutomorphicSide.rankIndexDecidableEq

namespace LafforgueAutomorphicSide

/-- Rank of an automorphic-side package as the cardinality of its `GL_n` index type. -/
def rank
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueAutomorphicSide Fq F E places) : Nat :=
  Fintype.card side.RankIndex

/-- The finite-adelic `GL_n` anchor carried by an automorphic-side package. -/
abbrev finiteAdeleGLn
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueAutomorphicSide Fq F E places) : Type (max uRank uF) :=
  FunctionFieldFiniteAdeleGLn Fq F side.RankIndex

theorem centralCharacter_finiteOrder
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueAutomorphicSide Fq F E places)
    (π : side.AutomorphicRepresentation) :
    (side.centralCharacter π).finiteOrder = (side.centralCharacter π).finiteOrder :=
  rfl

theorem satake_definedAtUnramified
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (side : LafforgueAutomorphicSide Fq F E places)
    (π : side.AutomorphicRepresentation) (v : places.Place)
    (hv : places.isUnramified v) :
    Nonempty (side.satakeParameters π).Parameter :=
  (side.satakeParameters π).definedAtUnramified v hv

end LafforgueAutomorphicSide

/--
Pointwise unramified Frobenius/Hecke polynomial matching for the checked C005
and C006 statement-boundary packages.

The terminal theorem should replace this equality field by a theorem derived
from a concrete unramified local Langlands/Satake construction.  At Stage1 it is
the precise repo-local interface where the Galois-side Frobenius characteristic
polynomial must meet the automorphic-side Hecke/Satake polynomial.
-/
def FrobeniusHeckePolynomialMatches
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {V : Type uV} [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    (galoisSide : LafforgueGaloisWeilSide.{uF, uE, uV, uPlace, uWeil} F E V places)
    (automorphicSide :
      LafforgueAutomorphicSide.{uFq, uF, uE, uPlace, uAuto, uRank, uSatake, uCentral}
        Fq F E places)
    (pi : automorphicSide.AutomorphicRepresentation)
    (v : places.Place) (hv : places.isUnramified v) : Prop :=
  LafforgueGaloisWeilSide.frobeniusCharacteristicPolynomial galoisSide v hv =
    (automorphicSide.satakeParameters pi).heckePolynomial v

/--
Abstract local-compatibility package for unramified places.

This is the strongest safe repo-local C007 artifact: it compiles the exact
polynomial-equality boundary requested by the child task, but it does not prove
Laurent Lafforgue's compatibility theorem because the concrete Hecke algebra,
Satake transform, local parameter, and Frobenius characteristic-polynomial
construction are still absent.
-/
structure UnramifiedLocalCompatibility
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (E : Type uE) [Field E] (V : Type uV) [AddCommGroup V] [Module E V]
    (places : FunctionFieldPlaceData.{uF, uPlace} F)
    (galoisSide : LafforgueGaloisWeilSide.{uF, uE, uV, uPlace, uWeil} F E V places)
    (automorphicSide :
      LafforgueAutomorphicSide.{uFq, uF, uE, uPlace, uAuto, uRank, uSatake, uCentral}
        Fq F E places)
    (rho : LafforgueGaloisParameter F E V)
    (pi : automorphicSide.AutomorphicRepresentation) :
    Type (max uFq uF uE uV uPlace uAuto uRank uSatake uCentral uWeil) where
  rankCompatible :
    LafforgueAutomorphicSide.rank automorphicSide = rho.rank
  satakeDefinedAtUnramified :
    ∀ v : places.Place, places.isUnramified v ->
      Nonempty (automorphicSide.satakeParameters pi).Parameter
  polynomialCompatibility :
    ∀ v : places.Place, (hv : places.isUnramified v) ->
      FrobeniusHeckePolynomialMatches galoisSide automorphicSide pi v hv

namespace UnramifiedLocalCompatibility

/-- Projection of the rank equality required by unramified local compatibility. -/
theorem rank_eq
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {V : Type uV} [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    {galoisSide : LafforgueGaloisWeilSide.{uF, uE, uV, uPlace, uWeil} F E V places}
    {automorphicSide :
      LafforgueAutomorphicSide.{uFq, uF, uE, uPlace, uAuto, uRank, uSatake, uCentral}
        Fq F E places}
    {rho : LafforgueGaloisParameter F E V}
    {pi : automorphicSide.AutomorphicRepresentation}
    (compat :
      UnramifiedLocalCompatibility Fq F E V places galoisSide automorphicSide rho pi) :
    LafforgueAutomorphicSide.rank automorphicSide = rho.rank :=
  compat.rankCompatible

/-- Projection of Satake definedness at every unramified place. -/
theorem satake_definedAtUnramified
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {V : Type uV} [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    {galoisSide : LafforgueGaloisWeilSide.{uF, uE, uV, uPlace, uWeil} F E V places}
    {automorphicSide :
      LafforgueAutomorphicSide.{uFq, uF, uE, uPlace, uAuto, uRank, uSatake, uCentral}
        Fq F E places}
    {rho : LafforgueGaloisParameter F E V}
    {pi : automorphicSide.AutomorphicRepresentation}
    (compat :
      UnramifiedLocalCompatibility Fq F E V places galoisSide automorphicSide rho pi)
    (v : places.Place) (hv : places.isUnramified v) :
    Nonempty (automorphicSide.satakeParameters pi).Parameter :=
  compat.satakeDefinedAtUnramified v hv

/-- Projection of the Frobenius characteristic polynomial / Hecke polynomial equality. -/
theorem frobeniusCharacteristicPolynomial_eq_heckePolynomial
    {Fq : Type uFq} {F : Type uF} [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    {E : Type uE} [Field E] {V : Type uV} [AddCommGroup V] [Module E V]
    {places : FunctionFieldPlaceData.{uF, uPlace} F}
    {galoisSide : LafforgueGaloisWeilSide.{uF, uE, uV, uPlace, uWeil} F E V places}
    {automorphicSide :
      LafforgueAutomorphicSide.{uFq, uF, uE, uPlace, uAuto, uRank, uSatake, uCentral}
        Fq F E places}
    {rho : LafforgueGaloisParameter F E V}
    {pi : automorphicSide.AutomorphicRepresentation}
    (compat :
      UnramifiedLocalCompatibility Fq F E V places galoisSide automorphicSide rho pi)
    (v : places.Place) (hv : places.isUnramified v) :
    LafforgueGaloisWeilSide.frobeniusCharacteristicPolynomial galoisSide v hv =
      (automorphicSide.satakeParameters pi).heckePolynomial v :=
  compat.polynomialCompatibility v hv

end UnramifiedLocalCompatibility

/--
Automorphic-side statement data for a future formal Laurent Lafforgue theorem.

The theorem should eventually replace this with cuspidal automorphic
representations of `GL n` over the adele ring of a global function field.
-/
structure LafforgueAutomorphicRepresentation
    (Fq : Type uFq) (F : Type uF) (E : Type uE) :
    Type (max uFq uF uE (uAuto + 1)) where
  Carrier : Type uAuto
  rank : Nat
  cuspidal : Prop
  centralCharacterFiniteOrder : Prop
  coefficientFieldMarker : Nonempty E

/--
Abstract local compatibility at unramified places.

This records the formalization boundary where Frobenius characteristic
polynomials, Satake parameters, and local `L`-factors must later be supplied.
-/
def HeckeFrobeniusCompatibility
    {Fq : Type uFq} {F : Type uF} {E : Type uE} {V : Type uV}
    [Field F] [Semiring E] [AddCommMonoid V] [Module E V]
    (places : FunctionFieldPlaceData F)
    (rho : LafforgueGaloisParameter F E V)
    (pi : LafforgueAutomorphicRepresentation Fq F E)
    (localFactorMatches : places.Place -> Prop) : Prop :=
  pi.rank = rho.rank ∧
    ∀ v : places.Place, places.isUnramified v -> localFactorMatches v

/--
Normalized Stage1 statement-shape candidate for Laurent Lafforgue's theorem.

For a finite constant field `Fq`, a separable one-variable function field `F`,
coefficient field `E`, representation space `V`, rank `n`, and local-place data,
every Galois parameter satisfying the expected source-side hypotheses has a
cuspidal automorphic counterpart with matching unramified local factors.

This is a statement boundary only, not a proof of the theorem.
-/
def StatementShape
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (E : Type uE) [Field E]
    (V : Type uV) [AddCommGroup V] [Module E V]
    (n : Nat) (places : FunctionFieldPlaceData F)
    (localFactorMatches :
      LafforgueGaloisParameter F E V ->
        LafforgueAutomorphicRepresentation Fq F E -> places.Place -> Prop) : Prop :=
  ∀ rho : LafforgueGaloisParameter F E V,
    rho.rank = n ->
    rho.continuous ->
    rho.irreducible ->
    rho.unramifiedOutsideFiniteSet ->
    rho.determinantFiniteOrderAfterTwist ->
      ∃ pi : LafforgueAutomorphicRepresentation Fq F E,
        pi.rank = n ∧
          pi.cuspidal ∧
          pi.centralCharacterFiniteOrder ∧
          HeckeFrobeniusCompatibility places rho pi (localFactorMatches rho pi)

/--
Low-risk introduction wrapper for the normalized statement boundary.

This is useful for later dependency integration: a checked upstream theorem with
the same explicit boundary can be routed through this wrapper.
-/
theorem statementShape_of_realization
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F]
    (E : Type uE) [Field E]
    (V : Type uV) [AddCommGroup V] [Module E V]
    (n : Nat) (places : FunctionFieldPlaceData F)
    (localFactorMatches :
      LafforgueGaloisParameter F E V ->
        LafforgueAutomorphicRepresentation Fq F E -> places.Place -> Prop)
    (h :
      ∀ rho : LafforgueGaloisParameter F E V,
        rho.rank = n ->
        rho.continuous ->
        rho.irreducible ->
        rho.unramifiedOutsideFiniteSet ->
        rho.determinantFiniteOrderAfterTwist ->
          ∃ pi : LafforgueAutomorphicRepresentation Fq F E,
            pi.rank = n ∧
              pi.cuspidal ∧
              pi.centralCharacterFiniteOrder ∧
              HeckeFrobeniusCompatibility places rho pi (localFactorMatches rho pi)) :
    StatementShape Fq F E V n places localFactorMatches :=
  h

/-- Checked mathlib wrapper: function-field class number one is equivalent to PID. -/
theorem functionField_classNumber_eq_one_iff_pid
    (Fq : Type uFq) (F : Type uF) [Field Fq] [Fintype Fq] [Field F]
    [Algebra Fq[X] F] [Algebra (RatFunc Fq) F]
    [IsScalarTower Fq[X] (RatFunc Fq) F]
    [FunctionField Fq F] [Algebra.IsSeparable (RatFunc Fq) F] :
    FunctionField.classNumber Fq F = 1 <->
      IsPrincipalIdealRing (FunctionField.ringOfIntegers Fq F) :=
  FunctionField.classNumber_eq_one_iff Fq F

/--
Checked mathlib wrapper: the generic arithmetic Frobenius construction is
available for invariant finite group actions with finite residue field.

This is not the Frobenius/Satake compatibility assertion in Lafforgue's theorem;
it is only a nearby algebraic anchor.
-/
theorem arithFrobAt_isArithFrobAt
    (R S G : Type*) [CommRing R] [CommRing S] [Algebra R S]
    [Group G] [MulSemiringAction G S] [SMulCommClass G R S]
    [Finite G] [Algebra.IsInvariant R S G]
    (Q : Ideal S) [Q.IsPrime] [Finite (S ⧸ Q)] :
    IsArithFrobAt R (arithFrobAt R G Q) Q :=
  IsArithFrobAt.arithFrobAt R G Q

/-! ## Audit probes retained in the checked file. -/

#check FunctionField
#check FunctionField.ringOfIntegers
#check FunctionField.classNumber_eq_one_iff
#check FunctionFieldFinitePlace
#check FunctionFieldResidueField
#check functionFieldPlaceDataOfHeightOneSpectrum
#check functionFieldPlaceDataOfHeightOneSpectrum_residueCardinality
#check functionFieldPlaceDataOfHeightOneSpectrum_residueCardinality_eq_fintype_card
#check Field.absoluteGaloisGroup
#check Representation
#check IsArithFrobAt
#check arithFrobAt
#check arithFrobAt_isArithFrobAt
#check StatementShape

/-- mathlib commit requested for the public Stage1 audit row for this slot. -/
def requestedPublicAuditMathlibCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact module set requested for the public Stage1 audit row for this slot. -/
def requestedPublicAuditModules : List String := [
  "Mathlib.NumberTheory.FunctionField",
  "Mathlib.NumberTheory.ClassNumber.FunctionField",
  "Mathlib.FieldTheory.AbsoluteGaloisGroup",
  "Mathlib.RepresentationTheory.Basic",
  "Mathlib.RingTheory.Frobenius"
]

/-- mathlib modules checked while locating local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.FunctionField",
  "Mathlib.NumberTheory.ClassNumber.FunctionField",
  "Mathlib.FieldTheory.AbsoluteGaloisGroup",
  "Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic",
  "Mathlib.RepresentationTheory.Basic",
  "Mathlib.RingTheory.Frobenius",
  "Mathlib.RingTheory.DedekindDomain.FiniteAdeleRing",
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.NumberTheory.NumberField.AdeleRing"
]

/-- Search terms that did not locate a terminal Laurent Lafforgue theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Lafforgue",
  "Langlands",
  "Automorphic",
  "GaloisRepresentation",
  "WeilRepresentation",
  "Satake",
  "LocalLanglands",
  "global function field GL_n"
]

/--
C003 public-status gate for Laurent Lafforgue.

This records the Stage1 rule that the public row must stay `not completed` with
`formalization_debt` until a terminal local Lean proof is validated or an
external Lean 4 proof is pinned, imported, and checked inside this repository.
-/
structure PublicStatusGate where
  publicStatus : String
  debtClass : String
  localArtifact : String
  validationCommand : String
  terminalLocalProofValidated : Bool
  externalLeanProofPinnedImportedChecked : Bool
  externalAnchorOnlyMayComplete : Bool
  repoLocalIntegrationDebtGate : String
  requiredBeforeCompletion : List String

/--
C003 result: the checked artifact is a statement boundary plus local anchors,
not a completed Laurent Lafforgue theorem.
-/
def c003PublicStatusGate : PublicStatusGate where
  publicStatus := "not completed"
  debtClass := "formalization_debt"
  localArtifact :=
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_061.lean"
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_061.lean"
  terminalLocalProofValidated := false
  externalLeanProofPinnedImportedChecked := false
  externalAnchorOnlyMayComplete := false
  repoLocalIntegrationDebtGate :=
    "pass_noncompletion: no completed state is claimed, so no completed state retains repo_local_integration_debt"
  requiredBeforeCompletion := [
    "replace StatementShape by a terminal local Lean proof body, or",
    "pin/import/check an external Lean 4 Laurent Lafforgue proof with repository URL, commit hash, toolchain, module path, theorem name, and local validation result"
  ]

/-- The C003 gate keeps the public status and debt classification open. -/
theorem c003PublicStatusGate_keeps_not_completed :
    c003PublicStatusGate.publicStatus = "not completed" ∧
      c003PublicStatusGate.debtClass = "formalization_debt" ∧
      c003PublicStatusGate.terminalLocalProofValidated = false ∧
      c003PublicStatusGate.externalLeanProofPinnedImportedChecked = false ∧
      c003PublicStatusGate.externalAnchorOnlyMayComplete = false := by
  simp [c003PublicStatusGate]

#check c003PublicStatusGate
#check c003PublicStatusGate_keeps_not_completed

/--
C008 external Lean proof integration gate.

This records the metadata that must be populated before any later public Lean 4
Laurent Lafforgue proof can affect the completion status.  A URL or theorem
name alone is deliberately insufficient: the proof must be pinned, imported into
the repository validation closure, and checked locally.
-/
structure ExternalLeanProofIntegrationGate where
  proofLocated : Bool
  repositoryUrl : String
  commitHash : String
  toolchain : String
  modulePath : String
  theoremName : String
  localValidationCommand : String
  localValidationResult : String
  pinnedDependencyOrVendor : Bool
  importedIntoRepoClosure : Bool
  locallyChecked : Bool
  anchorOnlyMayComplete : Bool
  statusChangePermitted : Bool
  repoLocalIntegrationDebtGate : String
  requiredMetadataBeforeStatusChange : List String

/--
C008 result: no external Lean 4 Laurent Lafforgue proof is currently part of
this repository's validation closure.
-/
def c008ExternalLeanProofIntegrationGate : ExternalLeanProofIntegrationGate where
  proofLocated := false
  repositoryUrl := "not located"
  commitHash := "not located"
  toolchain := "not located"
  modulePath := "not located"
  theoremName := "not located"
  localValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_061.lean"
  localValidationResult :=
    "local S1_M_061 statement-boundary artifact checked; no external proof checked"
  pinnedDependencyOrVendor := false
  importedIntoRepoClosure := false
  locallyChecked := false
  anchorOnlyMayComplete := false
  statusChangePermitted := false
  repoLocalIntegrationDebtGate :=
    "pass_noncompletion: no completed state is claimed; if an external proof is later located, anchor-only evidence must not be marked completed"
  requiredMetadataBeforeStatusChange := [
    "repository URL",
    "commit hash",
    "Lean toolchain",
    "module path",
    "theorem name",
    "pin or vendored dependency path",
    "repo-local import or wrapper target",
    "local validation command",
    "local validation result"
  ]

/-- C008 completion gate: anchor-only external evidence cannot change status. -/
theorem c008ExternalLeanProofIntegrationGate_blocks_anchor_only_completion :
    c008ExternalLeanProofIntegrationGate.proofLocated = false ∧
      c008ExternalLeanProofIntegrationGate.pinnedDependencyOrVendor = false ∧
      c008ExternalLeanProofIntegrationGate.importedIntoRepoClosure = false ∧
      c008ExternalLeanProofIntegrationGate.locallyChecked = false ∧
      c008ExternalLeanProofIntegrationGate.anchorOnlyMayComplete = false ∧
      c008ExternalLeanProofIntegrationGate.statusChangePermitted = false := by
  simp [c008ExternalLeanProofIntegrationGate]

#check c008ExternalLeanProofIntegrationGate
#check c008ExternalLeanProofIntegrationGate_blocks_anchor_only_completion

/--
C005 automorphic-side design gate.

This child adds checked Lean names for the finite-adelic function-field anchor,
`GL_n` over that anchor, central-character data, and Satake-parameter data.  It
does not claim the full automorphic side of Laurent Lafforgue, because the
full function-field adele ring, cuspidal automorphic representation category,
idele-class central characters, and Satake/local Hecke theory are still absent
from the repo-local Lean closure.
-/
structure AutomorphicSideDesignGate where
  finiteFunctionFieldAdeleAnchor : Bool
  finiteAdeleGLnAnchor : Bool
  abstractCuspidalAutomorphicRepresentationApi : Bool
  abstractCentralCharacterApi : Bool
  abstractSatakeParameterApi : Bool
  fullFunctionFieldAdeleRingApi : Bool
  concreteCuspidalAutomorphicRepresentationApi : Bool
  concreteIdeleClassCentralCharacterApi : Bool
  concreteSatakeHeckeApi : Bool
  terminalLaurentLafforgueAutomorphicSide : Bool
  repoLocalCompletionClaimed : Bool
  debtClassification : String
  missingLeaves : List String

/-- C005 result: checked design anchors only; terminal automorphic formalization remains open. -/
def c005AutomorphicSideDesignGate : AutomorphicSideDesignGate where
  finiteFunctionFieldAdeleAnchor := true
  finiteAdeleGLnAnchor := true
  abstractCuspidalAutomorphicRepresentationApi := true
  abstractCentralCharacterApi := true
  abstractSatakeParameterApi := true
  fullFunctionFieldAdeleRingApi := false
  concreteCuspidalAutomorphicRepresentationApi := false
  concreteIdeleClassCentralCharacterApi := false
  concreteSatakeHeckeApi := false
  terminalLaurentLafforgueAutomorphicSide := false
  repoLocalCompletionClaimed := false
  debtClassification := "formalization_debt_not_repo_local_integration_debt"
  missingLeaves := [
    "replace FunctionFieldFiniteAdeleRing by a full function-field adele ring including places above infinity",
    "replace FunctionFieldFiniteAdeleGLn by GL_n over the full function-field adele ring and its rational diagonal embedding",
    "define cuspidal automorphic representations of GL_n over function-field adeles with equivalence classes",
    "define central characters on the function-field idele class group and finite-order hypotheses",
    "define unramified Hecke algebras, Satake parameters, and Hecke polynomials at function-field places",
    "connect the Satake/Hecke polynomials to the Galois-side Frobenius characteristic polynomials"
  ]

/-- C005 completion gate: this child makes no theorem-completion claim. -/
theorem c005AutomorphicSideDesignGate_no_completion_claim :
    c005AutomorphicSideDesignGate.repoLocalCompletionClaimed = false ∧
      c005AutomorphicSideDesignGate.terminalLaurentLafforgueAutomorphicSide = false :=
  ⟨rfl, rfl⟩

#check FunctionFieldFiniteAdeleRing
#check GLn
#check FunctionFieldFiniteAdeleGLn
#check AutomorphicCentralCharacter
#check AutomorphicSatakeParameters
#check LafforgueAutomorphicSide
#check LafforgueAutomorphicSide.rank
#check LafforgueAutomorphicSide.finiteAdeleGLn
#check LafforgueAutomorphicSide.centralCharacter_finiteOrder
#check LafforgueAutomorphicSide.satake_definedAtUnramified
#check c005AutomorphicSideDesignGate
#check c005AutomorphicSideDesignGate_no_completion_claim

/--
C006 Galois/Weil-side design gate.

This child adds checked Lean names for continuous `l`-adic source predicates,
finite ramification, irreducibility, determinant/twist hypotheses, and
unramified Frobenius characteristic polynomials.  It does not claim the full
Galois/Weil side of Laurent Lafforgue, because the concrete function-field Weil
group, inertia/decomposition subgroups, continuity topology, and characteristic
polynomial construction are still absent from the repo-local Lean closure.
-/
structure GaloisWeilSideDesignGate where
  abstractAbsoluteGaloisRepresentationAnchor : Bool
  abstractLAdicContinuityPredicate : Bool
  abstractFiniteRamificationPredicate : Bool
  abstractIrreducibilityPredicate : Bool
  abstractDeterminantTwistPredicate : Bool
  abstractWeilGroupApi : Bool
  abstractFrobeniusCharacteristicPolynomialApi : Bool
  concreteFunctionFieldWeilGroupApi : Bool
  concreteRamificationInertiaApi : Bool
  concreteLAdicTopologyContinuityApi : Bool
  concreteFrobeniusCharacteristicPolynomialConstruction : Bool
  terminalLaurentLafforgueGaloisWeilSide : Bool
  repoLocalCompletionClaimed : Bool
  debtClassification : String
  missingLeaves : List String

/-- C006 result: checked Galois/Weil-side design anchors only; terminal formalization remains open. -/
def c006GaloisWeilSideDesignGate : GaloisWeilSideDesignGate where
  abstractAbsoluteGaloisRepresentationAnchor := true
  abstractLAdicContinuityPredicate := true
  abstractFiniteRamificationPredicate := true
  abstractIrreducibilityPredicate := true
  abstractDeterminantTwistPredicate := true
  abstractWeilGroupApi := true
  abstractFrobeniusCharacteristicPolynomialApi := true
  concreteFunctionFieldWeilGroupApi := false
  concreteRamificationInertiaApi := false
  concreteLAdicTopologyContinuityApi := false
  concreteFrobeniusCharacteristicPolynomialConstruction := false
  terminalLaurentLafforgueGaloisWeilSide := false
  repoLocalCompletionClaimed := false
  debtClassification := "formalization_debt_not_repo_local_integration_debt"
  missingLeaves := [
    "replace GaloisWeilFrobeniusData.WeilGroup by a concrete global-function-field Weil group",
    "define decomposition and inertia groups at function-field places and the finite-ramification condition outside a finite set",
    "define the l-adic coefficient topology and prove continuity for the selected representation API",
    "connect irreducibility and determinant/twist hypotheses to concrete representation-theoretic definitions",
    "construct arithmetic Frobenius elements at unramified places in the concrete Weil group",
    "define the Frobenius action on the l-adic representation space and its characteristic polynomial",
    "connect these Frobenius characteristic polynomials to the automorphic-side Hecke/Satake polynomials"
  ]

/-- C006 completion gate: this child makes no theorem-completion claim. -/
theorem c006GaloisWeilSideDesignGate_no_completion_claim :
    c006GaloisWeilSideDesignGate.repoLocalCompletionClaimed = false ∧
      c006GaloisWeilSideDesignGate.terminalLaurentLafforgueGaloisWeilSide = false :=
  ⟨rfl, rfl⟩

#check GaloisWeilFrobeniusData
#check LafforgueGaloisWeilSide
#check LafforgueGaloisWeilSide.lAdicContinuous_iff_continuous
#check LafforgueGaloisWeilSide.finitelyRamified_iff_unramifiedOutsideFiniteSet
#check LafforgueGaloisWeilSide.irreducibleParameter_iff_irreducible
#check LafforgueGaloisWeilSide.determinantTwistHypothesis_iff_statementShape
#check LafforgueGaloisWeilSide.frobeniusCharacteristicPolynomial
#check LafforgueGaloisWeilSide.arithmeticFrobeniusAt
#check c006GaloisWeilSideDesignGate
#check c006GaloisWeilSideDesignGate_no_completion_claim

/--
C007 unramified-local-compatibility design gate.

This child adds the checked equality interface connecting the C006 Frobenius
characteristic-polynomial package to the C005 Hecke/Satake polynomial package.
It does not claim the local compatibility theorem, because the concrete
unramified Hecke algebra, Satake isomorphism, local Galois parameter, and
characteristic-polynomial construction are still missing.
-/
structure UnramifiedLocalCompatibilityDesignGate where
  abstractFrobeniusPolynomialApi : Bool
  abstractHeckeSatakePolynomialApi : Bool
  checkedPointwisePolynomialEqualityInterface : Bool
  checkedRankCompatibilityProjection : Bool
  checkedSatakeDefinednessProjection : Bool
  concreteUnramifiedHeckeAlgebraApi : Bool
  concreteSatakeIsomorphismApi : Bool
  concreteLocalGaloisParameterApi : Bool
  concretePolynomialEqualityProof : Bool
  terminalLaurentLafforgueLocalCompatibility : Bool
  repoLocalCompletionClaimed : Bool
  debtClassification : String
  missingLeaves : List String

/-- C007 result: checked local-compatibility interface only; terminal proof remains open. -/
def c007UnramifiedLocalCompatibilityDesignGate :
    UnramifiedLocalCompatibilityDesignGate where
  abstractFrobeniusPolynomialApi := true
  abstractHeckeSatakePolynomialApi := true
  checkedPointwisePolynomialEqualityInterface := true
  checkedRankCompatibilityProjection := true
  checkedSatakeDefinednessProjection := true
  concreteUnramifiedHeckeAlgebraApi := false
  concreteSatakeIsomorphismApi := false
  concreteLocalGaloisParameterApi := false
  concretePolynomialEqualityProof := false
  terminalLaurentLafforgueLocalCompatibility := false
  repoLocalCompletionClaimed := false
  debtClassification := "formalization_debt_not_repo_local_integration_debt"
  missingLeaves := [
    "replace FrobeniusHeckePolynomialMatches by a theorem from concrete local data",
    "define or import unramified Hecke algebras at function-field places",
    "define or import the Satake transform and Satake parameter polynomial",
    "define decomposition-group Frobenius actions on the chosen l-adic representation",
    "prove equality of Frobenius characteristic polynomials and Hecke/Satake polynomials at every unramified place",
    "connect the local equality package to the terminal global Laurent Lafforgue correspondence statement"
  ]

/-- C007 completion gate: this child makes no theorem-completion claim. -/
theorem c007UnramifiedLocalCompatibilityDesignGate_no_completion_claim :
    c007UnramifiedLocalCompatibilityDesignGate.repoLocalCompletionClaimed = false ∧
      c007UnramifiedLocalCompatibilityDesignGate.terminalLaurentLafforgueLocalCompatibility =
        false :=
  ⟨rfl, rfl⟩

#check FrobeniusHeckePolynomialMatches
#check UnramifiedLocalCompatibility
#check UnramifiedLocalCompatibility.rank_eq
#check UnramifiedLocalCompatibility.satake_definedAtUnramified
#check UnramifiedLocalCompatibility.frobeniusCharacteristicPolynomial_eq_heckePolynomial
#check c007UnramifiedLocalCompatibilityDesignGate
#check c007UnramifiedLocalCompatibilityDesignGate_no_completion_claim

end AwesomeTheorems.Stage1.S1_M_061
