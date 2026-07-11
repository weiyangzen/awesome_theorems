import Mathlib.Algebra.Homology.SpectralObject.SpectralSequence
import Mathlib.Topology.FiberBundle.Basic

/-!
Elaboration probe for the THM-M-0556 statement blocker.

This file checks only that the pinned environment contains the two independent
substrates named by the source claim. It deliberately does not define a
Leray-Serre target: the source phrase does not fix enough mathematics to do so
without choosing a stronger or narrower theorem.
-/

open CategoryTheory

#check FiberBundle
#check E₂CohomologicalSpectralSequenceNat

