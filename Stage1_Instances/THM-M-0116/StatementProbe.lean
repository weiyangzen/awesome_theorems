import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.FieldTheory.IsAlgClosed.Basic
import Mathlib.GroupTheory.Finiteness

/-!
# THM-M-0116 statement-infrastructure probe

This module checks only the native base-field scheme, smooth relative
dimension, properness, additive quotient, and finite-generation substrate in
the pinned dependency closure. It deliberately does not declare a canonical
Neron-Severi target: the closure has no native projective-morphism predicate,
scheme-level divisor group, algebraic-equivalence relation on divisors, or
Neron-Severi quotient. Abstract carriers or proposition fields for those
notions would encode a substitute interface rather than the received theorem.
-/

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THMM0116.StatementProbe

universe u v

noncomputable section

abbrev SpecOf (k : Type u) [CommRing k] : Scheme.{u} :=
  Spec (CommRingCat.of k)

#check Scheme
#check Spec
#check IsAlgClosed
#check @SmoothOfRelativeDimension
#check @IsProper
#check AddCon
#check AddCon.Quotient
#check AddGroup.FG

/-- The native portion of the frozen surface domain. This omits projectivity,
the divisor group, and algebraic equivalence, so it is not the canonical target. -/
def SmoothProperDimensionTwoBoundary
    (k : Type u) [Field k] [IsAlgClosed k]
    (X : Scheme.{u}) (structureMap : X ⟶ SpecOf k) : Prop :=
  SmoothOfRelativeDimension 2 structureMap ∧ IsProper structureMap

/-- The native algebraic shape of a finitely generated additive quotient.
No supplied group or congruence is identified with divisors or algebraic equivalence. -/
def FinitelyGeneratedAdditiveQuotientBoundary
    (Divisor : Type v) [AddCommGroup Divisor]
    (algebraicEquivalence : AddCon Divisor) : Prop :=
  AddGroup.FG algebraicEquivalence.Quotient

#check SmoothProperDimensionTwoBoundary
#check FinitelyGeneratedAdditiveQuotientBoundary

end

end Stage1Instances.THMM0116.StatementProbe
