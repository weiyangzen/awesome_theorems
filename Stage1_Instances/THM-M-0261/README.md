# THM-M-0261 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository target named
`曼德博集合连通性` ("connectedness of the Mandelbrot set"). The catalog supplies Adrien Douady
and John Hubbard, the year 1982, that short gloss, and an `已验证` ("verified") label. Under
rev-5.6 the label is untrusted metadata and grants no human-source or Lean proof credit.

The record identifies a recognizable theorem family: for the normalized quadratic maps
`f_c(z) = z^2 + c`, the parameter locus for which the critical orbit does not escape is connected.
A hash-identified English Orsay-notes discovery copy defines `P_c(z) = z^2 + c`, defines `M` through
connectedness of the filled Julia set, and states in Chapter 8, Corollary 8.3(a), "The set M is
connected," following Theorem 8.1's conformal isomorphism of complements. The 1982 C. R. note is
the historical primary candidate cited by those notes. Neither candidate has the complete
edition/translation, incorporated-definition, premise, proof-boundary, correction/errata, and
independent-review record needed for `H0`.

The repository separately schedules an exact metadata duplicate as `THM-M-1431`. This dossier
records that collision but does not merge identities, modify the other owned path, or inherit its
receipts, statement, proof, or status. A remote Lean source also contains a promising connectedness
declaration, but it is under a different toolchain, outside this repository's pinned dependency
closure, and receives discovery credit only.

This intake therefore freezes the theorem-family boundary and the proposition-changing decisions,
while leaving the canonical mathematical and Lean statements null for the statement phase. The
provisional root vector is `[H1, M4, R3]`: pinpoint primary candidates exist but the exact source
mapping is unaccepted, no usable exact local Lean artifact is established, and only a scoped route
explanation exists.

`instance.json` is the structured scope authority. `scope-map.md` records permitted scope and
prohibited substitutions; `source-statement-crosswalk.md` maps the repository wording and source
candidates to the mathematical and Lean components that remain open. `task-dag.json` keeps all six
downstream phases open. `IntakeProbe.lean` checks only adjacent pinned APIs and states no target
theorem. No `H0`, `M0`, `R0`, accepted proof state, audit completion, theorem completion, duplicate
reconciliation, or master acceptance is claimed.
