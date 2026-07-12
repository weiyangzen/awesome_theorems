import Mathlib.Geometry.Manifold.Diffeomorph

/-!
Pinned-environment substrate probe for the THM-M-0610 exact-statement blocker.

This checks only mathlib's general smooth-diffeomorphism API. It does not define instanton Floer
homology, its gauge-theoretic chain complex, an integral homology 3-sphere, auxiliary-choice
independence, or orientation-preserving invariance, so it is not the canonical target.
-/

#check Diffeomorph
#check Diffeomorph.refl
#check Diffeomorph.trans
