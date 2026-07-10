import Mathlib.Algebra.LinearRecurrence
import Mathlib.NumberTheory.Divisors
import Mathlib.NumberTheory.EllipticDivisibilitySequence
import Mathlib.NumberTheory.LucasLehmer
import Mathlib.NumberTheory.LucasPrimality
import Mathlib.NumberTheory.Multiplicity
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.NumberTheory.Padics.PadicVal.Basic

/-!
# S1-M-018 / THM-M-0405: Bilu theorem repair artifact

Stage1 theorem-internal artifact for the item recorded as "Bilu theorem" on
prime factors of linear recurrence sequences.

The source title is still ambiguous at the public-planning level.  The strongest
candidate identified by the prior private audit is the Bilu-Hanrot-Voutier
primitive-divisor theorem for Lucas and Lehmer numbers: for `n > 30`, the
`n`-th Lucas or Lehmer number has a primitive divisor, with a classified finite
exception table for smaller indices.

The current repo-local Lean dependency closure has useful `LinearRecurrence`
and divisor APIs, but no terminal BHV theorem.  This file therefore records a
kernel-checkable statement shape and local object-model probes only.  It does
not introduce a proof placeholder for the full theorem.
-/

namespace AwesomeTheorems.Stage1.S1_M_018

universe u

/--
A prime `p` is primitive at index `n` for an integer sequence `u` when it divides
the absolute value of `u n` and divides no earlier positive-index term.

The exact Lucas/Lehmer source definition may exclude additional factors coming
from the branch-specific denominator or discriminant; those exclusions are
handled by `IsPrimitivePrimeDivisorAwayFrom`.
-/
def IsPrimitivePrimeDivisor (u : Nat -> Int) (p n : Nat) : Prop :=
  p.Prime
    ∧ p ∣ Int.natAbs (u n)
    ∧ ∀ m : Nat, 0 < m -> m < n -> ¬ p ∣ Int.natAbs (u m)

/--
Primitive-divisor predicate with a finite set of source-normalization factors
that the selected Lucas or Lehmer branch requires the primitive prime to avoid.
-/
def IsPrimitivePrimeDivisorAwayFrom
    (u : Nat -> Int) (excluded : Finset Nat) (p n : Nat) : Prop :=
  IsPrimitivePrimeDivisor u p n ∧ ∀ b : Nat, b ∈ excluded -> ¬ p ∣ b

/--
Integer-parameter Lucas sequence attached to a pair of source invariants
`P = alpha + beta` and `Q = alpha * beta`.

This recurrence-only encoding is deliberately weaker than the full
algebraic-integer Lucas-pair definition in BHV.  It is the repo-local object
model needed for the Lucas child branch, not a proof of primitive-divisor
existence.
-/
def lucasSequence (P Q : Int) : Nat -> Int
  | 0 => 0
  | 1 => 1
  | n + 2 => P * lucasSequence P Q (n + 1) - Q * lucasSequence P Q n

/-- Source-side integer invariants for the Lucas branch of the likely BHV target. -/
structure LucasPairData where
  P : Int
  Q : Int
  coprime_sum_product : Nat.Coprime (Int.natAbs P) (Int.natAbs Q)
  nonzero_sum : P ≠ 0
  nonzero_product : Q ≠ 0
  nonzero_discriminant : P ^ 2 - 4 * Q ≠ 0
  ratio_not_root_of_unity : Prop

namespace LucasPairData

/-- Discriminant `(alpha - beta)^2 = P^2 - 4Q` for the integer Lucas branch. -/
def discriminant (L : LucasPairData) : Int :=
  L.P ^ 2 - 4 * L.Q

/-- The associated Lucas sequence term `U_n(P,Q)`. -/
def term (L : LucasPairData) (n : Nat) : Int :=
  lucasSequence L.P L.Q n

/-- Source-normalization factors excluded from primitive divisors in this branch. -/
def primitiveExcludedFactors (L : LucasPairData) : Finset Nat :=
  {Int.natAbs L.discriminant}

/--
Lucas-branch primitive prime divisor: a prime divisor of `U_n(P,Q)` that divides
no earlier positive-index term and avoids the discriminant factor.
-/
def IsPrimitivePrimeDivisor (L : LucasPairData) (p n : Nat) : Prop :=
  IsPrimitivePrimeDivisorAwayFrom L.term L.primitiveExcludedFactors p n

/-- Lucas branch statement shape for the `n > 30` side of BHV. -/
def BranchPrimitiveDivisorStatement (L : LucasPairData) : Prop :=
  ∀ n : Nat, 30 < n -> ∃ p : Nat, L.IsPrimitivePrimeDivisor p n

theorem primitive_from_away
    {L : LucasPairData} {p n : Nat}
    (h : L.IsPrimitivePrimeDivisor p n) :
    S1_M_018.IsPrimitivePrimeDivisor L.term p n :=
  h.1

theorem primitive_avoids_discriminant
    {L : LucasPairData} {p n : Nat}
    (h : L.IsPrimitivePrimeDivisor p n) :
    ¬ p ∣ Int.natAbs L.discriminant := by
  exact h.2 (Int.natAbs L.discriminant) (by simp [primitiveExcludedFactors])

theorem term_zero (L : LucasPairData) :
    L.term 0 = 0 := by
  rfl

theorem term_one (L : LucasPairData) :
    L.term 1 = 1 := by
  rfl

theorem term_succ_succ (L : LucasPairData) (n : Nat) :
    L.term (n + 2) = L.P * L.term (n + 1) - L.Q * L.term n := by
  rfl

end LucasPairData

/--
Fibonacci toy branch encoded as the Lucas recurrence with `P = 1` and `Q = -1`.

This is only a low-index special-case wrapper for the Stage1 repair artifact.
It is not evidence for the `n > 30` BHV primitive-divisor theorem.
-/
def fibonacciToyTerm : Nat -> Int :=
  lucasSequence 1 (-1)

