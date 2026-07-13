/-
Discovery-only API probe for THM-M-0052.

This file checks pinned matrix, conjugate-transpose, Hermitian, and ordinary
inverse interfaces. It intentionally declares no Moore-Penrose target or proof.
-/
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

#check Matrix.conjTranspose
#check Matrix.conjTranspose_conjTranspose
#check Matrix.conjTranspose_mul
#check Matrix.IsHermitian
#check Matrix.isHermitian_mul_conjTranspose_self
#check Matrix.isHermitian_conjTranspose_mul_self
#check Matrix.mul_nonsing_inv
#check Matrix.nonsing_inv_mul
#check Matrix.nonsing_inv_cancel_or_zero
