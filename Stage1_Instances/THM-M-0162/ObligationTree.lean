import «Stage1_Instances».«THM-M-0162».Statement

/-!
# THM-M-0162 conditional obligation composition

This module checks only the interfaces and final composition frozen by the
obligation registry. It does not provide any of the three Frenet-Serret
equation packages.
-/

namespace Stage1Instances.THM_M_0162

open Matrix

def FrenetPremises (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
    (kappa tau : Real -> Real) : Prop :=
  IsOpen U /\
  (forall s, s ∈ U -> HasDerivAt alpha (T s) s) /\
  (forall s, s ∈ U -> HasDerivAt T (T' s) s) /\
  (forall s, s ∈ U -> HasDerivAt N (N' s) s) /\
  (forall s, s ∈ U -> HasDerivAt B (B' s) s) /\
  (forall s, s ∈ U -> euclideanNorm (T s) = 1) /\
  (forall s, s ∈ U -> kappa s = euclideanNorm (T' s)) /\
  (forall s, s ∈ U -> 0 < kappa s) /\
  (forall s, s ∈ U -> N s = (kappa s)⁻¹ • T' s) /\
  (forall s, s ∈ U -> B s = T s ⨯₃ N s) /\
  (forall s, s ∈ U -> tau s = -dotProduct (B' s) (N s))

def TangentEquationPackage : Prop :=
  forall (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
      (kappa tau : Real -> Real),
    FrenetPremises U alpha T T' N N' B B' kappa tau ->
    forall s, s ∈ U -> T' s = kappa s • N s

def NormalEquationPackage : Prop :=
  forall (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
      (kappa tau : Real -> Real),
    FrenetPremises U alpha T T' N N' B B' kappa tau ->
    forall s, s ∈ U -> N' s = -(kappa s) • T s + tau s • B s

def BinormalEquationPackage : Prop :=
  forall (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
      (kappa tau : Real -> Real),
    FrenetPremises U alpha T T' N N' B B' kappa tau ->
    forall s, s ∈ U -> B' s = -(tau s) • N s

/-- Checked child-to-parent composition. Its three arguments remain open proof
obligations and therefore this theorem supplies no proof of the root. -/
theorem root_of_equation_packages
    (hT : TangentEquationPackage)
    (hN : NormalEquationPackage)
    (hB : BinormalEquationPackage) : FrenetSerretTarget := by
  intro U alpha T T' N N' B B' kappa tau hU hAlpha hT' hN' hB'
    hUnit hKappa hKappaPos hNormal hBinormal hTau s hs
  have hPremises : FrenetPremises U alpha T T' N N' B B' kappa tau :=
    ⟨hU, hAlpha, hT', hN', hB', hUnit, hKappa, hKappaPos, hNormal, hBinormal, hTau⟩
  exact ⟨hT U alpha T T' N N' B B' kappa tau hPremises s hs,
    hN U alpha T T' N N' B B' kappa tau hPremises s hs,
    hB U alpha T T' N N' B B' kappa tau hPremises s hs⟩

#print axioms root_of_equation_packages

end Stage1Instances.THM_M_0162
