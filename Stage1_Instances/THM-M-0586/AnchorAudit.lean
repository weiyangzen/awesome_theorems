import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0586: pinned anchor probes

These probes check the usable topology/manifold substrate found by the anchor
audit. They do not prove the high-dimensional Poincare target. In particular,
mathlib's `proof_wanted` Poincare entry is not an exported declaration and is
therefore audited from pinned source rather than named below with `#check`.
-/

#check ContinuousMap.HomotopyEquiv
#check Homeomorph
#check Homeomorph.toHomotopyEquiv
#check ContinuousMap.HomotopyEquiv.simplyConnectedSpace_iff
#check ChartedSpace
#check IsManifold
#check CompactSpace
#check ContinuousMap.HomotopyEquiv.NonemptyDiffeomorphSphere