/-- The Fibonacci toy term at index `0`. -/
theorem fibonacciToyTerm_zero :
    fibonacciToyTerm 0 = 0 := by
  rfl

/-- The Fibonacci toy term at index `1`. -/
theorem fibonacciToyTerm_one :
    fibonacciToyTerm 1 = 1 := by
  rfl

/-- The Fibonacci toy term at index `2`. -/
theorem fibonacciToyTerm_two :
    fibonacciToyTerm 2 = 1 := by
  norm_num [fibonacciToyTerm, lucasSequence]

/-- The Fibonacci toy term at index `3`. -/
theorem fibonacciToyTerm_three :
    fibonacciToyTerm 3 = 2 := by
  norm_num [fibonacciToyTerm, lucasSequence]

/-- A concrete Lucas-pair package for the Fibonacci toy branch. -/
def fibonacciToyLucasPair : LucasPairData where
  P := 1
  Q := -1
  coprime_sum_product := by norm_num
  nonzero_sum := by norm_num
  nonzero_product := by norm_num
  nonzero_discriminant := by norm_num
  ratio_not_root_of_unity := True

/-- In the Fibonacci toy branch, `2` is primitive for the third term. -/
theorem fibonacciToyPrimitiveDivisorAtThree :
    IsPrimitivePrimeDivisor fibonacciToyTerm 2 3 := by
  constructor
  · exact Nat.prime_two
  constructor
  · norm_num [fibonacciToyTerm, lucasSequence]
  · intro m hm hlt hdiv
    interval_cases m <;> norm_num [fibonacciToyTerm, lucasSequence] at hdiv

/--
The same low-index fact through the concrete Lucas-pair primitive-divisor
predicate, including the branch-specific discriminant exclusion.
-/
theorem fibonacciToyLucasPair_primitiveAtThree :
    fibonacciToyLucasPair.IsPrimitivePrimeDivisor 2 3 := by
  constructor
  · simpa [fibonacciToyTerm, fibonacciToyLucasPair, LucasPairData.term]
      using fibonacciToyPrimitiveDivisorAtThree
  · intro b hb hdiv
    have hb5 : b = 5 := by
      simpa [fibonacciToyLucasPair, LucasPairData.primitiveExcludedFactors,
        LucasPairData.discriminant] using hb
    subst b
    norm_num at hdiv

/-- Statement shape for the checked Fibonacci toy special case. -/
def FibonacciToySpecialCaseStatement : Prop :=
  ∃ p : Nat, fibonacciToyLucasPair.IsPrimitivePrimeDivisor p 3

/-- Checked wrapper for the selected Fibonacci/Lucas toy branch. -/
theorem fibonacciToySpecialCaseWrapper :
    FibonacciToySpecialCaseStatement := by
  exact ⟨2, fibonacciToyLucasPair_primitiveAtThree⟩

/-- Denominator branch in the source definition of Lehmer numbers. -/
inductive LehmerDenominatorBranch where
  | oddDifference
  | evenSquaredDifference
  deriving DecidableEq, Repr

namespace LehmerDenominatorBranch

/--
Parity-sensitive denominator choice for Lehmer numbers.

For odd `n`, the source denominator is `alpha - beta`; for even `n`, it is
`alpha^2 - beta^2`.  The zero index is sent to the even branch only because it
is even; BHV primitive-divisor statements use positive indices.
-/
def forIndex (n : Nat) : LehmerDenominatorBranch :=
  if n % 2 = 0 then .evenSquaredDifference else .oddDifference

theorem forIndex_of_mod_eq_zero {n : Nat} (h : n % 2 = 0) :
    forIndex n = .evenSquaredDifference := by
  simp [forIndex, h]

theorem forIndex_of_mod_ne_zero {n : Nat} (h : n % 2 ≠ 0) :
    forIndex n = .oddDifference := by
  simp [forIndex, h]

end LehmerDenominatorBranch

/--
Source-side integer invariants and parity-sensitive term data for the Lehmer
branch of the likely BHV target.

The fields `sumSquare` and `product` stand for `(alpha + beta)^2` and
`alpha * beta`.  The actual algebraic-integer pair and quotient integrality
proofs are deliberately not asserted here; `oddQuotientTerm` and
`evenQuotientTerm` are the integer terms after the corresponding source
denominator has been applied.
-/
structure LehmerPairData where
  sumSquare : Int
  product : Int
  coprime_sumSquare_product : Nat.Coprime (Int.natAbs sumSquare) (Int.natAbs product)
  nonzero_sumSquare : sumSquare ≠ 0
  nonzero_product : product ≠ 0
  nonzero_discriminant : sumSquare - 4 * product ≠ 0
  ratio_not_root_of_unity : Prop
  oddQuotientTerm : Nat -> Int
  evenQuotientTerm : Nat -> Int

namespace LehmerPairData

/-- Squared difference `(alpha - beta)^2 = (alpha + beta)^2 - 4 alpha beta`. -/
def discriminant (L : LehmerPairData) : Int :=
  L.sumSquare - 4 * L.product

/--
Squared even-branch denominator
`(alpha^2 - beta^2)^2 = (alpha + beta)^2 * (alpha - beta)^2`.
-/
def squaredEvenDenominator (L : LehmerPairData) : Int :=
  L.sumSquare * L.discriminant

/--
The associated Lehmer sequence term using the source parity split:
odd indices use the quotient by `alpha - beta`, and even indices use the
quotient by `alpha^2 - beta^2`.
-/
def term (L : LehmerPairData) (n : Nat) : Int :=
  match LehmerDenominatorBranch.forIndex n with
  | .oddDifference => L.oddQuotientTerm n
  | .evenSquaredDifference => L.evenQuotientTerm n

/-- Source-normalization factor excluded from primitive divisors in this branch. -/
def primitiveExcludedFactors (L : LehmerPairData) : Finset Nat :=
  {Int.natAbs L.squaredEvenDenominator}

