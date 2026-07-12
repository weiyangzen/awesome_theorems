import Statement

/-!
# THM-M-1024 conditional obligation composition

This module checks the typed composition boundary for existence, converse, and
uniqueness. The three packages remain explicit premises; this is not a proof of
the Levy-Khintchine theorem.
-/

namespace Stage1Instances.THM_M_1024

open MeasureTheory

/-- Forward existence package required by the frozen architecture. -/
def ForwardExistencePackage : Prop :=
  forall (d : Nat) (mu : Measure (Space d)),
    InfinitelyDivisible mu -> exists data : LevyTriplet d, Represents mu data

/-- Converse package required by the frozen architecture. -/
def ConversePackage : Prop :=
  forall (d : Nat) (mu : Measure (Space d)),
    (exists data : LevyTriplet d, Represents mu data) -> InfinitelyDivisible mu

/-- Convention-relative uniqueness package required by the frozen architecture. -/
def UniquenessPackage : Prop :=
  forall (d : Nat) (mu : Measure (Space d)) (a b : LevyTriplet d),
    Represents mu a -> Represents mu b -> a = b

/-- Checked composition of the three open theorem packages into the exact root. -/
theorem root_of_packages
    (forward : ForwardExistencePackage)
    (converse : ConversePackage)
    (unique : UniquenessPackage) :
    LevyKhintchineTarget := by
  intro d mu
  constructor
  · intro hdiv
    obtain ⟨data, hdata⟩ := forward d mu hdiv
    exact ⟨data, hdata, fun other hother => unique d mu other data hother hdata⟩
  · rintro ⟨data, hdata, _⟩
    exact converse d mu ⟨data, hdata⟩

#print axioms root_of_packages

end Stage1Instances.THM_M_1024
