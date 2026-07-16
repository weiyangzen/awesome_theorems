import Mathlib.FieldTheory.Galois.Basic
import Mathlib.NumberTheory.LocalField.Basic

/-!
# THM-M-0421 statement-gate probe

The repository identifies this target only as local class field theory, with
the gloss "abelian extensions of local fields". It does not fix the local-field
scope, reciprocity normalization, extension equivalence, or exact
classification and functoriality conclusions. Choosing those data here would
substitute one formulation for an unresolved source claim.

This module therefore checks only the smallest pinned object boundary already
used by the historical discovery artifact. It deliberately declares no
canonical statement, transport, axiom, or proof.
-/

open ValuativeRel

universe uK uL

namespace Stage1Instances.THM_M_0421

#check IsNonarchimedeanLocalField
#check IsGalois
#check Algebra.norm
#check OpenSubgroup

end Stage1Instances.THM_M_0421
