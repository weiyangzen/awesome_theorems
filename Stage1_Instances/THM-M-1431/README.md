# THM-M-1431 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Douady-Hubbard theorem. The
repository gives Adrien Douady and John Hubbard, the year 1982, and the gloss `Mandelbrot set
connectedness`. Its catalog label `已验证` ("verified") is untrusted metadata under rev-5.6 and supplies no
human-source or Lean proof credit.

The gloss identifies a recognizable theorem family: for the quadratic maps `f_c(z) = z^2 + c`,
the parameter set for which the critical orbit is bounded is connected. A leading primary-source
candidate is Douady and Hubbard's 1982 note on iteration of complex quadratic polynomials; the
later Orsay notes state the same result as Corollary 8.3 after constructing a conformal
isomorphism from the complement of the Mandelbrot set to the complement of the closed unit disk.
Neither source has yet received the complete definition-chain, edition, errata, translation, and
independent source review required for `H0`.

This intake therefore freezes the theorem-family boundary and the proposition-changing decisions,
but leaves the canonical mathematical and Lean statements null. The provisional root vector is
`[H1, M4, R3]`: a primary theorem family and pinpoint source candidates are known, no exact usable
Lean artifact is located, and only a scoped route explanation exists. In particular, connectedness
must not be strengthened to path connectedness or local connectedness; local connectivity of the
whole Mandelbrot set is a separate conjectural claim in the inspected source.

The structured authority is `instance.json`. `scope-map.md` records the permitted theorem scope
and prohibited substitutions; `source-statement-crosswalk.md` maps the repository wording and
primary-source candidates to the mathematical and Lean components still requiring acceptance. All
six downstream phases remain open in `task-dag.json`. `IntakeProbe.lean` checks only adjacent
pinned APIs and states no target theorem. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
