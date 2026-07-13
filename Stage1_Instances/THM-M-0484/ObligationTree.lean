import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0484 conditional obligation composition

This module checks the exact interfaces in the frozen obligation graph. Every mathematical child
is an explicit argument. The pinned terminal declarations are inspected but are not installed as
the canonical proof in this phase.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0484.ObligationTree

open LucasLehmer

/-- Exact forward direction at the canonical lower bound. -/
def SufficiencyTarget : Prop :=
  forall p : Nat, 3 <= p -> LucasLehmerTest p -> Nat.Prime (mersenne p)

/-- Exact reverse direction at the canonical lower bound. -/
def NecessityTarget : Prop :=
  forall p : Nat, 3 <= p -> Nat.Prime (mersenne p) -> LucasLehmerTest p

/-- The order inequality used by the forward direction after writing `p = p' + 2`. -/
def OrderInequalityTarget : Prop :=
  forall p' : Nat, lucasLehmerResidue (p' + 2) = 0 ->
    2 ^ (p' + 2) < (q (p' + 2) : Nat) ^ 2

/-- The generic least-factor square estimate used when a natural number is not prime. -/
def MinFacSquareBoundTarget : Prop :=
  forall n : Nat, 1 < n -> Not n.Prime -> Nat.minFac n ^ 2 <= n

/-- Exact order of the quadratic-extension unit used by the forward direction. -/
def OmegaOrderTarget : Prop :=
  forall p' : Nat, lucasLehmerResidue (p' + 2) = 0 ->
    orderOf (LucasLehmer.ωUnit (p' + 2)) = 2 ^ (p' + 2)

/-- Strict upper bound on the number of units in the quadratic extension. -/
def UnitCardBoundTarget : Prop :=
  forall p' : Nat,
    Fintype.card (X (q (p' + 2)))ˣ < (q (p' + 2) : Nat) ^ 2

/-- Lower power boundary used to prove the exact order of `omega`. -/
def OmegaPowNegOneTarget : Prop :=
  forall p' : Nat, lucasLehmerResidue (p' + 2) = 0 ->
    (LucasLehmer.X.ω : X (q (p' + 2))) ^ 2 ^ (p' + 1) = -1

/-- Upper power boundary used to prove that the order of `omega` divides `2^(p'+2)`. -/
def OmegaPowOneTarget : Prop :=
  forall p' : Nat, lucasLehmerResidue (p' + 2) = 0 ->
    (LucasLehmer.X.ω : X (q (p' + 2))) ^ 2 ^ (p' + 2) = 1

/-- The least prime factor of the relevant Mersenne number is strictly larger than two. -/
def TwoLtQTarget : Prop :=
  forall p' : Nat, 2 < q (p' + 2)

/-- Divisibility and closed-form package immediately preceding `omega^(2^(p'+1)) = -1`. -/
def OmegaFormulaTarget : Prop :=
  forall p' : Nat, lucasLehmerResidue (p' + 2) = 0 ->
    exists k : Int,
      (LucasLehmer.X.ω : X (q (p' + 2))) ^ 2 ^ (p' + 1) =
        k * mersenne (p' + 2) * (LucasLehmer.X.ω : X (q (p' + 2))) ^ 2 ^ p' - 1

/-- The Mersenne number vanishes in the quadratic extension modulo its least factor. -/
def MersenneCoeXTarget : Prop :=
  forall p : Nat, (mersenne p : X (q p)) = 0

/-- Recurrence representation needed by the reverse direction. -/
def RecurrenceBridgeTarget : Prop :=
  forall p' i : Nat,
    sZMod (p' + 2) i = (s i : ZMod (2 ^ (p' + 2) - 1))

/-- Closed form for the Lucas-Lehmer recurrence in every quadratic extension. -/
def ClosedFormTarget : Prop :=
  forall (modulus i : Nat),
    (s i : X modulus) =
      (LucasLehmer.X.ω : X modulus) ^ 2 ^ i +
        (LucasLehmer.X.ωb : X modulus) ^ 2 ^ i

