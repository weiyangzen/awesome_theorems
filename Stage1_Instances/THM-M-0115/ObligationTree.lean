import Statement

/-!
# THM-M-0115 conditional obligation composition

This module checks only the interfaces by which future GRR proof packages will
compose into the exact frozen target. The mathematical packages remain explicit
premises; no premise is inhabited here and no proof obligation receives closure
credit from this architecture phase.
-/

noncomputable section

namespace Stage1Instances.THMM0115.ObligationTree

universe u v

open GrothendieckRiemannRochData

/-- The terminal equality package required for every datum satisfying the
frozen domain and semantic-interface hypotheses. -/
def FormulaPackage : Prop :=
  forall (k : Type u) [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k),
      D.Hypotheses -> forall alpha : D.KZero D.X, D.Formula alpha

/-- The exact root-shaped package produced by the final assembly node. Keeping
this alias separate makes the root certificate consume precisely its declared
`M0115-T-ASSEMBLE` child rather than the formula child's interface. -/
def AssembledRootPackage : Prop :=
  GrothendieckRiemannRochTarget.{u, v}

/-- An intermediate Chow class together with its target-side identification.
The source-side identification is deliberately owned by the separate relative
comparison package below. -/
structure IntermediateComparisonData
    {k : Type u} [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k)
    (alpha : D.KZero D.X) where
  intermediate : D.ChowHomologyQ D.Y
  targetIdentification :
    D.capY (D.chernCharacterY (D.kTheoryPushforward alpha))
        (D.toddClassY D.tangentBundleY) = intermediate

/-- The target Todd-action branch constructs target-identified intermediate
data for every admissible datum and K_0 class. -/
def TargetToddActionPackage : Prop :=
  forall (k : Type u) [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k),
      D.Hypotheses -> forall alpha : D.KZero D.X,
        Nonempty (IntermediateComparisonData D alpha)

/-- The relative branch identifies every target-side intermediate supplied by
the Todd-action branch with the source Chow pushforward. -/
def RelativeComparisonPackage : Prop :=
  forall (k : Type u) [Field k]
    (D : GrothendieckRiemannRochData.{u, v} k),
      D.Hypotheses -> forall alpha : D.KZero D.X,
        forall comparison : IntermediateComparisonData D alpha,
          comparison.intermediate = D.chowPushforward
            (D.capX (D.chernCharacterX alpha)
              (D.toddClassX D.tangentBundleX))

/-- Checked identity wrapper from the exact assembled-root child package to the
public canonical target. -/
theorem root_of_assembled_root_package
    (assembled : AssembledRootPackage.{u, v}) :
    GrothendieckRiemannRochTarget.{u, v} := by
  exact assembled

/-- Checked composition from the terminal formula package to the exact
assembled-root child package. -/
theorem assembled_root_package_of_formula_package
    (formula : FormulaPackage.{u, v}) :
    AssembledRootPackage.{u, v} := by
  intro k _ D hypotheses alpha
  exact formula k D hypotheses alpha

/-- Checked composition of both substantive comparison children into the exact
terminal formula. Both packages remain open proof work. -/
theorem formula_package_of_relative_and_todd
    (relative : RelativeComparisonPackage.{u, v})
    (todd : TargetToddActionPackage.{u, v}) :
    FormulaPackage.{u, v} := by
  intro k _ D hypotheses alpha
  let ⟨comparison⟩ := todd k D hypotheses alpha
  exact comparison.targetIdentification.trans
    (relative k D hypotheses alpha comparison)

#check root_of_assembled_root_package
#check assembled_root_package_of_formula_package
#check formula_package_of_relative_and_todd
#print axioms root_of_assembled_root_package
#print axioms assembled_root_package_of_formula_package
#print axioms formula_package_of_relative_and_todd

end Stage1Instances.THMM0115.ObligationTree
