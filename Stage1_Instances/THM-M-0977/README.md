# THM-M-0977 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0977`, the repository label
`Chernoff界` (Chernoff bound). The catalog gives Herman Chernoff, 1952, and only the gloss
`独立随机变量和的尾概率`, literally "tail probabilities for sums of independent random
variables." Its `已验证` status is untrusted inventory metadata, not an exact source statement or
proof evidence.

The wording names a family, not one proposition. It does not choose upper or lower tails, arbitrary
real variables or Bernoulli/binomial variables, an MGF/CGF bound or an optimized multiplicative
bound, finite versus asymptotic indexing, the threshold and tilt domains, integrability hypotheses,
or boundary cases. The canonical mathematical and Lean statements therefore remain null. Picking a
familiar variant at intake would silently substitute proposition-changing mathematics.

The repository also contains the near-duplicate target `THM-M-0993` (`切尔诺夫界`) with the same
attribution, year, and gloss in another category. Its legacy slot and provisional rev-5.6 worker
artifacts selected a finite independent-sum product-MGF upper-tail statement. They are useful
discovery leads, but they are independently owned and grant no statement, evidence, or status
credit to this target. The integration lane must decide whether the two catalog records are
intentional separate instances or a cross-language duplicate before either statement is inherited
or differentiated.

`IntakeProbe.lean` authenticates only pinned mathlib upper/lower MGF and CGF tail interfaces and
finite-sum factorization interfaces. It declares no target theorem. Those exact-topic candidates
justify provisional `M3`, not M0: no source-faithful root or checked transport has been frozen.

The provisional root vector is `[H1, M3, R4]`. A plausible primary bibliographic lead is recorded,
but its text, exact result, assumptions, corrections, and independent review remain open; usable
pinned formal candidates exist but are not mapped to a canonical target; and no source-faithful
readable proof exists. All six downstream tasks remain open. No H0, M0, R0, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
