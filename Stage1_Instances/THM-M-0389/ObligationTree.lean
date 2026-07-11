import Init

/-!
# THM-M-0389 obligation-tree composition surface

This standalone module checks the top-level case split and conditional
composition for the frozen integer Markov classification. Its three arguments
are open obligations; this file does not assert the classification theorem.
-/

namespace Stage1Instances.THM_M_0389_Obligations

def MarkovEquation (x y z : Int) : Prop :=
  x ^ 2 + y ^ 2 + z ^ 2 = 3 * x * y * z

inductive GeneratedMarkovTriple : Int -> Int -> Int -> Prop
  | seed : GeneratedMarkovTriple 1 1 1
  | swapXY {x y z} : GeneratedMarkovTriple x y z -> GeneratedMarkovTriple y x z
  | swapYZ {x y z} : GeneratedMarkovTriple x y z -> GeneratedMarkovTriple x z y
  | mutateX {x y z} : GeneratedMarkovTriple x y z ->
      GeneratedMarkovTriple (3 * y * z - x) y z
  | mutateY {x y z} : GeneratedMarkovTriple x y z ->
      GeneratedMarkovTriple x (3 * x * z - y) z
  | mutateZ {x y z} : GeneratedMarkovTriple x y z ->
      GeneratedMarkovTriple x y (3 * x * y - z)

def EvenSignVariant (x y z a b c : Int) : Prop :=
  (x = a  /\ y = b  /\ z = c)  \/
  (x = a  /\ y = -b /\ z = -c) \/
  (x = -a /\ y = b  /\ z = -c) \/
  (x = -a /\ y = -b /\ z = c)

def PositiveTriple (x y z : Int) : Prop := 0 < x /\ 0 < y /\ 0 < z

def ObligationTreeRoot : Prop :=
  forall x y z : Int, MarkovEquation x y z ->
    (x = 0 /\ y = 0 /\ z = 0) \/
    exists a b c : Int,
      GeneratedMarkovTriple a b c /\ EvenSignVariant x y z a b c

def ZeroCoordinateBranch : Prop :=
  forall x y z : Int, MarkovEquation x y z ->
    (x = 0 \/ y = 0 \/ z = 0) -> x = 0 /\ y = 0 /\ z = 0

def NonzeroSignNormalization : Prop :=
  forall x y z : Int, MarkovEquation x y z ->
    Not (x = 0 \/ y = 0 \/ z = 0) ->
    exists a b c : Int,
      PositiveTriple a b c /\ MarkovEquation a b c /\ EvenSignVariant x y z a b c

def PositiveGeneration : Prop :=
  forall x y z : Int, MarkovEquation x y z -> PositiveTriple x y z ->
    GeneratedMarkovTriple x y z

/-- Exact root expression fixture matching `Statement.lean`. -/
theorem obligationTreeRoot_exact_type :
    ObligationTreeRoot =
      (forall x y z : Int, MarkovEquation x y z ->
        (x = 0 /\ y = 0 /\ z = 0) \/
        exists a b c : Int,
          GeneratedMarkovTriple a b c /\ EvenSignVariant x y z a b c) :=
  rfl

/--
Checked top-level exhaustiveness and recomposition. Every declared child is
consumed, and no mathematical child is manufactured by the certificate.
-/
theorem root_compose
    (hzero : ZeroCoordinateBranch)
    (hsign : NonzeroSignNormalization)
    (hpositive : PositiveGeneration) :
    ObligationTreeRoot := by
  intro x y z heq
  by_cases hcoord : x = 0 \/ y = 0 \/ z = 0
  · exact Or.inl (hzero x y z heq hcoord)
  · rcases hsign x y z heq hcoord with ⟨a, b, c, hpos, habc, hvariant⟩
    exact Or.inr ⟨a, b, c, hpositive a b c habc hpos, hvariant⟩

#print root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0389_Obligations
