import Mathlib.Algebra.Homology.SpectralObject.SpectralSequence
import Mathlib.Topology.FiberBundle.Basic

/-!
# THM-M-0556 statement boundary

The repository source says only "the spectral sequence of a fibration". It
does not select the variance, coefficients, fibration model, page convention,
or convergence claim needed for one exact Leray-Serre proposition. This file
therefore checks only the two pinned interfaces common to the unresolved
interpretations. It deliberately declares no canonical target or transport.
-/

open CategoryTheory

#check FiberBundle
#check E₂CohomologicalSpectralSequenceNat

