import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Computability.Language
import Mathlib.Computability.Reduce

/-!
Discovery-only checks for pinned APIs adjacent to the THM-M-0873 theorem family.

These APIs can express graph isomorphism, formal languages, and computable reductions. They do not
define a finite-graph serialization, resource-bounded computation, quasipolynomial time, or the
source-selected graph-isomorphism complexity theorem.
-/

#check SimpleGraph.Iso
#check SimpleGraph.Iso.refl
#check SimpleGraph.Iso.symm
#check SimpleGraph.Iso.comp
#check Language
#check ManyOneReducible
#check OneOneReducible
