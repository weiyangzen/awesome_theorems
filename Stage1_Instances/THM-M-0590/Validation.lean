import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0590 same-worker differential validation

This module imports only the frozen statement. It independently reconstructs
the normal-operator boundary and the diagonal invariant equivalence checked in
the proof phase. It also checks the final logical adapter while retaining both
directional BDF packages as explicit premises.

These probes are same-worker implementation-diverse evidence, not an
unconditional BDF proof or the distinct signed verifier required for release.
-/

noncomputable section

open scoped ComplexConjugate InnerProduct

namespace THMM0590.Validation

universe u v

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

/-- Direct reconstruction of the normal-operator boundary without importing
the proof implementation. -/
theorem essentiallyNormalOfNormalDirect (A : E →L[ℂ] E)
    (h : A† ∘L A = A ∘L A†) : IsEssentiallyNormal A := by
  unfold IsEssentiallyNormal
  rw [h, sub_self]
  exact isCompactOperator_zero

/-- Direct reconstruction of the exact diagonal invariant equivalence. -/
theorem diagonalInvariantEquivalenceDirect (A : E →L[ℂ] E) :
    UnitaryEquivalentModuloCompacts A A ↔
      essentialSpectrum A = essentialSpectrum A ∧
        ∀ z : ℂ, z ∉ essentialSpectrum A →
          fredholmIndex (A - z • ContinuousLinearMap.id ℂ E) =
            fredholmIndex (A - z • ContinuousLinearMap.id ℂ E) := by
  constructor
  · intro _
    exact ⟨rfl, fun _ _ => rfl⟩
  · intro _
    refine ⟨LinearIsometryEquiv.refl ℂ E, ?_⟩
    have hzero :
        (LinearIsometryEquiv.refl ℂ E).toContinuousLinearEquiv.toContinuousLinearMap ∘L
              A ∘L
              (LinearIsometryEquiv.refl ℂ E).symm.toContinuousLinearEquiv.toContinuousLinearMap -
            A = 0 := by
      ext x
      simp
    rw [hzero]
    exact isCompactOperator_zero

/-- Independently checked final adapter. Both directional classification
packages remain visible premises and receive no root-closure credit. -/
theorem conditionalRootDirect
    (forward : ∀ (H : Type u) (K : Type v)
      [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
      [TopologicalSpace.SeparableSpace H]
      [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
      [TopologicalSpace.SeparableSpace K]
      (T : H →L[ℂ] H) (S : K →L[ℂ] K),
      (¬ FiniteDimensional ℂ H) → (¬ FiniteDimensional ℂ K) →
      IsEssentiallyNormal T → IsEssentiallyNormal S →
      UnitaryEquivalentModuloCompacts T S →
        essentialSpectrum T = essentialSpectrum S ∧
          ∀ z : ℂ, z ∉ essentialSpectrum T →
            fredholmIndex (T - z • ContinuousLinearMap.id ℂ H) =
              fredholmIndex (S - z • ContinuousLinearMap.id ℂ K))
    (backward : ∀ (H : Type u) (K : Type v)
      [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
      [TopologicalSpace.SeparableSpace H]
      [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
      [TopologicalSpace.SeparableSpace K]
      (T : H →L[ℂ] H) (S : K →L[ℂ] K),
      (¬ FiniteDimensional ℂ H) → (¬ FiniteDimensional ℂ K) →
      IsEssentiallyNormal T → IsEssentiallyNormal S →
      (essentialSpectrum T = essentialSpectrum S ∧
        ∀ z : ℂ, z ∉ essentialSpectrum T →
          fredholmIndex (T - z • ContinuousLinearMap.id ℂ H) =
            fredholmIndex (S - z • ContinuousLinearMap.id ℂ K)) →
        UnitaryEquivalentModuloCompacts T S) :
    brownDouglasFillmoreTarget.{u, v} := by
  intro H K _ _ _ _ _ _ _ _ T S hH hK hT hS
  exact ⟨forward H K T S hH hK hT hS, backward H K T S hH hK hT hS⟩

assert_no_sorry essentiallyNormalOfNormalDirect
assert_no_sorry diagonalInvariantEquivalenceDirect
assert_no_sorry conditionalRootDirect

#print sorries essentiallyNormalOfNormalDirect
#print sorries diagonalInvariantEquivalenceDirect
#print sorries conditionalRootDirect

#print axioms essentiallyNormalOfNormalDirect
#print axioms diagonalInvariantEquivalenceDirect
#print axioms conditionalRootDirect

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``essentiallyNormalOfNormalDirect,
    ``diagonalInvariantEquivalenceDirect,
    ``conditionalRootDirect
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let env <- getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE roots={roots.size} declarations={closure.size} modules={modules.size} bodyless_nonaxioms={bodyless.size} unsafe={unsafeDecls.size}"

#print_validation_closure

end THMM0590.Validation