/--
Lehmer-branch primitive prime divisor: a prime divisor of the parity-sensitive
Lehmer term that divides no earlier positive-index term and avoids
`(alpha^2 - beta^2)^2`.
-/
def IsPrimitivePrimeDivisor (L : LehmerPairData) (p n : Nat) : Prop :=
  IsPrimitivePrimeDivisorAwayFrom L.term L.primitiveExcludedFactors p n

/-- Lehmer branch statement shape for the `n > 30` side of BHV. -/
def BranchPrimitiveDivisorStatement (L : LehmerPairData) : Prop :=
  ∀ n : Nat, 30 < n -> ∃ p : Nat, L.IsPrimitivePrimeDivisor p n

theorem primitive_from_away
    {L : LehmerPairData} {p n : Nat}
    (h : L.IsPrimitivePrimeDivisor p n) :
    S1_M_018.IsPrimitivePrimeDivisor L.term p n :=
  h.1

theorem primitive_avoids_squaredEvenDenominator
    {L : LehmerPairData} {p n : Nat}
    (h : L.IsPrimitivePrimeDivisor p n) :
    ¬ p ∣ Int.natAbs L.squaredEvenDenominator := by
  exact h.2 (Int.natAbs L.squaredEvenDenominator) (by simp [primitiveExcludedFactors])

theorem term_of_even_mod {L : LehmerPairData} {n : Nat} (h : n % 2 = 0) :
    L.term n = L.evenQuotientTerm n := by
  simp [term, LehmerDenominatorBranch.forIndex_of_mod_eq_zero h]

theorem term_of_odd_mod {L : LehmerPairData} {n : Nat} (h : n % 2 ≠ 0) :
    L.term n = L.oddQuotientTerm n := by
  simp [term, LehmerDenominatorBranch.forIndex_of_mod_ne_zero h]

end LehmerPairData

/--
Abstract source boundary for a future precise Lucas/Lehmer formalization.

`Pair` is intentionally abstract because the final source disambiguation must
choose between a concrete algebraic-integer Lucas-pair encoding, a Lehmer-pair
encoding with parity-sensitive denominators, or a narrower 1995 predecessor.
The fields below force the future replacement to supply the sequence, branch
predicate, source hypotheses, and excluded factors explicitly.
-/
structure PrimitiveDivisorContext where
  Pair : Type u
  term : Pair -> Nat -> Int
  excludedFactors : Pair -> Nat -> Finset Nat
  IsLucasPair : Pair -> Prop
  IsLehmerPair : Pair -> Prop
  SourceHypotheses : Pair -> Prop

/-- The source branch package expected by the BHV-style theorem. -/
def SourceBranchHypotheses (C : PrimitiveDivisorContext.{u}) (P : C.Pair) :
    Prop :=
  C.SourceHypotheses P ∧ (C.IsLucasPair P ∨ C.IsLehmerPair P)

/-- The BHV-style primitive-divisor conclusion at index `n`. -/
def PrimitiveDivisorConclusion (C : PrimitiveDivisorContext.{u})
    (P : C.Pair) (n : Nat) : Prop :=
  ∃ p : Nat,
    IsPrimitivePrimeDivisorAwayFrom
      (C.term P) (C.excludedFactors P n) p n

/--
Adapter from the concrete Lucas branch into the abstract primitive-divisor
context used by the public statement-shape wrapper.
-/
def lucasPrimitiveDivisorContext : PrimitiveDivisorContext where
  Pair := LucasPairData
  term := LucasPairData.term
  excludedFactors := fun L _ => L.primitiveExcludedFactors
  IsLucasPair := fun _ => True
  IsLehmerPair := fun _ => False
  SourceHypotheses := fun L => L.ratio_not_root_of_unity

/-- The abstract context conclusion unfolds to the concrete Lucas predicate. -/
theorem lucasPrimitiveDivisorConclusion_iff
    (L : LucasPairData) (n : Nat) :
    PrimitiveDivisorConclusion lucasPrimitiveDivisorContext L n ↔
      ∃ p : Nat, L.IsPrimitivePrimeDivisor p n := by
  rfl

/--
Adapter from the concrete Lehmer branch into the abstract primitive-divisor
context used by the public statement-shape wrapper.
-/
def lehmerPrimitiveDivisorContext : PrimitiveDivisorContext where
  Pair := LehmerPairData
  term := LehmerPairData.term
  excludedFactors := fun L _ => L.primitiveExcludedFactors
  IsLucasPair := fun _ => False
  IsLehmerPair := fun _ => True
  SourceHypotheses := fun L => L.ratio_not_root_of_unity

/-- The abstract context conclusion unfolds to the concrete Lehmer predicate. -/
theorem lehmerPrimitiveDivisorConclusion_iff
    (L : LehmerPairData) (n : Nat) :
    PrimitiveDivisorConclusion lehmerPrimitiveDivisorContext L n ↔
      ∃ p : Nat, L.IsPrimitivePrimeDivisor p n := by
  rfl

/-- Status boundary for `THM-M-0405.lucas_branch_partial`. -/
def lucasBranchPartialStatus : String :=
  "repo-local checked Lucas recurrence and primitive-divisor predicate only; no BHV existence proof"

/-- Status boundary for `THM-M-0405.lehmer_branch_partial`. -/
def lehmerBranchPartialStatus : String :=
  "repo-local checked Lehmer parity split and primitive-divisor predicate only; no BHV existence proof"

/-- Status boundary for `THM-M-0405.special_case_wrapper`. -/
def specialCaseWrapperStatus : String :=
  "repo-local checked Fibonacci/Lucas toy case: 2 is primitive at index 3; no BHV n > 30 existence proof"

/--
Public statement-shape wrapper for the BHV-style primitive-divisor target.

