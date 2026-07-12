import Mathlib.Data.Set.Basic

namespace Stage1Instances.THM_M_0785.IntakeProbe

abbrev Play := Nat -> Nat
abbrev Strategy := List Nat -> Nat

def RespectsFirst (strategy : Strategy) (play : Play) : Prop :=
  forall n, play (2 * n) = strategy (List.ofFn fun i : Fin (2 * n) => play i)

def RespectsSecond (strategy : Strategy) (play : Play) : Prop :=
  forall n, play (2 * n + 1) = strategy (List.ofFn fun i : Fin (2 * n + 1) => play i)

def FirstWins (payoff : Set Play) (strategy : Strategy) : Prop :=
  forall play, RespectsFirst strategy play -> play ∈ payoff

def SecondWins (payoff : Set Play) (strategy : Strategy) : Prop :=
  forall play, RespectsSecond strategy play -> play ∉ payoff

-- This probes one standard game encoding. It is deliberately not selected as
-- the canonical target while the source's payoff pointclass remains unknown.
def FullDeterminacyCandidate : Prop :=
  forall payoff : Set Play,
    (exists strategy, FirstWins payoff strategy) ∨
      (exists strategy, SecondWins payoff strategy)

#check Play
#check Strategy
#check RespectsFirst
#check RespectsSecond
#check FirstWins
#check SecondWins
#check FullDeterminacyCandidate

end Stage1Instances.THM_M_0785.IntakeProbe
