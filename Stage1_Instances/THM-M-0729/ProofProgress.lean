import Statement

/-!
# THM-M-0729 proof progress

These lemmas expose a substantive semantic consequence of the frozen
finite-cardinality soundness definition. They do not construct either of the
two directional PCP inclusions and therefore do not close the canonical root.
-/

namespace Stage1Instances.THM_M_0729

/-- A proof accepted for every random string cannot exist on a no-instance.
The argument also covers the zero-randomness boundary because the finite
function space then has cardinality one. -/
theorem accepts_all_implies_language
    {checker : Checker} {language : Language}
    (sound : HasSoundnessHalf checker language) (input : Word)
    (proof : Nat -> Bool)
    (acceptsAll : forall coins, checker.accepts input proof coins = true) :
    language input := by
  by_contra notMember
  have soundBound := sound input notMember proof
  have allAccepted :
      (Finset.univ.filter fun coins => checker.accepts input proof coins).card =
        (Finset.univ :
          Finset (Fin (checker.randomLength input) -> Bool)).card := by
    congr 1
    ext coins
    simp [acceptsAll coins]
  rw [allAccepted] at soundBound
  have nonemptyRandomSpace :
      0 < (Finset.univ :
        Finset (Fin (checker.randomLength input) -> Bool)).card := by
    simp
  omega

/-- Perfect completeness and soundness one half characterize membership by
the existence of one oracle proof accepted for every random string. -/
theorem language_iff_exists_accepts_all
    {checker : Checker} {language : Language}
    (complete : forall input : Word, language input ->
      exists proof : Nat -> Bool,
        forall coins, checker.accepts input proof coins = true)
    (sound : HasSoundnessHalf checker language) (input : Word) :
    language input <-> exists proof : Nat -> Bool,
      forall coins, checker.accepts input proof coins = true := by
  constructor
  · exact complete input
  · rintro ⟨proof, acceptsAll⟩
    exact accepts_all_implies_language sound input proof acceptsAll

/-- Every frozen PCP witness carries a checker whose universal-acceptance
semantics exactly characterize the language. Resource certificates remain in
the originating `InPCPLogConst` witness; this lemma isolates the semantic fact
needed before constructing the reverse-direction NP verifier. -/
theorem inPCPLogConst_has_semantic_characterization
    {language : Language} (h : InPCPLogConst language) :
    exists checker : Checker, forall input : Word,
      language input <-> exists proof : Nat -> Bool,
        forall coins, checker.accepts input proof coins = true := by
  rcases h with
    ⟨checker, _randomConstant, _queryConstant, _threshold,
      _randomBound, _queryBound, complete, sound⟩
  exact ⟨checker, fun input =>
    language_iff_exists_accepts_all complete sound input⟩

/-- Every proof oracle is rejected on at least one random string for a
no-instance. This is the contrapositive form needed by the reverse direction. -/
theorem not_language_has_rejecting_coins
    {checker : Checker} {language : Language}
    (sound : HasSoundnessHalf checker language) (input : Word)
    (notMember : ¬ language input) :
    forall proof : Nat -> Bool, exists coins,
      checker.accepts input proof coins = false := by
  intro proof
  by_contra noRejectingCoins
  apply notMember
  apply accepts_all_implies_language sound input proof
  intro coins
  cases accepted : checker.accepts input proof coins
  · exact False.elim (noRejectingCoins ⟨coins, accepted⟩)
  · rfl

/-- A direct no-instance witness form of half-soundness: at least one random
string rejects each proposed proof oracle. -/
theorem hasSoundnessHalf_has_rejecting_coins
    {checker : Checker} {language : Language}
    (sound : HasSoundnessHalf checker language) :
    forall input : Word, (¬ language input) -> forall proof : Nat -> Bool,
      exists coins, checker.accepts input proof coins = false := by
  intro input notMember proof
  exact not_language_has_rejecting_coins sound input notMember proof

#print axioms accepts_all_implies_language
#print axioms language_iff_exists_accepts_all
#print axioms inPCPLogConst_has_semantic_characterization
#print axioms not_language_has_rejecting_coins
#print axioms hasSoundnessHalf_has_rejecting_coins

end Stage1Instances.THM_M_0729
