# THM-M-0916 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `欧拉五边形数定理` (Euler's
pentagonal number theorem). The repository attributes the item to Leonhard Euler in 1750 and gives
only the gloss `整数分拆的生成函数恒等式` (a generating-function identity for integer
partitions), with no formula, citation, assumptions, or trusted formal artifact. Its `已验证`
label is untrusted inventory metadata.

The name identifies a familiar theorem family, but the gloss does not freeze one proposition. A
source may state the infinite product as a signed series indexed by all integers, use the paired
positive-index form, give the reciprocal partition generating function, or derive the generalized
pentagonal recurrence for `p(n)`. Those forms need nontrivial decisions about the coefficient ring,
formal versus analytic convergence, signs, exponents, the constant term, and `p(0)`. They cannot be
silently merged or substituted.

An immutable English translation of Euler's E244 (published 1760) was inspected. Proposition 3 on
translation pages 3-5 proves the product expansion. NIST DLMF equations 27.14.4-27.14.5 provide an
authoritative modern paired-index statement. Secondary historical evidence reports that Euler first
gave the proof in a letter to Goldbach on 9 June 1750, making the catalog date plausible, but none of
these sources has yet received the complete admission, semantic crosswalk, errata audit, or
independent review required for H0.

Pinned mathlib supplies generic partition generating-function infrastructure in
`Mathlib.Combinatorics.Enumerative.Partition.GenFun`, but its module documentation marks the ordinary
partition-number specialization as TODO and contains no pentagonal expansion. `IntakeProbe.lean`
authenticates those adjacent APIs only.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
vector is `[H1, M4, R4]`: a matching human proof and modern statement lead are located but not fully
audited, no exact formal artifact is credited, and no proof reconstruction can attach before the
source-faithful root and encoding are selected.
All six downstream tasks remain open. No H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
