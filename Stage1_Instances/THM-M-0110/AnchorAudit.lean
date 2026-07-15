import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Topology.Sheaves.Abelian

/-!
# THM-M-0110 pinned anchor-audit probes

These probes bind the retained mathlib candidates to the repository's pinned
environment. They check only general sheaf cohomology, two stronger vanishing
routes, and one projective-spectrum properness interface. None is Kodaira
vanishing, and no declaration below connects the frozen target's semantic
labels to its actual sheaves.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits AlgebraicGeometry

universe u

namespace Stage1Instances.THMM0110.AnchorAudit

/-- The target-owned data surface, repeated only so the probe is standalone. -/
structure AuditedData (k : Type u) [Field k] where
  X : Scheme.{u}
  KTensorL : X.Modules

/-- The exact concrete cohomology carrier used by the frozen statement. -/
abbrev AuditedCohomology {k : Type u} [Field k]
    (D : AuditedData.{u} k) (i : Nat) : Type u :=
  ((SheafOfModules.toSheaf D.X.ringCatSheaf).obj D.KTensorL).H i

/--
The pinned zero-sheaf lemma reaches the target's concrete carrier only after
adding an `IsZero` premise absent from Kodaira's hypotheses.
-/
theorem subsingletonCohomology_of_isZero {k : Type u} [Field k]
    (D : AuditedData.{u} k)
    (hZero : IsZero ((SheafOfModules.toSheaf D.X.ringCatSheaf).obj D.KTensorL))
    (i : Nat) : Subsingleton (AuditedCohomology D i) :=
  Sheaf.subsingleton_H_of_isZero hZero i

def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

def retainedCandidateNames : List String := [
  "CategoryTheory.Sheaf.H",
  "CategoryTheory.Sheaf.subsingleton_H_of_isZero",
  "CategoryTheory.Abelian.Ext.subsingleton_of_injective",
  "AlgebraicGeometry.Proj.isProper"
]

def missingTerminalInterfaces : List String := [
  "projectivity predicate connected to the frozen structure map",
  "canonical or dualizing sheaf connected to K",
  "invertible ample line-bundle structure connected to L",
  "native tensor product identifying KTensorL with K tensor L",
  "Kodaira vanishing terminal theorem for the frozen exact target"
]

#check CategoryTheory.Sheaf.H
#check CategoryTheory.Sheaf.subsingleton_H_of_isZero
#check CategoryTheory.Abelian.Ext.subsingleton_of_injective
#check subsingletonCohomology_of_isZero

example {σ A : Type*} [CommRing A] [SetLike σ A] [AddSubgroupClass σ A]
    (𝒜 : Nat → σ) [GradedRing 𝒜] [Algebra.FiniteType (𝒜 0) A] :
    IsProper (Proj.toSpecZero 𝒜) := by
  infer_instance

#print axioms CategoryTheory.Sheaf.subsingleton_H_of_isZero
#print axioms CategoryTheory.Abelian.Ext.subsingleton_of_injective
#print axioms subsingletonCohomology_of_isZero

end Stage1Instances.THMM0110.AnchorAudit
