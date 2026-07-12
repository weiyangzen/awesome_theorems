import Mathlib.Computability.TuringMachine.Computable

/-!
# THM-M-0721: existence of an NP-complete language

This module fixes a concrete binary-string, verifier-based formulation. It
freezes and tests the statement boundary only; it contains no proof that such
a language exists.
-/

namespace Stage1Instances.THM_M_0721

abbrev Word := List Bool
abbrev Language := Word -> Prop

/-- A one-bit encoding of a Boolean output. -/
def encodeBool (b : Bool) : List Bool := [b]

/-- Self-delimiting pairing: `|x|` ones, a zero separator, then `x` and `y`. -/
def encodePair (xy : Word × Word) : Word :=
  List.replicate xy.1.length true ++ false :: xy.1 ++ xy.2

/-- A Boolean function on binary strings computed by a bundled TM2 in polynomial time. -/
def PolytimePredicate (f : Word -> Bool) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime id encodeBool f)

/-- A binary-string function computed by a bundled TM2 in polynomial time. -/
def PolytimeFunction (f : Word -> Word) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime id id f)

/-- Verifier-based NP over binary strings with polynomially bounded certificates. -/
def InNP (language : Language) : Prop :=
  exists verifier : Word × Word -> Bool, exists bound : Polynomial Nat,
    Nonempty (Turing.TM2ComputableInPolyTime encodePair encodeBool verifier) /\
      forall input : Word,
        language input <->
          exists certificate : Word,
            certificate.length <= bound.eval input.length /\ verifier (input, certificate) = true

/-- Polynomial-time many-one reduction between binary languages. -/
def PolyManyOneReducible (source target : Language) : Prop :=
  exists reduction : Word -> Word, PolytimeFunction reduction /\
    forall input : Word, source input <-> target (reduction input)

/-- Membership in NP together with hardness for every NP language. -/
def NPComplete (language : Language) : Prop :=
  InNP language /\ forall source : Language, InNP source -> PolyManyOneReducible source language

/-- Exact existential target selected for THM-M-0721. -/
def ExistsNPCompleteLanguage : Prop :=
  exists language : Language, NPComplete language

/-- Direct expansion used to check that the named target adds no hidden premise. -/
def ExpandedTarget : Prop :=
  exists language : Word -> Prop,
    InNP language /\ forall source : Word -> Prop, InNP source ->
      exists reduction : Word -> Word, PolytimeFunction reduction /\
        forall input : Word, source input <-> language (reduction input)

theorem existsNPCompleteLanguage_iff_expandedTarget :
    ExistsNPCompleteLanguage <-> ExpandedTarget := by
  rfl

-- Structural mutations separately elaborated and distinguished by check_statement.py.
def mutationUncheckedVerifier : Prop :=
  exists language : Language,
    (exists verifier : Word × Word -> Bool, exists bound : Polynomial Nat,
      forall input : Word,
        language input <-> exists certificate : Word,
          certificate.length <= bound.eval input.length /\ verifier (input, certificate) = true) /\
    forall source : Language, InNP source -> PolyManyOneReducible source language

def mutationChangedDomain : Prop :=
  exists _language : List Unit -> Prop, True

def mutationChangedBinderScope : Prop :=
  exists reduction : Word -> Word, PolytimeFunction reduction /\
    forall source target : Language, InNP source ->
      forall input : Word, source input <-> target (reduction input)

def mutationNoMembershipRequirement : Prop :=
  exists language : Language,
    forall source : Language, InNP source -> PolyManyOneReducible source language

theorem binary_alphabet_has_two_distinct_symbols : (false : Bool) != true := by
  decide

theorem encodePair_empty_empty : encodePair ([], []) = [false] := by
  rfl

theorem empty_certificate_is_in_boundary (bound : Polynomial Nat) (input : Word) :
    ([] : Word).length <= bound.eval input.length := by
  simp

end Stage1Instances.THM_M_0721

set_option pp.explicit true in
#print Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage
