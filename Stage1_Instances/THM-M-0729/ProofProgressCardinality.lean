import Statement

/-!
# THM-M-0729 finite-randomness proof progress

These lemmas make the frozen checker's finite random space and its
soundness-one-half boundary explicit. They support the enumeration and
certificate obligations but do not construct either directional PCP
inclusion.
-/

namespace Stage1Instances.THM_M_0729

/-- The frozen random-word representation has exactly the declared length. -/
@[simp] theorem randomWord_length {n : Nat} (coins : Fin n -> Bool) :
    (randomWord coins).length = n := by
  simp [randomWord]

/-- Converting a random word back to its coordinate function is lossless. -/
@[simp] theorem randomWord_get (randomness : Word) :
    randomWord (List.get randomness) = randomness := by
  exact List.ofFn_get randomness

/-- There are exactly `2 ^ n` random strings of length `n`. -/
theorem randomSpace_card (n : Nat) :
    (Finset.univ : Finset (Fin n -> Bool)).card = 2 ^ n := by
  simp

/-- All proof positions reachable from the finite random space. -/
def queriedPositions (checker : Checker) (input : Word) : Finset Nat :=
  (Finset.univ :
    Finset (Fin (checker.randomLength input) -> Bool)).biUnion fun coins =>
    (checker.queries (input, randomWord coins)).toFinset

/-- A finite assignment contains exactly the oracle bits reachable on an input. -/
abbrev FiniteOracle (checker : Checker) (input : Word) :=
  {position : Nat // position ∈ queriedPositions checker input} -> Bool

/-- Extend a finite reachable-position assignment to a total proof oracle. -/
def FiniteOracle.extend {checker : Checker} {input : Word}
    (assignment : FiniteOracle checker input) : Nat -> Bool := fun position =>
  if member : position ∈ queriedPositions checker input then
    assignment ⟨position, member⟩
  else false

/-- Every query made on a random word belongs to the reachable-position set. -/
theorem query_mem_queriedPositions (checker : Checker) (input : Word)
    (coins : Fin (checker.randomLength input) -> Bool) (position : Nat)
    (member : position ∈ checker.queries (input, randomWord coins)) :
    position ∈ queriedPositions checker input := by
  simp only [queriedPositions, Finset.mem_biUnion, Finset.mem_univ,
    List.mem_toFinset, true_and]
  exact ⟨coins, member⟩

/-- Checkers cannot distinguish total proof oracles that agree at every
position reachable from the finite random space for this input. -/
theorem accepts_congr_of_eq_on_queriedPositions
    (checker : Checker) (input : Word) (proof1 proof2 : Nat -> Bool)
    (agree : forall position, position ∈ queriedPositions checker input ->
      proof1 position = proof2 position) :
    forall coins,
      checker.accepts input proof1 coins = checker.accepts input proof2 coins := by
  intro coins
  simp only [Checker.accepts]
  congr 2
  simp only [oracleAnswers]
  apply List.map_congr_left
  intro position member
  exact agree position
    (query_mem_queriedPositions checker input coins position member)

/-- Universal acceptance depends on only the finite assignment of reachable
oracle positions, not on an arbitrary total proof oracle. -/
theorem finiteOracle_characterization (checker : Checker) (input : Word) :
    (Exists fun proof : Nat -> Bool => forall coins,
      checker.accepts input proof coins = true) <->
    Exists fun assignment : FiniteOracle checker input => forall coins,
      checker.accepts input assignment.extend coins = true := by
  constructor
  · rintro ⟨proof, acceptsAll⟩
    let assignment : FiniteOracle checker input := fun position => proof position
    refine ⟨assignment, ?_⟩
    intro coins
    rw [← accepts_congr_of_eq_on_queriedPositions
      checker input proof assignment.extend]
    · exact acceptsAll coins
    · intro position member
      simp only [FiniteOracle.extend, member, dite_true]
      rfl
  · rintro ⟨assignment, acceptsAll⟩
    exact ⟨assignment.extend, acceptsAll⟩

/-- There are exactly `2 ^ k` assignments to `k` reachable positions. -/
theorem finiteOracle_card (checker : Checker) (input : Word) :
    Fintype.card (FiniteOracle checker input) =
      2 ^ (queriedPositions checker input).card := by
  simp [FiniteOracle]

/-- The number of reachable oracle positions is controlled by the random-space
size times the uniform per-random-string query bound. -/
theorem queriedPositions_card_le
    (checker : Checker) (input : Word) (queryConstant : Nat)
    (queryBound : forall randomness : Word,
      randomness.length = checker.randomLength input ->
        (checker.queries (input, randomness)).length <= queryConstant) :
    (queriedPositions checker input).card <=
      2 ^ checker.randomLength input * queryConstant := by
  unfold queriedPositions
  rw [← randomSpace_card]
  apply Finset.card_biUnion_le_card_mul
  intro coins _member
  exact Nat.le_trans (List.toFinset_card_le _)
    (queryBound (randomWord coins) (randomWord_length coins))

/-- Half-soundness leaves at least as many rejecting coins as accepting coins. -/
theorem accepting_card_le_rejecting_card
    {checker : Checker} {language : Language}
    (sound : HasSoundnessHalf checker language) (input : Word)
    (notMember : Not (language input)) (proof : Nat -> Bool) :
    (Finset.univ.filter fun coins => checker.accepts input proof coins).card <=
      (Finset.univ.filter fun coins => checker.accepts input proof coins = false).card := by
  let accepted : Finset (Fin (checker.randomLength input) -> Bool) :=
    Finset.univ.filter fun coins => checker.accepts input proof coins
  have soundBound : 2 * accepted.card <=
      (Finset.univ : Finset (Fin (checker.randomLength input) -> Bool)).card :=
    sound input notMember proof
  have rejectingEq :
      (Finset.univ.filter fun coins => checker.accepts input proof coins = false) =
        Finset.univ.filter fun coins =>
          Not (checker.accepts input proof coins = true) := by
    ext coins
    cases checker.accepts input proof coins <;> simp
  have partition : accepted.card +
      (Finset.univ.filter fun coins =>
        Not (checker.accepts input proof coins = true)).card =
      (Finset.univ : Finset (Fin (checker.randomLength input) -> Bool)).card := by
    exact Finset.card_filter_add_card_filter_not _
  change accepted.card <=
    (Finset.univ.filter fun coins => checker.accepts input proof coins = false).card
  rw [rejectingEq]
  omega

/-- Half-soundness gives the concrete exponential accepting-count bound. -/
theorem accepting_card_double_le_two_pow
    {checker : Checker} {language : Language}
    (sound : HasSoundnessHalf checker language) (input : Word)
    (notMember : Not (language input)) (proof : Nat -> Bool) :
    2 * (Finset.univ.filter fun coins => checker.accepts input proof coins).card <=
      2 ^ checker.randomLength input := by
  simpa [randomSpace_card] using sound input notMember proof

/-- Half-soundness excludes universal acceptance even before the full reverse
direction packages a proof oracle into a finite certificate. -/
theorem has_rejecting_coins_of_soundness
    {checker : Checker} {language : Language}
    (sound : HasSoundnessHalf checker language) (input : Word)
    (notMember : Not (language input)) (proof : Nat -> Bool) :
    Exists fun coins => checker.accepts input proof coins = false := by
  have acceptingLeRejecting :=
    accepting_card_le_rejecting_card sound input notMember proof
  have nonemptyRandomSpace :
      0 < (Finset.univ :
        Finset (Fin (checker.randomLength input) -> Bool)).card := by
    simp
  by_contra noRejecting
  have rejectingEmpty :
      (Finset.univ.filter fun coins =>
        checker.accepts input proof coins = false).card = 0 := by
    rw [Finset.card_eq_zero]
    ext coins
    simp only [Finset.notMem_empty, iff_false, Finset.mem_filter,
      Finset.mem_univ, true_and]
    exact fun rejected => noRejecting ⟨coins, rejected⟩
  have acceptingEmpty :
      (Finset.univ.filter fun coins =>
        checker.accepts input proof coins).card = 0 := by
    omega
  have partition :
      (Finset.univ.filter fun coins =>
        checker.accepts input proof coins).card +
      (Finset.univ.filter fun coins =>
        Not (checker.accepts input proof coins = true)).card =
      (Finset.univ :
        Finset (Fin (checker.randomLength input) -> Bool)).card :=
    Finset.card_filter_add_card_filter_not _
  have rejectComplementEmpty :
      (Finset.univ.filter fun coins =>
        Not (checker.accepts input proof coins = true)).card = 0 := by
    rw [Finset.card_eq_zero]
    ext coins
    simp only [Finset.notMem_empty, iff_false, Finset.mem_filter,
      Finset.mem_univ, true_and]
    intro notAccepted
    apply noRejecting
    refine ⟨coins, ?_⟩
    cases accepted : checker.accepts input proof coins
    · rfl
    · exact False.elim (notAccepted accepted)
  omega

#print axioms randomWord_length
#print axioms randomWord_get
#print axioms randomSpace_card
#print axioms query_mem_queriedPositions
#print axioms accepts_congr_of_eq_on_queriedPositions
#print axioms finiteOracle_characterization
#print axioms finiteOracle_card
#print axioms queriedPositions_card_le
#print axioms accepting_card_le_rejecting_card
#print axioms accepting_card_double_le_two_pow
#print axioms has_rejecting_coins_of_soundness

end Stage1Instances.THM_M_0729
