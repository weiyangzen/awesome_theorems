import Mathlib.Topology.Homotopy.Lifting

/-!
# THM-M-0236 discovery-only intake probe

These checks authenticate pinned abstract homotopy-lifting interfaces relevant to the monodromy
theorem family. They do not construct an etale space of analytic germs, define analytic
continuation, select the repository's exact target, or add a proof body.
-/

#check IsLocalHomeomorph.monodromy_theorem
#check SimplyConnectedSpace.paths_homotopic
#check IsCoveringMap.existsUnique_continuousMap_lifts

#print axioms IsLocalHomeomorph.monodromy_theorem
