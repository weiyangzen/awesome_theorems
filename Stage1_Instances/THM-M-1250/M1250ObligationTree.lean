import Statement

/-! Canonically named proof interfaces for the THM-M-1250 blocker check. -/

namespace Stage1Instances.THM_M_1250

/-- The exact bundled-to-classical interface required by the frozen proof
architecture. -/
def M1250ForwardPackage : Prop :=
  forall (n : Nat) (f : EuclideanDomain n -> Complex)
    (phi : SchwartzMap (EuclideanDomain n) Complex),
    (phi : EuclideanDomain n -> Complex) = f -> IsSchwartzFunction f

/-- The exact classical-to-bundled interface required by the frozen proof
architecture. -/
def M1250ReversePackage : Prop :=
  forall (n : Nat) (f : EuclideanDomain n -> Complex),
    IsSchwartzFunction f ->
      exists phi : SchwartzMap (EuclideanDomain n) Complex,
        (phi : EuclideanDomain n -> Complex) = f

/-- Checked composition of the exact interfaces into the frozen root. -/
theorem characterization_of_m1250Packages
    (forward : M1250ForwardPackage) (reverse : M1250ReversePackage) :
    SchwartzSpaceCharacterization := by
  intro n f
  constructor
  · rintro ⟨phi, hphi⟩
    exact forward n f phi hphi
  · exact reverse n f

end Stage1Instances.THM_M_1250
