import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

open MeasureTheory
open scoped ContDiff

namespace Stage1.THM_M_1520

/-- Canonical coordinates `(q, p)` on a finite-dimensional phase space. -/
abbrev ConfigurationSpace (n : Nat) := EuclideanSpace Real (Fin n)

abbrev PhaseSpace (n : Nat) :=
  WithLp 2 (Prod (ConfigurationSpace n) (ConfigurationSpace n))

/-- The canonical symplectic rotation, with the convention `X_H = (dH/dp, -dH/dq)`. -/
def symplecticRotation {n : Nat} (v : PhaseSpace n) : PhaseSpace n :=
  WithLp.toLp 2 ((WithLp.ofLp v).2, -(WithLp.ofLp v).1)

/-- The Hamiltonian vector field in canonical coordinates. -/
noncomputable def hamiltonianVectorField {n : Nat} (H : PhaseSpace n -> Real) :
    PhaseSpace n -> PhaseSpace n :=
  fun z => symplecticRotation (gradient H z)

/-- Exact Lean target for Liouville's theorem: every globally defined `C^1` flow solving
Hamilton's equations for a `C^2` Hamiltonian preserves phase-space Lebesgue volume.

The flow law is explicit so that `Phi` denotes a flow rather than an unrelated family of ODE
solutions. The sign convention is `X_H = (dH/dp, -dH/dq)`. -/
def LiouvilleStatement : Prop :=
  forall (n : Nat) (H : PhaseSpace n -> Real) (Phi : Real -> PhaseSpace n -> PhaseSpace n),
    ContDiff Real 2 H ->
    (forall z, ContDiff Real 1 (fun t => Phi t z)) ->
    (forall t z, HasDerivAt (fun s => Phi s z) (hamiltonianVectorField H (Phi t z)) t) ->
    (forall z, Phi 0 z = z) ->
    (forall s t z, Phi (s + t) z = Phi s (Phi t z)) ->
    forall t, MeasurePreserving (Phi t) volume volume

#check LiouvilleStatement
#check (LiouvilleStatement : Prop)
set_option pp.all true in
#print LiouvilleStatement

end Stage1.THM_M_1520
