# THM-M-0818 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the theorem family cataloged as the
Erdos-Szekeres theorem with the gloss "existence of a monotone subsequence." The catalog does not
say whether the intended root is the finite sharp two-parameter theorem, its square specialization,
or the infinitary theorem, and it does not settle strict versus weak monotonicity or repeated values.

The original 1935 paper was inspected at an immutable observed SHA-256. Its second proof states the
finite geometric sequence lemma: after ordering planar points by increasing abscissa, sufficiently
many ordinates contain a monotonically increasing or decreasing selection, with equal ordinates
allowed on either side. It introduces the sharp asymmetric quantity `f(i,k)` and says that
`(i-1)(k-1)` points can avoid both alternatives. This is a strong primary-source lead, but the OCR
does not reliably preserve every displayed formula and no independent source review or errata audit
has accepted a canonical modern statement.

Pinned mathlib also contains `exists_increasing_or_nonincreasing_subseq` in
`Mathlib.Order.OrderIsoNat`, explicitly documented as the infinitary Erdos-Szekeres theorem. The
narrow Lean probe checks its exact displayed type and supporting sequence embedding APIs. This is a
credible formal candidate, not proof credit: it is infinitary and relation-parametric, while the
catalog may intend the sharp finite theorem.

Accordingly the intake leaves the canonical statement and formal target null, records the root as
`[H1, M3, R4]`, and opens the six downstream tasks. Accepted proof state, audit completion, and
theorem completion are false. Only the integration lane may accept this self-tested worker proposal.
