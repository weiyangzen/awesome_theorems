/-!
# THM-M-0389: validation probe

This validation suffix is appended to `Proof.lean` by the fail-closed verifier.
It independently spells the frozen root expression and checks both its
definitional identity and that the proof-phase theorem inhabits it. It adds no
mathematical premise or proof implementation.
-/

namespace Stage1Instances.THM_M_0389_Validation

/-- An independently declared exact copy of the frozen root expression. -/
def ExactRoot : Prop :=
  forall x y z : Int,
    x ^ 2 + y ^ 2 + z ^ 2 = 3 * x * y * z ->
      (x = 0 /\ y = 0 /\ z = 0) \/
      exists a b c : Int,
        Stage1Instances.THM_M_0389.GeneratedMarkovTriple a b c /\
        Stage1Instances.THM_M_0389.EvenSignVariant x y z a b c

theorem exactRoot_iff_frozen :
    ExactRoot <-> Stage1Instances.THM_M_0389.IntegerMarkovClassification :=
  Iff.rfl

theorem validationExactRoot : ExactRoot :=
  Stage1Instances.THM_M_0389.integerMarkovClassification

#check validationExactRoot
#print axioms validationExactRoot

end Stage1Instances.THM_M_0389_Validation