The carrier, Lucas/Lehmer branch predicates, source hypotheses, and conclusion
predicate are explicit parameters.  The first hypothesis ties the supplied
conclusion predicate to the primitive-divisor conclusion used by this local
artifact; the remaining conclusion is the expected `n > 30` theorem shape.
-/
def PublicStatementShape
    (Pair : Type u)
    (term : Pair -> Nat -> Int)
    (excludedFactors : Pair -> Nat -> Finset Nat)
    (IsLucasPair IsLehmerPair SourceHypotheses : Pair -> Prop)
    (Conclusion : Pair -> Nat -> Prop) : Prop :=
  (∀ (P : Pair) (n : Nat),
      Conclusion P n ↔
        ∃ p : Nat,
          IsPrimitivePrimeDivisorAwayFrom
            (term P) (excludedFactors P n) p n) ->
    ∀ (P : Pair) (n : Nat),
      SourceHypotheses P ->
        (IsLucasPair P ∨ IsLehmerPair P) ->
          30 < n ->
            Conclusion P n

/--
Normalized statement shape for the likely BHV target.

This is a `Prop` boundary, not a proof claim.  A future integrator must replace
`PrimitiveDivisorContext` by the exact Lucas/Lehmer algebraic-number-theory
objects and must discharge the source hypotheses from the primary paper.
-/
def StatementShape : Prop :=
  ∀ C : PrimitiveDivisorContext.{u},
    PublicStatementShape
      C.Pair
      C.term
      C.excludedFactors
      C.IsLucasPair
      C.IsLehmerPair
      C.SourceHypotheses
      (PrimitiveDivisorConclusion C)

/--
The public wrapper specializes back to the original `PrimitiveDivisorContext`
statement boundary by unfolding the local conclusion predicate.
-/
theorem publicStatementShape_from_context
    (C : PrimitiveDivisorContext.{u})
    (h :
      ∀ (P : C.Pair) (n : Nat),
        SourceBranchHypotheses C P ->
          30 < n ->
            PrimitiveDivisorConclusion C P n) :
    PublicStatementShape
      C.Pair
      C.term
      C.excludedFactors
      C.IsLucasPair
      C.IsLehmerPair
      C.SourceHypotheses
      (PrimitiveDivisorConclusion C) := by
  intro _ P n hSource hBranch hn
  exact h P n ⟨hSource, hBranch⟩ hn

/--
A generic linear-recurrence partial statement shape.  It is useful as a
mathlib object-model boundary, but it is weaker than the BHV Lucas/Lehmer
statement and must not be counted as the terminal theorem.
-/
def GenericLinearRecurrencePrimitiveDivisorShape : Prop :=
  ∀ (R : Type u) [CommRing R] (E : LinearRecurrence R)
    (uR : Nat -> R) (uZ : Nat -> Int) (n : Nat),
    E.IsSolution uR ->
    30 < n ->
    (∃ p : Nat, IsPrimitivePrimeDivisor uZ p n) ->
    ∃ p : Nat, IsPrimitivePrimeDivisor uZ p n

/--
Checked wrapper around mathlib's `LinearRecurrence.IsSolution` type.  This only
confirms the object model is available in the local dependency closure.
-/
theorem genericLinearRecurrencePrimitiveDivisorShape_checked :
    GenericLinearRecurrencePrimitiveDivisorShape.{u} := by
  intro R _ E uR uZ n _ _ hprimitive
  exact hprimitive

/-- Exact pinned mathlib revision audited for this Stage1 artifact. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Classification for exact mathlib anchors at the pinned revision. -/
inductive MathlibAnchorKind where
  | positiveSubstrate
  | nearbyNonTarget
  | terminalSearchMiss
  deriving DecidableEq, Repr

/-- One exact module/declaration audit row for the pinned mathlib checkout. -/
structure MathlibAnchorAuditRow where
  moduleName : String
  declarationName : String
  kind : MathlibAnchorKind
  role : String
  deriving Repr

/--
Exact pinned mathlib modules and declaration names audited for this Stage1 slot.

