import Mathlib.Topology.CWComplex.Classical.Finite
import Mathlib.Topology.VectorBundle.Basic

/-!
Elaboration probe for the THM-M-0575 exact-statement blocker.

This checks only that the pinned environment contains finite-CW-complex and
complex-vector-bundle substrate. It deliberately does not define topological
K-theory or Bott periodicity: neither an exact source formulation nor those
formal interfaces are present in the dossier and pinned mathlib tree.
-/

#check Topology.CWComplex
#check Topology.CWComplex.Finite
#check VectorBundle
