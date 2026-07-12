import Mathlib.SetTheory.Ordinal.Basic
import Mathlib.SetTheory.Ordinal.Veblen

-- Discovery only: these semantic ordinal APIs do not select the proof-theoretic source claim.
#check Ordinal.lt_wf
#check WellFoundedLT.induction
#check Ordinal.epsilon0_eq_nfp
