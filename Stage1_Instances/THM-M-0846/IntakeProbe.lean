import Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma
import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.MeasureTheory.Integral.Prod

/-!
# THM-M-0846 discovery-only intake probe

These checks authenticate pinned finite-graph density, graph-homomorphism, regularity, measurable
function, product-measure, and Fubini interfaces adjacent to dense graph limits. They do not define
homomorphism density for graph sequences, select one Lovasz-Szegedy result, define a graphon
quotient, or prove THM-M-0846.
-/

#check SimpleGraph
#check SimpleGraph.Hom
#check SimpleGraph.edgeDensity
#check SimpleGraph.edgeDensity_nonneg
#check SimpleGraph.edgeDensity_le_one
#check szemeredi_regularity
#check Measurable
#check MeasureTheory.Measure.prod
#check MeasureTheory.integral_prod

#print axioms SimpleGraph.edgeDensity_nonneg
#print axioms SimpleGraph.edgeDensity_le_one
#print axioms szemeredi_regularity
