import Mathlib.Topology.UniformSpace.HeineCantor

/-!
# THM-M-0633 discovery-only intake probe

These checks authenticate the two direct pinned Heine-Cantor interfaces and their adjacent
predicates. They do not select the catalog's exact source statement, freeze a canonical target,
audit terminal proof bodies, or supply proof credit.
-/

#check IsCompact
#check CompactSpace
#check Continuous
#check ContinuousOn
#check UniformContinuous
#check UniformContinuousOn
#check IsCompact.uniformContinuousOn_of_continuous
#check CompactSpace.uniformContinuous_of_continuous
#check IsCompact.uniformContinuousAt_of_continuousAt

#print axioms IsCompact.uniformContinuousOn_of_continuous
#print axioms CompactSpace.uniformContinuous_of_continuous
