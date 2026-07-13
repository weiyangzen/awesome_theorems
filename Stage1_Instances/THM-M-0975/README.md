# THM-M-0975 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Azuma-Hoeffding inequality. The repository supplies Kazuoki Azuma and Wassily Hoeffding, the year
1967, and only the gloss "concentration of martingale difference sequences." Its `已验证` label is
untrusted inventory metadata, not a source audit, an exact proposition, or proof evidence.

The catalog contains this record twice and separately assigns the same gloss to `THM-M-1080`,
Azuma's inequality. The manifest nevertheless treats the two IDs as distinct targets in different
categories and lanes. This intake therefore preserves the Azuma-Hoeffding family while leaving the
exact distinction unresolved. It does not inherit `THM-M-1080`'s scope, statements, receipts, or
proof work.

Azuma's 1967 primary paper was inspected in the J-STAGE scan. It defines bounded martingale
differences, a conditional sub-Gaussian property `[G]`, and a bounded orthogonality property `[M]`.
Lemma 1 proves the exponential-moment bound for weighted `[M]` sequences; Remark 1 derives `[G]`
from bounded martingale differences. The paper's numbered theorems concern asymptotic behavior of
weighted sums rather than the familiar finite-horizon tail inequality. This is a strong historical
lead, but the catalog's joint Azuma/Hoeffding attribution, intended finite or asymptotic root,
modern naming, complete proof boundary, correction history, and independent review remain open.

Pinned mathlib contains the explicitly documented declaration
`ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF`. It gives a one-sided finite-sum
Azuma-Hoeffding tail estimate for a strongly adapted process with an initial sub-Gaussian term and
conditionally sub-Gaussian later terms. `IntakeProbe.lean` checks that declaration and its main
supporting interfaces at the pinned revision. It is an exact-topic candidate, not root proof credit:
the catalog does not say whether that conditional sub-Gaussian formulation, the classical bounded
martingale-difference corollary, or an asymptotic result is intended.

The provisional vector is `[H1, M3, R4]`. A matching primary source and a pinned exact-topic formal
candidate are known, but exact source fidelity, canonical statement identity, checked transport,
and readable reconstruction remain open. All six downstream phases stay open. No H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
