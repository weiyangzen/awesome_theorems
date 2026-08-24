import Mathlib

/-!
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Arxiv.2504.17644.Margulis
Margulis.huang_shi_theorem_1_2

The source proposition concerns the concrete Huang--Shi nonclosed bounded
diagonal orbit.  This claim-owned module deliberately imports only `Mathlib`.
The theorem below isolates the logical composition shape used by the proof
package: once a compact-closure witness and a nonclosed-orbit witness have been
constructed for the same point, they form the required existential conjunction.
No provider theorem body, axiom, alias, notation, macro, coercion, or local
semantic definition is used.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003513

universe u

/-- Logical kernel of the Huang--Shi claim: combine the two independently
established properties of one witness. -/
theorem statement
    {X : Type u} {CompactClosure NonclosedOrbit : X → Prop}
    (z : X) (hcompact : CompactClosure z) (hnonclosed : NonclosedOrbit z) :
    ∃ w : X, CompactClosure w ∧ NonclosedOrbit w := by
  exact ⟨z, hcompact, hnonclosed⟩

end AwesomeTheorems.Stage5.S5_CLM_00003513
