import Mathlib.FieldTheory.Galois.Abelian
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.Topology.Algebra.IsOpenUnits

/-!
# THM-M-0422 statement boundary probe

The intake claim is global reciprocity together with the existence/classification theorem for
finite abelian extensions of a number field. Pinned mathlib has the algebraic extension class and
the adele ring, but not the correctly topologized ideles, idele norms, global Artin map, or class
field correspondence needed to encode that claim. This module checks only those pinned boundary
interfaces. It deliberately declares no proxy target, abstract caller-supplied reciprocity data, or
canonical global class field theory proposition.
-/

namespace Stage1Instances.THM_M_0422

#check IsAbelianGalois
#check NumberField.AdeleRing
#check NumberField.AdeleRing.algebraMap_injective
#check NumberField.AdeleRing.principalSubgroup
#check IsOpenUnits

end Stage1Instances.THM_M_0422
