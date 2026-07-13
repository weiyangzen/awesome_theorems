# THM-M-0263 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item
`实数完备性定理` (the completeness theorem for the real numbers). The received claim is only
"the completeness of the real-number set," attributed jointly to Richard Dedekind and Karl
Weierstrass in 1872 and marked `已验证`. The status label is untrusted inventory metadata and gives
no source or proof credit.

The gloss identifies a classical real-completeness family but not one proposition. It can refer to
Dedekind or least-upper-bound completeness, metric/Cauchy completeness, convergence of bounded
monotone sequences, the nested-interval property, or another theorem connected by additional
bridges. These forms have different binders, definitions, boundary cases, and formal targets. The
Dedekind attribution and date make order completeness a strong lead, while the joint Weierstrass
attribution does not resolve the intended formulation. Intake therefore does not silently choose
one.

Dedekind's 1901 authorized English translation of *Continuity and Irrational Numbers* was inspected
as a source-family lead. Section V, theorem IV (book pages 19-20) states and proves a cut-continuity
property of the real-number domain. The repository does not cite this edition, the theorem is not
literally the modern nonempty-bounded-set least-upper-bound proposition, and the Weierstrass side of
the joint attribution is not mapped. It supports `H1` discovery, not `H0` acceptance.

Pinned mathlib contains strong but distinct formal candidates. `Real.exists_isLUB` supplies the
nonempty bounded-above set form, and `Real.instCompleteSpace` supplies metric completeness.
`IntakeProbe.lean` authenticates both interfaces without selecting either as the root. The
provisional vector is `[H1, M3, R4]`: an inspected human source and direct formal candidates exist,
but exact source-to-root identity, canonical Lean target, and source-faithful reconstruction remain
open.

All six downstream phases remain open. No canonical statement, H0, M0, R0, accepted proof state,
audit completion, theorem completion, accepted receipt, or master acceptance is claimed.
