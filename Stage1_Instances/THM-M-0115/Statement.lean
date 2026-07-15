import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
# THM-M-0115: Grothendieck-Riemann-Roch statement

This module freezes the classical nonsingular quasi-projective variety formula
selected at intake. The pinned mathlib snapshot supplies schemes, morphisms over
a base scheme, smoothness, and properness. It does not supply the combined
scheme-level APIs for quasi-projectivity, `K_0`, rational Chow homology, the two
pushforwards, Chern character, tangent bundles, Todd classes, and cap action.
Those missing notions are therefore represented by typed data and named
compatibility predicates. No field assumes or implies the GRR equality.

This file states and mutation-tests the target only. It does not prove GRR.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u v

namespace Stage1Instances.THMM0115

/-- The base scheme of a commutative ring. -/
abbrev SpecOf (k : Type u) [CommRing k] : Scheme.{u} :=
  Spec (CommRingCat.of k)

/--
Typed data needed for the intake-selected GRR formula. `KZero Z` denotes
`K_0(Z)`, while `ChowHomologyQ Z` denotes rational Chow homology. The fields
name the standard semantic interpretations that are absent from the pinned
native APIs; none contains the desired equality.
-/
structure GrothendieckRiemannRochData (k : Type u) [Field k] where
  /-- Source and target varieties are modeled by their underlying schemes. -/
  X : Scheme.{u}
  Y : Scheme.{u}
  sourceStructureMap : X ⟶ SpecOf k
  targetStructureMap : Y ⟶ SpecOf k
  map : X ⟶ Y
  /-- These predicates assert that the schemes and structure maps are the
  varieties over `k` named by the source statement. -/
  sourceIsVarietyOverBase : Prop
  targetIsVarietyOverBase : Prop
  /-- Quasi-projectivity of the two structure morphisms. -/
  sourceIsQuasiProjectiveOverBase : Prop
  targetIsQuasiProjectiveOverBase : Prop
  /-- The actual `K_0` and rational Chow-homology families selected by the
  semantic compatibility fields below. -/
  KZero : Scheme.{u} → Type v
  [kZeroAddCommGroup : ∀ Z, AddCommGroup (KZero Z)]
  ChowHomologyQ : Scheme.{u} → Type v
  [chowHomologyQAddCommGroup : ∀ Z, AddCommGroup (ChowHomologyQ Z)]
  kTheoryPushforward : KZero X → KZero Y
  chowPushforward : ChowHomologyQ X → ChowHomologyQ Y
  chernCharacterX : KZero X → ChowHomologyQ X
  chernCharacterY : KZero Y → ChowHomologyQ Y
  tangentClassX : Type v
  tangentClassY : Type v
  toddClassX : tangentClassX → ChowHomologyQ X
  toddClassY : tangentClassY → ChowHomologyQ Y
  tangentBundleX : tangentClassX
  tangentBundleY : tangentClassY
  capX : ChowHomologyQ X → ChowHomologyQ X → ChowHomologyQ X
  capY : ChowHomologyQ Y → ChowHomologyQ Y → ChowHomologyQ Y
  kZeroModelsGrothendieckGroup : Prop
  chowHomologyQModelsRationalChowHomology : Prop
  kTheoryPushforwardModelsProperPushforward : Prop
  chowPushforwardModelsProperPushforward : Prop
  chernCharactersModelChernCharacter : Prop
  tangentClassesModelTangentBundles : Prop
  toddClassesModelToddClasses : Prop
  capActionsModelChowCapProduct : Prop

namespace GrothendieckRiemannRochData

variable {k : Type u} [Field k]

/-- All domain and semantic-interface hypotheses of the frozen target. -/
def Hypotheses (D : GrothendieckRiemannRochData.{u, v} k) : Prop :=
  (D.sourceStructureMap = D.map ≫ D.targetStructureMap) ∧
    D.sourceIsVarietyOverBase ∧ D.targetIsVarietyOverBase ∧
    Smooth D.sourceStructureMap ∧ Smooth D.targetStructureMap ∧
      D.sourceIsQuasiProjectiveOverBase ∧
        D.targetIsQuasiProjectiveOverBase ∧ IsProper D.map ∧
          D.kZeroModelsGrothendieckGroup ∧
            D.chowHomologyQModelsRationalChowHomology ∧
              D.kTheoryPushforwardModelsProperPushforward ∧
                D.chowPushforwardModelsProperPushforward ∧
                  D.chernCharactersModelChernCharacter ∧
                    D.tangentClassesModelTangentBundles ∧
                      D.toddClassesModelToddClasses ∧
                        D.capActionsModelChowCapProduct

/-- The typed GRR equality in rational Chow homology of `Y`. -/
def Formula (D : GrothendieckRiemannRochData.{u, v} k)
    (alpha : D.KZero D.X) : Prop :=
  D.capY (D.chernCharacterY (D.kTheoryPushforward alpha))
      (D.toddClassY D.tangentBundleY) =
    D.chowPushforward
      (D.capX (D.chernCharacterX alpha) (D.toddClassX D.tangentBundleX))

end GrothendieckRiemannRochData

