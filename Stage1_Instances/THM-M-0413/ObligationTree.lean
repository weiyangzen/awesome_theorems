import Mathlib.NumberTheory.NumberField.Basic

/-!
Conditional composition checks for the frozen THM-M-0413 obligation architecture.
Every component below is an explicit premise; this file does not assert a new proof of any component.
-/

namespace Stage1.THMM0413.ObligationTree

universe u

open scoped NumberField

def Root : Prop :=
  forall (K : Type u) [Field K] [NumberField K],
    IsDedekindDomain (NumberField.RingOfIntegers K)

def InterfaceTarget : Prop :=
  forall (K : Type u) [Field K] [NumberField K],
    IsDedekindDomain (NumberField.RingOfIntegers K)

def GenericIntegralClosureTarget : Prop :=
  forall (K : Type u) [Field K] [NumberField K],
    IsDedekindDomain (NumberField.RingOfIntegers K)

def DomainComponent : Prop :=
  forall (K : Type u) [Field K] [NumberField K],
    IsDomain (NumberField.RingOfIntegers K)

def NoetherianComponent : Prop :=
  forall (K : Type u) [Field K] [NumberField K],
    IsNoetherianRing (NumberField.RingOfIntegers K)

def DimensionComponent : Prop :=
  forall (K : Type u) [Field K] [NumberField K],
    Ring.DimensionLEOne (NumberField.RingOfIntegers K)

def IntegralClosedComponent : Prop :=
  forall (K : Type u) [Field K] [NumberField K],
    IsIntegrallyClosed (NumberField.RingOfIntegers K)

/-- The four defining components conditionally compose to the generic integral-closure target. -/
theorem components_compose
    (hdomain : DomainComponent.{u})
    (hnoetherian : NoetherianComponent.{u})
    (hdimension : DimensionComponent.{u})
    (hintegral : IntegralClosedComponent.{u}) :
    GenericIntegralClosureTarget.{u} := by
  intro K _ _
  letI : IsDomain (NumberField.RingOfIntegers K) := hdomain K
  letI : IsNoetherianRing (NumberField.RingOfIntegers K) := hnoetherian K
  letI : Ring.DimensionLEOne (NumberField.RingOfIntegers K) := hdimension K
  letI : IsIntegrallyClosed (NumberField.RingOfIntegers K) := hintegral K
  exact @IsDedekindDomain.mk _ _ (hdomain K)
    (@IsDedekindRing.mk _ _ (hnoetherian K) (hdimension K) (hintegral K))

/-- The generic terminal result supplies the exact number-field interface. -/
theorem interface_from_generic
    (h : GenericIntegralClosureTarget.{u}) : InterfaceTarget.{u} := h

/-- The checked interface has exactly the frozen root type. -/
theorem root_from_interface (h : InterfaceTarget.{u}) : Root.{u} := h

theorem root_exact_type :
    Root.{u} =
      (forall (K : Type u) [Field K] [NumberField K],
        IsDedekindDomain (NumberField.RingOfIntegers K)) := rfl

#check components_compose
#check interface_from_generic
#check root_from_interface
#print axioms components_compose

end Stage1.THMM0413.ObligationTree
