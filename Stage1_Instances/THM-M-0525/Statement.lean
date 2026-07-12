import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup

/-!
The exact target packages a group structure on based path-homotopy classes and fixes its three
operations to concatenation, the constant loop, and reversal.  The laws are carried by `Group`;
the equations prevent an unrelated group structure on the same carrier from satisfying the target.
-/

universe u

namespace THM_M_0525

abbrev BasedLoopClass (X : Type u) [TopologicalSpace X] (x : X) :=
  Path.Homotopic.Quotient x x

structure CanonicalBasedLoopGroup (X : Type u) [TopologicalSpace X] (x : X) where
  group : Group (BasedLoopClass X x)
  mul_eq : forall p q : BasedLoopClass X x,
    @Mul.mul (BasedLoopClass X x) group.toMul p q = Path.Homotopic.Quotient.trans p q
  one_eq :
    @One.one (BasedLoopClass X x) group.toOne = Path.Homotopic.Quotient.refl x
  inv_eq : forall p : BasedLoopClass X x,
    @Inv.inv (BasedLoopClass X x) group.toInv p = Path.Homotopic.Quotient.symm p

/-- Exact formal target for THM-M-0525. -/
def Statement (X : Type u) [TopologicalSpace X] (x : X) : Prop :=
  Nonempty (CanonicalBasedLoopGroup X x)

-- The mathlib vertex-group carrier is definitionally the carrier frozen above.
example (X : Type u) [TopologicalSpace X] (x : X) :
    FundamentalGroup X x = BasedLoopClass X x := rfl

-- Binder order, universe, and typeclass context are deliberately explicit here.
#check @Statement
#print Statement

-- Boundary witness: the target elaborates at the unique point of the one-point space.
#check Statement PUnit PUnit.unit

end THM_M_0525
