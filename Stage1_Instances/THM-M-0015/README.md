# THM-M-0015 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `Artin reciprocity`. The repository
supplies only the Chinese gloss `类域论的核心定理` ("the central theorem of class field theory"),
the attribution Emil Artin, and the year 1927. It does not state domains, hypotheses, a map, or a
conclusion, and its `已验证` label is explicitly untrusted under rev-5.6.

An inspected modern source identifies the intended theorem family. In its number-field setup,
Milne, *Class Field Theory* v4.03, Chapter V, Theorem 5.3, states the global idelic reciprocity law:
the global Artin map kills principal ideles and induces, for each finite abelian extension, the
expected quotient isomorphism with its Galois group. This is the leading statement candidate, not
an accepted canonical claim.
The catalog still does not choose the modern idelic or historical ideal/ray-class encoding, number
fields or all global fields, a Frobenius convention, or whether it conflates reciprocity with the
separate class-field existence theorem. Selecting those choices at intake would add mathematics
not present in the repository record.

The provisional root vector is `[H1, M4, R3]`. A published theorem and proof source are known, but
proof completeness, exact source fidelity, assumptions, conventions, historical-to-modern
transport, errata, and independent review were not audited here. No usable exact Lean artifact was
located. This dossier explains the scope boundary but does not reconstruct the proof.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` enumerate the choices the statement phase must resolve. All six
dependent phases remain open in `task-dag.json`. `IntakeProbe.lean` checks only nearby pinned Lean
substrates and states no Artin reciprocity theorem. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
