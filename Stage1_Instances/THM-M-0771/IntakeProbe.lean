import Mathlib.SetTheory.Cardinal.Order

#check exists_wellOrder
#check WellOrderingRel
#check WellOrderingRel.isWellOrder

-- Intake-only probe of the direct relation formulation. The statement phase
-- must choose and fingerprint the canonical surface and its transports.
#check fun (alpha : Type*) => Nonempty { r : alpha -> alpha -> Prop // IsWellOrder alpha r }
