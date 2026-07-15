import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0419 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
independently restates and checks the cyclotomic-identification transport
implemented in the proof phase. It supplies no local Kronecker-Weber package,
globalization package, or exact-root proof.
-/

namespace Stage1.THM_M_0419.Validation

universe uK uL

/-- The input boundary before an abstract singleton cyclotomic extension is
identified with mathlib's canonical `CyclotomicField`. -/
def AbstractPositiveContainmentTarget : Prop :=
  ∀ (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
      [IsAbelianGalois ℚ K],
    ∃ n : ℕ, 1 ≤ n ∧
      ∃ (L : Type uL) (_ : Field L) (_ : Algebra ℚ L)
        (_ : IsCyclotomicExtension {n} ℚ L),
        Nonempty (K →ₐ[ℚ] L)

/-- The positive-index output boundary consumed by the frozen final
transport. -/
def PositiveContainmentTarget : Prop :=
  ∀ (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
      [IsAbelianGalois ℚ K],
    ∃ n : ℕ, 1 ≤ n ∧
      letI : Algebra ℚ (CyclotomicField n ℚ) :=
        CyclotomicField.algebraBase n ℚ ℚ
      Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ)

/-- Separately written reconstruction of the proof-phase transport, using
only the frozen statement import and pinned cyclotomic infrastructure. -/
theorem differentialCyclotomicIdentify :
    AbstractPositiveContainmentTarget.{uK, uL} →
      PositiveContainmentTarget.{uK} := by
  intro abstract K _ _ _ _
  obtain ⟨n, hn, L, fieldL, algebraL, cyclotomicL, ⟨f⟩⟩ := abstract K
  letI : Field L := fieldL
  letI : Algebra ℚ L := algebraL
  letI : IsCyclotomicExtension {n} ℚ L := cyclotomicL
  letI : NeZero n := ⟨Nat.ne_of_gt hn⟩
  letI : Algebra ℚ (CyclotomicField n ℚ) :=
    CyclotomicField.algebraBase n ℚ ℚ
  letI : IsCyclotomicExtension {n} ℚ (CyclotomicField n ℚ) :=
    CyclotomicField.isCyclotomicExtension n ℚ
  refine ⟨n, hn, ?_⟩
  exact ⟨(IsCyclotomicExtension.algEquiv {n} ℚ L
    (CyclotomicField n ℚ)).toAlgHom.comp f⟩

assert_no_sorry differentialCyclotomicIdentify

#print sorries differentialCyclotomicIdentify
#print sorries IsCyclotomicExtension.algEquiv
#print axioms differentialCyclotomicIdentify
#print axioms IsCyclotomicExtension.algEquiv

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1.THM_M_0419.Validation.differentialCyclotomicIdentify,
    ``IsCyclotomicExtension.algEquiv
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1.THM_M_0419.Validation
