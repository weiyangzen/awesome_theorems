import Mathlib.Topology.Compactness.Compact

/-!
# THM-M-0617 discovery-only intake probe

These checks authenticate the two direct compactness interfaces in the pinned mathlib snapshot.
They do not freeze a canonical conjunction, establish source-statement identity, or credit either
upstream proof body to the target.
-/

#check IsCompact
#check IsCompact.of_isClosed_subset
#check IsCompact.image_of_continuousOn
#check IsCompact.image

#print axioms IsCompact.of_isClosed_subset
#print axioms IsCompact.image