Rows marked `positiveSubstrate` are usable object-model anchors.  Rows marked
`nearbyNonTarget` compile in mathlib but prove a different theorem family.
There is no row for a terminal BHV primitive-divisor theorem because the pinned
checkout has no such declaration.
-/
def mathlibAnchorAuditRows : List MathlibAnchorAuditRow := [
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence"
    kind := .positiveSubstrate
    role := "linear recurrence object model"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.IsSolution"
    kind := .positiveSubstrate
    role := "recurrence solution predicate"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.mkSol"
    kind := .positiveSubstrate
    role := "solution generated from initial values"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.is_sol_mkSol"
    kind := .positiveSubstrate
    role := "generated solution satisfies recurrence"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.eq_mk_of_is_sol_of_eq_init"
    kind := .positiveSubstrate
    role := "solution uniqueness from initial segment"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.solSpace"
    kind := .positiveSubstrate
    role := "solution submodule"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.tupleSucc"
    kind := .positiveSubstrate
    role := "companion-style shift operator"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.charPoly"
    kind := .positiveSubstrate
    role := "characteristic polynomial for a recurrence"
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence"
    declarationName := "LinearRecurrence.geom_sol_iff_root_charPoly"
    kind := .positiveSubstrate
    role := "geometric solutions versus characteristic roots"
  },
  {
    moduleName := "Mathlib.NumberTheory.Divisors"
    declarationName := "Nat.divisors"
    kind := .positiveSubstrate
    role := "finite divisor set for primitive-divisor predicates"
  },
  {
    moduleName := "Mathlib.NumberTheory.Divisors"
    declarationName := "Nat.properDivisors"
    kind := .positiveSubstrate
    role := "proper divisor set for earlier-factor bookkeeping"
  },
  {
    moduleName := "Mathlib.NumberTheory.Divisors"
    declarationName := "Nat.mem_divisors"
    kind := .positiveSubstrate
    role := "membership-to-divisibility bridge"
  },
  {
    moduleName := "Mathlib.NumberTheory.Divisors"
    declarationName := "Nat.primeFactors_eq_to_filter_divisors_prime"
    kind := .positiveSubstrate
    role := "prime factors as filtered divisors"
  },
  {
    moduleName := "Mathlib.NumberTheory.Multiplicity"
    declarationName := "Int.emultiplicity_pow_sub_pow"
    kind := .positiveSubstrate
    role := "integer lifting-the-exponent style valuation lemma"
  },
  {
    moduleName := "Mathlib.NumberTheory.Multiplicity"
    declarationName := "Nat.emultiplicity_pow_sub_pow"
    kind := .positiveSubstrate
    role := "natural-number lifting-the-exponent style valuation lemma"
  },
  {
    moduleName := "Mathlib.NumberTheory.Padics.PadicVal.Basic"
    declarationName := "padicValNat"
    kind := .positiveSubstrate
    role := "natural p-adic valuation"
  },
  {
    moduleName := "Mathlib.NumberTheory.Padics.PadicVal.Basic"
    declarationName := "padicValInt"
    kind := .positiveSubstrate
    role := "integer p-adic valuation"
  },
  {
    moduleName := "Mathlib.NumberTheory.Padics.PadicVal.Basic"
    declarationName := "padicValRat"
    kind := .positiveSubstrate
    role := "rational p-adic valuation"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.Basic"
    declarationName := "NumberField"
    kind := .positiveSubstrate
    role := "number-field carrier predicate"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.Basic"
    declarationName := "NumberField.RingOfIntegers"
    kind := .positiveSubstrate
    role := "ring of integers for Lucas/Lehmer algebraic integers"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.ClassNumber"
    declarationName := "NumberField.classNumber"
    kind := .positiveSubstrate
    role := "class-number API for possible ideal-class reductions"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.ClassNumber"
    declarationName := "NumberField.classNumber_eq_one_iff"
    kind := .positiveSubstrate
    role := "principal ideal ring bridge at class number one"
  },
  {
    moduleName := "Mathlib.NumberTheory.EllipticDivisibilitySequence"
    declarationName := "IsEllSequence"
    kind := .positiveSubstrate
    role := "divisibility-sequence substrate, not BHV by itself"
  },
  {
    moduleName := "Mathlib.NumberTheory.EllipticDivisibilitySequence"
    declarationName := "IsDivSequence"
    kind := .positiveSubstrate
    role := "abstract divisibility-sequence predicate"
  },
  {
    moduleName := "Mathlib.NumberTheory.EllipticDivisibilitySequence"
    declarationName := "IsEllDivSequence"
    kind := .positiveSubstrate
    role := "elliptic divisibility sequence predicate"
  },
  {
    moduleName := "Mathlib.NumberTheory.EllipticDivisibilitySequence"
    declarationName := "isEllDivSequence_id"
    kind := .positiveSubstrate
    role := "minimal checked EDS example"
  },
  {
    moduleName := "Mathlib.NumberTheory.LucasLehmer"
    declarationName := "LucasLehmer.LucasLehmerTest"
    kind := .nearbyNonTarget
    role := "Lucas-Lehmer primality-test predicate for Mersenne primes"
  },
  {
    moduleName := "Mathlib.NumberTheory.LucasLehmer"
    declarationName := "LucasLehmer.lucasLehmerResidue"
    kind := .nearbyNonTarget
    role := "Lucas-Lehmer residue sequence for the primality test"
  },
  {
    moduleName := "Mathlib.NumberTheory.LucasLehmer"
    declarationName := "lucas_lehmer_sufficiency"
    kind := .nearbyNonTarget
    role := "sufficiency direction for Mersenne primality, not primitive divisors"
  },
  {
    moduleName := "Mathlib.NumberTheory.LucasPrimality"
    declarationName := "lucas_primality"
    kind := .nearbyNonTarget
    role := "Lucas primality test, not Lucas/Lehmer primitive-divisor theorem"
  },
  {
    moduleName := "Mathlib.NumberTheory.LucasPrimality"
    declarationName := "reverse_lucas_primality"
    kind := .nearbyNonTarget
    role := "converse Lucas primality certificate"
  },
  {
    moduleName := "Mathlib.NumberTheory.LucasPrimality"
    declarationName := "lucas_primality_iff"
    kind := .nearbyNonTarget
    role := "iff form of Lucas primality test"
  }
]

/-- Negative terminal mathlib search result at the pinned revision. -/
def mathlibTerminalSearchMisses : List String := [
  "no declaration or namespace matching Bilu",
  "no declaration or namespace matching BHV",
  "no declaration or namespace matching Hanrot",
  "no declaration or namespace matching Voutier",
  "no declaration or namespace matching Zsigmondy",
  "no terminal Lucas/Lehmer primitive-divisor theorem",
  "no declaration matching PrimitiveDivisor outside this Stage1 artifact"
]

/--
Legacy compact export of the exact declaration names from
`mathlibAnchorAuditRows`.  Prefer the structured audit table above for public
backfill.
-/
def mathlibAnchorNames : List String :=
  mathlibAnchorAuditRows.map (fun row => row.declarationName)

/-- Public status boundary for the mathlib anchor audit child. -/
def mathlibAnchorAuditStatus : String :=
  "partial_object_model_only: no pinned mathlib terminal BHV primitive-divisor theorem"

/-- External Lean-search surfaces audited for the BHV child task. -/
inductive ExternalLeanAuditSurface where
  | githubCliAuth
  | githubRestCodeSearch
  | githubRestRepositorySearch
  | reservoirStaticPackageList
  | loogleMathlibSearch
  | webSearch
  deriving DecidableEq, Repr

/-- One external Lean-search audit row. -/
structure ExternalLeanAuditRow where
  surface : ExternalLeanAuditSurface
  query : String
  result : String
  integrationImpact : String
  deriving Repr

/-- Date of the repeated external Lean audit for `THM-M-0405.external_lean_audit`. -/
def externalLeanAuditDate : String :=
  "2026-05-01"

/--
Repeated GitHub / Reservoir / Lean-search audit for external BHV formalization
anchors.

