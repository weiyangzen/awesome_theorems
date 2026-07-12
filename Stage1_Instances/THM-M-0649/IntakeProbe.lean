import Mathlib.ModelTheory.DirectLimit
import Mathlib.ModelTheory.ElementarySubstructures

open FirstOrder

namespace Stage1.THM_M_0649.IntakeProbe

open FirstOrder.Language

#check Language.ElementaryEmbedding
#check Language.ElementarySubstructure
#check Language.Substructure.IsElementary
#check Language.Substructure.isElementary_of_exists
#check Language.Substructure.mem_iSup_of_directed
#check Language.DirectLimit.of
#check Language.DirectLimit.Equiv_iSup

universe u v w

variable {L : Language.{u, v}} {M : Type w} [L.Structure M]

-- This checks the common-ambient union carrier lemma needed by one faithful encoding.
example {ι : Type*} [Nonempty ι] (S : ι → L.Substructure M)
    (hS : Directed (· ≤ ·) S) (x : M) :
    x ∈ iSup S ↔ ∃ i, x ∈ S i :=
  Language.Substructure.mem_iSup_of_directed hS

end Stage1.THM_M_0649.IntakeProbe
