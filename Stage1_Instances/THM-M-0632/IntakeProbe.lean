import Mathlib.Topology.Baire.CompleteMetrizable
import Mathlib.Topology.Baire.LocallyCompactRegular

/-!
# THM-M-0632 discovery-only intake probe

These checks authenticate distinct adjacent pinned Baire-space interfaces. They do not select a
canonical meaning of "Baire-Hausdorff theorem" or provide a proof body for the catalog phrase
"properties of Baire spaces."
-/

#check BaireSpace
#check BaireSpace.baire_property
#check dense_iInter_of_isOpen
#check IsGδ.baireSpace_of_dense
#check mem_residual
#check not_isMeagre_of_isOpen
#check BaireSpace.of_completelyPseudoMetrizable
#check BaireSpace.of_t2Space_locallyCompactSpace
#check IsGδ.of_t2Space_locallyCompactSpace