No row below is a proof claim.  Rows either record concrete negative search
results or an access blocker that prevents treating GitHub code search as
complete in this runtime.
-/
def externalLeanAuditRows : List ExternalLeanAuditRow := [
  {
    surface := .githubCliAuth
    query := "gh auth status; GH_TOKEN/GITHUB_TOKEN presence check"
    result := "gh reports no authenticated GitHub host; no GH_TOKEN or GITHUB_TOKEN is present"
    integrationImpact := "authenticated GitHub code search is blocked until credentials are supplied"
  },
  {
    surface := .githubRestCodeSearch
    query := "\"Bilu\" \"Hanrot\" \"Voutier\" language:Lean"
    result := "GitHub REST code search returned API rate-limit/access failure for unauthenticated runtime"
    integrationImpact := "not completion evidence; rerun with authenticated GitHub code search before public closure"
  },
  {
    surface := .githubRestRepositorySearch
    query := "\"Zsigmondy\" Lean"
    result := "repository search returned total_count = 0"
    integrationImpact := "no repository-level external Lean proof anchor identified"
  },
  {
    surface := .githubRestRepositorySearch
    query := "\"LucasLehmer\" Lean"
    result := "repository search returned total_count = 0"
    integrationImpact := "no repository-level external BHV anchor identified; mathlib LucasLehmer remains a non-target"
  },
  {
    surface := .githubRestRepositorySearch
    query := "\"primitive divisor\" Lean"
    result := "repository search returned total_count = 0"
    integrationImpact := "no repository-level primitive-divisor Lean project identified"
  },
  {
    surface := .reservoirStaticPackageList
    query := "Bilu|Hanrot|Voutier|primitive divisor|Zsigmondy|Lucas|Lehmer|BHV"
    result := "Reservoir package-list module dated 2026-04-29 had no matching package object"
    integrationImpact := "no Reservoir package candidate to pin/import/check"
  },
  {
    surface := .loogleMathlibSearch
    query := "\"Bilu\""
    result := "0 declarations"
    integrationImpact := "no mathlib declaration-name anchor"
  },
  {
    surface := .loogleMathlibSearch
    query := "\"Hanrot\""
    result := "0 declarations"
    integrationImpact := "no mathlib declaration-name anchor"
  },
  {
    surface := .loogleMathlibSearch
    query := "\"Voutier\""
    result := "0 declarations"
    integrationImpact := "no mathlib declaration-name anchor"
  },
  {
    surface := .loogleMathlibSearch
    query := "\"Zsigmondy\""
    result := "0 declarations"
    integrationImpact := "no mathlib declaration-name anchor"
  },
  {
    surface := .loogleMathlibSearch
    query := "\"primitive divisor\""
    result := "0 declarations"
    integrationImpact := "no primitive-divisor declaration-name anchor"
  },
  {
    surface := .loogleMathlibSearch
    query := "\"LucasLehmer\" / \"Lehmer\""
    result := "positive hits are Mathlib.NumberTheory.LucasLehmer declarations for Mersenne primality testing"
    integrationImpact := "nearby non-target only; not a BHV primitive-divisor theorem"
  },
  {
    surface := .webSearch
    query := "site:github.com Lean Bilu Hanrot Voutier; primitive divisor Lucas Lehmer; Zsigmondy"
    result := "no primary public Lean 4 project with a closed BHV primitive-divisor theorem identified"
    integrationImpact := "terminal status remains not_repo_local_closed / formalization_debt"
  }
]

/-- Compact status boundary for the external Lean audit child. -/
def externalLeanAuditStatus : String :=
  "blocked-negative: no external Lean BHV proof identified; authenticated GitHub code search needs credentials"

/-- Source-disambiguation buckets for the public "Bilu theorem" title. -/
inductive SourceDisambiguationResult where
  | bhvPreferred
  | voutier1995Predecessor
  | anotherBiluTheorem
  deriving DecidableEq, Repr

/--
Current repo-local source-disambiguation result for `THM-M-0405`.

The preferred target is the Bilu-Hanrot-Voutier primitive-divisor theorem for
Lucas and Lehmer numbers, not the 1995 Voutier predecessor by itself.
-/
def sourceDisambiguationResult : SourceDisambiguationResult :=
  .bhvPreferred

/--
Audit notes backing the source-disambiguation result.

These strings are metadata only: they do not claim a proof of the terminal
primitive-divisor theorem.
-/
def sourceDisambiguationEvidence : List String := [
  "preferred_target: Bilu-Hanrot-Voutier, Existence of primitive divisors of Lucas and Lehmer numbers, J. reine angew. Math. 539 (2001), 75-122",
  "source_statement: for n > 30, every n-th Lucas and Lehmer number has a primitive divisor, with all defective terms listed",
  "preprint_record: 1999 report, 41 pages, with keywords linear recurrence sequence, diophantine equations, Thue equations, and linear form in logarithms",
  "predecessor_1995: Paul M. Voutier, Primitive divisors of Lucas and Lehmer sequences, Math. Comp. 64 (1995), 869-888; this handles n <= 30 and conjectures the n > 30 theorem",
  "not_other_1995_Bilu: Bilu's publication list records a 1995 integral-points article, not a Bilu-authored linear-recurrence prime-factor theorem"
]

/-- Public merge gate for this child source-disambiguation result. -/
def sourceDisambiguationPublicGate : String :=
  "integration-ready: public docs should name BHV as the preferred target; no theorem completion is claimed"

/--
Package lanes for the public phrase "arithmetic-dynamics or Diophantine package
split".

The current source-disambiguation points to the Diophantine BHV primitive-
divisor theorem.  The arithmetic-dynamics lane is kept only as an explicit
non-target unless a later public source audit identifies a different Bilu
theorem.
-/
inductive PackageLane where
  | sourceDisambiguation
  | diophantineLucasLehmer
  | algebraicNumberTheoryBridge
  | thueAndLogForms
  | finiteExceptionClassification
  | arithmeticDynamicsNonTarget
  | repoLocalIntegrationGate
  deriving DecidableEq, Repr

/-- A compact, kernel-checkable description of one proof-package leaf. -/
structure ProofPackage where
  code : String
  lane : PackageLane
  stablePublicName : String
  localRole : String
  requiredInputs : List String
  downstreamOutput : String
  closureState : String
  deriving Repr

