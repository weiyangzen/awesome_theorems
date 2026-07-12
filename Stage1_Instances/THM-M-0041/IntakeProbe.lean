import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Charpoly.Basic

/-!
# THM-M-0041 discovery-only intake probe

These checks authenticate pinned matrix and finite-free-module Cayley-Hamilton interfaces. They do
not freeze the canonical source statement, establish a source transport, audit terminal proof-body
provenance, or promote either declaration to the theorem root.
-/

#check Matrix.charmatrix
#check Matrix.charpoly
#check Matrix.eval_charpoly
#check Matrix.aeval_self_charpoly
#check LinearMap.charpoly
#check LinearMap.eval_charpoly
#check LinearMap.aeval_self_charpoly
#check Polynomial.aeval

#print axioms Matrix.aeval_self_charpoly
#print axioms LinearMap.aeval_self_charpoly
