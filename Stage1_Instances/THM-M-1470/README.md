# THM-M-1470 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog
label `后验误差估计` (a posteriori error estimation). The repository attributes the topic to Ivo
Babuška in 1971 but supplies only the gloss `数值解的误差估计` ("error estimation for a numerical
solution"). It does not identify the numerical problem, approximation, computable estimator,
norm, assumptions, inequality, constants, or conclusion. The catalog value `已验证` is untrusted
metadata and gives neither source nor proof credit.

The attribution and year have a strong bibliographic match: Babuška's 1971 paper *Error-bounds for
finite element method*, *Numerische Mathematik* 16(4), 322-333, DOI
`10.1007/BF02165003`. Publisher and Crossref metadata were inspected, but the article body is not
openly available through those surfaces and the catalog does not cite a theorem or page within it.
No theorem passage, assumption list, proof boundary, correction audit, source-to-catalog identity,
or independent review is accepted here.

A posteriori estimates form a large theorem family. A root might assert reliability, local or
global efficiency, a two-sided bound up to data oscillation, asymptotic exactness, or adaptive
contraction, for one of many PDEs, discretizations, estimator constructions, and error norms.
Likewise, mathlib's pinned fixed-point declaration
`ContractingWith.aposteriori_dist_iterate_fixedPoint_le` is an exact phrase match but a different
mathematical target; it cannot be substituted.

The provisional vector is `[H5, M4, R4]`. `H5` says that the received catalog gloss is not yet one
stable truth-valued proposition; it does not refute established a posteriori error-estimation
theorems. `IntakeProbe.lean` authenticates adjacent pinned APIs only. All six downstream phases
remain open. No canonical statement, H0, M0, R0, accepted state, audit completion, theorem
completion, or master acceptance is claimed.
