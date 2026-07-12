import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Set.Card
import Mathlib.ModelTheory.Definability
import Mathlib.NumberTheory.Height.Basic
import Mathlib.RingTheory.MvPolynomial.Basic
import Mathlib.Topology.Connected.Basic

/-!
# THM-M-0464 pinned-mathlib anchor audit

This module checks the library ingredients available to the frozen statement. It does not state
or prove Pila-Wilkie.
-/

namespace AwesomeTheorems.THM_M_0464.AnchorAudit

open Set

noncomputable section

/-- Mathlib has the first-order definability surface, but no o-minimal structure API was found. -/
example (L : FirstOrder.Language) [L.Structure Real]
    (X : Set (Fin n -> Real)) : Prop :=
  (Set.univ : Set Real).Definable L X

/-- Multivariate real polynomials support the dossier's semialgebraic syntax. -/
example (p : MvPolynomial (Fin n) Real) (x : Fin n -> Real) : Real :=
  MvPolynomial.eval x p

/-- Connectedness and non-singleton predicates support the algebraic-part boundary. -/
example (A : Set (Fin n -> Real)) : Prop :=
  IsConnected A /\ Not A.Subsingleton

/-- Explicit finiteness and `ncard` support the counting conclusion. -/
example (S : Set (Fin n -> Rat)) : Prop :=
  S.Finite /\ (S.ncard : Real) <= 1

/-- Real powers support the source exponent. -/
example (T : Nat) (epsilon : Real) : Real :=
  (T : Real) ^ epsilon

#check Set.Definable
#check MvPolynomial.eval
#check IsConnected
#check Set.Subsingleton
#check Set.ncard
#check Real.rpow

end

end AwesomeTheorems.THM_M_0464.AnchorAudit
