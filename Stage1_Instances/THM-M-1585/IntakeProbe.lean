import Mathlib.InformationTheory.Coding.KraftMcMillan
import Mathlib.InformationTheory.Hamming

/-!
# THM-M-1585 discovery-only intake probe

These checks authenticate pinned Hamming-space, uniquely-decodable-code, and Kraft-McMillan
interfaces adjacent to coding theory. They do not select an error-correcting-code model, combine
the catalog's neighboring theorem families, or state or prove a canonical THM-M-1585 target.
-/

#check hammingDist
#check hammingDist_triangle
#check hammingDist_le_card_fintype
#check Hamming
#check Hamming.dist_eq_hammingDist
#check InformationTheory.UniquelyDecodable
#check InformationTheory.UniquelyDecodable.epsilon_not_mem
#check InformationTheory.UniquelyDecodable.flatten_injective
#check InformationTheory.kraft_mcmillan_inequality

#print axioms hammingDist_triangle
#print axioms InformationTheory.UniquelyDecodable.flatten_injective
#print axioms InformationTheory.kraft_mcmillan_inequality
