import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Projective
import Mathlib.LinearAlgebra.Projectivization.Action

/-!
# THM-M-0217 discovery-only intake probe

These checks authenticate adjacent pinned disk, convex-segment, projectivization, projective-action,
and projective general-linear-group interfaces. They do not select a Klein-model carrier or metric,
declare the target proposition, define a cross ratio, establish hyperbolic model laws, or supply
proof credit.
-/

open scoped LinearAlgebra.Projectivization MatrixGroups

#check Complex.UnitDisc
#check Complex.UnitDisc.norm_lt_one
#check convex_ball
#check segment
#check openSegment
#check Projectivization
#check Projectivization.mk
#check Projectivization.map
#check Projectivization.generalLinearGroup_smul_def
#check Matrix.ProjGenLinGroup
#check Matrix.ProjGenLinGroup.mk
