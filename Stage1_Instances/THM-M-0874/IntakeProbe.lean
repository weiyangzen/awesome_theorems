import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Computability.Language
import Mathlib.Computability.Reduce
import Mathlib.Computability.TuringMachine.Computable

/-!
Discovery-only checks for pinned APIs adjacent to the THM-M-0874 theorem family.

These APIs express graph isomorphisms, languages, computable reductions, and Turing-machine time
bounds. They do not define a finite graph serialization, the Graph Isomorphism decision language,
a polynomial-resource reduction, a quasipolynomial bound, Babai's algorithm, or its proof.
-/

#check SimpleGraph.Iso
#check SimpleGraph.Iso.refl
#check SimpleGraph.Iso.symm
#check SimpleGraph.Iso.comp
#check Language
#check ManyOneReducible
#check OneOneReducible
#check Turing.TM2OutputsInTime
#check Turing.TM2ComputableInTime
#check Turing.TM2ComputableInPolyTime
