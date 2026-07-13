# THM-M-0917 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `分拆函数`
("partition function"). The repository attributes the item to Leonhard Euler in 1748 and gives
only the gloss `整数分拆的计数` ("counting integer partitions"). It supplies no formula,
quantifiers, hypotheses, conclusion, source locator, or proof. Its `已验证` label is untrusted
metadata under rev-5.6 and grants no human-source or machine-proof credit.

The gloss identifies a standard mathematical object, not one truth-valued proposition. A future
target could define the ordinary partition number, prove that the definition counts unordered
positive summands, establish its generating function, give a recurrence or congruence, or state an
asymptotic or exact formula. These are different claims. This intake therefore does not silently
substitute Euler's pentagonal identity (`THM-M-0916`), Rogers-Ramanujan (`THM-M-0918`), the
Hardy-Ramanujan asymptotic (`THM-M-0510`), the Rademacher formula (`THM-M-0511`), or a convenient
definition theorem.

Pinned mathlib does provide genuine interface substrate: `Nat.Partition n` represents multisets of
positive naturals summing to `n`; it has a `Fintype`; and the zero and one cases are unique. Thus
`Fintype.card (Nat.Partition n)` is a viable future representation of the ordinary partition
number. `IntakeProbe.lean` authenticates only these pinned APIs and the generic partition generating
function. Mathlib's own generating-function module explicitly leaves its ordinary partition-count
specialization as a TODO. None of this selects or proves the catalog root.

The provisional root vector is `[H5, M3, R4]`. `H5` classifies only the received noun-phrase record
as not yet a stable proposition; it does not say that partition theory is false or open. `M3`
records usable definitions and interfaces without an exact elaborated target or root proof. `R4`
records that no source-faithful proof reconstruction can attach to an unfrozen claim. All six
downstream phases remain open. No canonical statement, H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
