import Mathlib.Analysis.Complex.Harmonic.Liouville

/-!
# THM-M-1143 anchor audit

This file checks the closest pinned mathlib declaration.  It deliberately does not provide a
proof of the frozen target: the mathlib theorem is restricted to the complex plane, while the
target quantifies over every positive finite dimension.
-/

open Bornology Set
open InnerProductSpace

#check InnerProductSpace.bounded_harmonic_on_complex_plane_is_constant

example (f : Complex -> Real) (h_harm : HarmonicOnNhd f univ)
    (h_bound : IsBounded (range f)) : forall z w, f z = f w := by
  exact bounded_harmonic_on_complex_plane_is_constant f h_harm h_bound

#print axioms InnerProductSpace.bounded_harmonic_on_complex_plane_is_constant
