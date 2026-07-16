import Mathlib.Algebra.Homology.SpectralObject.HasSpectralSequence
import Mathlib.Topology.FiberBundle.Basic

/-!
# THM-M-0555 statement boundary

The repository source supplies only "the homology spectral sequence of a
fibration". It does not select the fibration model, coefficients and local
system, ordered hypotheses, page convention, or convergence statement needed
for one exact Serre proposition. This file therefore checks only two pinned
interfaces common to unresolved interpretations. It deliberately declares no
canonical target or transport.
-/

open CategoryTheory

#check FiberBundle
#check Abelian.SpectralObject.coreE₂HomologicalNat
