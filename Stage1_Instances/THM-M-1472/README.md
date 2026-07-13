# THM-M-1472 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `Lax等价定理` (the Lax
equivalence theorem). The repository supplies only the slogan `稳定性+相容性=收敛性`
("stability + consistency = convergence"), attributes it to Peter Lax in 1956, and labels it
`已验证`. The status is untrusted metadata. The plus and equals signs do not determine whether
the claim is an implication, an equivalence under consistency, or an informal summary.

The likely historical source family is P. D. Lax and R. D. Richtmyer's 1956 article *Survey of
the stability of linear finite difference equations*. Bibliographic metadata confirms both
authors, the date, journal, volume, issue, pages, and DOI, but the original article body was not
available during intake. The repository omits Richtmyer and cites neither the article nor a
theorem/page. No historical definition, assumption, proof, or erratum has therefore been admitted.

Tekriwal, Duraisamy, and Jeannin's 2021 paper *A Formal Proof of the Lax Equivalence Theorem for
Finite Difference Schemes* was inspected as a modern source and formal-artifact lead. Its Theorem
1 follows the broader Sanz-Serna-Palencia discretization setting and states only that consistency
and stability imply convergence. It fixes normed solution/data spaces, well-posed continuous and
discrete problems, restriction maps, a dense consistency core, and a uniform inverse bound. The
paper's public Coq artifact contains declaration `is_convergent` at an immutable Git revision. It
is neither automatically source-identical to Lax-Richtmyer nor a Lean 4 dependency, so it supplies
no `H0` or machine-closure credit here.

Pinned mathlib provides operator-norm, Banach-Steinhaus, limit, and squeeze interfaces that may be
substrate for a future formulation. `IntakeProbe.lean` authenticates those adjacent APIs only. It
does not declare or prove the Lax equivalence theorem.

The provisional vector is `[H1, M4, R4]`: the named theorem has published source and formalization
leads, but exact root selection, complete source mapping, errata review, and independent review are
open; no source-identical Lean artifact is credited; and no readable proof can attach to an
unfrozen root. All six downstream tasks remain open. No canonical statement, accepted proof state,
audit completion, theorem completion, accepted receipt, or master acceptance is claimed.
