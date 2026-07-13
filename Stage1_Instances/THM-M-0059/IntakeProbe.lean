import Mathlib.Analysis.InnerProductSpace.Orientation

/-!
# THM-M-0059 discovery-only intake probe

These checks authenticate a pinned coordinate-free Hadamard inequality and plausible determinant
bridges. They do not select the underspecified catalog root, choose rows or columns, establish a
matrix/volume-form transport, add an equality characterization, or credit a root proof.
-/

#check Orientation.volumeForm
#check Orientation.volumeForm_robust'
#check Orientation.abs_volumeForm_apply_le
#check Orientation.abs_volumeForm_apply_of_pairwise_orthogonal
#check Module.Basis.det_apply
#check Pi.basisFun_det_apply
#check Matrix.det

#print axioms Orientation.abs_volumeForm_apply_le
