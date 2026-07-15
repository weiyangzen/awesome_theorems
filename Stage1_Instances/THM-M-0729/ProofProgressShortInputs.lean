import ProofProgress
import ProofProgressSerialization
import Mathlib.Data.Set.Finite.List

/-!
# THM-M-0729 short-input certificate proof progress

This module closes the finite below-threshold part of the semantic certificate
bound used by the PCP-to-NP direction.  Together with the existing large-input
estimate, it packages one polynomial that bounds the serialized reachable
oracle assignment on every input.  It still does not construct the executable
polynomial-time verifier required by `InNP`.
-/

namespace Stage1Instances.THM_M_0729

/-- Only finitely many binary inputs lie below a fixed length threshold, so
their reachable-oracle certificate sizes have a common numerical bound. -/
theorem exists_shortInput_queriedPositions_bound
    (checker : Checker) (threshold : Nat) :
    exists shortBound : Nat, forall input : Word, input.length < threshold ->
      (queriedPositions checker input).card <= shortBound := by
  have finiteInputs : {input : Word | input.length < threshold}.Finite :=
    List.finite_length_lt Bool threshold
  have finiteSizes :
      ((fun input : Word => (queriedPositions checker input).card) ''
        {input : Word | input.length < threshold}).Finite :=
    finiteInputs.image _
  rcases finiteSizes.bddAbove with ⟨shortBound, bound⟩
  refine ⟨shortBound, ?_⟩
  intro input short
  exact bound ⟨input, short, rfl⟩

/-- Add the finite below-threshold maximum to the eventual certificate
polynomial.  The extra constant is deliberately explicit. -/
noncomputable def globalFiniteOracleCertificateBound
    (randomConstant queryConstant shortBound : Nat) : Polynomial Nat :=
  finiteOracleCertificateBound randomConstant queryConstant +
    Polynomial.C shortBound

@[simp] theorem globalFiniteOracleCertificateBound_eval
    (randomConstant queryConstant shortBound inputLength : Nat) :
    (globalFiniteOracleCertificateBound randomConstant queryConstant shortBound).eval
        inputLength =
      (inputLength + 1) ^ randomConstant * queryConstant + shortBound := by
  simp [globalFiniteOracleCertificateBound]

/-- The frozen logarithmic-randomness and constant-query estimates yield one
polynomial certificate-size bound for both the eventual and finite branches. -/
theorem exists_global_queriedPositions_polynomial_bound
    (checker : Checker) (randomConstant queryConstant threshold : Nat)
    (randomBound : forall input : Word, threshold <= input.length ->
      checker.randomLength input <=
        randomConstant * Nat.log2 (input.length + 1))
    (queryBound : forall input randomness,
      randomness.length = checker.randomLength input ->
        (checker.queries (input, randomness)).length <= queryConstant) :
    exists bound : Polynomial Nat, forall input : Word,
      (queriedPositions checker input).card <= bound.eval input.length := by
  rcases exists_shortInput_queriedPositions_bound checker threshold with
    ⟨shortBound, shortBounded⟩
  refine ⟨globalFiniteOracleCertificateBound randomConstant queryConstant shortBound, ?_⟩
  intro input
  rw [globalFiniteOracleCertificateBound_eval]
  by_cases large : threshold <= input.length
  · calc
      (queriedPositions checker input).card <=
          (finiteOracleCertificateBound randomConstant queryConstant).eval input.length :=
        queriedPositions_card_le_certificatePolynomial checker randomConstant
          queryConstant threshold randomBound queryBound input large
      _ = (input.length + 1) ^ randomConstant * queryConstant :=
        finiteOracleCertificateBound_eval _ _ _
      _ <= (input.length + 1) ^ randomConstant * queryConstant + shortBound :=
        Nat.le_add_right _ _
  · exact Nat.le_trans (shortBounded input (Nat.lt_of_not_ge large))
      (Nat.le_add_left shortBound _)

/-- Enumerate every binary random string by extending shorter strings with
both possible leading bits. -/
def allRandomWords : (n : Nat) -> List (Fin n -> Bool)
  | 0 => [Fin.elim0]
  | n + 1 =>
      (allRandomWords n).flatMap fun tail =>
        [Fin.cons false tail, Fin.cons true tail]

