import Mathlib.Computability.PartrecCode
import Mathlib.InformationTheory.Coding.KraftMcMillan

/-!
# THM-M-1583 discovery-only intake probe

These checks authenticate adjacent pinned partial-recursive-code and finite coding APIs. They do
not turn the catalog's algorithmic-information-theory field label into a proposition, define a
source-selected complexity or universal prefix machine, or prove THM-M-1583.
-/

#check Nat.Partrec.Code
#check Nat.Partrec.Code.encodeCode
#check Nat.Partrec.Code.eval
#check Nat.Partrec.Code.exists_code
#check Nat.Partrec.Code.eval_part
#check InformationTheory.UniquelyDecodable
#check InformationTheory.kraft_mcmillan_inequality
