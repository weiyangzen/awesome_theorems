# THM-M-0785 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "axiom of
determinacy". The inventory gloss says only "determinacy of certain games on sets of reals" and
attributes the item to Jan Mycielski and Stanislaw Swierczkowski in 1964. It supplies no definition
of a game, payoff pointclass, axiom scheme, or consequence to be proved.

That omission is decisive. Full AD, determinacy restricted to a descriptive pointclass, Borel
determinacy, and a consequence proved from a determinacy hypothesis are materially different
claims with different foundational status. The adjacent Stage0 entry for Martin's theorem also
shows that silently choosing Borel determinacy would collide with another repository target.

The intake freezes this ambiguity rather than inventing a theorem. `IntakeProbe.lean` checks that a
standard length-omega integer-game schema can be expressed using the pinned environment; the schema
is explicitly only an encoding probe and is not the canonical target. The root remains
`[H3, M4, R4]`. Exact commands and results are recorded in `validation.md`.
