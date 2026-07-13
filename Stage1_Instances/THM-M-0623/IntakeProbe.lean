import Mathlib.Topology.Metrizable.Urysohn

/-!
# THM-M-0623 discovery-only intake probe

These checks authenticate the pinned separation, countability, metrization, and l-infinity
interfaces relevant to the Urysohn metrization family. They do not choose whether the catalogue's
"regular" includes T0, select a canonical target, prove a source transport, or confer root proof
credit.
-/

#check RegularSpace
#check T0Space
#check T3Space
#check SecondCountableTopology
#check TopologicalSpace.PseudoMetrizableSpace
#check TopologicalSpace.MetrizableSpace
#check RegularSpace.t3Space_iff_t0Space
#check TopologicalSpace.exists_isInducing_l_infty
#check TopologicalSpace.PseudoMetrizableSpace.of_regularSpace_secondCountableTopology
#check TopologicalSpace.exists_embedding_l_infty
#check TopologicalSpace.metrizableSpace_of_t3_secondCountable

#print axioms TopologicalSpace.PseudoMetrizableSpace.of_regularSpace_secondCountableTopology
#print axioms TopologicalSpace.metrizableSpace_of_t3_secondCountable

/-! The two-point indiscrete space checks the convention boundary used by the intake. -/

example : @RegularSpace Bool ⊤ := by
  letI : TopologicalSpace Bool := ⊤
  constructor
  intro s a hs ha
  rw [IndiscreteTopology.isClosed_iff] at hs
  rcases hs with rfl | rfl
  · simp
  · simp at ha

example : @SecondCountableTopology Bool ⊤ := by infer_instance

example : ¬ @T0Space Bool ⊤ := by
  intro h
  letI : TopologicalSpace Bool := ⊤
  letI : T0Space Bool := h
  exact Bool.false_ne_true (Inseparable.all false true).eq

example : ¬ @TopologicalSpace.MetrizableSpace Bool ⊤ := by
  intro h
  letI : TopologicalSpace Bool := ⊤
  letI : TopologicalSpace.MetrizableSpace Bool := h
  exact Bool.false_ne_true (Inseparable.all false true).eq
