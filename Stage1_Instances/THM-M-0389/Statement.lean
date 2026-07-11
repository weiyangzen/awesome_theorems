import Init

/-!
# THM-M-0389: integer Markov-triple classification statement

This module freezes the statement boundary only. It contains no proof of the
classification theorem.
-/

namespace Stage1Instances.THM_M_0389

/-- The integer Markov equation. -/
def MarkovEquation (x y z : Int) : Prop :=
  x ^ 2 + y ^ 2 + z ^ 2 = 3 * x * y * z

/-- The closure of `(1,1,1)` under coordinate swaps and Vieta involutions. -/
inductive GeneratedMarkovTriple : Int -> Int -> Int -> Prop
  | seed : GeneratedMarkovTriple 1 1 1
  | swapXY {x y z : Int} :
      GeneratedMarkovTriple x y z -> GeneratedMarkovTriple y x z
  | swapYZ {x y z : Int} :
      GeneratedMarkovTriple x y z -> GeneratedMarkovTriple x z y
  | mutateX {x y z : Int} :
      GeneratedMarkovTriple x y z -> GeneratedMarkovTriple (3 * y * z - x) y z
  | mutateY {x y z : Int} :
      GeneratedMarkovTriple x y z -> GeneratedMarkovTriple x (3 * x * z - y) z
  | mutateZ {x y z : Int} :
      GeneratedMarkovTriple x y z -> GeneratedMarkovTriple x y (3 * x * y - z)

/-- Sign changes of zero or two coordinates, precisely those preserving `xyz`. -/
def EvenSignVariant (x y z a b c : Int) : Prop :=
  (x = a  /\ y = b  /\ z = c)  \/
  (x = a  /\ y = -b /\ z = -c) \/
  (x = -a /\ y = b  /\ z = -c) \/
  (x = -a /\ y = -b /\ z = c)

/--
Canonical classification of the integer solutions of the Markov equation.

Every solution is the zero triple or an even-sign variant of a triple generated
from `(1,1,1)` by permutations and Vieta mutations.
-/
def IntegerMarkovClassification : Prop :=
  forall x y z : Int,
    MarkovEquation x y z ->
      (x = 0 /\ y = 0 /\ z = 0) \/
      exists a b c : Int,
        GeneratedMarkovTriple a b c /\ EvenSignVariant x y z a b c

/-- Checked identity with the historically discovered Stage1 statement shape. -/
def LegacyStatementShape : Prop :=
  forall x y z : Int,
    MarkovEquation x y z ->
      (x = 0 /\ y = 0 /\ z = 0) \/
      exists a b c : Int,
        GeneratedMarkovTriple a b c /\ EvenSignVariant x y z a b c

theorem integerMarkovClassification_iff_legacyStatementShape :
    IntegerMarkovClassification <-> LegacyStatementShape :=
  Iff.rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationEquationOnly : Prop :=
  exists x y z : Int, MarkovEquation x y z

def mutationPositiveDomainOnly : Prop :=
  forall x y z : Int,
    0 < x -> 0 < y -> 0 < z -> MarkovEquation x y z ->
      GeneratedMarkovTriple x y z

def mutationOmitsZeroCase : Prop :=
  forall x y z : Int,
    MarkovEquation x y z ->
      exists a b c : Int,
        GeneratedMarkovTriple a b c /\ EvenSignVariant x y z a b c

def mutationAllowsOneSignChange : Prop :=
  forall x y z : Int,
    MarkovEquation x y z ->
      (x = 0 /\ y = 0 /\ z = 0) \/
      exists a b c : Int,
        GeneratedMarkovTriple a b c /\
          (EvenSignVariant x y z a b c \/ (x = -a /\ y = b /\ z = c))

end Stage1Instances.THM_M_0389

set_option pp.explicit true in
#print Stage1Instances.THM_M_0389.IntegerMarkovClassification