/--
Integration-ready package split for `THM-M-0405`.

These are not proof claims.  They are stable child leaves that a public
integrator can merge into the Stage1 blueprint after serial review.
-/
def biluPackageSplit : List ProofPackage := [
  {
    code := "THM-M-0405.P01"
    lane := .sourceDisambiguation
    stablePublicName := "source_disambiguation_BHV"
    localRole := "Fix the public target as BHV primitive divisors for Lucas and Lehmer numbers unless a primary source contradicts it."
    requiredInputs := [
      "Bilu-Hanrot-Voutier 2001 J. reine angew. Math. statement",
      "Voutier 1995 predecessor boundary",
      "Stage1 public title line"
    ]
    downstreamOutput := "canonical theorem name and no-completion status boundary"
    closureState := "integration-ready, not theorem-complete"
  },
  {
    code := "THM-M-0405.P02"
    lane := .diophantineLucasLehmer
    stablePublicName := "lucas_pair_statement_shape"
    localRole := "Replace the abstract `PrimitiveDivisorContext` with Lucas-pair data, recurrence terms, and primitive-divisor exclusions."
    requiredInputs := [
      "algebraic integer pair",
      "nonzero coprime integer invariants",
      "ratio not a root of unity",
      "Lucas sequence term formula"
    ]
    downstreamOutput := "Lucas branch theorem wrapper for n > 30"
    closureState := "open formalization_debt"
  },
  {
    code := "THM-M-0405.P03"
    lane := .diophantineLucasLehmer
    stablePublicName := "lehmer_pair_statement_shape"
    localRole := "Add the parity-sensitive Lehmer term denominator and primitive-divisor exclusions."
    requiredInputs := [
      "Lehmer pair hypotheses",
      "odd/even term formula split",
      "squared discriminant exclusion",
      "earlier-term product exclusion"
    ]
    downstreamOutput := "Lehmer branch theorem wrapper for n > 30"
    closureState := "open formalization_debt"
  },
  {
    code := "THM-M-0405.P04"
    lane := .algebraicNumberTheoryBridge
    stablePublicName := "number_field_divisibility_bridge"
    localRole := "Connect algebraic-integer pair data to integer divisibility, valuations, and primitive prime divisors."
    requiredInputs := [
      "number field or quadratic extension encoding",
      "integrality and coprimality APIs",
      "Nat.Prime / Int.natAbs divisibility bridge"
    ]
    downstreamOutput := "usable primitive-divisor predicate for both branches"
    closureState := "open formalization_debt"
  },
  {
    code := "THM-M-0405.P05"
    lane := .thueAndLogForms
    stablePublicName := "thue_log_forms_reduction"
    localRole := "Isolate the deep Diophantine inputs used by BHV: Thue equations, linear forms in logarithms, and the finite search reduction."
    requiredInputs := [
      "Thue equation solver boundary",
      "linear forms in logarithms estimates",
      "height and cyclotomic factor estimates"
    ]
    downstreamOutput := "n > 30 primitive-divisor existence engine"
    closureState := "deep formalization_debt"
  },
  {
    code := "THM-M-0405.P06"
    lane := .finiteExceptionClassification
    stablePublicName := "defective_exception_tables"
    localRole := "Represent the classified defective Lucas and Lehmer terms for n <= 30 without using the table as evidence for n > 30."
    requiredInputs := [
      "BHV defective Lucas table",
      "BHV defective Lehmer table",
      "equivalence relation on pairs"
    ]
    downstreamOutput := "finite-exception audit and small-index public notes"
    closureState := "open formalization_debt"
  },
  {
    code := "THM-M-0405.P07"
    lane := .arithmeticDynamicsNonTarget
    stablePublicName := "arithmetic_dynamics_non_target_gate"
    localRole := "Record that dynatomic/Zsigmondy-style arithmetic dynamics is not the selected target for this Stage1 slot."
    requiredInputs := [
      "public title disambiguation",
      "BHV source audit",
      "no alternate Bilu arithmetic-dynamics theorem selected"
    ]
    downstreamOutput := "prevents mixing a different theorem family into the BHV proof tree"
    closureState := "integration-ready blocker, not a proof leaf"
  },
  {
    code := "THM-M-0405.P08"
    lane := .repoLocalIntegrationGate
    stablePublicName := "external_or_local_closure_gate"
    localRole := "Require a local proof body, mathlib wrapper, or pinned external dependency before any completed status."
    requiredInputs := [
      "repo-local Lean validation command",
      "external Lean search result",
      "placeholder-free proof inventory"
    ]
    downstreamOutput := "completion gate with no residual repo_local_integration_debt"
    closureState := "open gate; no completed status"
  }
]

/-- Human-readable decision for the arithmetic-dynamics-or-Diophantine split. -/
def packageSplitDecision : String :=
  "select Diophantine/Lucas-Lehmer BHV package split; keep arithmetic dynamics as a non-target gate until source disambiguation changes"

/--
Machine proof debt classification for this Stage1 slot.

No external Lean 4 proof has been pinned into this repository, and no local
proof body for the terminal BHV theorem is present.
-/
def machineProofDebtClassification : List String := [
  "formalization_debt: BHV/source theorem has no repo-local Lean proof body",
  "not_repo_local_closed: no pinned external Lean 4 dependency for BHV found",
  "external Lean audit 2026-05-01 found no Reservoir or Lean-search proof anchor; authenticated GitHub code search is credential-blocked",
  "repo_local_integration_debt gate not opened because no external closure was identified"
]

/-- Repo-local integration-debt gate for this repair artifact. -/
def repoLocalIntegrationDebtGate : String :=
  "no completed status: external Lean closure not identified; if found later, pin/import/check or record a concrete blocker"

/--
Public completion gate proposed by `THM-M-0405.integration_gate`.

