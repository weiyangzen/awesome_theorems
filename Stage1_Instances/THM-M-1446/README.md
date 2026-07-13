# THM-M-1446 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog entry
`LU分解` (LU decomposition). The repository supplies only the topic gloss `矩阵的三角分解`
("triangular decomposition of a matrix"), attributes it to Alan Turing in 1948, and labels it
verified. Under rev-5.6 that label is untrusted metadata, not a proposition, source proof, or
machine-proof receipt.

The wording does not choose an LU theorem. If it means that every square matrix is `L * U` without
pivoting, it is false: over the rationals the swap matrix `[[0, 1], [1, 0]]` has no lower-times-upper
factorization. `IntakeProbe.lean` kernel-checks this obstruction using pinned mathlib triangular
predicates. Adding pivoting, nonzero leading-minor conditions, normalization, or a scalar domain
would materially change the claim and cannot be done silently.

The repository's separate `THM-M-0047` target led discovery to A. M. Turing's 1948 paper. The
primary scan was independently inspected for this target: Section 3, journal pages 289-290, proves
unique `A = L D U` under nonsingular-principal-minor conditions, and also gives the reverse
`A = U' D' L'` form. This is a qualified LDU theorem, not the catalog gloss as a universal LU
statement. Exact scalar/domain interpretation, principal-minor convention, LDU-to-LU transport,
reverse-clause scope, errata, preservation, duplicate identity, and independent review remain open.

The provisional vector is `[H1, M4, R4]`. `H1` records an inspected complete primary proof lead but
not an accepted exact source crosswalk. `M4` records no selected canonical Lean proposition or
credited exact formal artifact. `R4` records no source-faithful proof reconstruction. The dossier
keeps all six downstream phases open and claims no accepted state, audit completion, theorem
completion, identity merger with `THM-M-0047`, or master acceptance.
