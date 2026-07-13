import Mathlib.InformationTheory.Hamming
import Mathlib.LinearAlgebra.Matrix.Circulant
import Mathlib.LinearAlgebra.Pi
import Mathlib.Logic.Equiv.Fin.Rotate

/-!
# THM-M-1590 discovery-only intake probe

These checks authenticate pinned coordinate-rotation, function-space linear transport, Hamming,
and circulant-matrix interfaces near possible cyclic-code encodings. They do not define a cyclic
code, select a catalog proposition, or prove THM-M-1590.
-/

#check finRotate
#check finCycle
#check LinearEquiv.piCongrLeft
#check hammingDist
#check hammingDist_triangle
#check Hamming
#check Matrix.circulant
#check Matrix.circulant_mul_comm