This is intentionally a data row rather than a proof of the BHV theorem.  It
records the condition that must be merged into the public blueprint before any
future completed status is allowed.
-/
def publicIntegrationGateEntry : List String := [
  "THM-M-0405.integration_gate",
  "completed status requires repo-local validation by `lake build` or `lake env lean AwesomeTheorems/Stage1/S1_M_018.lean` after the terminal proof/wrapper is in the Lake closure",
  "if an external Lean proof is found but cannot be pinned/imported/checked, record the exact toolchain/dependency/license blocker instead of marking completed",
  "anchor-only mathlib or external evidence is not completion evidence",
  "no completed state may retain repo_local_integration_debt"
]

/-- Canonical theorem-internal child leaves for later M0387-level backfill. -/
def theoremInternalChildLeaves : List String := [
  "THM-M-0405.L001.source_disambiguation_BHV_or_predecessor",
  "THM-M-0405.L002.formal_lucas_pair_predicate",
  "THM-M-0405.L003.formal_lehmer_pair_predicate",
  "THM-M-0405.L004.primitive_divisor_predicate_lucas",
  "THM-M-0405.L005.primitive_divisor_predicate_lehmer",
  "THM-M-0405.L006.defective_pair_exception_table",
  "THM-M-0405.L007.mathlib_linear_recurrence_bridge",
  "THM-M-0405.L008.number_field_integral_closure_bridge",
  "THM-M-0405.L009.valuation_and_divisibility_bridge",
  "THM-M-0405.L010.lucas_branch_n_gt_30_wrapper",
  "THM-M-0405.L011.lehmer_branch_n_gt_30_wrapper",
  "THM-M-0405.L012.external_dependency_or_local_proof_closure_gate"
]

/-! ## Audit probes -/

#check LinearRecurrence
#check LinearRecurrence.IsSolution
#check LinearRecurrence.mkSol
#check LinearRecurrence.is_sol_mkSol
#check LinearRecurrence.eq_mk_of_is_sol_of_eq_init
#check LinearRecurrence.solSpace
#check LinearRecurrence.tupleSucc
#check LinearRecurrence.charPoly
#check LinearRecurrence.geom_sol_iff_root_charPoly
#check Nat.divisors
#check Nat.properDivisors
#check Nat.mem_divisors
#check Nat.primeFactors_eq_to_filter_divisors_prime
#check Int.emultiplicity_pow_sub_pow
#check Nat.emultiplicity_pow_sub_pow
#check padicValNat
#check padicValInt
#check padicValRat
#check NumberField
#check NumberField.RingOfIntegers
#check NumberField.classNumber
#check NumberField.classNumber_eq_one_iff
#check IsEllSequence
#check IsDivSequence
#check IsEllDivSequence
#check isEllDivSequence_id
#check LucasLehmer.LucasLehmerTest
#check LucasLehmer.lucasLehmerResidue
#check lucas_lehmer_sufficiency
#check lucas_primality
#check reverse_lucas_primality
#check lucas_primality_iff
#check IsPrimitivePrimeDivisor
#check IsPrimitivePrimeDivisorAwayFrom
#check lucasSequence
#check LucasPairData
#check LucasPairData.discriminant
#check LucasPairData.term
#check LucasPairData.primitiveExcludedFactors
#check LucasPairData.IsPrimitivePrimeDivisor
#check LucasPairData.BranchPrimitiveDivisorStatement
#check LucasPairData.primitive_from_away
#check LucasPairData.primitive_avoids_discriminant
#check LucasPairData.term_zero
#check LucasPairData.term_one
#check LucasPairData.term_succ_succ
#check fibonacciToyTerm
#check fibonacciToyTerm_zero
#check fibonacciToyTerm_one
#check fibonacciToyTerm_two
#check fibonacciToyTerm_three
#check fibonacciToyLucasPair
#check fibonacciToyPrimitiveDivisorAtThree
#check fibonacciToyLucasPair_primitiveAtThree
#check FibonacciToySpecialCaseStatement
#check fibonacciToySpecialCaseWrapper
#check LehmerDenominatorBranch
#check LehmerDenominatorBranch.forIndex
#check LehmerDenominatorBranch.forIndex_of_mod_eq_zero
#check LehmerDenominatorBranch.forIndex_of_mod_ne_zero
#check LehmerPairData
#check LehmerPairData.discriminant
#check LehmerPairData.squaredEvenDenominator
#check LehmerPairData.term
#check LehmerPairData.primitiveExcludedFactors
#check LehmerPairData.IsPrimitivePrimeDivisor
#check LehmerPairData.BranchPrimitiveDivisorStatement
#check LehmerPairData.primitive_from_away
#check LehmerPairData.primitive_avoids_squaredEvenDenominator
#check LehmerPairData.term_of_even_mod
#check LehmerPairData.term_of_odd_mod
#check lucasPrimitiveDivisorContext
#check lucasPrimitiveDivisorConclusion_iff
#check lehmerPrimitiveDivisorContext
#check lehmerPrimitiveDivisorConclusion_iff
#check lucasBranchPartialStatus
#check lehmerBranchPartialStatus
#check specialCaseWrapperStatus
#check PublicStatementShape
#check StatementShape
#check publicStatementShape_from_context
#check GenericLinearRecurrencePrimitiveDivisorShape
#check genericLinearRecurrencePrimitiveDivisorShape_checked
#check mathlibPinnedRevision
#check MathlibAnchorKind
#check MathlibAnchorAuditRow
#check mathlibAnchorAuditRows
#check mathlibTerminalSearchMisses
#check mathlibAnchorNames
#check mathlibAnchorAuditStatus
#check ExternalLeanAuditSurface
#check ExternalLeanAuditRow
#check externalLeanAuditDate
#check externalLeanAuditRows
#check externalLeanAuditStatus
#check SourceDisambiguationResult
#check sourceDisambiguationResult
#check sourceDisambiguationEvidence
#check PackageLane
#check ProofPackage
#check biluPackageSplit
#check packageSplitDecision
#check publicIntegrationGateEntry

end AwesomeTheorems.Stage1.S1_M_018
