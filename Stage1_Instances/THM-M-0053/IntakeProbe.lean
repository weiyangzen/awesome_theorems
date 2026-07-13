import Mathlib.LinearAlgebra.Matrix.Gershgorin

-- Discovery-only interface probe; it declares no canonical target or proof body.
#check Matrix.toLin'
#check Module.End.HasEigenvalue
#check Metric.closedBall
#check eigenvalue_mem_ball
#check det_ne_zero_of_sum_row_lt_diag
#check det_ne_zero_of_sum_col_lt_diag

#print axioms eigenvalue_mem_ball
