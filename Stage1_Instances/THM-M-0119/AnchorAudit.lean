import Mathlib.Algebra.Homology.LocalCohomology
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic

/-!
# THM-M-0119 immutable anchor probes

These probes elaborate nearby APIs in pinned mathlib. They provide ambient
scheme, properness, module-sheaf, sheaf-cohomology, and local-cohomology
infrastructure only. None states or proves Kawamata--Viehweg vanishing.
-/

open CategoryTheory AlgebraicGeometry

#check Scheme
#check Spec
#check IsProper
#check LocallyOfFiniteType
#check (fun X : Scheme => X.presheaf)
#check Scheme.Γ
#check Scheme.Modules
#check Scheme.Modules.presheaf
#check CategoryTheory.Sheaf.H
#check localCohomology
