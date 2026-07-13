# THM-M-0820 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Mirsky's theorem. The repository
gloss says only that the theorem gives the minimum number of antichains in a decomposition of a
partially ordered set. It omits the finite carrier, the meaning of decomposition, the height
convention, ordered binders, boundary cases, a source locator, and a formal declaration.

## Intake result

Leon Mirsky's 1971 article *A Dual of Dilworth's Decomposition Theorem* is the strong primary
bibliographic lead. An inspected 2017 Coq formalization states the finite-poset theorem as equality
between maximum chain cardinality and the minimum size of an antichain cover. Its cover need not be
disjoint, so the common partition wording needs a checked cover-to-partition transport. The primary
article was not accessible in this run, so no exact primary passage, incorporated definitions,
proof, corrections, errata, or independent source review is credited.

Pinned mathlib supplies `IsAntichain`, `Set.chainHeight`, finite partitions, and strict relation
series. `IntakeProbe.lean` authenticates those adjacent interfaces only. A bounded target search
found no Mirsky declaration or theorem joining antichain partitions to maximum chain size. That
search is intake discovery, not the dependent exhaustive anchor audit.

The provisional vector is `[H1, M3, R4]`: the published theorem family is strongly identified but
its exact source mapping remains open; useful statement and reduction interfaces elaborate but no
exact target or proof body is credited; and no source-faithful readable proof exists. All six
downstream tasks remain open. No canonical Lean expression, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
