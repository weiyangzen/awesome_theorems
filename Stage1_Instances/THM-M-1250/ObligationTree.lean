import Statement

/-! Conditional composition for the frozen THM-M-1250 proof architecture. -/

namespace Stage1Instances.THM_M_1250

/-- The bundled-to-classical direction, kept explicit as a proof obligation. -/
def ForwardPackage : Prop :=
  forall (n : Nat) (f : EuclideanDomain n -> Complex)
    (phi : SchwartzMap (EuclideanDomain n) Complex),
    (phi : EuclideanDomain n -> Complex) = f -> IsSchwartzFunction f

/-- The classical-to-bundled direction, kept explicit as a proof obligation. -/
def ReversePackage : Prop :=
  forall (n : Nat) (f : EuclideanDomain n -> Complex),
    IsSchwartzFunction f ->
      exists phi : SchwartzMap (EuclideanDomain n) Complex,
        (phi : EuclideanDomain n -> Complex) = f

/-- Checked child-to-parent composition. The two mathematical directions remain
explicit premises, so this theorem does not close the canonical root. -/
theorem characterization_of_packages
    (forward : ForwardPackage) (reverse : ReversePackage) :
    SchwartzSpaceCharacterization := by
  intro n f
  constructor
  · rintro ⟨phi, hphi⟩
    exact forward n f phi hphi
  · exact reverse n f

#print axioms characterization_of_packages

end Stage1Instances.THM_M_1250
