import Mathlib.AlgebraicGeometry.AlgClosed.Basic
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.GroupTheory.Finiteness
import Mathlib.RingTheory.PicardGroup

/-!
# THM-M-0116 exact-statement boundary probe

The frozen human claim concerns the concrete Neron-Severi group of a smooth
projective algebraic surface, defined by divisors modulo algebraic equivalence.
The pinned environment supplies the adjacent interfaces checked below, but not
all of the objects needed to encode that claim. This file therefore declares no
canonical target, alternate transport, mutation fixture, or proof body.
-/

open CategoryTheory
open AlgebraicGeometry

#check Scheme
#check Spec
#check IsAlgClosed
#check IsProper
#check Smooth
#check SmoothOfRelativeDimension
#check Proj.toSpecZero
#check AddCon
#check AddCon.Quotient
#check AddGroup.FG
#check CommRing.Pic

#check_failure NeronSeveriGroup
#check_failure AlgebraicGeometry.IsProjective