@[simp] theorem allRandomWords_length (n : Nat) :
    (allRandomWords n).length = 2 ^ n := by
  induction n with
  | zero => simp [allRandomWords]
  | succ n inductionHypothesis => simp [allRandomWords, inductionHypothesis, pow_succ]

theorem mem_allRandomWords (coins : Fin n -> Bool) :
    coins ∈ allRandomWords n := by
  induction n with
  | zero =>
      have coinsEq : coins = Fin.elim0 := Subsingleton.elim _ _
      simp [allRandomWords, coinsEq]
  | succ n inductionHypothesis =>
      rw [← Fin.cons_self_tail coins]
      cases first : coins 0 <;>
        simp [allRandomWords, inductionHypothesis]

/-- On the finitely many below-threshold inputs, the random spaces have a
common size bound. -/
theorem exists_shortInput_randomSpace_bound
    (checker : Checker) (threshold : Nat) :
    exists shortBound : Nat, forall input : Word, input.length < threshold ->
      2 ^ checker.randomLength input <= shortBound := by
  have finiteInputs : {input : Word | input.length < threshold}.Finite :=
    List.finite_length_lt Bool threshold
  have finiteSizes :
      ((fun input : Word => 2 ^ checker.randomLength input) ''
        {input : Word | input.length < threshold}).Finite :=
    finiteInputs.image _
  rcases finiteSizes.bddAbove with ⟨shortBound, bound⟩
  refine ⟨shortBound, ?_⟩
  intro input short
  exact bound ⟨input, short, rfl⟩

/-- A global polynomial bound for the number of random strings. -/
noncomputable def globalRandomSpaceBound
    (randomConstant shortBound : Nat) : Polynomial Nat :=
  (Polynomial.X + 1) ^ randomConstant + Polynomial.C shortBound

@[simp] theorem globalRandomSpaceBound_eval
    (randomConstant shortBound inputLength : Nat) :
    (globalRandomSpaceBound randomConstant shortBound).eval inputLength =
      (inputLength + 1) ^ randomConstant + shortBound := by
  simp [globalRandomSpaceBound]

theorem exists_global_randomSpace_polynomial_bound
    (checker : Checker) (randomConstant threshold : Nat)
    (randomBound : forall input : Word, threshold <= input.length ->
      checker.randomLength input <=
        randomConstant * Nat.log2 (input.length + 1)) :
    exists bound : Polynomial Nat, forall input : Word,
      2 ^ checker.randomLength input <= bound.eval input.length := by
  rcases exists_shortInput_randomSpace_bound checker threshold with
    ⟨shortBound, shortBounded⟩
  refine ⟨globalRandomSpaceBound randomConstant shortBound, ?_⟩
  intro input
  rw [globalRandomSpaceBound_eval]
  by_cases large : threshold <= input.length
  · calc
      2 ^ checker.randomLength input <=
          2 ^ (randomConstant * Nat.log2 (input.length + 1)) :=
        Nat.pow_le_pow_right (by decide) (randomBound input large)
      _ = (2 ^ Nat.log2 (input.length + 1)) ^ randomConstant := by
        rw [Nat.mul_comm, pow_mul]
      _ <= (input.length + 1) ^ randomConstant :=
        Nat.pow_le_pow_left (Nat.log2_self_le (by omega)) randomConstant
      _ <= (input.length + 1) ^ randomConstant + shortBound :=
        Nat.le_add_right _ _
  · exact Nat.le_trans (shortBounded input (Nat.lt_of_not_ge large))
      (Nat.le_add_left shortBound _)

/-- The recursive exhaustive enumeration itself therefore has polynomial
length under the frozen logarithmic-randomness hypothesis. -/
theorem exists_global_allRandomWords_polynomial_bound
    (checker : Checker) (randomConstant threshold : Nat)
    (randomBound : forall input : Word, threshold <= input.length ->
      checker.randomLength input <=
        randomConstant * Nat.log2 (input.length + 1)) :
    exists bound : Polynomial Nat, forall input : Word,
      (allRandomWords (checker.randomLength input)).length <=
        bound.eval input.length := by
  rcases exists_global_randomSpace_polynomial_bound checker randomConstant
      threshold randomBound with ⟨bound, bounded⟩
  exact ⟨bound, fun input => by simpa using bounded input⟩

