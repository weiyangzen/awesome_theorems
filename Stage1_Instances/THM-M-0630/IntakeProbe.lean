import Mathlib.Topology.Category.CompHaus.Basic
import Mathlib.Topology.Separation.CompletelyRegular

/-!
# THM-M-0630 discovery-only intake probe

These commands authenticate pinned Stone-Cech construction, complete-regularity, dense-embedding,
extension, uniqueness, and categorical universal-property interfaces. They do not select the
catalog's exact statement, establish a source-to-Lean transport, or prove THM-M-0630.
-/

#check StoneCech
#check stoneCechUnit
#synth CompactSpace (StoneCech PUnit)
#synth T2Space (StoneCech PUnit)
#check continuous_stoneCechUnit
#check denseRange_stoneCechUnit
#check isDenseInducing_stoneCechUnit
#check isDenseEmbedding_stoneCechUnit
#check stoneCechExtend
#check stoneCechExtend_extends
#check continuous_stoneCechExtend
#check stoneCech_hom_ext
#check stoneCechEquivalence
#check topToCompHaus

#print axioms continuous_stoneCechUnit
#print axioms denseRange_stoneCechUnit
#print axioms isDenseEmbedding_stoneCechUnit
#print axioms stoneCechExtend_extends
#print axioms continuous_stoneCechExtend
#print axioms stoneCech_hom_ext
