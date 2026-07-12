import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Computability.Language
import Mathlib.Computability.Reduce

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0876 catalog topic.

These APIs can express graph isomorphism, languages, and computable reductions. They do not select
an encoding of finite graphs or provide P, NP, quasipolynomial time, a graph-isomorphism algorithm,
or the catalog's missing truth-valued proposition.
-/

#check SimpleGraph.Iso
#check SimpleGraph.Iso.refl
#check SimpleGraph.Iso.symm
#check SimpleGraph.Iso.comp
#check Language
#check ManyOneReducible
#check OneOneReducible
