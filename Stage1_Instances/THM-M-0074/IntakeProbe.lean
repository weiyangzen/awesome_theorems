import Mathlib.Data.Finite.Card
import Mathlib.GroupTheory.Subgroup.Simple

/-!
# THM-M-0074 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to possible future encodings of Monster-group
existence. They do not define the Monster, select the source statement, construct the Griess
algebra, or state or prove the Griess theorem.
-/

namespace Stage1Instances.THM_M_0074

/-- Exact order recorded by the 1981 construction announcement; not a Monster definition. -/
def monsterOrderEnvelope : ℕ :=
  2 ^ 46 * 3 ^ 20 * 5 ^ 9 * 7 ^ 6 * 11 ^ 2 * 13 ^ 3 * 17 * 19 * 23 * 29 * 31 * 41 *
    47 * 59 * 71

/-- Candidate statement envelope only. It omits the source-selected construction/identity data. -/
def monsterExistenceEnvelope : Prop :=
  ∃ (G : Type) (group : Group G),
    @IsSimpleGroup G group ∧ Finite G ∧ @Nat.card G = monsterOrderEnvelope

#check Finite
#check Nat.card
#check Nat.card_congr
#check IsSimpleGroup
#check isSimpleGroup_iff
#check MulEquiv
#check MulEquiv.isSimpleGroup
#check MulEquiv.isSimpleGroup_congr
#check Finite.card_pos
#check monsterOrderEnvelope
#check monsterExistenceEnvelope

example {G H : Type*} [Group G] [Group H] (e : G ≃* H) :
    IsSimpleGroup G ↔ IsSimpleGroup H :=
  e.isSimpleGroup_congr

example {G : Type*} [Finite G] [Nonempty G] : 0 < Nat.card G :=
  Finite.card_pos

end Stage1Instances.THM_M_0074