/-- Evaluate a serialized certificate on every random string. -/
def exhaustiveCertificateVerifier (checker : Checker)
    (input certificate : Word) : Bool :=
  (allRandomWords (checker.randomLength input)).all fun coins =>
    checker.accepts input
      (FiniteOracle.decode checker input certificate).extend coins

@[simp] theorem exhaustiveCertificateVerifier_eq_true
    (checker : Checker) (input certificate : Word) :
    exhaustiveCertificateVerifier checker input certificate = true <->
      forall coins, checker.accepts input
        (FiniteOracle.decode checker input certificate).extend coins = true := by
  constructor
  · intro accepted coins
    exact (List.all_eq_true.mp accepted) coins (mem_allRandomWords coins)
  · intro accepted
    exact List.all_eq_true.mpr fun coins _ => accepted coins

/-- A PCP witness therefore has a literal binary certificate, polynomially
bounded on every input, whose decoded finite oracle is accepted for every
random string exactly on language members. -/
theorem inPCPLogConst_has_polynomial_binary_certificates
    {language : Language} (h : InPCPLogConst language) :
    exists checker : Checker, exists bound : Polynomial Nat,
      forall input : Word, language input <->
        exists certificate : Word,
          certificate.length <= bound.eval input.length /\
          forall coins, checker.accepts input
            (FiniteOracle.decode checker input certificate).extend coins = true := by
  rcases h with
    ⟨checker, randomConstant, queryConstant, threshold,
      randomBound, queryBound, complete, sound⟩
  rcases exists_global_queriedPositions_polynomial_bound checker randomConstant
      queryConstant threshold randomBound queryBound with ⟨bound, bounded⟩
  refine ⟨checker, bound, ?_⟩
  intro input
  rw [language_iff_exists_accepts_all complete sound input,
    binaryCertificate_characterization]
  constructor
  · rintro ⟨certificate, lengthEq, acceptsAll⟩
    exact ⟨certificate, lengthEq.le.trans (bounded input), acceptsAll⟩
  · rintro ⟨certificate, _lengthBound, acceptsAll⟩
    let assignment := FiniteOracle.decode checker input certificate
    exact ⟨assignment.encode, FiniteOracle.encode_length assignment, by simpa using acceptsAll⟩

/-- Executable-Boolean form of the global certificate characterization.  This
separates correctness of exhaustive checking from its still-open TM2 cost and
implementation proof. -/
theorem inPCPLogConst_has_exhaustive_certificate_verifier
    {language : Language} (h : InPCPLogConst language) :
    exists checker : Checker, exists bound : Polynomial Nat,
      forall input : Word, language input <->
        exists certificate : Word,
          certificate.length <= bound.eval input.length /\
          exhaustiveCertificateVerifier checker input certificate = true := by
  rcases inPCPLogConst_has_polynomial_binary_certificates h with
    ⟨checker, bound, characterizes⟩
  exact ⟨checker, bound, fun input => by simpa using characterizes input⟩

#print axioms exists_shortInput_queriedPositions_bound
#print axioms globalFiniteOracleCertificateBound
#print axioms globalFiniteOracleCertificateBound_eval
#print axioms exists_global_queriedPositions_polynomial_bound
#print axioms allRandomWords
#print axioms allRandomWords_length
#print axioms mem_allRandomWords
#print axioms exists_shortInput_randomSpace_bound
#print axioms globalRandomSpaceBound
#print axioms globalRandomSpaceBound_eval
#print axioms exists_global_randomSpace_polynomial_bound
#print axioms exists_global_allRandomWords_polynomial_bound
#print axioms exhaustiveCertificateVerifier
#print axioms exhaustiveCertificateVerifier_eq_true
#print axioms inPCPLogConst_has_polynomial_binary_certificates
#print axioms inPCPLogConst_has_exhaustive_certificate_verifier

end Stage1Instances.THM_M_0729
