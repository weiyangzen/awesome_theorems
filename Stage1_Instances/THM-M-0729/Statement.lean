import Mathlib.Computability.TuringMachine.Computable

/-!
# THM-M-0729: the PCP theorem

This module freezes a binary, nonadaptive, perfect-completeness formulation of
`NP = PCP[O(log n), O(1)]`.  It defines the statement boundary only; it does
not prove either inclusion.
-/

namespace Stage1Instances.THM_M_0729

abbrev Word := List Bool
abbrev Language := Word -> Prop

def encodeBool (b : Bool) : Word := [b]

/-- A prefix-free encoding of a pair of binary words. -/
def encodePair (xy : Word × Word) : Word :=
  List.replicate xy.1.length true ++ false :: xy.1 ++ xy.2

/-- Unary naturals are sufficient for fixing the machine interface. -/
def encodeNat (n : Nat) : Word := List.replicate n true ++ [false]

/-- A prefix-free concatenation of unary natural-number encodings. -/
def encodeNats (ns : List Nat) : Word := ns.flatMap encodeNat

def PolytimeNatFunction (f : Word -> Nat) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime id encodeNat f)

def PolytimeQueryFunction (f : Word × Word -> List Nat) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodePair encodeNats f)

def PolytimeDecision (f : Word × Word -> Bool) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodePair encodeBool f)

/-- Verifier-based NP over binary strings with polynomially bounded certificates. -/
def InNP (language : Language) : Prop :=
  exists verifier : Word × Word -> Bool, exists bound : Polynomial Nat,
    PolytimeDecision verifier /\
      forall input : Word,
        language input <->
          exists certificate : Word,
            certificate.length <= bound.eval input.length /\ verifier (input, certificate) = true

/-- A nonadaptive oracle checker. Randomness first selects query positions;
the decision procedure receives only the corresponding proof bits. -/
structure Checker where
  randomLength : Word -> Nat
  queries : Word × Word -> List Nat
  decide : Word × Word -> Bool
  randomLength_polytime : PolytimeNatFunction randomLength
  queries_polytime : PolytimeQueryFunction queries
  decide_polytime : PolytimeDecision decide

def randomWord {n : Nat} (coins : Fin n -> Bool) : Word := List.ofFn coins

def oracleAnswers (proof : Nat -> Bool) (positions : List Nat) : Word :=
  positions.map proof

def Checker.accepts (checker : Checker) (input : Word) (proof : Nat -> Bool)
    (coins : Fin (checker.randomLength input) -> Bool) : Bool :=
  let randomness := randomWord coins
  checker.decide (input, oracleAnswers proof (checker.queries (input, randomness)))

/-- At most half of the uniformly distributed random strings accept. The
cardinality formulation avoids adding a probability library to the target. -/
def HasSoundnessHalf (checker : Checker) (language : Language) : Prop :=
  forall input : Word, (language input -> False) -> forall proof : Nat -> Bool,
    2 * (Finset.univ.filter fun coins => checker.accepts input proof coins).card <=
      (Finset.univ : Finset (Fin (checker.randomLength input) -> Bool)).card

/-- PCP with perfect completeness, soundness `1/2`, logarithmic randomness,
and a uniform constant bound on nonadaptive oracle queries. -/
def InPCPLogConst (language : Language) : Prop :=
  exists checker : Checker, exists randomConstant queryConstant threshold : Nat,
    (forall input : Word, threshold <= input.length ->
      checker.randomLength input <= randomConstant * Nat.log2 (input.length + 1)) /\
    (forall input randomness,
      randomness.length = checker.randomLength input ->
        (checker.queries (input, randomness)).length <= queryConstant) /\
    (forall input : Word, language input -> exists proof : Nat -> Bool,
      forall coins, checker.accepts input proof coins = true) /\
    HasSoundnessHalf checker language

/-- Canonical target: binary verifier-based NP is exactly binary PCP with
`O(log n)` randomness and `O(1)` nonadaptive queries. -/
def PCPTheorem : Prop :=
  {language : Language | InNP language} = {language : Language | InPCPLogConst language}

def ExpandedTarget : Prop :=
  forall language : Language, InNP language <-> InPCPLogConst language

theorem pcpTheorem_iff_expandedTarget : PCPTheorem <-> ExpandedTarget := by
  simp only [PCPTheorem, Set.ext_iff, Set.mem_setOf_eq, ExpandedTarget]

-- Structural mutations separately elaborated by `check_statement.py`.
def mutationOneInclusion : Prop :=
  forall language : Language, InNP language -> InPCPLogConst language

def mutationPolynomialRandomness : Prop :=
  forall language : Language, InNP language <->
    exists checker : Checker, exists randomPolynomial : Polynomial Nat,
      (forall input, checker.randomLength input <= randomPolynomial.eval input.length) /\
      HasSoundnessHalf checker language

def mutationUnboundedQueries : Prop :=
  forall language : Language, InNP language <->
    exists checker : Checker, exists randomConstant threshold : Nat,
      (forall input, threshold <= input.length ->
        checker.randomLength input <= randomConstant * Nat.log2 (input.length + 1)) /\
      (forall input, language input -> exists proof, forall coins,
        checker.accepts input proof coins = true) /\
      HasSoundnessHalf checker language

def mutationNoSoundness : Prop :=
  forall language : Language, InNP language <->
    exists checker : Checker, exists randomConstant queryConstant threshold : Nat,
      (forall input, threshold <= input.length ->
        checker.randomLength input <= randomConstant * Nat.log2 (input.length + 1)) /\
      (forall input randomness, randomness.length = checker.randomLength input ->
        (checker.queries (input, randomness)).length <= queryConstant) /\
      (forall input, language input -> exists proof, forall coins,
        checker.accepts input proof coins = true)

/-- Zero random bits has exactly one random string, the empty string. -/
theorem zero_randomness_boundary :
    (Finset.univ : Finset (Fin 0 -> Bool)).card = 1 := by simp

end Stage1Instances.THM_M_0729

set_option pp.explicit true in
#print Stage1Instances.THM_M_0729.PCPTheorem
