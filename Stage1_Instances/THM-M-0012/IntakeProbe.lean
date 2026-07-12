import Mathlib.Analysis.Complex.Polynomial.Basic

/-!
# THM-M-0012 discovery-only intake probe

These checks authenticate the pinned complex-polynomial types and declarations adjacent to the
catalog claim. They do not freeze the canonical Lean target, perform the later anchor audit, or
grant proof credit to `THM-M-0012`.
-/

open Polynomial

#check Polynomial
#check Polynomial.degree
#check Polynomial.eval
#check Polynomial.IsRoot
#check Complex.exists_root
#check Complex.isAlgClosed
#check IsAlgClosed.exists_root
