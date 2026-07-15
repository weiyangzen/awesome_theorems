import ProofProgressCardinality

/-!
# THM-M-0729 binary-certificate proof progress

This module serializes the finite reachable part of a proof oracle as a binary
certificate.  It proves lossless round trips, transfers universal acceptance
to the serialized certificate, and derives the eventual polynomial length
bound supplied by the frozen PCP resource hypotheses.  It does not construct
the polynomial-time verifier required for the PCP-to-NP inclusion.
-/

namespace Stage1Instances.THM_M_0729

/-- A deterministic enumeration of the reachable oracle positions. -/
def finiteOraclePositionEquiv (checker : Checker) (input : Word) :
    Fin (queriedPositions checker input).card ≃
      {position : Nat // position ∈ queriedPositions checker input} :=
  ((queriedPositions checker input).orderIsoOfFin rfl).toEquiv

/-- Serialize a finite reachable-position assignment in increasing-position
order. The result is literally a binary word of the required length. -/
def FiniteOracle.encode {checker : Checker} {input : Word}
    (assignment : FiniteOracle checker input) : Word :=
  List.ofFn fun index => assignment (finiteOraclePositionEquiv checker input index)

/-- Read a binary certificate as an assignment on all reachable positions.
Missing bits default to `false`; the round-trip results below use exact-length
certificates and therefore never take that fallback. -/
def FiniteOracle.decode (checker : Checker) (input : Word)
    (certificate : Word) : FiniteOracle checker input := fun position =>
  certificate.getD
    ((finiteOraclePositionEquiv checker input).symm position : Nat) false

@[simp] theorem FiniteOracle.encode_length {checker : Checker} {input : Word}
    (assignment : FiniteOracle checker input) :
    assignment.encode.length = (queriedPositions checker input).card := by
  simp [FiniteOracle.encode]

@[simp] theorem FiniteOracle.decode_encode {checker : Checker} {input : Word}
    (assignment : FiniteOracle checker input) :
    FiniteOracle.decode checker input assignment.encode = assignment := by
  funext position
  simp [FiniteOracle.decode, FiniteOracle.encode, finiteOraclePositionEquiv]

theorem FiniteOracle.encode_decode_of_length
    (checker : Checker) (input : Word) (certificate : Word)
    (lengthEq : certificate.length = (queriedPositions checker input).card) :
    (FiniteOracle.decode checker input certificate).encode = certificate := by
  apply List.ext_get
  · simp [FiniteOracle.encode, lengthEq]
  · intro index _ _
    simp [FiniteOracle.decode, FiniteOracle.encode, finiteOraclePositionEquiv,
      lengthEq]

theorem FiniteOracle.encode_injective (checker : Checker) (input : Word) :
    Function.Injective
      (FiniteOracle.encode (checker := checker) (input := input)) := by
  intro assignment1 assignment2 equalEncoding
  rw [← FiniteOracle.decode_encode assignment1,
    ← FiniteOracle.decode_encode assignment2, equalEncoding]

/-- The arbitrary total oracle in the frozen semantics can be replaced by a
binary word containing exactly the reachable bits. -/
theorem binaryCertificate_characterization (checker : Checker) (input : Word) :
    (exists proof : Nat -> Bool, forall coins,
      checker.accepts input proof coins = true) <->
    exists certificate : Word,
      certificate.length = (queriedPositions checker input).card /\
      forall coins, checker.accepts input
        (FiniteOracle.decode checker input certificate).extend coins = true := by
  rw [finiteOracle_characterization]
  constructor
  · rintro ⟨assignment, acceptsAll⟩
    refine ⟨assignment.encode, FiniteOracle.encode_length assignment, ?_⟩
    simpa using acceptsAll
  · rintro ⟨certificate, _lengthEq, acceptsAll⟩
    exact ⟨FiniteOracle.decode checker input certificate, acceptsAll⟩

/-- An exact-length binary certificate inherits the finite reachable-position
bound proved in `ProofProgressCardinality`. -/
theorem binaryCertificate_length_le
    (checker : Checker) (input certificate : Word) (queryConstant : Nat)
    (queryBound : forall randomness : Word,
      randomness.length = checker.randomLength input ->
        (checker.queries (input, randomness)).length <= queryConstant)
    (lengthEq : certificate.length = (queriedPositions checker input).card) :
    certificate.length <=
      2 ^ checker.randomLength input * queryConstant := by
  rw [lengthEq]
  exact queriedPositions_card_le checker input queryConstant queryBound

/-- The explicit polynomial used to bound serialized certificates on inputs
where the checker's logarithmic-randomness estimate applies. -/
noncomputable def finiteOracleCertificateBound
    (randomConstant queryConstant : Nat) : Polynomial Nat :=
  (Polynomial.X + 1) ^ randomConstant * Polynomial.C queryConstant

@[simp] theorem finiteOracleCertificateBound_eval
    (randomConstant queryConstant inputLength : Nat) :
    (finiteOracleCertificateBound randomConstant queryConstant).eval inputLength =
      (inputLength + 1) ^ randomConstant * queryConstant := by
  simp [finiteOracleCertificateBound]

/-- Logarithmic randomness and a constant query bound make the serialized
reachable proof polynomially short on the eventual (large-input) branch. -/
theorem queriedPositions_card_le_certificatePolynomial
    (checker : Checker) (randomConstant queryConstant threshold : Nat)
    (randomBound : forall input : Word, threshold <= input.length ->
      checker.randomLength input <=
        randomConstant * Nat.log2 (input.length + 1))
    (queryBound : forall input randomness,
      randomness.length = checker.randomLength input ->
        (checker.queries (input, randomness)).length <= queryConstant)
    (input : Word) (large : threshold <= input.length) :
    (queriedPositions checker input).card <=
      (finiteOracleCertificateBound randomConstant queryConstant).eval
        input.length := by
  rw [finiteOracleCertificateBound_eval]
  calc
    (queriedPositions checker input).card <=
        2 ^ checker.randomLength input * queryConstant :=
      queriedPositions_card_le checker input queryConstant (queryBound input)
    _ <= (input.length + 1) ^ randomConstant * queryConstant := by
      apply Nat.mul_le_mul_right
      calc
        2 ^ checker.randomLength input <=
            2 ^ (randomConstant * Nat.log2 (input.length + 1)) :=
          Nat.pow_le_pow_right (by decide) (randomBound input large)
        _ = (2 ^ Nat.log2 (input.length + 1)) ^ randomConstant := by
          rw [Nat.mul_comm, pow_mul]
        _ <= (input.length + 1) ^ randomConstant :=
          Nat.pow_le_pow_left (Nat.log2_self_le (by omega)) randomConstant

#print axioms finiteOraclePositionEquiv
#print axioms FiniteOracle.encode
#print axioms FiniteOracle.decode
#print axioms FiniteOracle.encode_length
#print axioms FiniteOracle.decode_encode
#print axioms FiniteOracle.encode_decode_of_length
#print axioms FiniteOracle.encode_injective
#print axioms binaryCertificate_characterization
#print axioms binaryCertificate_length_le
#print axioms finiteOracleCertificateBound
#print axioms finiteOracleCertificateBound_eval
#print axioms queriedPositions_card_le_certificatePolynomial

end Stage1Instances.THM_M_0729
