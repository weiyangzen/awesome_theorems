import Statement

/-!
# THM-M-0783 conditional obligation composition

This module checks the exact child-to-parent interface frozen by the obligation
registry. `solve` is deliberately an explicit premise: it is precisely the
open `MA` content and receives no proof credit here.
-/

namespace Stage1Instances.THM_M_0783.ObligationTree

universe u

/-- The substantive open obligation after all binders and forcing conventions
have been exposed. -/
abbrev DenseFamilySolver := ExpandedMartinsAxiom.{u}

/-- Checked composition from the expanded obligation to the canonical target. -/
theorem root_of_denseFamilySolver (solve : DenseFamilySolver.{u}) :
    MartinsAxiom.{u} :=
  martinsAxiom_iff_expanded.mpr solve

#check DenseFamilySolver
#check root_of_denseFamilySolver
#print axioms root_of_denseFamilySolver

end Stage1Instances.THM_M_0783.ObligationTree
