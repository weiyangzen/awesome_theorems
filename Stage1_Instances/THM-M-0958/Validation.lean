import Statement
import Mathlib.Combinatorics.Additive.AP.Three.Behrend
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0958 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the exact digit-image package directly against the frozen
statement imports and checks the conditional witness-to-root transport. It
does not construct the open Elkin-scale witness package and is not an
independent-runner attestation.
-/

noncomputable section

open Finset

namespace Stage1Instances.THM_M_0958.Validation

/-- Validation-local one-based base-radix image. -/
def validationDigitImage {k y : Nat}
    (s : Finset (Fin k -> Nat)) : Finset Nat :=
  (s.image (Behrend.map (2 * y))).image (1 + .)

/-- A separately written reconstruction of the proof phase's finite digit
embedding package. Its hypotheses explicitly expose the still-missing vector
construction input, so this theorem supplies no Elkin-scale witness. -/
theorem digitEmbeddingPackage_validation {k y n : Nat}
    {s : Finset (Fin k -> Nat)}
    (hdigits : forall x, x ∈ s -> forall i, x i < y)
    (hy : 0 < y)
    (hpow : (2 * y) ^ k <= n)
    (hfree : ThreeAPFree (s : Set (Fin k -> Nat))) :
    exists t : Finset Nat,
      t ⊆ Ico 1 (n + 1) /\
      ThreeAPFree (t : Set Nat) /\
      t.card = s.card := by
  have hinj : Set.InjOn (Behrend.map (2 * y))
      {x : Fin k -> Nat | forall i, x i < y} :=
    Behrend.map_injOn.mono (by
      intro x hx i
      exact (hx i).trans_le (Nat.le_mul_of_pos_left y Nat.zero_lt_two))
  have himageFree :
      ThreeAPFree ((s.image (Behrend.map (2 * y))) : Set Nat) := by
    rw [coe_image]
    apply ThreeAPFree.image' (Behrend.map (2 * y)) _ hfree
    intro a ha b hb hab
    obtain ⟨a1, ha1, a2, ha2, rfl⟩ := ha
    obtain ⟨b1, hb1, b2, hb2, rfl⟩ := hb
    exact Behrend.map_injOn
      (fun j => by
        change a1 j + a2 j < 2 * y
        have h1 := hdigits a1 ha1 j
        have h2 := hdigits a2 ha2 j
        omega)
      (fun j => by
        change b1 j + b2 j < 2 * y
        have h1 := hdigits b1 hb1 j
        have h2 := hdigits b2 hb2 j
        omega)
      (by simpa only [map_add] using hab)
  have hcard : (s.image (Behrend.map (2 * y))).card = s.card := by
    apply Finset.card_image_of_injOn
    exact hinj.mono (by
      intro x hx
      exact hdigits x hx)
  have hrange : forall z, z ∈ s.image (Behrend.map (2 * y)) ->
      z < (2 * y) ^ k := by
    intro z hz
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hz
    calc
      Behrend.map (2 * y) x
          <= ∑ i : Fin k, (y - 1) * (2 * y) ^ (i : Nat) := by
            change (∑ i : Fin k, x i * (2 * y) ^ (i : Nat)) <= _
            exact Finset.sum_le_sum (fun i _ =>
              Nat.mul_le_mul_right _ (Nat.le_sub_one_of_lt (hdigits x hx i)))
      _ < (2 * y) ^ k := by
        rw [Fin.sum_univ_eq_sum_range (fun i => (y - 1) * (2 * y) ^ i)]
        calc
          _ <= ∑ i ∈ Finset.range k, ((2 * y) - 1) * (2 * y) ^ i := by
            gcongr
            omega
          _ = (2 * y) ^ k - 1 := by
            rw [Finset.sum_congr rfl (fun i _ => mul_comm _ _),
              <- Finset.sum_mul, Nat.geomSum_eq (by omega),
              Nat.div_mul_cancel]
            exact Nat.sub_one_dvd_pow_sub_one (2 * y) k
          _ < (2 * y) ^ k := Nat.sub_one_lt (pow_ne_zero k (by omega))
  refine ⟨validationDigitImage (y := y) s, ?_, ?_, ?_⟩
  · intro z hz
    obtain ⟨w, hw, rfl⟩ := Finset.mem_image.mp hz
    rw [Finset.mem_Ico]
    exact ⟨by omega, by
      simpa [Nat.add_comm] using
        Nat.add_lt_add_right ((hrange w hw).trans_le hpow) 1⟩
  · rw [validationDigitImage, coe_image]
    rintro _ ⟨a, ha, rfl⟩ _ ⟨b, hb, rfl⟩ _ ⟨c, hc, rfl⟩ habc
    apply congrArg (1 + .)
    apply himageFree ha hb hc
    change 1 + a + (1 + c) = 1 + b + (1 + b) at habc
    omega
  · rw [validationDigitImage, Finset.card_image_of_injective _
      (fun _ _ h => Nat.add_left_cancel h), hcard]

/-- Differential check of the exact conditional transport from the missing
construction witness to the frozen canonical target. -/
theorem conditionalRoot_validation
    (witness : Stage1Instances.THM_M_0958.WitnessConstructionTarget) :
    Stage1Instances.THM_M_0958.ElkinConstructionTarget := by
  exact Stage1Instances.THM_M_0958.elkinConstructionTarget_iff_witnessConstructionTarget.mpr
    witness

assert_no_sorry digitEmbeddingPackage_validation
assert_no_sorry conditionalRoot_validation
#print sorries digitEmbeddingPackage_validation
#print sorries conditionalRoot_validation
#print axioms digitEmbeddingPackage_validation
#print axioms conditionalRoot_validation

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0958.Validation.digitEmbeddingPackage_validation,
    ``Stage1Instances.THM_M_0958.Validation.conditionalRoot_validation
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

end Stage1Instances.THM_M_0958.Validation