/--
The fully expanded target is a named definition so its exact expression can be
fingerprinted independently of the convenient `Hypotheses` and `Formula`
abbreviations.
-/
def GrothendieckRiemannRochExpandedTarget : Prop :=
  ∀ (k : Type u) [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k),
      (D.sourceStructureMap = D.map ≫ D.targetStructureMap) ∧
        D.sourceIsVarietyOverBase ∧ D.targetIsVarietyOverBase ∧
          Smooth D.sourceStructureMap ∧ Smooth D.targetStructureMap ∧
            D.sourceIsQuasiProjectiveOverBase ∧
              D.targetIsQuasiProjectiveOverBase ∧ IsProper D.map ∧
                D.kZeroModelsGrothendieckGroup ∧
                  D.chowHomologyQModelsRationalChowHomology ∧
                    D.kTheoryPushforwardModelsProperPushforward ∧
                      D.chowPushforwardModelsProperPushforward ∧
                        D.chernCharactersModelChernCharacter ∧
                          D.tangentClassesModelTangentBundles ∧
                            D.toddClassesModelToddClasses ∧
                              D.capActionsModelChowCapProduct →
        ∀ alpha : D.KZero D.X,
          D.capY (D.chernCharacterY (D.kTheoryPushforward alpha))
              (D.toddClassY D.tangentBundleY) =
            D.chowPushforward
              (D.capX (D.chernCharacterX alpha)
                (D.toddClassX D.tangentBundleX))

/--
The exact normalized target: GRR for every proper morphism of nonsingular
quasi-projective varieties over a field and every class in `K_0(X)`.
-/
def GrothendieckRiemannRochTarget : Prop :=
  GrothendieckRiemannRochExpandedTarget.{u, v}

/-- Checked expansion fixing every ordered binder, hypothesis, map, and factor. -/
theorem grothendieckRiemannRochTarget_iff_expanded :
    GrothendieckRiemannRochTarget.{u, v} ↔
      GrothendieckRiemannRochExpandedTarget.{u, v} :=
  Iff.rfl

/-! Structural mutations elaborate independently and receive no identity credit. -/

def MutationRemovedProperness : Prop :=
  ∀ (k : Type u) [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k),
      (D.sourceStructureMap = D.map ≫ D.targetStructureMap) ∧
        D.sourceIsVarietyOverBase ∧ D.targetIsVarietyOverBase ∧
        Smooth D.sourceStructureMap ∧ Smooth D.targetStructureMap ∧
          D.sourceIsQuasiProjectiveOverBase ∧
            D.targetIsQuasiProjectiveOverBase ∧
              D.kZeroModelsGrothendieckGroup ∧
                D.chowHomologyQModelsRationalChowHomology ∧
                  D.kTheoryPushforwardModelsProperPushforward ∧
                    D.chowPushforwardModelsProperPushforward ∧
                      D.chernCharactersModelChernCharacter ∧
                        D.tangentClassesModelTangentBundles ∧
                          D.toddClassesModelToddClasses ∧
                            D.capActionsModelChowCapProduct →
        ∀ alpha : D.KZero D.X, D.Formula alpha

def MutationChangedBaseDomain : Prop :=
  ∀ (k : Type u) [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k),
      D.sourceIsVarietyOverBase ∧ D.targetIsVarietyOverBase ∧
        D.sourceIsQuasiProjectiveOverBase ∧
          D.targetIsQuasiProjectiveOverBase ∧ IsProper D.map ∧
            D.kZeroModelsGrothendieckGroup ∧
              D.chowHomologyQModelsRationalChowHomology ∧
                D.kTheoryPushforwardModelsProperPushforward ∧
                  D.chowPushforwardModelsProperPushforward ∧
                    D.chernCharactersModelChernCharacter ∧
                      D.tangentClassesModelTangentBundles ∧
                        D.toddClassesModelToddClasses ∧
                          D.capActionsModelChowCapProduct →
        ∀ alpha : D.KZero D.X, D.Formula alpha

def MutationChangedAlphaBinderScope : Prop :=
  ∀ (k : Type u) [Field k],
    ∃ (D : GrothendieckRiemannRochData.{u, v} k)
      (alpha : D.KZero D.X), D.Hypotheses ∧ D.Formula alpha

def MutationOnlyZeroClass : Prop :=
  ∀ (k : Type u) [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k),
      letI := D.kZeroAddCommGroup D.X
      D.Hypotheses → D.Formula (0 : D.KZero D.X)

variable
  (hRemoved : MutationRemovedProperness.{u, v})
  (hDomain : MutationChangedBaseDomain.{u, v})
  (hScope : MutationChangedAlphaBinderScope.{u, v})
  (hBoundary : MutationOnlyZeroClass.{u, v})

#check_failure (show GrothendieckRiemannRochTarget.{u, v} from hRemoved)
#check_failure (show GrothendieckRiemannRochTarget.{u, v} from hDomain)
#check_failure (show GrothendieckRiemannRochTarget.{u, v} from hScope)
#check_failure (show GrothendieckRiemannRochTarget.{u, v} from hBoundary)

#check grothendieckRiemannRochTarget_iff_expanded
#print axioms grothendieckRiemannRochTarget_iff_expanded

set_option pp.universes true in
set_option pp.explicit true in
#print GrothendieckRiemannRochExpandedTarget

end Stage1Instances.THMM0115
