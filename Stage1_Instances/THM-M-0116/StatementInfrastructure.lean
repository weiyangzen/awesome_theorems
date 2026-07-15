import Mathlib.AlgebraicGeometry.AlgClosed.Basic
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.GroupTheory.Finiteness
import Mathlib.RingTheory.PicardGroup

/-!
# THM-M-0116 pinned statement-infrastructure probe

This file checks only adjacent pinned APIs for the exact-statement blocker. It
does not define a Neron-Severi group, algebraic equivalence of divisors, or the
canonical finite-generation target, and it receives no statement or proof
credit.
-/

open CategoryTheory
open AlgebraicGeometry

universe u

#check Scheme
#check Spec
#check IsAlgClosed
#check IsProper
#check Smooth
#check SmoothOfRelativeDimension
#check Proj.toSpecZero
#check AddGroup.FG
#check CommRing.Pic

#check_failure NeronSeveriGroup
#check_failure AlgebraicGeometry.IsProjective
