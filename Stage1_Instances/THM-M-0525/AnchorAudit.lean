import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup

/-!
Pinned-candidate audit for THM-M-0525.  These checks expose the exact mathlib carrier and
operations used by the frozen statement; they do not implement the statement theorem.
-/

universe u

open CategoryTheory

namespace THM_M_0525.AnchorAudit

#check FundamentalGroup
#check instGroupFundamentalGroup
#check FundamentalGroupoid.instGroupoid
#check Path.Homotopic.Quotient.refl
#check Path.Homotopic.Quotient.trans
#check Path.Homotopic.Quotient.symm
#check Path.Homotopic.Quotient.refl_trans
#check Path.Homotopic.Quotient.trans_refl
#check Path.Homotopic.Quotient.trans_assoc
#check Path.Homotopic.Quotient.trans_symm
#check Path.Homotopic.Quotient.symm_trans

-- The public fundamental-group carrier unfolds to the endpoint-fixed path quotient.
example (X : Type u) [TopologicalSpace X] (x : X) :
    FundamentalGroup X x = Path.Homotopic.Quotient x x := rfl

-- `End` multiplication reverses categorical composition, so this inherited group is not an exact
-- operation-level anchor for Statement.lean's forward `trans p q` multiplication.
example (X : Type u) [TopologicalSpace X] (x : X)
    (p q : FundamentalGroup X x) : p * q = q.trans p := rfl

example (X : Type u) [TopologicalSpace X] (x : X) :
    (1 : FundamentalGroup X x) = Path.Homotopic.Quotient.refl x := rfl

example (X : Type u) [TopologicalSpace X] (x : X)
    (p : FundamentalGroup X x) : p⁻¹ = p.symm := rfl

#print axioms Path.Homotopic.Quotient.refl_trans
#print axioms Path.Homotopic.Quotient.trans_refl
#print axioms Path.Homotopic.Quotient.trans_assoc
#print axioms Path.Homotopic.Quotient.trans_symm
#print axioms Path.Homotopic.Quotient.symm_trans

end THM_M_0525.AnchorAudit
