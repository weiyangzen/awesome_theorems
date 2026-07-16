import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0122 conditional obligation composition

This module freezes the exact interfaces at the top of the selected
Faltings/Mordell-Lang route.  The arithmetic-geometric engines remain explicit
premises.  The declarations below check child-to-parent composition only; they
do not prove or install Faltings' theorem.
-/

set_option autoImplicit false

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace Stage1Instances.THMM0122.ObligationTree

/-- The exact frozen theorem interface. -/
abbrev ExactRoot : Prop :=
  Stage1Instances.THMM0122.FaltingsTarget.{u}

/-- Normalize the unpointed curve after a finite extension and retain the
injection from the original rational-point type. -/
def FiniteExtensionNormalization : Prop :=
  forall (K : Type u) [Field K] [NumberField K]
      (C : Stage1Instances.THMM0122.CurveOver.{u} K),
    C.Hypotheses ->
      exists (L : Type u) (_ : Field L) (_ : NumberField L),
        exists (D : Stage1Instances.THMM0122.CurveOver.{u} L),
          D.Hypotheses /\
            Nonempty (Stage1Instances.THMM0122.RationalPoint D.scheme D.structureMap) /\
              exists f :
                  Stage1Instances.THMM0122.RationalPoint C.scheme C.structureMap ->
                    Stage1Instances.THMM0122.RationalPoint D.scheme D.structureMap,
                Function.Injective f

/-- For a pointed normalized curve, construct its Jacobian and an injective
Abel-Jacobi map on rational points.  The target type stands for the rational
points of the constructed Jacobian. -/
def AbelJacobiPackage : Prop :=
  forall (K : Type u) [Field K] [NumberField K]
      (C : Stage1Instances.THMM0122.CurveOver.{u} K),
    C.Hypotheses ->
      Nonempty (Stage1Instances.THMM0122.RationalPoint C.scheme C.structureMap) ->
        exists J : Type u,
          exists i : Stage1Instances.THMM0122.RationalPoint C.scheme C.structureMap -> J,
            Function.Injective i

/-- Mordell-Weil plus the exact curve-intersection form of Mordell-Lang makes
the Abel-Jacobi image finite. -/
def MordellLangFinitenessPackage : Prop :=
  forall (K : Type u) [Field K] [NumberField K]
      (C : Stage1Instances.THMM0122.CurveOver.{u} K),
    C.Hypotheses ->
      Nonempty (Stage1Instances.THMM0122.RationalPoint C.scheme C.structureMap) ->
        forall (J : Type u)
          (i : Stage1Instances.THMM0122.RationalPoint C.scheme C.structureMap -> J),
          Function.Injective i ->
            Finite (Set.range i)

/-- The exact terminal package consumed by the root. -/
def ExactTerminal : Prop :=
  Stage1Instances.THMM0122.FaltingsTarget.{u}

/-- Finiteness transports back through an injective map whose range is finite. -/
theorem finite_of_injective_and_finite_range
    {alpha beta : Type u} (f : alpha -> beta) (hf : Function.Injective f)
    (hRange : Finite (Set.range f)) : Finite alpha := by
  let toRange : alpha -> Set.range f := fun a => ⟨f a, ⟨a, rfl⟩⟩
  apply @Finite.of_injective alpha (Set.range f) hRange toRange
  intro a b h
  apply hf
  simpa [toRange] using congrArg Subtype.val h

/-- Checked terminal composition.  Every arithmetic-geometric child is
consumed, while none of those children is proved here. -/
theorem terminal_of_normalization_abelJacobi_mordellLang
    (normalize : FiniteExtensionNormalization.{u})
    (abelJacobi : AbelJacobiPackage.{u})
    (mordellLang : MordellLangFinitenessPackage.{u}) : ExactTerminal.{u} := by
  intro K _ _ C hC
  rcases normalize K C hC with ⟨L, fieldL, numberFieldL, D, hD, pointD, f, hf⟩
  letI : Field L := fieldL
  letI : NumberField L := numberFieldL
  rcases abelJacobi L D hD pointD with ⟨J, i, hi⟩
  have hImage : Finite (Set.range i) := mordellLang L D hD pointD J i hi
  have hDL : Finite (Stage1Instances.THMM0122.RationalPoint D.scheme D.structureMap) :=
    finite_of_injective_and_finite_range i hi hImage
  exact @Finite.of_injective
    (Stage1Instances.THMM0122.RationalPoint C.scheme C.structureMap)
    (Stage1Instances.THMM0122.RationalPoint D.scheme D.structureMap)
    hDL f hf

/-- Identity certificate from the terminal package to the canonical root. -/
theorem root_of_exactTerminal (terminal : ExactTerminal.{u}) : ExactRoot.{u} :=
  terminal

#check FiniteExtensionNormalization
#check AbelJacobiPackage
#check MordellLangFinitenessPackage
#check finite_of_injective_and_finite_range
#check terminal_of_normalization_abelJacobi_mordellLang
#check root_of_exactTerminal

assert_no_sorry finite_of_injective_and_finite_range
assert_no_sorry terminal_of_normalization_abelJacobi_mordellLang
assert_no_sorry root_of_exactTerminal

#print sorries finite_of_injective_and_finite_range
  terminal_of_normalization_abelJacobi_mordellLang root_of_exactTerminal
#print axioms finite_of_injective_and_finite_range
#print axioms terminal_of_normalization_abelJacobi_mordellLang
#print axioms root_of_exactTerminal

set_option pp.universes true in
set_option pp.explicit true in
#print ExactRoot

end Stage1Instances.THMM0122.ObligationTree
