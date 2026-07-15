import Statement

/-!
# THM-M-0812 obligation-tree composition harness

This module checks only the interfaces and child-to-parent composition selected
by the frozen obligation registry. The difficult matching-to-cover construction
is an explicit hypothesis. No proof of that construction or of the root theorem
is asserted here.
-/

namespace Stage1Instances.THM_M_0812_Obligations

universe uL uR uE

open Stage1Instances.THM_M_0812

/-- Finite matching candidates attain a maximum cardinality. This package is
split from the alternating-path construction so root composition records the
attainment boundary explicitly. -/
def MatchingAttainmentTarget : Prop :=
  forall {L : Type uL} {R : Type uR} {E : Type uE} [Finite E]
    (left : E -> L) (right : E -> R),
    exists k : Nat, HasMatchingNumber left right k

/-- Every matching has at most as many edges as any vertex cover. -/
def WeakDualityTarget : Prop :=
  forall {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (M : Set E)
    (CLeft : Set L) (CRight : Set R),
    IsEdgeMatching left right M ->
      IsBipartiteVertexCover left right CLeft CRight ->
        M.ncard <= CLeft.ncard + CRight.ncard

/-- The hard source-facing construction: a maximum matching of size `k`
produces a vertex cover of the same size. This is an open proof interface. -/
def MaximumMatchingCoverTarget : Prop :=
  forall {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (k : Nat),
    HasMatchingNumber left right k ->
      exists CLeft : Set L, exists CRight : Set R,
        IsBipartiteVertexCover left right CLeft CRight /\
          CLeft.ncard + CRight.ncard = k

/-- Exact pair of proof packages consumed by root composition. -/
def AssemblyTarget : Prop :=
  MatchingAttainmentTarget.{uL, uR, uE} /\
    MaximumMatchingCoverTarget.{uL, uR, uE} /\
      WeakDualityTarget.{uL, uR, uE}

/-- Both typed proof packages are consumed by the assembly. -/
theorem assembly_of_construction_and_duality
    (attainment : MatchingAttainmentTarget.{uL, uR, uE})
    (construction : MaximumMatchingCoverTarget.{uL, uR, uE})
    (duality : WeakDualityTarget.{uL, uR, uE}) :
    AssemblyTarget.{uL, uR, uE} :=
  ⟨attainment, construction, duality⟩

/-- Conditional exact child-to-root certificate. It chooses a maximum matching
by finiteness, applies the open construction, and derives cover minimality from
weak duality. -/
theorem root_of_assembly
    (assembly : AssemblyTarget.{uL, uR, uE}) :
    KonigMatchingCoverTarget.{uL, uR, uE} := by
  intro L R E _ _ _ left right
  rcases assembly.1 left right with ⟨k, hMatching⟩
  rcases assembly.2.1 left right k hMatching with ⟨CLeft, CRight, hCover, hCard⟩
  refine ⟨k, hMatching, ⟨⟨CLeft, CRight, hCover, hCard⟩, ?_⟩⟩
  intro DLeft DRight hDCover
  rcases hMatching.1 with ⟨M, hM, hMCard⟩
  rw [← hMCard]
  exact assembly.2.2 left right M DLeft DRight hM hDCover

/-- Combined conditional root harness. Neither proof child is inhabited here. -/
theorem root_of_construction_and_duality
    (attainment : MatchingAttainmentTarget.{uL, uR, uE})
    (construction : MaximumMatchingCoverTarget.{uL, uR, uE})
    (duality : WeakDualityTarget.{uL, uR, uE}) :
    KonigMatchingCoverTarget.{uL, uR, uE} :=
  root_of_assembly
    (assembly_of_construction_and_duality attainment construction duality)

#check MatchingAttainmentTarget
#check WeakDualityTarget
#check MaximumMatchingCoverTarget
#check AssemblyTarget
#check assembly_of_construction_and_duality
#check root_of_assembly
#check root_of_construction_and_duality

#print axioms assembly_of_construction_and_duality
#print axioms root_of_assembly
#print axioms root_of_construction_and_duality

end Stage1Instances.THM_M_0812_Obligations
