import Mathlib.Computability.TuringMachine.Computable
import Mathlib.Data.Fintype.Card

#check (Fin 2 -> Bool)
#check (Fintype.card (Fin 2 -> Bool))
#check Fintype.card_fun
#check Turing.FinTM2
#check Turing.TM2ComputableInPolyTime

