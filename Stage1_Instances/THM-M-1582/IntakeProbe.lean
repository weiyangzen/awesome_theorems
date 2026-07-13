import Mathlib.Computability.Encoding
import Mathlib.Computability.PartrecCode
import Mathlib.Computability.TuringMachine.Computable

/-!
# THM-M-1582 discovery-only intake probe

These checks authenticate pinned encoding, partial-recursive program, evaluator, universality, and
Turing-machine interfaces adjacent to a possible future Kolmogorov-complexity encoding. They do not
select a complexity convention, define a shortest-description function, state an invariance
theorem, or prove THM-M-1582.
-/

#check Computability.Encoding
#check Computability.FinEncoding
#check Computability.finEncodingNatBool
#check Nat.Partrec.Code
#check Nat.Partrec.Code.eval
#check Nat.Partrec.Code.exists_code
#check Turing.FinTM2
#check Turing.TM2Outputs
#check Turing.TM2Computable
