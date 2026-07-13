import Mathlib.Computability.TuringMachine.Computable
import Mathlib.Probability.Distributions.Uniform

/-!
# THM-M-1596 discovery-only intake probe

These checks authenticate adjacent pinned uniform-probability and polynomial-time computation APIs.
They do not define a cryptographic primitive, security game, adversary, or advantage; select a
canonical proposition; or prove any cryptography theorem.
-/

#check PMF
#check PMF.uniformOfFinset
#check PMF.uniformOfFintype
#check Turing.FinTM2
#check Turing.TM2Computable
#check Turing.TM2ComputableInPolyTime
