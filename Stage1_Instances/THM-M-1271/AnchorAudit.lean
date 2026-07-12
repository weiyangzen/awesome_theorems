import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Topology.Connected.PathConnected
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.Sequences

/-!
# THM-M-1271 immutable mathlib anchor probe

These declarations support the statement's calculus, path, compact-maximum,
and subsequence layers. None is a mountain-pass or deformation theorem.
-/

open Filter Set
open scoped Topology unitInterval

#check fderiv
#check ContDiff
#check ContDiff.continuous
#check Path
#check Path.source
#check Path.target
#check IsCompact.exists_isMaxOn
#check IsCompact.tendsto_subseq
#check StrictMono.tendsto_atTop

