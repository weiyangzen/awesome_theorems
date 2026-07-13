import Mathlib.Analysis.Convex.Integral

/-!
# THM-M-0281 discovery-only intake probe

These commands authenticate pinned integral, average, set-average, and finite Jensen interfaces.
They do not select the catalog's exact proposition, establish a source-to-Lean transport, or prove
the target.
-/

#check ConvexOn.map_integral_le
#check ConvexOn.map_average_le
#check ConvexOn.map_set_average_le
#check ConvexOn.map_centerMass_le
#check ConvexOn.map_sum_le
#check ConcaveOn.le_map_integral
#check StrictConvexOn.ae_eq_const_or_map_average_lt
#check StrictConvexOn.map_sum_eq_iff

#print axioms ConvexOn.map_integral_le
#print axioms ConvexOn.map_sum_le
