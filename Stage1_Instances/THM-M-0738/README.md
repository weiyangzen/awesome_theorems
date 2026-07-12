# THM-M-0738 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`扩展Frege系统` (Extended Frege systems). The repository supplies only the gloss "properties of
Extended Frege systems", an attribution to Stephen Cook, and the year 1975. That identifies a
proof-complexity topic, not one proposition.

Extended Frege is a family of propositional proof systems whose exact syntax, extension rule,
proof encoding, and size measure must be fixed before stating soundness, completeness, simulation,
or lower-bound results. Those are materially different claims. In particular, the famous question
of superpolynomial lower bounds for Extended Frege is not interchangeable with an elementary
soundness or simulation theorem.

The intake freezes that ambiguity rather than inventing a convenient theorem. The root is
`[H5, M4, R4]`: the supplied wording is not a stable proposition, no exact formal artifact is
identified, and no readable proof reconstruction exists. `IntakeProbe.lean` checks only that the
pinned environment supplies finite Boolean-function and polynomial-time computation vocabulary
that may support a later encoding. It is neither the target statement nor a proof.

