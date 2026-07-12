# THM-M-0772 rev-5.6 intake

This directory is the fail-closed `planned` intake for Hausdorff's maximal principle. The repository
claim is: every partially ordered set has a maximal chain. Here "maximal" means inclusion-maximal
among chains, not a chain of greatest cardinality and not the existence of a maximal element of the
underlying order.

The statement-phase worker has now proposed the exact Lean declaration
`Stage1Instances.THM_M_0772.HausdorffMaximalPrinciple`, with minimal direct import
`Mathlib.Order.Preorder.Chain`, a checked definitional expansion of `IsMaxChain`, structural
mutation tests, and empty/singleton boundary proofs. This proposal is self-tested but remains
pending master acceptance. Pinned mathlib's more general `maxChain_spec` is still only a downstream
audit candidate and receives no proof credit here.

The provisional root vector remains `[H1, M4, R4]`: statement elaboration alone does not promote
machine-proof debt. The source edition/locator, independent source review, candidate provenance and
trust audit, obligation registry, and all completion gates remain open. No audit completion or
theorem completion is claimed.