/-- Trace identity specialized to a prime Mersenne modulus. -/
def MersenneTraceTarget : Prop :=
  forall p' : Nat, 3 <= p' + 2 -> Nat.Prime (mersenne (p' + 2)) ->
    (LucasLehmer.X.ω : X (mersenne (p' + 2))) ^ 2 ^ p' +
      (LucasLehmer.X.ωb : X (mersenne (p' + 2))) ^ 2 ^ p' = 0

/-- Exact root composition from both directions. -/
theorem root_of_directions
    (sufficiency : SufficiencyTarget) (necessity : NecessityTarget) :
    Stage1Instances.THM_M_0484.LucasLehmerTestTarget := by
  intro p hp
  exact Iff.intro (sufficiency p hp) (necessity p hp)

/-- The terminal composition node delivers the exact frozen root unchanged. -/
theorem root_of_terminal
    (terminal : Stage1Instances.THM_M_0484.LucasLehmerTestTarget) :
    Stage1Instances.THM_M_0484.LucasLehmerTestTarget :=
  terminal

/-- The forward terminal consumes the complete conclusion delivered by its reconstructed branch. -/
theorem sufficiency_of_branch (branch : SufficiencyTarget) : SufficiencyTarget :=
  branch

/-- Conditional reconstruction of the forward terminal from its two mathematical engines. -/
theorem sufficiency_of_order_and_minFac
    (orderBound : OrderInequalityTarget)
    (minFacBound : MinFacSquareBoundTarget) : SufficiencyTarget := by
  intro p hp htest
  set p' := p - 2 with hp'
  clear_value p'
  obtain rfl : p = p' + 2 := by omega
  by_contra hprime
  have h1 := orderBound p' htest
  have h2 := minFacBound (mersenne (p' + 2)) (by simp) hprime
  have h2' : (q (p' + 2) : Nat) ^ 2 <= mersenne (p' + 2) := by
    simpa [q] using h2
  have h := lt_of_lt_of_le h1 h2'
  exact not_lt_of_ge (Nat.sub_le _ _) h

/-- The reverse terminal consumes the complete conclusion delivered by its reconstructed branch. -/
theorem necessity_of_branch (branch : NecessityTarget) : NecessityTarget :=
  branch

/-- Conditional reconstruction of the order inequality from exact order and cardinality bounds. -/
theorem orderInequality_of_order_and_card
    (exactOrder : OmegaOrderTarget) (cardBound : UnitCardBoundTarget) :
    OrderInequalityTarget := by
  intro p' h
  calc
    2 ^ (p' + 2) = orderOf (LucasLehmer.ωUnit (p' + 2)) := (exactOrder p' h).symm
    _ <= Fintype.card (X (q (p' + 2)))ˣ := orderOf_le_card_univ
    _ < (q (p' + 2) : Nat) ^ 2 := cardBound p'

/-- Conditional reconstruction of the exact order from both power boundaries and `2 < q`. -/
theorem omegaOrder_of_power_boundaries
    (powNegOne : OmegaPowNegOneTarget)
    (powOne : OmegaPowOneTarget)
    (twoLtQ : TwoLtQTarget) : OmegaOrderTarget := by
  intro p' h
  apply Nat.eq_prime_pow_of_dvd_least_prime_pow
  · exact Nat.prime_two
  · intro o
    have omegaPow :=
      congr_arg
        (Units.coeHom (X (q (p' + 2))) : Units (X (q (p' + 2))) -> X (q (p' + 2)))
        (orderOf_dvd_iff_pow_eq_one.1 o)
    have hone : (1 : ZMod (q (p' + 2))) = -1 :=
      congr_arg Prod.fst (omegaPow.symm.trans (powNegOne p' h))
    haveI : Fact (2 < (q (p' + 2) : Nat)) := ⟨twoLtQ p'⟩
    exact ZMod.neg_one_ne_one hone.symm
  · apply orderOf_dvd_iff_pow_eq_one.2
    apply Units.ext
    push_cast
    exact powOne p' h

/-- The lower power boundary implies the upper boundary by squaring. -/
theorem omegaPowOne_of_negOne (powNegOne : OmegaPowNegOneTarget) :
    OmegaPowOneTarget := by
  intro p' h
  calc
    (LucasLehmer.X.ω : X (q (p' + 2))) ^ 2 ^ (p' + 2) =
        ((LucasLehmer.X.ω : X (q (p' + 2))) ^ 2 ^ (p' + 1)) ^ 2 := by
      rw [← pow_mul, ← Nat.pow_succ]
    _ = (-1) ^ 2 := by rw [powNegOne p' h]
    _ = 1 := by simp

/-- The divisibility formula and vanishing Mersenne coefficient yield the lower power boundary. -/
theorem omegaPowNegOne_of_formula_and_vanishing
    (formula : OmegaFormulaTarget) (vanishing : MersenneCoeXTarget) :
    OmegaPowNegOneTarget := by
  intro p' h
  obtain ⟨k, hk⟩ := formula p' h
  rw [vanishing] at hk
  simpa using hk

/-- Conditional reconstruction of the reverse terminal from recurrence, closed form, and trace. -/
theorem necessity_of_recurrence_closedForm_trace
    (recurrence : RecurrenceBridgeTarget)
    (closedForm : ClosedFormTarget)
    (trace : MersenneTraceTarget) : NecessityTarget := by
  intro p hp hprime
  set p' := p - 2 with hp'
  clear_value p'
  obtain rfl : p = p' + 2 := by omega
  dsimp [LucasLehmerTest, lucasLehmerResidue]
  have hindex : p' + 2 - 2 = p' := by omega
  rw [hindex]
  rw [recurrence p' p', ← X.fst_intCast, closedForm]
  have htrace := trace p' hp hprime
  exact congr_arg Prod.fst htrace

#check lucas_lehmer_sufficiency
#check lucas_lehmer_necessity
#check LucasLehmer.order_ineq
#check LucasLehmer.order_ω
#check Nat.minFac_sq_le_self

assert_no_sorry root_of_directions
assert_no_sorry root_of_terminal
assert_no_sorry sufficiency_of_branch
assert_no_sorry sufficiency_of_order_and_minFac
assert_no_sorry necessity_of_branch
assert_no_sorry orderInequality_of_order_and_card
assert_no_sorry omegaOrder_of_power_boundaries
assert_no_sorry omegaPowOne_of_negOne
assert_no_sorry omegaPowNegOne_of_formula_and_vanishing
assert_no_sorry necessity_of_recurrence_closedForm_trace

#print sorries root_of_directions root_of_terminal sufficiency_of_branch
  sufficiency_of_order_and_minFac necessity_of_branch
  orderInequality_of_order_and_card omegaOrder_of_power_boundaries omegaPowOne_of_negOne
  omegaPowNegOne_of_formula_and_vanishing necessity_of_recurrence_closedForm_trace

#print axioms root_of_directions
#print axioms root_of_terminal
#print axioms sufficiency_of_branch
#print axioms sufficiency_of_order_and_minFac
#print axioms necessity_of_branch
#print axioms orderInequality_of_order_and_card
#print axioms omegaOrder_of_power_boundaries
#print axioms omegaPowOne_of_negOne
#print axioms omegaPowNegOne_of_formula_and_vanishing
#print axioms necessity_of_recurrence_closedForm_trace

end Stage1Instances.THM_M_0484.ObligationTree
