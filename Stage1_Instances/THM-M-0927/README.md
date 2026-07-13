# THM-M-0927 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0927`, the catalog entry
named `比内公式` (Binet's formula). The repository attributes it to Jacques Binet in 1843 and
supplies only the gloss `斐波那契数列的显式公式` (an explicit formula for the Fibonacci sequence).
Its `已验证` label is untrusted metadata under rev-5.6, not a source audit or proof receipt.

The gloss identifies the classical Binet-formula family, but it does not print a formula. It leaves
open the Fibonacci indexing and value domain, natural versus integer indices, the ambient number
system, definitions of the two characteristic roots, square-root and power conventions, and
pointwise versus function equality. It also supplies no primary citation, edition, page or theorem
locator, definition chain, proof boundary, correction history, errata review, or independent
review. Intake therefore does not silently promote one familiar spelling into the canonical root.

NIST DLMF section 26.11 gives the zero-based recurrence and an explicit radical formula for
nonnegative integer indices. Stable equation-TeX responses were captured by digest. This is a
strong modern authoritative statement lead, but not Binet's primary 1843 text, a proof crosswalk,
or an independently accepted source packet. The catalog's historical attribution and date remain
unreviewed.

Pinned mathlib has unusually direct interfaces in `Mathlib.NumberTheory.Real.GoldenRatio`:
`Real.coe_fib_eq'` is a function equality, `Real.coe_fib_eq` is the pointwise natural-index formula,
and `Real.coe_intFib_eq` extends it to integer indices. `IntakeProbe.lean` authenticates all three
and their axiom diagnostics at the pinned revision. These are strong exact-topic candidates and
support provisional `M3`, but source-root selection, exact expression freeze, checked transports,
terminal-body provenance, and trust acceptance belong to later phases.

The provisional vector is `[H1, M3, R4]`: a recognizable, published formula has modern source and
pinned Lean leads, but exact historical/source fidelity is not accepted; no canonical proposition
is frozen; and no source-faithful readable proof reconstruction exists. All six downstream tasks
remain open. No H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
