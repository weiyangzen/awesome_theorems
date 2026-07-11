import «Statement»
import Mathlib.FieldTheory.IsAlgClosed.AlgebraicClosure

/-!
# THM-M-0120 proof-phase blocker witness

This module does not prove the Mori cone theorem. It kernel-checks that the
frozen target has a concrete countermodel: all geometric input hypotheses can
hold while `Conclusion` is false. Consequently no truthful proof body can be
implemented for the current statement boundary.
-/

noncomputable section

open CategoryTheory

namespace Stage1Instances.THMM0120.Proof

private def emptyData : ConeTheoremData.{0, 0, 0, 0} where
  k := AlgebraicClosure Rat
  X := AlgebraicGeometry.Spec (CommRingCat.of (AlgebraicClosure Rat))
  S := AlgebraicGeometry.Spec (CommRingCat.of (AlgebraicClosure Rat))
  f := 𝟙 _
  definedOverBaseField := True
  projective := True
  normal := True
  qFactorial := True
  klt := True
  relativeDimension := 0
  N1 := Real
  moriCone := {-1}
  moriConeClosed := isClosed_singleton
  canonicalPairing := LinearMap.id
  RationalCurve := Empty
  curveClass := Empty.elim
  antiCanonicalDegree := Empty.elim
  antiCanonicalDegree_spec := by intro C; exact C.elim
  isContracted := fun _ _ => False

private theorem emptyData_proper : AlgebraicGeometry.IsProper emptyData.f := by
  dsimp [emptyData]
  infer_instance

private theorem emptyData_no_conclusion : ¬emptyData.Conclusion := by
  rintro ⟨ι, _, ray, rayPackage, decomposition, localFiniteness, contractions⟩
  let z : emptyData.N1 := (-1 : Real)
  have hmem : z ∈ emptyData.moriCone := by
    change (-1 : Real) ∈ ({-1} : Set Real)
    simp
  obtain ⟨z0, hz0, terms, hterms, hsum⟩ := (decomposition z).mp hmem
  have hz0mem : (z0 : Real) ∈ ({-1} : Set Real) := by
    simpa [ConeTheoremData.NonnegativePart, emptyData] using hz0.1
  have hz0nonneg : (0 : Real) ≤ z0 := by
    simpa [ConeTheoremData.NonnegativePart, emptyData] using hz0.2
  have hz0eq : (z0 : Real) = (-1 : Real) := by simpa using hz0mem
  have : ¬(0 : Real) ≤ -1 := by norm_num
  exact this (hz0eq ▸ hz0nonneg)

/-- The exact frozen proposition is refutable, despite every input hypothesis
being inhabited. This is a blocker certificate, not theorem closure. -/
theorem not_moriConeTheoremTarget :
    ¬MoriConeTheoremTarget.{0, 0, 0, 0} := by
  intro h
  have conclusion := h emptyData emptyData_proper (by trivial) (by trivial)
    (by trivial) (by trivial) (by trivial)
  exact emptyData_no_conclusion conclusion

#print axioms not_moriConeTheoremTarget

end Stage1Instances.THMM0120.Proof
