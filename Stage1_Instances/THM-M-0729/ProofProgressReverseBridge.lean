import ProofProgressShortInputs

/-!
# THM-M-0729 reverse-direction assembly bridge

The finite-certificate development already supplies an extensional Boolean
verifier for each frozen PCP checker. This module proves that the one remaining
machine-level premise, polynomial-time computability of that exact verifier,
is sufficient to construct the `InNP` witness. It does not assume that premise
for an arbitrary checker and therefore does not close the PCP-to-NP inclusion.
-/

namespace Stage1Instances.THM_M_0729

/-- Pair-uncurried form of the exhaustive verifier, matching the input shape
required by `PolytimeDecision`. -/
def exhaustiveCertificateDecision (checker : Checker) : Word × Word -> Bool :=
  fun inputCertificate =>
    exhaustiveCertificateVerifier checker inputCertificate.1 inputCertificate.2

@[simp] theorem exhaustiveCertificateDecision_apply
    (checker : Checker) (input certificate : Word) :
    exhaustiveCertificateDecision checker (input, certificate) =
      exhaustiveCertificateVerifier checker input certificate := by
  rfl

/-- Once the exact exhaustive Boolean verifier has a polynomial-time TM2
implementation, the already-checked global certificate characterization
assembles directly into the frozen verifier-based definition of NP. -/
theorem inNP_of_inPCPLogConst_of_exhaustiveDecision_polytime
    {language : Language} (h : InPCPLogConst language)
    (decisionPolytime : forall checker : Checker,
      PolytimeDecision (exhaustiveCertificateDecision checker)) :
    InNP language := by
  rcases inPCPLogConst_has_exhaustive_certificate_verifier h with
    ⟨checker, bound, characterizes⟩
  refine ⟨exhaustiveCertificateDecision checker, bound,
    decisionPolytime checker, ?_⟩
  intro input
  simpa only [exhaustiveCertificateDecision_apply] using characterizes input

/-- Per-language implication form of the same assembly boundary. -/
theorem inPCPLogConst_imp_inNP_of_exhaustiveDecision_polytime
    (language : Language)
    (decisionPolytime : forall checker : Checker,
      PolytimeDecision (exhaustiveCertificateDecision checker)) :
    InPCPLogConst language -> InNP language := by
  intro h
  exact inNP_of_inPCPLogConst_of_exhaustiveDecision_polytime h decisionPolytime

/-- A uniform implementation of the exact exhaustive verifier closes the
whole frozen PCP-to-NP directional obligation. -/
theorem pcpToNP_of_exhaustiveDecision_polytime
    (decisionPolytime : forall checker : Checker,
      PolytimeDecision (exhaustiveCertificateDecision checker)) :
    forall language : Language, InPCPLogConst language -> InNP language := by
  intro language
  exact inPCPLogConst_imp_inNP_of_exhaustiveDecision_polytime language
    decisionPolytime

/-- Dependency-local variant: only the checker extracted from a particular
PCP witness needs a machine implementation. This formulation pinpoints the
remaining reverse-direction proof obligation without universally quantifying
over unrelated checkers. -/
theorem inPCPLogConst_has_reverseDecision_obligation
    {language : Language} (h : InPCPLogConst language) :
    exists checker : Checker, exists bound : Polynomial Nat,
      (forall input : Word, language input <->
        exists certificate : Word,
          certificate.length <= bound.eval input.length /\
          exhaustiveCertificateDecision checker (input, certificate) = true) /\
      (PolytimeDecision (exhaustiveCertificateDecision checker) ->
        InNP language) := by
  rcases inPCPLogConst_has_exhaustive_certificate_verifier h with
    ⟨checker, bound, characterizes⟩
  refine ⟨checker, bound, ?_, ?_⟩
  · intro input
    simpa only [exhaustiveCertificateDecision_apply] using characterizes input
  · intro decisionPolytime
    exact ⟨exhaustiveCertificateDecision checker, bound,
      decisionPolytime, fun input => by
        simpa only [exhaustiveCertificateDecision_apply] using characterizes input⟩

#print axioms exhaustiveCertificateDecision
#print axioms exhaustiveCertificateDecision_apply
#print axioms inNP_of_inPCPLogConst_of_exhaustiveDecision_polytime
#print axioms inPCPLogConst_imp_inNP_of_exhaustiveDecision_polytime
#print axioms pcpToNP_of_exhaustiveDecision_polytime
#print axioms inPCPLogConst_has_reverseDecision_obligation

end Stage1Instances.THM_M_0729
