import Statement
import Mathlib.NumberTheory.Padics.PadicNumbers

/-!
# THM-M-0419 conditional obligation composition

This module checks the child-to-parent interfaces frozen by the obligation
registry. The local induction engine, its three cyclic branches, and the
local-to-global package are explicit premises. No declaration below supplies
one of those mathematical packages.
-/

namespace Stage1.THM_M_0419.ObligationTree

universe uK uE

/-- The local containment conclusion used by the source-shaped p-adic route. -/
def LocalContainment (p : Nat) [Fact (Nat.Prime p)]
    (E : Type uE) [Field E] [Algebra ℚ_[p] E] : Prop :=
  ∃ n : Nat, n ≠ 0 ∧
    letI : Algebra ℚ_[p] (CyclotomicField n ℚ_[p]) :=
      CyclotomicField.algebraBase n ℚ_[p] ℚ_[p]
    Nonempty (E →ₐ[ℚ_[p]] CyclotomicField n ℚ_[p])

/-- The complete local Kronecker-Weber package required by globalization. -/
def LocalContainmentPackage : Prop :=
  ∀ (p : Nat) [Fact (Nat.Prime p)]
      (E : Type uE) [Field E] [Algebra ℚ_[p] E]
      [FiniteDimensional ℚ_[p] E] [IsAbelianGalois ℚ_[p] E],
    LocalContainment p E

/-- The tame cyclic prime-power branch, where the degree prime differs from p. -/
def TameBranchPackage : Prop :=
  ∀ (p : Nat) [Fact (Nat.Prime p)]
      (E : Type uE) [Field E] [Algebra ℚ_[p] E]
      [FiniteDimensional ℚ_[p] E] [IsAbelianGalois ℚ_[p] E]
      [IsCyclic (E ≃ₐ[ℚ_[p]] E)]
      (ℓ : Nat) (hℓ : Nat.Prime ℓ) (hℓp : ℓ ≠ p) (r : Nat),
    Module.finrank ℚ_[p] E = ℓ ^ r → LocalContainment p E

/-- The wildly ramified odd-prime cyclic branch. -/
def WildOddBranchPackage : Prop :=
  ∀ (p : Nat) [Fact (Nat.Prime p)], p ≠ 2 →
    ∀ (E : Type uE) [Field E] [Algebra ℚ_[p] E]
      [FiniteDimensional ℚ_[p] E] [IsAbelianGalois ℚ_[p] E]
      [IsCyclic (E ≃ₐ[ℚ_[p]] E)] (r : Nat),
      Module.finrank ℚ_[p] E = p ^ r → LocalContainment p E

/-- The wildly ramified 2-adic cyclic branch. -/
def WildTwoBranchPackage : Prop :=
  ∀ (E : Type uE) [Field E] [Algebra ℚ_[2] E]
      [FiniteDimensional ℚ_[2] E] [IsAbelianGalois ℚ_[2] E]
      [IsCyclic (E ≃ₐ[ℚ_[2]] E)] (r : Nat),
    Module.finrank ℚ_[2] E = 2 ^ r → LocalContainment 2 E

/-- The cyclic prime-power package produced by the three exhaustive branches. -/
def CyclicPrimePowerPackage : Prop :=
  ∀ (p : Nat) [Fact (Nat.Prime p)]
      (E : Type uE) [Field E] [Algebra ℚ_[p] E]
      [FiniteDimensional ℚ_[p] E] [IsAbelianGalois ℚ_[p] E]
      [IsCyclic (E ≃ₐ[ℚ_[p]] E)]
      (ℓ : Nat) (hℓ : Nat.Prime ℓ) (r : Nat),
    Module.finrank ℚ_[p] E = ℓ ^ r → LocalContainment p E

/-- Checked exhaustiveness and recomposition of the tame, odd-wild, and
2-adic-wild cyclic branches. The theorem proves none of the three premises. -/
theorem cyclicPrimePower_of_branches
    (tame : TameBranchPackage.{uE})
    (wildOdd : WildOddBranchPackage.{uE})
    (wildTwo : WildTwoBranchPackage.{uE}) :
    CyclicPrimePowerPackage.{uE} := by
  intro p hp E _ _ _ _ _ ℓ hℓ r hdegree
  by_cases hℓp : ℓ = p
  · subst ℓ
    by_cases hp2 : p = 2
    · subst p
      exact wildTwo E r hdegree
    · exact wildOdd p hp2 E r hdegree
  · exact tame p E ℓ hℓ hℓp r hdegree

/-- The strong-induction and complementary-subfield reduction interface. -/
def LocalInductionPackage : Prop :=
  CyclicPrimePowerPackage.{uE} → LocalContainmentPackage.{uE}

/-- Checked local recomposition. The induction engine and cyclic package stay
explicit, open premises. -/
theorem localContainment_of_induction
    (induction : LocalInductionPackage.{uE})
    (cyclic : CyclicPrimePowerPackage.{uE}) :
    LocalContainmentPackage.{uE} :=
  induction cyclic

/-- The positive-index presentation used by the audited external architecture. -/
def PositiveContainmentTarget : Prop :=
  ∀ (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
      [IsAbelianGalois ℚ K],
    ∃ n : Nat, 1 ≤ n ∧
      letI : Algebra ℚ (CyclotomicField n ℚ) :=
        CyclotomicField.algebraBase n ℚ ℚ
      Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ)

/-- A checked transport from the positive-index presentation to the exact
nonzero-index canonical statement. -/
def PositiveTransportPackage : Prop :=
  PositiveContainmentTarget.{uK} → Statement.{uK}

theorem checkedPositiveTransport : PositiveTransportPackage.{uK} := by
  intro positive K _ _ _ _
  obtain ⟨n, hn, embedding⟩ := positive K
  exact ⟨n, Nat.ne_of_gt hn, embedding⟩

/-- The substantive local-to-global interface: completions, conductor,
inertia/Minkowski, and cyclotomic-field identification all live below it. -/
def GlobalizationPackage : Prop :=
  LocalContainmentPackage.{uE} → PositiveContainmentTarget.{uK}

/-- The exact final assembly interface. Each required child is an explicit
argument, so no support or documentation edge can become a proof premise. -/
def RootAssemblyPackage : Prop :=
  PositiveTransportPackage.{uK} →
  LocalContainmentPackage.{uE} →
  GlobalizationPackage.{uK, uE} →
  Statement.{uK}

theorem checkedRootAssembly : RootAssemblyPackage.{uK, uE} := by
  intro transport localPackage global
  exact transport (global localPackage)

/-- Checked composition into the exact frozen root. The four arguments are
precisely the four proof children recorded for the root obligation. -/
theorem root_of_packages
    (transport : PositiveTransportPackage.{uK})
    (localPackage : LocalContainmentPackage.{uE})
    (global : GlobalizationPackage.{uK, uE})
    (assembly : RootAssemblyPackage.{uK, uE}) :
    Statement.{uK} :=
  assembly transport localPackage global

#check LocalContainmentPackage
#check CyclicPrimePowerPackage
#check PositiveContainmentTarget
#check Stage1.THM_M_0419.Statement

#print axioms cyclicPrimePower_of_branches
#print axioms localContainment_of_induction
#print axioms checkedPositiveTransport
#print axioms checkedRootAssembly
#print axioms root_of_packages

end Stage1.THM_M_0419.ObligationTree
