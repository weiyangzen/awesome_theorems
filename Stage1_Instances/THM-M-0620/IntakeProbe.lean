import Mathlib.Topology.Compactness.Compact

/-!
# THM-M-0620 discovery-only intake probe

These checks authenticate pinned compact-product interfaces and selected boundary instances. They
do not select a canonical source formulation, freeze an exact target, or prove `THM-M-0620`.
-/

#check isCompact_pi_infinite
#check isCompact_univ_pi
#check Pi.compactSpace
#check isCompact_empty

#synth CompactSpace Empty
#synth CompactSpace (Empty → Empty)
#synth CompactSpace (Bool → Empty)

section

universe u v

variable {I : Type u} {X : I → Type v}
variable [∀ i, TopologicalSpace (X i)] [∀ i, CompactSpace (X i)]

#check (inferInstance : CompactSpace (∀ i, X i))

end


#print axioms isCompact_pi_infinite
#print axioms isCompact_univ_pi
#print axioms Pi.compactSpace
